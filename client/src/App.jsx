import { useState, useEffect } from 'react';
import './App.css';
import OllamaForm from './components/OllamaForm';
import LoginModal from './components/LoginModal';
import RegisterModal from './components/RegisterModal';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  // Al cargar la aplicación, verificamos si ya hubo clic usando localStorage
  useEffect(() => {
    const checkSession = async () => {
      const response = await fetch('http://localhost:5000/check_session', {
        credentials: 'include',
      });
      const data = await response.json();

      if (data.logged_in) {
        setIsLoggedIn(true);
        setShowLoginModal(false);
        // Guardar en localStorage que ya se inició sesión para evitar mostrar el modal
        localStorage.setItem('hasLoggedOnce', 'true');
      } else {
        setIsLoggedIn(false);
        setShowLoginModal(true);  // Mostrar el modal automaticamente si no esta logueado
      }
    };

    checkSession();
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLoginModal(false);
    // Guardar en localStorage que ya se inició sesión exitosamente
    localStorage.setItem('hasLoggedOnce', 'true');
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        setIsLoggedIn(false);
        setShowLoginModal(true);
        // Al cerrar sesión, eliminamos el estado del localStorage
        localStorage.removeItem('hasLoggedOnce');
      }
    } catch (err) {
      console.error('Error al conectarse al servidor:', err);
    }
  };

  const openRegisterModal = () => {
    setShowLoginModal(false);
    setShowRegisterModal(true);
  };

  const handleCloseLoginModal = () => {
    setShowLoginModal(false);
  };

  const handleRegister = () => {
    setShowRegisterModal(false);
    setShowLoginModal(true);
  };

  const handleCloseRegisterModal = () => {
    setShowRegisterModal(false);
    setShowLoginModal(true);
  };

  const handleBackgroundClick = () => {
    // Verificar si ya se inició sesión al menos una vez (en localStorage)
    const hasLoggedOnce = localStorage.getItem('hasLoggedOnce') === 'true';

    // Mostrar el modal solo si NO se ha iniciado sesión y nunca se hizo clic antes
    if (!isLoggedIn && !hasLoggedOnce) {
      setShowLoginModal(true);
    }
  };

  return (
    <div onClick={handleBackgroundClick}>
      <OllamaForm onLogout={handleLogout} />
      {showLoginModal && (
        <LoginModal
          onClose={handleCloseLoginModal}
          onLogin={handleLogin}
          onSwitchToRegister={openRegisterModal}
        />
      )}
      {showRegisterModal && (
        <RegisterModal
          onClose={handleCloseRegisterModal}
          onRegister={handleRegister}
        />
      )}
    </div>
  );
}

export default App;
