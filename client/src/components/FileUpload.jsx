// components/FileUpload.jsx
import React from "react";
import styles from "../styles/ChatWithAI.module.css";

const FileUpload = ({ handleFileChange }) => (
  <div className={styles.fileUploadWrapper}>
    <label htmlFor="file">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 337 337">
        <circle strokeWidth="20" stroke="#6c6c6c" fill="none" r="158.5" cy="168.5" cx="168.5"></circle>
        <path strokeLinecap="round" strokeWidth="25" stroke="#6c6c6c" d="M167.759 79V259"></path>
        <path strokeLinecap="round" strokeWidth="25" stroke="#6c6c6c" d="M79 167.138H259"></path>
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
);

export default FileUpload;
