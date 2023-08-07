import React from 'react';
import ReactDOM from 'react-dom/client';
import './remedy.css'
import './index.css';
import App from './pages/app';
import { PostContextProvider } from './contexts/PostContext/index'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <PostContextProvider>
      <App />
    </PostContextProvider>
  </React.StrictMode>
);


