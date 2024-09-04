import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ollama_url = 'http://localhost:11434/api/generate'

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        # Obtiene el prompt del request JSON
        data = request.get_json()
        prompt = data.get('prompt', '')

        # Prepara la solicitud a ollama
        ollama_data = {
            'model': 'mistral',
            'prompt': prompt,
            'format': 'json',
            'stream': False
        }

        # Envia la solicitud a ollama
        response = requests.post(ollama_url, json=ollama_data)
        response_json = response.json()

        # Extrae el campo 'response' de la respuesta JSON
        generated_text = response_json.get('response', 'No se genero respuesta')

        # Devuelve el texto generado como JSON
        return jsonify({'response': generated_text})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': e})

if __name__ == "__main__":
    app.run(debug=True)
