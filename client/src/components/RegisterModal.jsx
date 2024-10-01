import React, { useState } from 'react';
import '../styles/AuthModals.css';


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
    <div className="modal">
      <div className="modal-content">
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
            />
          </div>
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
          <button type="submit">Registrar</button>
        </form>
        <button onClick={onClose}>Volver</button>
      </div>
    </div>
  );
};

export default RegisterModal;
