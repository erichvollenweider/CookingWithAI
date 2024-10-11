from flask import Flask, request, url_for, redirect, jsonify, session
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from langchain_community.llms import Ollama
from database.models import Users, Chats
from database.conexion import db, init_app, create_db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
cors = CORS(app, origins='*')
bcrypt = Bcrypt(app)

# Inicializar la base de datos
init_app(app)

# Obtener la ruta absoluta donde se encuentra app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta absoluta para el archivo CSV
csv_file = os.path.join(basedir, 'dataset_clean_one_hot.csv')

# Verificar si el archivo CSV existe
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    class_labels = df.columns[1:]  # La primera columna es 'image', el resto son las etiquetas one-hot
    print("CSV cargado correctamente.")
else:
    raise FileNotFoundError(f"El archivo CSV no se encuentra en la ruta: {csv_file}")

# Ruta para cargar el modelo
model_path = os.path.join(basedir, 'modeloEntrenado')
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
    print("Modelo cargado correctamente.")
else:
    raise FileNotFoundError(f"La ruta {model_path} no existe o es incorrecta.")

# Inicializar Ollama
ollama = Ollama(
    base_url='http://localhost:11434',
    model="gemma2:2b"
)


def preprocess_image(image):
    """Función para procesar la imagen antes de la predicción."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión extra para el batch
    img_array = img_array / 255.0  # Normalizar los valores de píxeles
    
    return img_array

def get_ingredients_from_image(image):
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)  # Hacer la predicción
    
    # Obtener las etiquetas predichas usando un umbral
    predicted_labels = (predictions > 0.1).astype(int)  # Umbral de 0.5 para convertir a etiquetas
    print(f"Predicciones: {predictions}")
    print(f"Etiquetas predichas: {predicted_labels}")
    print(f"Clases disponibles (ingredientes): {list(class_labels)}")

    # Obtener los ingredientes correspondientes a las etiquetas predichas
    ingredients = [class_labels[i] for i in range(len(predicted_labels[0])) if predicted_labels[0][i] == 1]
    return ingredients  # Devolver la lista de ingredientes

@app.route('/')
def index():
    return "Falta hacer el front..."


app.secret_key = os.urandom(24)


@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    """Recibe texto e imágenes, procesa los ingredientes y consulta Ollama."""
    try:
        # Obtener el texto y las imágenes
        text = request.form.get('text', '')
        images = request.files.getlist('images')
        all_ingredients = []

        if images:
            for image_file in images:
                try:
                    image = Image.open(image_file)
                    ingredients = get_ingredients_from_image(image)
                    print(f"Ingredientes predichos: {ingredients}")
                    all_ingredients.extend(ingredients)
                except Exception as e:
                    return jsonify({'error': f'Error al procesar la imagen: {str(e)}'}), 400

            # Eliminar duplicados de ingredientes
            all_ingredients = list(set(all_ingredients))

        if text:
            user_ingredients = text.split(',')
            all_ingredients.extend([ingredient.strip() for ingredient in user_ingredients])
            all_ingredients = list(set(all_ingredients))  # Eliminar duplicados de nuevo

        if all_ingredients:
            prompt = f"Dame una receta sencilla con los siguientes ingredientes: {', '.join(all_ingredients)}. Evita incluir elementos no relacionados o creativos."
            try:
                generated_text = ollama.invoke(prompt)
                return jsonify({'response': generated_text})
            except Exception as e:
                return jsonify({'error': f'Error al consultar Ollama: {str(e)}'}), 500
        else:
            return jsonify({'error': 'No se recibieron ingredientes ni en texto ni en imágenes.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/register', methods=['POST'])
def register():
    """Ruta para registrar un nuevo usuario."""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if Users.query.filter_by(username=username).first():
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400
        if Users.query.filter_by(email=email).first():
            return jsonify({'message': 'El correo electrónico ya está registrado'}), 400

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/usuarios')
def get_usuarios():
    """Lista de todos los usuarios registrados."""
    try:
        usuarios = Users.query.all()
        return jsonify({'usuarios': [usuario.username for usuario in usuarios]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """Ruta para iniciar sesión."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = Users.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Credenciales incorrectas'}), 401

        session['logged_in'] = True
        session['user_id'] = user.id
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/logout', methods=['POST'])
def logout():
    """Ruta para cerrar sesión."""
    session.pop('user_id', None)
    session['logged_in'] = False
    return jsonify({'message': 'Cierre de sesión exitoso'}), 200


@app.route('/check_session', methods=['GET'])
def check_session():
    """Verifica si la sesión está activa."""
    return jsonify({'logged_in': session.get('logged_in', False)}), 200


def pagina_no_encotrada(error):
    """Manejo de error 404, redirige al índice."""
    return redirect(url_for('index'))


if __name__ == "__main__":
    create_db()
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(debug=True)
