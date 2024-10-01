import React, { useState } from 'react';

import '../styles/ChatWithAI.css';

const OllamaForm = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResponse('');

    // Crear un objeto FormData para enviar la imagen o el texto
    const formData = new FormData();
    if (file) {
      formData.append('image', file);
    } else if (text) {
      formData.append('text', text);
    } else {
      setError('Por favor, sube una imagen o ingresa un texto.');
      setLoading(false);
      return;
    }

    try {
      const res = await fetch('http://localhost:5000/consulta_ollama', {
        method: 'POST',
        body: formData,
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
      <h2>Sube una imagen o ingresa los ingredientes para obtener una receta</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Subir imagen:</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setText(''); // Limpiar el campo de texto si se selecciona una imagen
            }}
          />
        </div>
        <div>
          <label>O ingresa ingredientes:</label>
          <input
            type="text"
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              setFile(null); // Limpiar el campo de imagen si se ingresa texto
            }}
          />
        </div>
        <button type="submit">Enviar</button>
      </form>

      {loading && <p>Cargando...</p>}
      {response && <p>Respuesta: {response}</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
    </div>
  );
};

export default OllamaForm;
