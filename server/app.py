from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from langchain_community.llms import Ollama
from database.models import Users
from database.conexion import db, init_app
from flask_bcrypt import Bcrypt

csv_file = 'dataset_clean.csv'
df = pd.read_csv(csv_file)
class_labels = df['label'].unique()

app = Flask(__name__)
cors = CORS(app, origins='*')
bcrypt = Bcrypt(app)

# Inicializar la base de datos
init_app(app)

model_path = '/mnt/c/Users/mat5b/Onedrive/Escritorio/Computacion/Proyecto/CookingWithAI/server/modeloEntrenado'
if os.path.exists(model_path):
    print(f'La ruta {model_path} es válida y existe.')
    # Cargar el modelo
    model = tf.keras.models.load_model(model_path)
    print("Modelo cargado correctamente.")
else:
    print(f'La ruta {model_path} no existe o es incorrecta.')

ollama = Ollama(
    base_url='http://localhost:11434',
    model="gemma2:2b"
)

def preprocess_image(image):
    image = image.resize((224, 224))  # Redimensionar al mismo tamaño usado en el entrenamiento
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión extra para el batch
    img_array = img_array / 255.0  # Normalizar como se hizo en el entrenamiento
    return img_array

# Obtener los ingredientes a partir de la imagen utilizando el modelo entrenado
def get_ingredients_from_image(image):
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)  # predicción
    
    # Obtener la clase con mayor probabilidad
    predicted_class = np.argmax(predictions, axis=1)[0]  # Obtener el índice de la clase predicha
    # Obtener el nombre de la clase predicha utilizando el índice
    ingredient = class_labels[predicted_class]
    return ingredient


# Ruta principal de la app
@app.route('/')
def index():
    return "Falta hacer el front..."

app.secret_key = os.urandom(24)

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        # Verificar si hay una imagen en la solicitud
        if 'image' in request.files:
            image_file = request.files['image']
            image = Image.open(image_file)

            ingredient = get_ingredients_from_image(image)
            print(f"Ingrediente predecido: {ingredient}")

            if not ingredient:
                return jsonify({'error': 'No se detectaron ingredientes en la imagen'})

            prompt = f"Dame una receta sencilla con el siguiente ingrediente: {ingredient}. Evita incluir elementos no relacionados o creativos."
            generated_text = ollama.invoke(prompt)
            return jsonify({'response': generated_text})
        else:
            return jsonify({'error': 'No se encuentra imagen o texto'})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Obtener los datos en formato JSON desde el frontend
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Encriptamos la contraseña
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Verificamos si el usuario ya existe
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'El nombre de usuario ya existe'}), 400
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'El correo electrónico ya está registrado'}), 400
    
    # Creamos y agregamos el nuevo usuario a la base de datos
    new_user = Users(username=username, email=email, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 200


# Ruta para listar los usuarios registrados dentro de la bdd
# no tiene uso, sirve para verificar que los usuarios se crean
# y se agregan de manera correcta
@app.route('/usuarios')
def get_usuarios():
    try:
        usuarios = Users.query.all()
        return f"Usuarios: {[usuario.username for usuario in usuarios]}"
    except Exception as e:
        return str(e), 500

# Si el usuario quiere ingresar a cualquier pagina que no este
# definida, se lo redirecciona al inicio
def pagina_no_encotrada(error):
    # return render_template('404.html'), 404 (opcion para mostrar un index personalizado en vez de solo redireccionar)
    return redirect(url_for('index'))

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recibe los datos en formato JSON
    email = data.get('email')
    password = data.get('password')
    
    # Verificar si el usuario existe en la base de datos
    user = Users.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({'message': 'El usuario no existe'}), 401  # Usuario no encontrado
    
    # Verificar si la contraseña es correcta
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Las credenciales no coinciden'}), 401  # Contraseña incorrecta
    
    # Si las credenciales son correctas, iniciar sesión
    session['user_id'] = user.id
    return jsonify({'message': 'Inicio de sesión exitoso'}), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session['logged_in'] = False
    return jsonify({'message': 'Cierre de sesión exitoso'}), 200

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 200


if __name__ == "__main__":
    from database.conexion import create_db
    create_db()
    # Manejamos los errores con el metodo que creamos
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(debug=True)
