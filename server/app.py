from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import tensorflow as tf
import numpy as np
from langchain_community.llms import Ollama

app = Flask(__name__)
cors = CORS(app, origins='*')

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

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        if 'image' in request.files:
            image_file = request.files['image']
            image = Image.open(image_file)

            # Obtener los ingredientes de la imagen utilizando la función anterior
            ingredients = get_ingredients_from_image(image)

            if not ingredients:
                return jsonify({'error': 'No se detectaron ingredientes en la imagen'})

            # Crear el prompt para el modelo Ollama
            prompt = f"Give me a simple recipe using only the following ingredients: {', '.join(ingredients)}. Please avoid including unrelated or creative elements. You can add another simple ingredients to make a recipe if the provided ingredients aren't enough."

            # Llamar al modelo Ollama para generar la receta
            generated_text = ollama.invoke(prompt)
            return jsonify({'response': generated_text})
        else:
            return jsonify({'error': 'No image found in the request'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)