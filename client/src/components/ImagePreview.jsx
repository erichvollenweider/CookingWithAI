// components/ImagePreview.jsx
import React from "react";
import styles from "../styles/ChatWithAI.module.css";

const ImagePreview = ({ previewUrls, handleRemoveImage }) => (
  <div className={styles.imagePreviewContainer}>
    {previewUrls.map((url, index) => (
      <div key={index} className={styles.imageWrapper}>
        <img src={url} alt={`preview-${index}`} className={styles.imagePreview} />
        <button
          className={styles.removeButton}
          onClick={(e) => handleRemoveImage(index, e)}
        >
          ✖
        </button>
      </div>
    ))}
  </div>
);

export default ImagePreview;
