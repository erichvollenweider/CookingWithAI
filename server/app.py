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

def cargar_csv(archivo_csv):
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        print(f"CSV {archivo_csv} cargado correctamente.")
        return df
    else:
        print(f"El archivo CSV {archivo_csv} no se encuentra en la ruta: {archivo_csv}")
        raise FileNotFoundError(f"El archivo CSV {archivo_csv} no se encuentra en la ruta: {archivo_csv}")

def cargar_modelo(modelo_path):
    if os.path.exists(modelo_path):
        print(f'La ruta {modelo_path} es válida y existe.')
        model = tf.keras.models.load_model(modelo_path)
        print(f"Modelo cargado correctamente desde {modelo_path}.")
        return model
    else:
        print(f'La ruta {modelo_path} no existe o es incorrecta.')
        raise FileNotFoundError(f'La ruta {modelo_path} no existe o es incorrecta.')

# Rutas de archivos CSV
csv_v1 = os.path.join(basedir, 'dataset-v1.csv')
csv_v2 = os.path.join(basedir, 'dataset-v2.csv')
csv_f = os.path.join(basedir, 'dataset-f.csv')
csv_file_carnes = os.path.join(basedir, 'dataset-carnes.csv')

# Cargar los archivos CSV
df_v1 = cargar_csv(csv_v1)
df_v2 = cargar_csv(csv_v2)
df_f = cargar_csv(csv_f)
df_carnes = cargar_csv(csv_file_carnes)

# Etiquetas para cada archivo CSV
class_labels_v1 = df_v1.columns[1:]
class_labels_v2 = df_v2.columns[1:]
class_labels_f = df_f.columns[1:]
class_labels_carnes = df_carnes.columns[1:]

# Rutas de modelos
model_v1_path = os.path.join(basedir, 'modeloEntrenado-v1')
model_v2_path = os.path.join(basedir, 'modeloEntrenado-v2')
model_f_path = os.path.join(basedir, 'modeloEntrenado-f')
model_carnes_path = os.path.join(basedir, 'modeloEntrenadoCarnes')

# Cargar los modelos
model_v1 = cargar_modelo(model_v1_path)
model_v2 = cargar_modelo(model_v2_path)
model_f = cargar_modelo(model_f_path)
model_carnes = cargar_modelo(model_carnes_path)

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

def mostrar_predicciones(predictions, predicted_labels, labels, label_name):
    print(f"Predicciones {label_name}: ")
    
    # Imprimir las predicciones en formato texto
    predictions_text = [f"{label}: {pred:.2f}" for label, pred in zip(labels, predictions[0])]
    print(", ".join(predictions_text))
    
    # Imprimir las etiquetas predichas
    predicted_labels_text = [label for label, pred in zip(labels, predicted_labels[0]) if pred == 1]
    print(f"Etiquetas predichas {label_name}:", ", ".join(predicted_labels_text))
    print("-----------------------------------------------------------------------------------------------------")

def get_ingredients_from_image(image):
    img_array = preprocess_image(image)
    predictions_v1 = model_v1.predict(img_array)
    predictions_v2 = model_v2.predict(img_array)
    predictions_f = model_f.predict(img_array)
    predictions_carnes = model_carnes.predict(img_array)
    
    # Obtener las etiquetas predichas usando un umbral
    predicted_labels_v1 = (predictions_v1 > 0.3).astype(int)
    predicted_labels_v2 = (predictions_v2 > 0.5).astype(int)
    predicted_labels_f = (predictions_f > 0.5).astype(int)
    predicted_labels_carnes = (predictions_carnes > 0.82).astype(int)

    labels_v1 = ["anquito", "apio", "berenjena", "cebolla", "cebolla morada", "choclo", "coliflor", 
                "huevo", "lechuga", "papa", "pimiento amarillo", "pimiento rojo", "pimiento verde", "remolacha"]
    labels_v2 = ["ajo","arveja", "batata", "brocoli", "cebolla de verdeo", "espinaca", "palta", "pepino","rabanito", "repollo morado",
                "tomate","zanahoria", "zapallito"]
    labels_f = ["aceituna", "ananá", "banana", "cereza", "durazno", "frutilla", "jengibre", "kiwi", "limón", "manzana", "naranja", "pera", "sandía"]
    labels_c = ["alita", "chinchulin", "chorizo", "costeleta de cerdo", "hamburguesa", "milanesa", "morcilla", "pan", "pata-muslo", "pechuga", "pollo", "riñon"]
    
    mostrar_predicciones(predictions_v1, predicted_labels_v1, labels_v1, "verduras V1")
    mostrar_predicciones(predictions_v2, predicted_labels_v2, labels_v2, "verduras V2")
    mostrar_predicciones(predictions_f, predicted_labels_f, labels_f, "frutas")
    mostrar_predicciones(predictions_carnes, predicted_labels_carnes, labels_c, "carnes")
    
    # Concatenar etiquetas y predicciones en una sola lista para simplificar
    all_labels = list(class_labels_v1) + list(class_labels_v2) + list(class_labels_f) + list(class_labels_carnes)
    all_predictions = np.concatenate([predicted_labels_v1[0], predicted_labels_v2[0], predicted_labels_f[0], predicted_labels_carnes[0]])

    # Obtener ingredientes en una sola línea
    ingredients = [all_labels[i] for i in range(len(all_predictions)) if all_predictions[i] == 1]
    return ingredients

# Ruta principal de la app
@app.route('/')
def index():
    return "App activo"

@app.route('/ingredientes_detectados', methods=['POST'])
def detectar_ingredientes():
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
            return jsonify({'response': all_ingredients})
        else:
            return jsonify({'error': 'No se recibieron ingredientes ni en texto ni en imágenes.'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        ingredients = request.json.get('ingredients', [])

        if ingredients:
            all_ingredients = list(set(ingredient.strip() for ingredient in ingredients))

            print("INGREDIENTES:", all_ingredients)

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
    return jsonify({'message': 'Inicio de sesion exitoso'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Cierre de sesion exitoso'}), 200

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'logged_in' in session and session['logged_in']:
        user = Users.query.get(session['user_id'])
        if user is not None:
            return jsonify({'logged_in': True}), 200
    session.clear()
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


URL_REACT = "http://127.0.1.1:5173"


if __name__ == "__main__":  
    # Manejamos los errores con el metodo que creamos
    app.register_error_handler(404, pagina_no_encotrada)
    app.run(host='0.0.0.0', port=5000,debug = True)
    CORS(app, origins=[URL_REACT])
