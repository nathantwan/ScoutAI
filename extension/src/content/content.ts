import { draftDetector } from '../utils/draft-detector';

class ScoutAIContentScript {
  private sidebarContainer: HTMLElement | null = null;
  private isSidebarVisible = false;

  constructor() {
    this.init();
  }

  private init() {
    // Check if we're on a supported platform
    const platform = draftDetector.detectPlatform();
    if (!platform) {
      console.log('ScoutAI: Not on a supported fantasy platform');
      return;
    }

    // Check if we're on a draft page
    if (!draftDetector.isDraftPage()) {
      console.log('ScoutAI: Not on a draft page');
      return;
    }

    console.log('ScoutAI: Detected draft page, initializing...');
    
    // Wait for page to load completely
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupSidebar());
    } else {
      this.setupSidebar();
    }

    // Listen for navigation changes (for SPA sites)
    this.setupNavigationListener();
  }

  private setupSidebar() {
    // Create sidebar container
    this.createSidebarContainer();
    
    // Inject the React app
    this.injectSidebar();
    
    // Add toggle button
    this.addToggleButton();
  }

  private createSidebarContainer() {
    // Remove existing sidebar if any
    const existingSidebar = document.getElementById('scoutai-sidebar');
    if (existingSidebar) {
      existingSidebar.remove();
    }

    // Create new sidebar container
    this.sidebarContainer = document.createElement('div');
    this.sidebarContainer.id = 'scoutai-sidebar';
    this.sidebarContainer.style.cssText = `
      position: fixed;
      top: 0;
      right: 0;
      width: 384px;
      height: 100vh;
      z-index: 9999;
      background: white;
      box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
      border-left: 1px solid #e5e7eb;
      transform: translateX(100%);
      transition: transform 0.3s ease-in-out;
    `;

    document.body.appendChild(this.sidebarContainer);
  }

  private injectSidebar() {
    if (!this.sidebarContainer) return;

    // Create a script element to load the sidebar React app
    const script = document.createElement('script');
    script.src = chrome.runtime.getURL('sidebar.js');
    script.type = 'module';
    
    // Create a div for React to mount
    const mountPoint = document.createElement('div');
    mountPoint.id = 'scoutai-sidebar-root';
    this.sidebarContainer.appendChild(mountPoint);

    // Load the sidebar script
    document.head.appendChild(script);
  }

  private addToggleButton() {
    // Remove existing toggle button if any
    const existingButton = document.getElementById('scoutai-toggle');
    if (existingButton) {
      existingButton.remove();
    }

    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.id = 'scoutai-toggle';
    toggleButton.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12L5 10M5 10L12 3L19 10M5 10V20C5 20.5523 5.44772 21 6 21H9M19 10L21 12M19 10V20C19 20.5523 18.5523 21 18 21H15M9 21C9.55228 21 10 20.5523 10 20V16C10 15.4477 10.4477 15 11 15H13C13.5523 15 14 15.4477 14 16V20C14 20.5523 14.4477 21 15 21M9 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `;
    
    toggleButton.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      width: 48px;
      height: 48px;
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
      transition: all 0.2s ease-in-out;
    `;

    toggleButton.addEventListener('mouseenter', () => {
      toggleButton.style.transform = 'scale(1.1)';
      toggleButton.style.boxShadow = '0 6px 16px rgba(59, 130, 246, 0.4)';
    });

    toggleButton.addEventListener('mouseleave', () => {
      toggleButton.style.transform = 'scale(1)';
      toggleButton.style.boxShadow = '0 4px 12px rgba(59, 130, 246, 0.3)';
    });

    toggleButton.addEventListener('click', () => this.toggleSidebar());

    document.body.appendChild(toggleButton);
  }

  private toggleSidebar() {
    if (!this.sidebarContainer) return;

    this.isSidebarVisible = !this.isSidebarVisible;
    
    if (this.isSidebarVisible) {
      this.sidebarContainer.style.transform = 'translateX(0)';
    } else {
      this.sidebarContainer.style.transform = 'translateX(100%)';
    }
  }

  private setupNavigationListener() {
    // For SPAs, we need to detect navigation changes
    let currentUrl = window.location.href;
    
    const checkForNavigation = () => {
      if (window.location.href !== currentUrl) {
        currentUrl = window.location.href;
        
        // Small delay to let the page load
        setTimeout(() => {
          if (draftDetector.isDraftPage()) {
            this.setupSidebar();
          } else {
            this.cleanup();
          }
        }, 1000);
      }
    };

    // Check for navigation every second
    setInterval(checkForNavigation, 1000);
  }

  private cleanup() {
    const sidebar = document.getElementById('scoutai-sidebar');
    const toggle = document.getElementById('scoutai-toggle');
    
    if (sidebar) sidebar.remove();
    if (toggle) toggle.remove();
    
    this.sidebarContainer = null;
    this.isSidebarVisible = false;
  }
}

// Initialize the content script
new ScoutAIContentScript(); 