// LoadingSpinner.jsx
import React from "react";
import styles from "../styles/ChatWithAI.module.css";

const LoadingSpinner = () => {
  return (
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
  );
};

export default LoadingSpinner;
