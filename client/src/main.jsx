import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';


import './styles/AuthModals.module.css';
import './styles/ChatWithAI.module.css';
import './styles/ImageUploader.module.css';
import './index.css'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
