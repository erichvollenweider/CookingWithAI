import React, { useState } from 'react';
import styles from '../styles/AuthModals.module.css';

const LoginModal = ({ onClose, onLogin, onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        onLogin(); // Si es exitoso, se cierra el modal
      } else {
        setError(data.message || 'Error en el inicio de sesión');  // Muestra error
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Error al conectarse al servidor');
    }
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>Iniciar Sesión</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>} {/* Muestra el mensaje de error */}
        <form onSubmit={handleSubmit}>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Contraseña:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Ingresar</button>
        </form>
        <button onClick={onSwitchToRegister} className={styles.closeBtn}>Registrarse</button> {/* Botón para ir a registro */}
      </div>
    </div>
  );
};

export default LoginModal;