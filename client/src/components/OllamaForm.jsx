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
      } else if (data.response) {
        setResponse(data.response);
      }
    } catch (err) {
      setError("Error en la solicitud al servidor.");
    } finally {
      setLoading(false);
    }
  };

  // Función para formatear la respuesta de la receta
  const renderRecipe = () => {
    if (!response) return null;

    // Aquí asumimos que la respuesta de Gemma2 está en un formato que podemos procesar
    const recipeLines = response.split("\n");
    let title = "";
    let ingredients = [];
    let preparation = [];
    let consejos = [];
    let currentSection = "";

    // Recorremos cada línea para clasificarla en su sección correspondiente
    recipeLines.forEach((line) => {
      if (line.includes("Ingredientes:")) {
        currentSection = "ingredients";
      } else if (line.includes("Preparación:") || line.includes("Instrucciones:")) {
        currentSection = "preparation";
      } else if (line.includes("Consejos:") || line.includes("Tips:")) {
        currentSection = "consejos";
      } else if (currentSection === "ingredients") {
        ingredients.push(line.trim());
      } else if (currentSection === "preparation") {
        preparation.push(line.trim());
      } else if (currentSection === "consejos") {
        consejos.push(line.trim());
      } else if (!title) {
        title = line.replace("##", "").trim();  // Eliminamos el "##" del título
      
        if (title.includes("Receta generada para los ingredientes:")) {
          title = title.replace("Receta generada para los ingredientes:", "").trim();
        }
      }
    });

    // Mostrar la receta formateada
    return (
      <div className={styles.recipeContainer}>
        <h2>{title}</h2>
        <h4>Ingredientes:</h4>
        <ul className={styles.cleanList}>
          {ingredients
            .filter((ingredient) => ingredient.length > 0 && !ingredient.match(/^\d+$/)) // Filtramos los números y espacios en blanco
            .map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
        </ul>

        <h4>Preparación:</h4>
        <ul className={styles.cleanList}>
          {preparation
            .filter((step) => step.length > 0 && !step.match(/^\d+$/)) // Filtramos los números y espacios en blanco
            .map((step, index) => (
              <li key={index}>{step}</li>
            ))}
        </ul>

        {consejos.length > 0 && (
          <>
            <h4>Consejos:</h4>
            <ul className={styles.cleanList}>
              {consejos
                .filter((consejo) => consejo.length > 0 && !consejo.match(/^\d+$/)) // Filtramos los números y espacios en blanco
                .map((consejo, index) => (
                  <li key={index}>{consejo}</li>
                ))}
            </ul>
          </>
        )}
      </div>
    );
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
        <div>
          {/* <button onClick={onLogout}>
            Cerrar sesión
          </button> 
          POR EL MOMENTO NO FUNCIONA, PONE TODA LA PANTALLA NEGRA*/}
        </div>
      </div>
      <div className={styles.chatContainer}>
        <img src="../../public/icon.png"></img>
        <h1>CookingWithAI</h1>
        <h2>Sube una imagen o ingresa los ingredientes para obtener una receta</h2>

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
          {response && renderRecipe()}
          {error && <p className={styles.errorMessage}>Error: {error}</p>}
        </div>
      </div>
    </div>
  );
};

export default OllamaForm;