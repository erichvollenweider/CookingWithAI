import React from "react";
import styles from "../styles/ChatWithAI.module.css";
import Book from "./Book";

const Sidebar = ({
  sidebarOpen,
  toggleSidebar,
  openModal,
  isModalOpen,
  closeModal,
  goPrevPage,
  goNextPage,
  numOfPapers,
  maxLocation,
  onLogout,
  handleExport,
  fetchNumOfPapers,
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
          <button onClick={() => { openModal(); fetchNumOfPapers(); }}>
            <div className={styles.content}>
              <img src="../../public/book.svg"/>
              <p>Recetas Guardadas</p>
            </div>
          </button>

          <Book
            isModalOpen={isModalOpen}
            closeModal={closeModal}
            goPrevPage={goPrevPage}
            goNextPage={goNextPage}
            numOfPapers={numOfPapers}
            maxLocation={maxLocation}
          />
        </div>

        <div className={styles.recipeDownload}>
          <button onClick={handleExport} >
            <div className={styles.content}>
              <img src="../../public/download_icon.svg"/>
              <p>Descargar Recetas</p>
            </div>
          </button>
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
