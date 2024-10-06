import { useState, useEffect } from 'react';
import './App.css'
import OllamaForm from './components/OllamaForm';; 
import LoginModal from './components/LoginModal'; 
import RegisterModal from './components/RegisterModal'; 

function App() {  
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(true);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  useEffect(() => {
    const checkSession = async () => {
      const response = await fetch('http://localhost:5000/check_session');
      const data = await response.json();
  
      if (data.logged_in) {
        setIsLoggedIn(true);  // Usuario está logueado
        setShowLoginModal(false);  // Oculta el modal de login si está logueado
      } else {
        setIsLoggedIn(false); // Usuario no está logueado
      }
    };
  
    checkSession();
  }, []);
  

  // Maneja el login
  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLoginModal(false); // Cierra el modal de login al iniciar sesión
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/logout', {
        method: 'POST',
      });
  
      if (response.ok) {
        console.log('Sesión cerrada correctamente');
        setIsLoggedIn(false); // Actualiza el estado del usuario
        setShowLoginModal(true);  // Muestra el modal de login nuevamente
      } else {
        console.error('Error al cerrar sesión');
      }
    } catch (err) {
      console.error('Error al conectarse al servidor:', err);
    }
  };

  // Abre el modal de registro
  const openRegisterModal = () => {
    setShowLoginModal(false); 
    setShowRegisterModal(true);
  };

  // Maneja el registro
  const handleRegister = () => {
    setShowRegisterModal(false); 
    setShowLoginModal(true); 
  };

  const handleCloseLoginModal = () => {
    setShowLoginModal(false); // Cierra el modal de login
  };

  const handleCloseRegisterModal = () => {
    setShowRegisterModal(false); // Cierra el modal de registro
    setShowLoginModal(true);
  };

  return (
    <div className={showLoginModal || showRegisterModal ? 'app-blur' : ''}>
      {isLoggedIn ? (
        <div>
          <OllamaForm />
          <button onClick={handleLogout}>Cerrar sesión</button>
        </div>
      ) : (
        <>
          {showLoginModal && (
            <LoginModal
              onClose={handleCloseLoginModal}
              onLogin={handleLogin}
              onSwitchToRegister={openRegisterModal} // Función para cambiar a modal de registro
            />
          )}
          {showRegisterModal && (
            <RegisterModal
              onClose={handleCloseRegisterModal}
              onRegister={handleRegister} // Función para manejar el registro exitoso
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
