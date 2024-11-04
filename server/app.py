from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from langchain_community.llms import Ollama
from database.models import Users, Recetas
from database import db, create_app
from flask_bcrypt import Bcrypt
from jinja2 import Environment, FileSystemLoader

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

template_loader = FileSystemLoader('templates')

template_env = Environment(loader=template_loader)

template = template_env.get_template('camera.html')

bcrypt = Bcrypt(app)

# Obtener la ruta absoluta donde se encuentra app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta absoluta para el archivo CSV
csv_file = os.path.join(basedir, 'dataset_clean_one_hot.csv')

# Verificar si el archivo CSV existe
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    class_labels = df.columns[1:] # La primera columna es 'image', el resto son las etiquetas one-hot
    print("CSV cargado correctamente.")
else:
    print(f"El archivo CSV no se encuentra en la ruta: {csv_file}")
    # Manejamos el error con una excepción
    raise FileNotFoundError(f"El archivo CSV no se encuentra en la ruta: {csv_file}")

model_path = os.path.join(basedir, 'modeloEntrenado')
if os.path.exists(model_path):
    print(f'La ruta {model_path} es válida y existe.')
    # Cargar el modelo
    model = tf.keras.models.load_model(model_path)
    print("Modelo cargado correctamente.")
else:
    print(f'La ruta {model_path} no existe o es incorrecta.')
    # Manejamos el error con una excepción
    raise FileNotFoundError(f'La ruta {model_path} no existe o es incorrecta.')

ollama = Ollama(
    base_url='http://localhost:11434',
    model="gemma2:2b"
)


def preprocess_image(image):
    # Convertir cualquier imagen a RGB para garantizar que tenga 3 canales
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    # Redimensionar la imagen al tamaño usado en el entrenamiento
    image = image.resize((224, 224))
    
    # Convertir la imagen a un array de NumPy
    img_array = np.array(image)
    
    # Asegurar que la imagen tenga las dimensiones correctas (224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión extra para el batch
    
    # Normalizar los valores de píxeles (0 a 255) a (0.0 a 1.0)
    img_array = img_array / 255.0
    
    return img_array


def get_ingredients_from_image(image):
    img_array = preprocess_image(image)
    predictions = model.predict(img_array)  # Hacer la predicción
    
    # Obtener las etiquetas predichas usando un umbral
    predicted_labels = (predictions > 0.1).astype(int)  # Umbral de 0.5 para convertir a etiquetas
    print(f"Predicciones: {predictions}")
    print(f"Etiquetas predichas: {predicted_labels}")

    # Obtener los ingredientes correspondientes a las etiquetas predichas
    ingredients = [class_labels[i] for i in range(len(predicted_labels[0])) if predicted_labels[0][i] == 1]
    return ingredients  # Devolver la lista de ingredientes


# Ruta principal de la app
@app.route('/')
def index():
    return "App activo"

app.secret_key = os.getenv('SECRET_KEY') or 'clave-secreta'

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        # Verificar si hay texto en la solicitud
        text = request.form.get('text', '')
        
        # Verificar si hay una imagen en la solicitud
        images = request.files.getlist('images')

        all_ingredients = []
        
        print(f"Texto recibido: {text}")
        print(f"Cantidad de imagenes recibidas: {len(images)}")

        if images:
            for image_file in images:
                image = Image.open(image_file)
                ingredients = get_ingredients_from_image(image)
                print(f"Ingredientes predichos: {ingredients}")

                if not ingredients:
                    return jsonify({'error': 'No se detectaron ingredientes en una o más imágenes.'})

                all_ingredients.extend(ingredients)
            
            # Eliminar duplicados
            all_ingredients = list(set(all_ingredients))

        if text:
            # Si hay texto, añadirlo a los ingredientes detectados
            user_ingredients = text.split(',')
            all_ingredients.extend([ingredient.strip() for ingredient in user_ingredients])

            # Eliminar duplicados después de agregar los ingredientes del texto
            all_ingredients = list(set(all_ingredients))

        if all_ingredients:
            prompt = f"Dame una receta sencilla con los siguientes ingredientes: {', '.join(all_ingredients)}. Evita incluir elementos no relacionados o creativos. Quiero que me dividas la respuesta en 4 categorias (Titulo, Ingredientes, Preparación y Consejos) donde cada una de ellas tienen que comenzar con las siguientes exactas palabras segun corresponda a cada una de ellas: 'Titulo', 'Ingredientes:', 'Peparación:' y 'Consejos'."
            generated_text = ollama.invoke(prompt)
            titulo = parse_receta(generated_text)
            
            return jsonify({'response': generated_text})
        else:
            return jsonify({'error': 'No se recibieron ingredientes ni en texto ni en imágenes.'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/guardar_receta', methods=['POST'])
def guardar_receta():
    try:
        data = request.get_json()
        response = data.get('response')

        if not response:
            return jsonify({'error': 'No se recibió ninguna receta para guardar'}), 400

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuario no está logueado'}), 401

        user = Users.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        titulo = parse_receta(response)
        if not titulo:
            return jsonify({'error': 'No se pudo extraer el título de la receta'}), 400

        nueva_receta = Recetas(titulo=titulo, descripcion=response, user_id=user.id)
        db.session.add(nueva_receta)
        db.session.commit()

        return jsonify({'message': 'Receta guardada exitosamente'}), 200

    except Exception as e:
        print(f"Error al guardar receta: {str(e)}")  # Imprime el error en la consola del servidor
        return jsonify({'error': str(e)}), 500

def parse_receta(generated_text):
    titulo = ''
    # Filtrar solo el titulo
    try:
        if "Titulo" in generated_text:
            titulo = generated_text.split("Titulo:")[1].split("Ingredientes:")[0].strip()
        else:
            titulo = generated_text.split('\n')[0].strip()
    except IndexError as e:
        print(f"Error al analizar el texto generado: {e}")

    return titulo

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'El nombre de usuario ya existe'}), 400
    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'El correo electronico ya esta registrado'}), 400
    
    new_user = Users(username=username, email=email, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 200


# Ruta para listar los usuarios registrados dentro de la bdd
# Para verificar que los usuarios se crean
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
    
    session['logged_in'] = True  
    
    # Si las credenciales son correctas, iniciar sesión
    session['user_id'] = user.id
    session.permanent = True
    return jsonify({'message': 'Inicio de sesion exitoso'}), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Cierre de sesion exitoso'}), 200

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 200


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Aquí puedes guardar o procesar el archivo
    # file.save(os.path.join('uploads', file.filename))

    return jsonify({"message": "Archivo subido con éxito"}), 200

@app.route('/camera', methods=['GET'])
def camera():
    print("Accediendo a /camera")  # Debug
    return send_from_directory(app.template_folder, 'camera.html')


URL_REACT = "http://192.168.100.5:5173"


if __name__ == "__main__":  
    # Manejamos los errores con el metodo que creamos
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(host='0.0.0.0', port=5000,debug = True)
    CORS(app, origins=[URL_REACT])
