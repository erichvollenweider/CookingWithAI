from flask import Flask, request, url_for, redirect, jsonify, session
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
from model_rag import load_model

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
bcrypt = Bcrypt(app)

# Obtener la ruta absoluta donde se encuentra app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta absoluta para el archivo CSV
csv_v1 = os.path.join(basedir, 'dataset-v1.csv')
csv_v2 = os.path.join(basedir, 'dataset-v2.csv')
csv_f = os.path.join(basedir, 'dataset-f.csv')
csv_file_carnes = os.path.join(basedir, 'dataset-carnes.csv')

# Verificar si el archivo CSV existe
if os.path.exists(csv_v1):
    df_v1 = pd.read_csv(csv_v1)
    class_labels_v1 = df_v1.columns[1:]  # Etiquetas para frutas y verduras
    print("CSV frutas y verduras cargado correctamente.")
else:
    print(f"El archivo CSV frutas y verduras no se encuentra en la ruta: {csv_v1}")
    # Manejamos el error con una excepción
    raise FileNotFoundError(f"El archivo CSV frutas y verduras no se encuentra en la ruta: {csv_v1}")

if os.path.exists(csv_v2):
    df_v2 = pd.read_csv(csv_v2)
    class_labels_v2 = df_v2.columns[1:]  # Etiquetas para frutas y verduras
    print("CSV frutas y verduras cargado correctamente.")
else:
    print(f"El archivo CSV frutas y verduras no se encuentra en la ruta: {csv_v2}")
    # Manejamos el error con una excepción
    raise FileNotFoundError(f"El archivo CSV frutas y verduras no se encuentra en la ruta: {csv_v2}")

if os.path.exists(csv_f):
    df_f = pd.read_csv(csv_f)
    class_labels_f = df_f.columns[1:]  # Etiquetas para frutas y verduras
    print("CSV frutas y verduras cargado correctamente.")
else:
    print(f"El archivo CSV frutas y verduras no se encuentra en la ruta: {csv_f}")
    # Manejamos el error con una excepción
    raise FileNotFoundError(f"El archivo CSV frutas y verduras no se encuentra en la ruta: {csv_f}")

if os.path.exists(csv_file_carnes):
    df_carnes = pd.read_csv(csv_file_carnes)
    class_labels_carnes = df_carnes.columns[1:]  # Etiquetas para carnes
    print("CSV carnes cargado correctamente.")
else:
    print(f"El archivo CSV carnes no se encuentra en la ruta: {csv_file_carnes}")
    raise FileNotFoundError(f"El archivo CSV carnes no se encuentra en la ruta: {csv_file_carnes}")

model_v1_path = os.path.join(basedir, 'modeloEntrenado-v1')
model_v2_path = os.path.join(basedir, 'modeloEntrenado-v2')
model_f_path = os.path.join(basedir, 'modeloEntrenado-f')
model_carnes_path = os.path.join(basedir, 'modeloEntrenadoCarnes')

if os.path.exists(model_v1_path):
    print(f'La ruta {model_v1_path} es válida y existe.')
    # Cargar el modelo
    model_v1 = tf.keras.models.load_model(model_v1_path)
    print("Modelo frutas y verduras cargado correctamente.")
else:
    print(f'La ruta {model_v1_path} no existe o es incorrecta.')
    # Manejamos el error con una excepción
    raise FileNotFoundError(f'La ruta {model_v1_path} no existe o es incorrecta.')

if os.path.exists(model_v2_path):
    print(f'La ruta {model_v2_path} es válida y existe.')
    # Cargar el modelo
    model_v2 = tf.keras.models.load_model(model_v2_path)
    print("Modelo frutas y verduras cargado correctamente.")
else:
    print(f'La ruta {model_v2_path} no existe o es incorrecta.')
    # Manejamos el error con una excepción
    raise FileNotFoundError(f'La ruta {model_v2_path} no existe o es incorrecta.')

if os.path.exists(model_f_path):
    print(f'La ruta {model_f_path} es válida y existe.')
    # Cargar el modelo
    model_f = tf.keras.models.load_model(model_f_path)
    print("Modelo frutas y verduras cargado correctamente.")
else:
    print(f'La ruta {model_f_path} no existe o es incorrecta.')
    # Manejamos el error con una excepción
    raise FileNotFoundError(f'La ruta {model_f_path} no existe o es incorrecta.')

if os.path.exists(model_carnes_path):
    print(f'La ruta {model_carnes_path} es válida y existe.')
    model_carnes = tf.keras.models.load_model(model_carnes_path)
    print("Modelo carnes cargado correctamente.")
else:
    print(f'La ruta {model_carnes_path} no existe o es incorrecta.')
    raise FileNotFoundError(f'La ruta {model_carnes_path} no existe o es incorrecta.')

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
    predictions_v1 = model_v1.predict(img_array)
    predictions_v2 = model_v2.predict(img_array)
    predictions_f = model_f.predict(img_array)
    predictions_carnes = model_carnes.predict(img_array)
    
    # Obtener las etiquetas predichas usando un umbral
    predicted_labels_v1 = (predictions_v1 > 0.3).astype(int)
    predicted_labels_v2 = (predictions_v2 > 0.5).astype(int)
    predicted_labels_f = (predictions_f > 0.5).astype(int)
    predicted_labels_carnes = (predictions_carnes > 0.82).astype(int)

    # Imprimir predicciones en una línea continua
    print("Predicciones verduras V1: ")
    labels_v1 = ["anquito", "apio", "berenjena", "cebolla", "cebolla morada", "choclo", "coliflor", 
                "huevo", "lechuga", "papa", "pimiento amarillo", "pimiento rojo", "pimiento verde", "remolacha"]

    # Convertir predicciones a una lista de texto
    predictions_text_v1 = [f"{label}: {pred:.2f}" for label, pred in zip(labels_v1, predictions_v1[0])]
    print(", ".join(predictions_text_v1))

    # Imprimir etiquetas predichas en una línea continua
    predicted_labels_text_v1 = [label for label, pred in zip(labels_v1, predicted_labels_v1[0]) if pred == 1]
    print("Etiquetas predichas verduras V1:", ", ".join(predicted_labels_text_v1))
    print("-----------------------------------------------------------------------------------------------------")

    print("Predicciones verduras V2: ")
    labels_v2 = ["ajo","arveja", "batata", "brocoli", "cebolla de verdeo", "espinaca", "palta", "pepino","rabanito", "repollo morado",
                 "tomate","zanahoria", "zapallito"]

    predictions_text_v2 = [f"{label}: {pred:.2f}" for label, pred in zip(labels_v2, predictions_v2[0])]
    print(", ".join(predictions_text_v2))

    predicted_labels_text_v2 = [label for label, pred in zip(labels_v2, predicted_labels_v2[0]) if pred == 1]
    print("Etiquetas predichas verduras V2:", ", ".join(predicted_labels_text_v2))
    print("-----------------------------------------------------------------------------------------------------")

    print("Predicciones frutas: ")
    labels_f = ["aceituna", "ananá", "banana", "cereza", "durazno", "frutilla", "jengibre", "kiwi", "limón", "manzana", "naranja", "pera", "sandía"]

    predictions_text_f = [f"{label}: {pred:.2f}" for label, pred in zip(labels_f, predictions_f[0])]
    print(", ".join(predictions_text_f))

    predicted_labels_text_f = [label for label, pred in zip(labels_f, predicted_labels_f[0]) if pred == 1]
    print("Etiquetas predichas frutas:", ", ".join(predicted_labels_text_f))
    print("-----------------------------------------------------------------------------------------------------")

    print("Predicciones carnes: ")
    labels_c = ["alita", "chinchulin", "chorizo", "costeleta de cerdo", "hamburguesa", "milanesa", "morcilla", "pan", "pata-muslo", "pechuga", "pollo", "riñon"]

    predictions_text_c = [f"{label}: {pred:.2f}" for label, pred in zip(labels_c, predictions_carnes[0])]
    print(", ".join(predictions_text_c))

    predicted_labels_text_c = [label for label, pred in zip(labels_c, predicted_labels_carnes[0]) if pred == 1]
    print("Etiquetas predichas frutas:", ", ".join(predicted_labels_text_c))
    print("-----------------------------------------------------------------------------------------------------")

    # Concatenar etiquetas y predicciones en una sola lista para simplificar
    all_labels = list(class_labels_v1) + list(class_labels_v2) + list(class_labels_f) + list(class_labels_carnes)
    all_predictions = np.concatenate([predicted_labels_v1[0], predicted_labels_v2[0], predicted_labels_f[0], predicted_labels_carnes[0]])

    # Obtener ingredientes en una sola línea
    ingredients = [all_labels[i] for i in range(len(all_predictions)) if all_predictions[i] == 1]
    return ingredients

# Ruta principal de la app
@app.route('/')
def index():
    return "Falta hacer el front..."

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        rag_chain, retriever = load_model()
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
            # prompt = f"Dame una receta con los siguientes ingredientes: {', '.join(all_ingredients)}."
            # generated_text = ollama.invoke(prompt)
            generated_text = ""
            titulo = parse_receta(generated_text)
            for chunk in rag_chain.stream({"context": retriever, "question": all_ingredients}):
                generated_text += chunk.content
            
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

if __name__ == "__main__":
    # Manejamos los errores con el metodo que creamos
    app.register_error_handler(404, pagina_no_encotrada)
    app.run()
