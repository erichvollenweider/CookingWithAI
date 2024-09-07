from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langchain_community.llms import Ollama

app = Flask(__name__)
cors = CORS(app, origins='*')

# Inicializa el modelo Ollama
ollama = Ollama(
    base_url='http://localhost:11434',
    model="mistral"
)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/consulta_ollama', methods=['POST'])
def consulta_ollama():
    try:
        # Obtiene el prompt del request JSON
        data = request.get_json()
        prompt = data.get('prompt', '')

        # Usa el modelo Ollama para obtener la respuesta
        generated_text = ollama.invoke(prompt)

        # Devuelve el texto generado como JSON
        return jsonify({'response': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
