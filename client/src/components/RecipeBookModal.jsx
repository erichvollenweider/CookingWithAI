import React from "react";
import styles from "../styles/ChatWithAI.module.css";

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
  if (!isModalOpen) return null;

  return (
    <div className={styles.modalOverlay} onClick={closeModal}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.bookContainer}>
          <button onClick={goPrevPage} disabled={currentLocation === 1}>
            &lt;
          </button>

          <div className={styles.book} style={getBookStyle}>
            {[...Array(numOfPapers)].map((_, i) => (
              <div
                key={i}
                className={`${styles.paper} ${currentLocation > i + 1 ? styles.flipped : ""}`}
                style={{ zIndex: currentLocation > i + 1 ? i + 1 : "" }}
              >
                <div className={styles.front}>
                  <div className={styles.frontContent}>Front {i + 1}</div>
                </div>
                <div className={styles.back}>
                  <div className={styles.backContent}>Back {i + 1}</div>
                </div>
              </div>
            ))}
          </div>

          <button onClick={goNextPage} disabled={currentLocation === maxLocation}>
            &gt;
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecipeBookModal;
