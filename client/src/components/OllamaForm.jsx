import React, { useState } from "react";
import styles from "../styles/ChatWithAI.module.css";

const OllamaForm = ({ onLogout }) => {
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
      if (line.includes("Ingredientes:") || line.includes("Receta de:")) {
        currentSection = "ingredients";
      } else if (line.includes("Preparación:") || line.includes("Instrucciones:")) {
        currentSection = "preparation";
      } else if (line.includes("Consejos:") || line.includes("Tips:") || line.includes("Notas:")) {
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
        <div className={styles.bottomButton}>
          <button onClick={onLogout} className={styles.logoutButton}>
            Cerrar sesión
          </button>
        </div>
      </div>
      <div className={styles.chatContainer}>
        <h1>CookingWithAI</h1>
        <h3>Descubre recetas con ingredientes en casa</h3>
        <img src="../../public/icon.png"></img>

        <div className={styles.submits}>
          <form onSubmit={handleSubmit}>

            <div className={styles.messageBox}>
              <div className={styles.fileUploadWrapper}>
                <label htmlFor="file">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 337 337">
                    <circle
                      stroke-width="20"
                      stroke="#6c6c6c"
                      fill="none"
                      r="158.5"
                      cy="168.5"
                      cx="168.5"
                    ></circle>
                    <path
                      stroke-linecap="round"
                      stroke-width="25"
                      stroke="#6c6c6c"
                      d="M167.759 79V259"
                    ></path>
                    <path
                      stroke-linecap="round"
                      stroke-width="25"
                      stroke="#6c6c6c"
                      d="M79 167.138H259"
                    ></path>
                  </svg>
                  <span
                    className={styles.tooltip}>Add an image
                  </span>
                </label>
                <input
                  type="file"
                  id="file"
                  accept="image/*"
                  multiple
                  onChange={(e) => {
                    setFiles(Array.from(e.target.files));
                  }}
                  className={styles.file}
                  name="file"
                />
              </div>
              <input
                placeholder="Ingredientes..."
                type="text"
                value={text}
                onChange={(e) => {
                  setText(e.target.value);
                }}
                className={styles.messageInput}
              />
              <button className={styles.sendButton} type="submit">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 664 663">
                  <path
                    fill="none"
                    d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
                  ></path>
                  <path
                    stroke-linejoin="round"
                    stroke-linecap="round"
                    stroke-width="33.67"
                    stroke="#6c6c6c"
                    d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
                  ></path>
                </svg>
              </button>
            </div>
          </form>
        </div>

        <div className={styles.aiResponse}>
          {loading &&
            (<div className={styles.spinner}>
              <span>C</span>
              <span>O</span>
              <span>C</span>
              <span>I</span>
              <span>N</span>
              <span>A</span>
              <span>N</span>
              <span>D</span>
              <span>O</span>
            </div>)}
          {response && renderRecipe()}
          {error && <p className={styles.errorMessage}>Error: {error}</p>}
        </div>
      </div>
    </div>
  );
};

export default OllamaForm;