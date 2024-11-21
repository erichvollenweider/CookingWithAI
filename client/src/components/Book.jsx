import React, { useState, useEffect } from "react";
import "../styles/Book.css";
import 'font-awesome/css/font-awesome.min.css';
import {backendUrl} from "../config.js";

const Book = ({ isModalOpen,
                closeModal,
                numOfPapers,
                maxLocation,}) => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentLocation, setCurrentLocation] = useState(1);

  const openBook = () => {
    document.querySelector("#book").style.transform = "translateX(50%)";
    document.querySelector("#prev-btn").style.transform = "translateX(-360px)";
    document.querySelector("#next-btn").style.transform = "translateX(360px)";
  };

  const closeBook = (isAtBeginning) => {
    const bookElement = document.querySelector("#book");
    if (isAtBeginning) {
      bookElement.style.transform = "translateX(0%)";
    } else {
      bookElement.style.transform = "translateX(100%)";
    }
    document.querySelector("#prev-btn").style.transform = "translateX(0px)";
    document.querySelector("#next-btn").style.transform = "translateX(0px)";
  };

  const goNextPage = () => {
    if (currentLocation < maxLocation) {
      const paper = document.querySelector(`#p${currentLocation}`);
      if (paper) {
        paper.classList.add("flipped");
        paper.style.zIndex = currentLocation;
      }
      if (currentLocation === 1) openBook();
      if (currentLocation === numOfPapers) closeBook(false);
      setCurrentLocation((prev) => prev + 1);
    }
  };

  const goPrevPage = () => {
    if (currentLocation > 1) {
      const paper = document.querySelector(`#p${currentLocation - 1}`);
      if (paper) {
        paper.classList.remove("flipped");
        paper.style.zIndex = numOfPapers - currentLocation + 1;
      }
      if (currentLocation === 2) closeBook(true);
      if (currentLocation === maxLocation) openBook();
      setCurrentLocation((prev) => prev - 1);
    }
  };

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

      const cleanedRecipes = data.recetas.map((recipe) => {
        const parsedRecipe = parseRecipe(recipe.descripcion);
        return {
          ...recipe,
          titulo: cleanText(recipe.titulo),
          ingredientes: parsedRecipe.Ingredientes,
          preparacion: parsedRecipe.Preparación,
          consejos: parsedRecipe.Consejos,
        };
      });

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

  const parseRecipe = (text) => {
    const sections = cleanText(text)
      .split(/(Ingredientes|Preparación|Consejos)/g)
      .map((section) => section.trim())
      .filter((section) => section.length > 0);

    const result = {
      Ingredientes: "",
      Preparación: "",
      Consejos: "",
    };

    let currentKey = "";
    for (const section of sections) {
      if (["Ingredientes", "Preparación", "Consejos"].includes(section)) {
        currentKey = section;
      } else if (currentKey) {
        result[currentKey] += section;
      }
    }

    return result;
  };

  if (!isModalOpen) return null;

  return (
    <div className="modalOverlay" onClick={closeModal}>
      <div className="modalContent" onClick={(e) => e.stopPropagation()}>
        <div className="bookContainer">
          <button id="prev-btn" onClick={goPrevPage}>
            <i className="fa-solid fa-circle-arrow-left"></i>
          </button>

          <div id="book" className="book">
            {recipes.reduce((acc, _, index, arr) => {
              if (index % 2 === 0) {
                const frontRecipe = arr[index];
                const backRecipe = arr[index + 1];

                acc.push(
                  <div id={`p${Math.floor(index / 2) + 1}`} key={index} className="paper">
                    <div className="front">
                      <div className="frontContent">
                        <h3>{frontRecipe?.titulo}</h3>
                        <h4>Ingredientes:</h4>
                        <p>{frontRecipe?.ingredientes}</p>
                        <h4>Preparación:</h4>
                        <p>{frontRecipe?.preparacion}</p>
                        <h4>Consejos:</h4>
                        <p>{frontRecipe?.consejos}</p>
                      </div>
                    </div>
                    <div className="back">
                    <div className="backContent">
                      <h3>{backRecipe?.titulo}</h3>
                      <h4>Ingredientes:</h4>
                      <p>{backRecipe?.ingredientes}</p>
                      <h4>Preparación:</h4>
                      <p>{backRecipe?.preparacion}</p>
                      <h4>Consejos:</h4>
                      <p>{backRecipe?.consejos}</p>
                    </div>
                    </div>
                  </div>
                );
              }
              return acc;
            }, [])}
          </div>


          <button id="next-btn" onClick={goNextPage}>
            <i className="fa-solid fa-circle-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Book;

