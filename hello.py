import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

ollama_url = 'http://localhost:11434/api/generate'

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/consulta_ollama', methods=['POST'])
def consulta_olama():
    try:
        # datos pasados por ejemplo, por consola con el curl
        data = request.get_json()
        # print("Datos recibidos:", data) 
        # post a ollama con el prompt
        response = requests.post(ollama_url, json=data)
        # obtenemos la respuesta de ollama
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})

