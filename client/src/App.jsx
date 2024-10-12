import { useState, useEffect } from 'react';
import './App.css';
import OllamaForm from './components/OllamaForm';
import LoginModal from './components/LoginModal';
import RegisterModal from './components/RegisterModal';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [hasClicked, setHasClicked] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  useEffect(() => {
    const checkSession = async () => {
      const response = await fetch('http://localhost:5000/check_session');
      const data = await response.json();

      if (data.logged_in) {
        setIsLoggedIn(true);
      }
    };

    checkSession();
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLoginModal(false);
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/logout', {
        method: 'POST',
      });

      if (response.ok) {
        setIsLoggedIn(false);
        setShowLoginModal(true);
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
  }

  const handleCloseRegisterModal = () => {
    setShowRegisterModal(false);
    setShowLoginModal(true);
  };

  const handleBackgroundClick = () => {
    if (!isLoggedIn && !hasClicked) {
      setShowLoginModal(true);
      setHasClicked(true);
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

