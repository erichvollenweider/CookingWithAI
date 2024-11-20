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
      goPrevPage && goPrevPage(1);
    }
  }, [isModalOpen]);

  const cleanText = (text) =>
    text.replace(/[^a-zA-ZÀ-ÿ0-9\s.,!?-]/g, "").trim();


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

      const cleanedRecipes = data.recetas.map((recipe) => ({
        ...recipe,
        titulo: cleanText(recipe.titulo),
        descripcion: cleanText(recipe.descripcion),
      }));

      const uniqueRecipes = Array.from(
        new Map(cleanedRecipes.map((recipe) => [recipe.id, recipe])).values()
      );

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
          <button
            onClick={() => goPrevPage(currentLocation - 1)}
            disabled={currentLocation === 1}
          >
            &lt;
          </button>

          <div className={styles.book} style={getBookStyle}>
            {loading ? (
              <p>Cargando recetas...</p>
            ) : error ? (
              <p>Error: {error}</p>
            ) : currentLocation === 1 ? (
              <div className={styles.initialPage}>
                <img src="../../public/tapa.png" className={styles.logoBookT} />
              </div>
            ) : currentLocation === maxLocation ? (
              <div className={styles.finalPage}>
                <img
                  src="../../public/contratapa.png"
                  className={styles.logoBookCT}
                />
              </div>
            ) : recipes.length === 0 ? (
              <p>No tienes recetas guardadas.</p>
            ) : (
              recipes.map((recipe, i) => {
                const isFlipped = currentLocation > i + 1; // Páginas ya pasadas
                const isCurrent = currentLocation === i + 1; // Página actual

                return (
                  <div
                    key={recipe.id}
                    className={`${styles.paper} ${
                      isFlipped ? styles.flipped : ""
                    } ${isCurrent ? styles.reverseFlip : ""}`}
                    style={{ zIndex: recipes.length - i }}
                  >
                    <div className={styles.front}>
                      <div className={styles.frontContent}>
                        <h3 className={styles.recipeTitle}>
                          {recipe.titulo}
                        </h3>
                        <p className={styles.recipeDescription}>
                          {recipe.descripcion}
                        </p>
                      </div>
                    </div>

                    <div className={styles.back}>
                      <div className={styles.backContent}>
                        <h3 className={styles.recipeTitle}>
                          {recipe.titulo}
                        </h3>
                        <p className={styles.recipeDescription}>
                          {recipe.descripcion}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          <button
            onClick={() => goNextPage(currentLocation + 1)}
            disabled={currentLocation === maxLocation}
          >
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
