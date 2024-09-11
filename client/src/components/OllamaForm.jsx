import React, { useState } from 'react';

const OllamaForm = () => {
  const [prompt, setPrompt] = useState('');  // Almacena el prompt
  const [loading, setLoading] = useState(false);  // Estado de carga
  const [response, setResponse] = useState('');  // Almacena la respuesta
  const [error, setError] = useState(null);  // Almacena los errores

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);  // Muestra el mensaje de "Cargando"
    setError(null);
    setResponse('');

    try {
      const res = await fetch('http://localhost:5000/consulta_ollama', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResponse(data.response);
      }
    } catch (err) {
      setError('Error en la solicitud al servidor.');
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div>
      <h1>CookingWithAI</h1>
      <h2>¿Qué quieres cocinar?</h2>
      
      <form onSubmit={handleSubmit}>
        {/* Input con el estilo de Uiverse */}
        <div className="textInputWrapper">
          <input
            placeholder="Escribe aquí..."
            type="text"
            className="textInput"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            required
          />
        </div>
        <button type="submit">Enviar</button>
      </form>

      {/* Mostrar estado de carga */}
      {loading && <p>Cargando...</p>}

      {/* Mostrar respuesta */}
      {response && <p>Respuesta: {response}</p>}

      {/* Mostrar error */}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
    </div>
  );
};

export default OllamaForm;
