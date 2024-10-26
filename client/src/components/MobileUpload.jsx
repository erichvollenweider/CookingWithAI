import React, { useState } from "react";

const MobileUpload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]); // Guardar el archivo seleccionado en el estado
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

    if (!file) {
      alert("Por favor, selecciona un archivo antes de subir.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        " https://951d-186-122-108-6.ngrok-free.app/upload", // Cambiar la URL si el túnel cambia
        {
          method: "POST", // Asegúrate de que el método es POST
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Error al subir la imagen");
      }

      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("Error:", error);
      alert("Hubo un problema al subir la imagen.");
    }

    };
  

  return (
    <div>
      <h1>Subir Imagen</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          capture="camera" // Esto abrirá la cámara en dispositivos móviles
          onChange={handleFileChange}
        />
        <button type="submit">Subir Imagen</button>
      </form>
    </div>
  );
};

export default MobileUpload;
