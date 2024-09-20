from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import tensorflow as tf
import numpy as np
from langchain_community.llms import Ollama
from database.models import Users
from database.conexion import db, init_app
from flask_bcrypt import Bcrypt

app = Flask(__name__)
cors = CORS(app, origins='*')
bcrypt = Bcrypt(app)

# Inicializar la base de datos
init_app(app)

# Cargar el modelo MobileNet preentrenado de TensorFlow
model = tf.keras.applications.MobileNetV2(weights="imagenet")
decode_predictions = tf.keras.applications.mobilenet_v2.decode_predictions
preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

ollama = Ollama(
    base_url='http://localhost:11434',
    model="gemma2:2b"
)

def get_ingredients_from_image(image):
    """Procesa la imagen y extrae los ingredientes utilizando MobileNet."""
    image = image.resize((224, 224))  # Redimensionar la imagen a lo que espera el modelo
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Preprocesar la imagen para MobileNet

    # Realizar predicción con el modelo
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=5)[0]  # Obtener las 5 principales predicciones

    # Filtrar las predicciones más relevantes
    ingredients = [pred[1] for pred in decoded_predictions]  # Obtenemos el nombre del objeto predicho
    return ingredients

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

            # Obtener los ingredientes de la imagen
            ingredients = get_ingredients_from_image(image)

            if not ingredients:
                return jsonify({'error': 'No se detectaron ingredientes en la imagen'})

            # Crear el prompt para Ollama basado en los ingredientes
            prompt = f"Dame una receta con los siguiente ingredientes: {', '.join(ingredients)}."
        
        # Verificar si se envio texto en lugar de una imagen
        elif 'text' in request.form:
            text = request.form['text']
            
            # Crear el prompt basado en el texto del usuario
            prompt = text
        
        else:
            return jsonify({'error': 'No image or text found in the request'})
        
        # Llamar al modelo Ollama para generar la receta
        generated_text = ollama.invoke(prompt)
        return jsonify({'response': generated_text})

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