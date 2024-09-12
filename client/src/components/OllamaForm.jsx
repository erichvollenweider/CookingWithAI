import React, { useState } from 'react';

const OllamaForm = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResponse('');

    // Crear un objeto FormData para enviar la imagen
    const formData = new FormData();
    formData.append('image', file);

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
      <h2>Sube una imagen para analizar los ingredientes</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />
        <button type="submit">Enviar</button>
      </form>

      {loading && <p>Cargando...</p>}
      {response && <p>Respuesta: {response}</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
    </div>
  );
};

export default OllamaForm;