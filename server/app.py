from flask import Flask, render_template, request, url_for, redirect, jsonify
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

#model_path = '/home/juancho_gonzalez/Escritorio/Proyecto/server/CookingWithAI/server/modeloEntrenado'

# Obtener la ruta absoluta de la carpeta donde se encuentra el script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Crear la ruta al modelo entrenado
model_path = os.path.join(base_dir, 'modeloEntrenado')

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
    
    # para q tenga 3 canales de rgb
    #if img_array.shape[-1] != 3:
    #    img_array = np.stack((img_array,)*3, axis=-1)  # Convertir a RGB si no lo era 
    
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

# Metodo get y post para el manejo del registro de un nuevo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Si el metodo es un POST
    if request.method == 'POST':
        # Obtenemos los datos del request
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Encriptamos la contraseña
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Verificamos si el usuario ya existe
        if Users.query.filter_by(username=username).first() is not None:
            return redirect(url_for('register'))
        if Users.query.filter_by(email=email).first() is not None:
            return redirect(url_for('register'))
        
        # Creamos y agregamos el nuevo usuario a la bdd
        new_user = Users(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('get_usuarios'))
    
    #Si el metodo es un GET
    return render_template('register.html')

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

if __name__ == "__main__":
    from database.conexion import create_db
    create_db()
    # Manejamos los errores con el metodo que creamos
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(debug=True)