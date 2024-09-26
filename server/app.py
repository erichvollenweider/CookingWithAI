from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
import numpy as np
import pandas as pd
import os
from langchain_community.llms import Ollama

# csv que contiene el nombre y las etiquetas
csv_file = 'dataset_clean.csv'
df = pd.read_csv(csv_file)

class_labels = df['label'].unique()

app = Flask(__name__)
cors = CORS(app, origins='*')
model_path = '/home/juancho_gonzalez/Escritorio/Proyecto/server/CookingWithAI/server/mejorModelo'

if os.path.exists(model_path):
    print(f'La ruta {model_path} es válida y existe.')
    # Cargar el modelo
    model = tf.keras.models.load_model(model_path)
    print("Modelo cargado correctamente.")
else:
    print(f'La ruta {model_path} no existe o es incorrecta.')

# procesar la imagen antes de hacer la predicción
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

@app.route("/")
def home():
    return render_template("index.html")

# Conexión Ollama
ollama = Ollama(
    base_url='http://localhost:11434',
    model="gemma2:2b"
)

# Ya con el modelo cargado y predecido, consultarle a ollama 
@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        if 'image' in request.files:
            image_file = request.files['image']
            image = Image.open(image_file)

            ingredient = get_ingredients_from_image(image)
            print(f"Predicted ingredient: {ingredient}")
            if not ingredient:
                return jsonify({'error': 'No se detectaron ingredientes en la imagen'})
            # Crear el prompt para el modelo Ollama
            prompt = f"Give me a simple recipe using the following ingredient: {ingredient}. Please avoid including unrelated or creative elements."
            # Llamar al modelo Ollama para generar la receta
            generated_text = ollama.invoke(prompt)
            return jsonify({'response': generated_text})
        else:
            return jsonify({'error': 'No image found in the request'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
# Ejecución
if __name__ == "__main__":
    app.run(debug=True)
