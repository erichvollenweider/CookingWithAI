import React, { useState } from "react"; // Importa useState
import styles from "../styles/ChatWithAI.module.css";
import FileUpload from "./FileUpload";
import { QRCodeCanvas } from "qrcode.react";
import {frontUrl} from "../config.js"; // Importa QRCodeCanvas correctamente


const MessageBox = ({ handleFileChange, text, setText, handleSubmit }) => {
  const [showQR, setShowQR] = useState(false);
  const mobileUploadUrl = `${frontUrl}`;
  const toggleQR = () => {
    setShowQR((prev) => !prev);
  };

  return (
    <div className={styles.messageBox}>
      <FileUpload handleFileChange={handleFileChange} />
      <button type="button" onClick={toggleQR} className={styles.qrButton}>
        <i className="fa fa-mobile-alt"></i>
      </button>
      {showQR && (
        <div className={styles.modalOverlayQR}>
          <div className={styles.modalContentQR}>
            <button className={styles.closeButtonQR} onClick={toggleQR}>
              &times;
            </button>
            <QRCodeCanvas value={mobileUploadUrl} size={200} />
            <p>¡ Escanea el QR para abrir la aplicación en tu telefono !</p>
          </div>
        </div>
      )}
      <input
        placeholder="Ingredientes..."
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className={styles.messageInput}
      />
      <button className={styles.sendButton} type="submit" onClick={handleSubmit}>
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
            strokeLinejoin="round"
            strokeLinecap="round"
            strokeWidth="33.67"
            stroke="#6c6c6c"
            d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
          ></path>
        </svg>
      </button>
    </div>
  );
};

export default MessageBox;
