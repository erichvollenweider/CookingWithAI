import React, { useState } from "react";
import { QRCodeCanvas } from 'qrcode.react';
import styles from "../styles/ChatWithAI.module.css";
import mobileStyles from "../styles/ImageUploader.module.css";
import { frontUrl, backendUrl } from '../config';


const OllamaForm = ({ onLogout }) => {
  const [files, setFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [text, setText] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [error, setError] = useState(null);
  const [showSubmits, setShowSubmits] = useState(true);
  const [savedRecipes, setSavedRecipes] = useState([]);
  const [buttonVisible, setButtonVisible] = useState(true);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [showQR, setShowQR] = useState(false);  
  const [isMobile, setIsMobile] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const [isModalOpen, setIsModalOpen] = useState(false); 

  const handleFileChange = (e) => {
    const filesArray = Array.from(e.target.files); // Convertimos el FileList en array

    // Concatenamos los archivos nuevos con los anteriores
    setFiles((prevFiles) => [...prevFiles, ...filesArray]);

    // Creamos URLs para previsualizar las nuevas imágenes y las agregamos al estado
    const newUrls = filesArray.map((file) => URL.createObjectURL(file));
    setPreviewUrls((prevUrls) => [...prevUrls, ...newUrls]);
  };

  const handleRemoveImage = (index, event) => {
    event.preventDefault();
    const newFiles = [...files];
    const newPreviewUrls = [...previewUrls];

    newFiles.splice(index, 1);
    newPreviewUrls.splice(index, 1);

    setFiles(newFiles);
    setPreviewUrls(newPreviewUrls);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const toggleQR = () => setShowQR(!showQR);

  const mobileUploadUrl = `${frontUrl}`;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setButtonVisible(true);
    setShowSubmits(true);
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
      const res = await fetch(`${backendUrl}/consulta_ollama`, {
        method: "POST",
        body: formData,
        credentials: "include",
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
      setShowSubmits(false);
    }
  };

  // Función para guardar la receta manualmente
  const handleSaveRecipe = async () => {
    if (response) {
      try {
        const res = await fetch(`${backendUrl}/guardar_receta`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ response }),
          credentials: "include",
        });
        const data = await res.json();
        if (data.error) {
          alert(`Error: ${data.error}`);
        } else {
          setSavedRecipes((prevRecipes) => [...prevRecipes, response]);

          // Ocultar el botón y mostrar mensaje de éxito
          setButtonVisible(false);
          setShowSuccessMessage(true);

          // Ocultar el mensaje de éxito después de 3 segundos
          setTimeout(() => setShowSuccessMessage(false), 3000);
        }
      } catch (error) {
        alert("Hubo un error al guardar la receta.");
      }
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
      } else if (line.includes("Preparación:")) {
        currentSection = "preparation";
      } else if (line.includes("Consejos:")) {
        currentSection = "consejos";
      } else if (currentSection === "ingredients") {
        ingredients.push(line.replace(/\*/g, "").trim()); // Elimina los "*"
      } else if (currentSection === "preparation") {
        preparation.push(line.replace(/\*/g, "").trim()); // Elimina los "*"
      } else if (currentSection === "consejos") {
        consejos.push(line.replace(/\*/g, "").trim()); // Elimina los "*"
      } else if (!title) {
        title = line.replace("##", "").trim(); // Eliminamos el "##" del título
      }
    });

    // Mostrar la receta formateada
    return (
      <div>
        <h2>{title}</h2>
        <div className={styles.recipeContainer}>
          <h4>Ingredientes</h4>
          <ul className={styles.bulletList}>
            {ingredients
              .filter((ingredient) => ingredient.trim() !== "")
              .map((ingredient, index) => (
                <li key={index}>{ingredient}</li>
              ))}
          </ul>
        </div>
        <div className={styles.recipeContainer}>
          <h4>Preparación</h4>
          <ul className={styles.cleanList}>
            {preparation.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ul>
        </div>
        <div className={styles.recipeContainer}>
          {consejos.length > 0 && (
            <>
              <h4>Consejos</h4>
              <ul className={styles.cleanList}>
                {consejos.map((consejo, index) => (
                  <li key={index}>{consejo}</li>
                ))}
              </ul>
            </>
          )}
        </div>
        <div className={styles.saveRecipe}>
          {buttonVisible && (
            <button
              className={`${styles.confirmSave} ${styles.animateSave}`}
              onClick={handleSaveRecipe}
            >
              Guardar receta
            </button>
          )}

          {showSuccessMessage && (
            <p className={styles.successMessage}>Receta guardada con éxito</p>
          )}
        </div>
        <div className={styles.submitsPost}>
          <form onSubmit={handleSubmit}>
            <div className={styles.imagePreviewContainer}>
              {previewUrls.map((url, index) => (
                <div key={index} className={styles.imageWrapper}>
                  <img
                    key={index}
                    src={url}
                    alt={`preview-${index}`}
                    className={styles.imagePreview}
                  />
                  <button
                    className={styles.removeButton}
                    onClick={(e) => handleRemoveImage(index, e)}
                  >
                    ✖
                  </button>
                </div>
              ))}
            </div>

            <div className={styles.messageBox}>
              <div className={styles.fileUploadWrapper}>
                <label htmlFor="file">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 337 337"
                  >
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
                  <span className={styles.tooltip}>Add an image</span>
                </label>
                <input
                  type="file"
                  id="file"
                  accept="image/*"
                  multiple
                  onChange={handleFileChange}
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
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 664 663"
                >
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
      </div>
    );
  };

  return (
    <div className={isMobile ? mobileStyles.main : styles.main}>
      <div className={isMobile ? mobileStyles.container : styles.container}>
        <input
          className={styles.toggleCheckbox}
          id="toggle"
          type="checkbox"
          checked={sidebarOpen}
          onChange={toggleSidebar}
        />
        <label className={styles.hamburger} htmlFor="toggle">
          <div className={styles.bar}></div>
          <div className={styles.bar}></div>
          <div className={styles.bar}></div>
        </label>
        <div className={`${styles.sidebar} ${sidebarOpen ? styles.open : ""}`}>
          <h1>Mis Recetas</h1>
          <ul>
            <li>Receta 1</li>
            <li>Receta 2</li>
            <li>Receta 3</li>
            <li>Receta 4</li>
            <li>Receta 5</li>
            {/* {savedRecipes.map((recipe, index) => (
              <li key={index}>{recipe.split("\n")[0]}</li> // Mostrar título de la receta guardada
            ))} 
            POR AHORA NO AGREGAMOS AL COSTADO, HAY QUE VER COMO TRAER DE LA 
            BASE DE DATOS LAS RECETAS QUE TIENE EL USUARIO*/}
          </ul>
          <div className={styles.bottomButton}>
            <button onClick={onLogout} className={styles.logoutButton}>
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
      <div className={styles.chatContainer}>
        <div className={styles.header}>
          <img src="../../public/icon.png" className={styles.logo} />
          <div className={styles.headerLetters}>
            <h2>CookingWithAI</h2>
            <h3>¡ Las mejores y mas rapidas recetas !</h3>
          </div>
        </div>

        <div className={styles.aiResponse}>
          {loading && (
            <div className={styles.spinner}>
              <span>C</span>
              <span>O</span>
              <span>C</span>
              <span>I</span>
              <span>N</span>
              <span>A</span>
              <span>N</span>
              <span>D</span>
              <span>O</span>
            </div>
          )}
          {response && renderRecipe()}
          {error && <p className={styles.errorMessage}>Error: {error}</p>}
        </div>

        {showSubmits && (
          <div className={styles.submits}>
            <form onSubmit={handleSubmit}>
              <div className={styles.imagePreviewContainer}>
                {previewUrls.map((url, index) => (
                  <div key={index} className={styles.imageWrapper}>
                    <img
                      key={index}
                      src={url}
                      alt={`preview-${index}`}
                      className={styles.imagePreview}
                    />
                    <button
                      className={styles.removeButton}
                      onClick={(e) => handleRemoveImage(index, e)}
                    >
                      ✖
                    </button>
                  </div>
                ))}
              </div>

              {!isMobile && (
                <button onClick={toggleQR} className={styles.qrButton}>
                  {showQR ? "Ocultar QR" : "Subir desde móvil"}
                </button>
              )}

              {showQR && !isMobile && (  
                  <div className={styles.qrContainer}>
                    <QRCodeCanvas value={mobileUploadUrl} size={200} />
                    <p>Escanea el QR para subir imágenes desde tu móvil</p>
                  </div>
              )}

              <div className={styles.messageBox}>
                <div className={styles.fileUploadWrapper}>
                  <label htmlFor="file">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 337 337"
                    >
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
                    <span className={styles.tooltip}>Add an image</span>
                  </label>
                  <input
                    type="file"
                    id="file"
                    accept="image/*"
                    multiple
                    onChange={handleFileChange}
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
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 664 663"
                  >
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
        )}
      </div>
    </div>
  );
};

export default OllamaForm;
