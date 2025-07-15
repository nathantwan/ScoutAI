import React from 'react';
import { createRoot } from 'react-dom/client';
import Sidebar from '../components/Sidebar';
import '../index.css';

// Initialize the sidebar React app
const initSidebar = () => {
  const mountPoint = document.getElementById('scoutai-sidebar-root');
  
  if (!mountPoint) {
    console.error('ScoutAI: Could not find sidebar mount point');
    return;
  }

  const root = createRoot(mountPoint);
  
  const handleClose = () => {
    const sidebar = document.getElementById('scoutai-sidebar');
    if (sidebar) {
      sidebar.style.transform = 'translateX(100%)';
    }
  };

  root.render(
    <React.StrictMode>
      <Sidebar onClose={handleClose} />
    </React.StrictMode>
  );
};

// Wait for DOM to be ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSidebar);
} else {
  initSidebar();
} 