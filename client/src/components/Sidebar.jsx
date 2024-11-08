import React from "react";
import styles from "../styles/ChatWithAI.module.css";
import RecipeBookModal from "./RecipeBookModal";

const Sidebar = ({
  sidebarOpen,
  toggleSidebar,
  openModal,
  isModalOpen,
  closeModal,
  currentLocation,
  goPrevPage,
  goNextPage,
  getBookStyle,
  numOfPapers,
  maxLocation,
  onLogout,
}) => {
  return (
    <div className={styles.container}>
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
        <h4>¡No dejes que se escapen!</h4>
        <h5>Guarda estas recetas en tu libro para disfrutarlas siempre</h5>

        <div className={styles.recipeBookButton}>
          <button onClick={openModal}>
            <img src="../../public/libRecetas.png" alt="Mi Libro" />
            <h2>Mi Libro de</h2>
            <h2>Recetas</h2>
          </button>

          <RecipeBookModal
            isModalOpen={isModalOpen}
            closeModal={closeModal}
            currentLocation={currentLocation}
            goPrevPage={goPrevPage}
            goNextPage={goNextPage}
            getBookStyle={getBookStyle}
            numOfPapers={numOfPapers}
            maxLocation={maxLocation}
          />
        </div>

        <div className={styles.bottomButton}>
          <button onClick={onLogout} className={styles.logoutButton}>
            Cerrar sesión
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
