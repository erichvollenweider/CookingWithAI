from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langchain_community.llms import Ollama

app = Flask(__name__)
cors = CORS(app, origins='*')

ollama = Ollama(
    base_url='http://localhost:11434',
    model="gemma2:2b"
)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '') + "Responde en español"

        generated_text = ollama.invoke(prompt)

        # Devuelve el texto generado como JSON
        return jsonify({'response': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)