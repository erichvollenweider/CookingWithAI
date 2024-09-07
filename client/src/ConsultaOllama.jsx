import { useState } from 'react';

function ConsultaOllama() {
    const [prompt, setPrompt] = useState('');
    const [result, setResult] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:5000/consulta_ollama', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

        const data = await response.json();
        setResult(data.response || 'No se generó respuesta');
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h1>Consulta a Ollama</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="prompt">Ingresa tu prompt:</label>
                <input
                    type="text"
                    id="prompt"
                    name="prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    required
                /> 
                <button type="submit">Enviar</button>
            </form>
            <div id="result">{result}</div>
        </div>
    );
}

export default ConsultaOllama;
