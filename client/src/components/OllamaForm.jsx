import React, { useState } from "react";
import styles from "../styles/ChatWithAI.module.css";

const OllamaForm = () => {
  const [files, setFiles] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResponse("");

    const formData = new FormData();
    if (files.length > 0) {
      for (let i = 0; i < files.length; i++) {
        formData.append("images", files[i]);
      }
    }
    if (text) {
      formData.append("text", text);
    }

    if (files.length === 0 && !text) {
      setError("Por favor, sube una o más imágenes o ingresa un texto.");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch("http://localhost:5000/consulta_ollama", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else if (data.results) {
        setResponse(data.results);
      } else if (data.response) {
        setResponse(data.response);
      }
    } catch (err) {
      setError("Error en la solicitud al servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.main}>
      <div className={styles.sidebar}>
        <h1>Recetas</h1>
        <p>Consultas previas</p>
        <ul>
          <li>Receta 1</li>
          <li>Receta 2</li>
          <li>Receta 3</li>
          <li>Receta 4</li>
          <li>Receta 5</li>
        </ul>
      </div>
      <div className={styles.chatContainer}>
        <img src="../../public/icon.png"></img>
        <h1>CookingWithAI</h1>
        <h2>
          Sube una imagen o ingresa los ingredientes para obtener una receta
        </h2>

        <div className={styles.submits}>
          <form onSubmit={handleSubmit}>
            <div className={styles.x}>
              <label className={styles.x}>Subir imágenes:</label>
              <input
                type="file"
                accept="image/*"
                multiple
                onChange={(e) => {
                  setFiles(Array.from(e.target.files));
                  setText("");
                }}
                className={styles.uploadButton}
              />
            </div>

            <div className={styles.x}>
              <label className={styles.x}>Ingresa ingredientes:</label>
              <input
                type="text"
                value={text}
                onChange={(e) => {
                  setText(e.target.value);
                  setFiles([]);
                }}
                className={styles.uploadText}
              />
            </div>
            <button type="submit" className={styles.sendButton}>
              Enviar
            </button>
          </form>
        </div>

        <div className={styles.aiResponse}>
          <h1>Zona de respuestas</h1>
          {loading && <p className={styles.x}>Cargando...</p>}
          {response && <p className={styles.x}>Respuesta: {response}</p>}
          {error && <p className={styles.errorMessage}>Error: {error}</p>}
        </div>
      </div>
    </div>
  );
};

export default OllamaForm;
