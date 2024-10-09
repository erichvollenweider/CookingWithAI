import React, { useState } from 'react';
import styles from '../styles/AuthModals.module.css'; // Importa los estilos correctamente

const RegisterModal = ({ onClose, onRegister }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // Para manejar los mensajes de error

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(''); // Limpiar el mensaje de error

    // Llamar a la API de registro
    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }), // Enviar datos al backend
      });

      if (response.ok) {
        // Registro exitoso
        onRegister(); // Simula un registro exitoso y cierra el modal de registro
      } else {
        const data = await response.json();
        setError(data.message || 'Error en el registro'); // Mostrar mensaje de error
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Error al conectarse al servidor');
    }
  };

  return (
    <div className={styles.modalOverlay}> {/* Cambiado para usar los estilos del fondo oscuro */}
      <div className={styles.modalContainer}>
        <div className={styles.information}>
        <h2>COOKING</h2>
        <h2>WITH</h2>
        <h2>AI</h2> 
          <p>¡La nueva forma de cocinar!</p>
          <p>Descubre nuevas recetas y cocina con facilidad</p>
        </div>
        <div className={styles.modalContent}> {/* Cambiado para usar los estilos del contenido del modal */}
          <h2>Registrarse</h2>
          {error && <p style={{ color: 'red' }}>{error}</p>} {/* Mostrar mensaje de error */}
          <form onSubmit={handleSubmit}>
            <div>
              <label>Usuario:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className={styles.inputField} 
              />
            </div>
            <div>
              <label>Email:</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className={styles.inputField} 
              />
            </div>
            <div>
              <label>Contraseña:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={styles.inputField} 
              />
            </div>
            <button type="submit" className={styles.submitBtn}>Registrar</button> {/* Botón con estilos */}
            <button onClick={onClose} className={styles.closeBtn}>Volver</button> {/* Botón de cerrar */}
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterModal;
