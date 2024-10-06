import React, { useState } from 'react';

import '../styles/ChatWithAI.module.css';

const OllamaForm = () => {
  const [files, setFiles] = useState([]);
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
    if (files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]);  // Subir cada archivo de imagen
      }
    }
    if (text) {
      formData.append('text', text);
    }
    
    // Verificar si no se envían ni texto ni imágenes
    if (files.length === 0 && !text) {
      setError('Por favor, sube una o más imágenes o ingresa un texto.');
      setLoading(false);
      return;
    }

    try {
      const res = await fetch('http://localhost:5000/consulta_ollama', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      // Manejar el error desde el backend
      if (data.error) {
        setError(data.error);
      } else if (data.results) {
        setResponse(data.results);  // En caso de que haya un resultado para texto
      } else if (data.response) {
        setResponse(data.response);  // En caso de que haya un resultado para imágenes
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
          <label>Subir imagenes:</label>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={(e) => {
              setFiles(Array.from(e.target.files));
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
              setFiles([]); // Limpiar el campo de imagen si se ingresa texto
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
