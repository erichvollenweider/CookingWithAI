import React, { useState } from 'react';
import LoginModal from './LoginModal';
import RegisterModal from './RegisterModal';


const AuthModals = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const handleOpenLogin = () => {
    setShowLogin(true);
    setShowRegister(false);
  };

  const handleOpenRegister = () => {
    setShowRegister(true);
    setShowLogin(false);
  };

  const handleCloseModals = () => {
    setShowLogin(false);
    setShowRegister(false);
  };

  return (
    <div>
      <button className="btn" onClick={handleOpenLogin}>Iniciar sesión</button>
      <button className="btn" onClick={handleOpenRegister}>Registrarse</button>

      {showLogin && <LoginModal onClose={handleCloseModals} />}
      {showRegister && <RegisterModal onClose={handleCloseModals} />}
    </div>
  );
};

export default AuthModals;
