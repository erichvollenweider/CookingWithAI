import React, { useState, useEffect } from "react";
import styles from "../styles/ChatWithAI.module.css";
import { backendUrl } from "../config";

const RecipeBookModal = ({
  isModalOpen,
  closeModal,
  currentLocation,
  goPrevPage,
  goNextPage,
  getBookStyle,
  numOfPapers,
  maxLocation,
}) => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isModalOpen) {
      fetchRecipes();
      // Aseguramos que currentLocation empiece en 1 al abrir el modal
      goPrevPage(1); // Si goPrevPage establece currentLocation, debe ir a la primera página
    }
  }, [isModalOpen]); // El hook se ejecuta cada vez que isModalOpen cambia

  const cleanText = (text) => {
    return text.replace(/[^a-zA-Z0-9\s.,!?]/g, ''); 
  };

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${backendUrl}/get_recipes`, {
        method: "GET",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Error al obtener recetas");
      }
      const data = await response.json();

      // Asegúrate de que solo se guarden recetas únicas
      const cleanedRecipes = data.recetas.map((recipe) => ({
        ...recipe,
        titulo: cleanText(recipe.titulo),
        descripcion: cleanText(recipe.descripcion),
      }));

      // Evitar duplicados
      const uniqueRecipes = Array.from(new Map(cleanedRecipes.map((recipe) => [recipe.id, recipe])).values());

      setRecipes(uniqueRecipes); 
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isModalOpen) return null;

  return (
    <div className={styles.modalOverlay} onClick={closeModal}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.bookContainer}>
          <button onClick={() => goPrevPage(currentLocation)} disabled={currentLocation === 1}>
            &lt;
          </button>

          <div className={styles.book} style={getBookStyle}>
            {loading ? (
              <p>Cargando recetas...</p>
            ) : error ? (
              <p>Error: {error}</p>
            ) : currentLocation === 1 ? (
              <div className={styles.initialPage}>
                <h2>CookingWithAI</h2>
                <p>Bienvenido a nuestro libro de recetas, donde la inteligencia artificial te ayuda a crear platos deliciosos.</p>
              </div>
            ) : currentLocation === maxLocation ? (
              <div className={styles.finalPage}>
                <h2>CookingWithAI</h2>
                <p>Gracias por usar nuestra app. ¡Esperamos que hayas disfrutado de las recetas!</p>
              </div>
            ) : recipes.length === 0 ? (
              <p>No tienes recetas guardadas.</p>
            ) : (
              recipes.map((recipe, i) => (
                <div
                  key={recipe.id}
                  className={`${styles.paper} ${currentLocation > i + 1 ? styles.flipped : ""}`}
                  style={{ zIndex: currentLocation > i + 1 ? i + 1 : "" }}
                >
                  <div className={styles.front}>
                    <div className={styles.frontContent}>
                      <h3 className={styles.recipeTitle}>{recipe.titulo}</h3>
                      <p className={styles.recipeDescription}>{recipe.descripcion}</p>
                    </div>
                  </div>
                  <div className={styles.back}>
                    <div className={styles.backContent}>
                      <h3 className={styles.recipeTitle}>{recipe.titulo}</h3>
                      <p className={styles.recipeDescription}>{recipe.descripcion}</p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          <button onClick={() => goNextPage(currentLocation)} disabled={currentLocation === maxLocation}>
            &gt;
          </button>
          <button className={styles.closeButton} onClick={closeModal}>
            &times;
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecipeBookModal;
