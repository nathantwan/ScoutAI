// Popup script for ScoutAI extension

document.addEventListener('DOMContentLoaded', async () => {
  const statusElement = document.getElementById('status');
  const toggleButton = document.getElementById('toggleButton');
  const refreshButton = document.getElementById('refreshButton');

  // Check current tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  if (!tab.url) {
    statusElement.textContent = 'Unable to access current tab';
    statusElement.className = 'status error';
    return;
  }

  // Check if we're on a supported platform
  const isSupportedPlatform = tab.url.includes('espn.com') || tab.url.includes('yahoo.com');
  const isDraftPage = tab.url.includes('draft') || tab.url.includes('live');

  if (isSupportedPlatform && isDraftPage) {
    statusElement.textContent = 'Draft page detected! Click the toggle button to open ScoutAI.';
    statusElement.className = 'status success';
    toggleButton.disabled = false;
    toggleButton.textContent = 'Toggle ScoutAI Sidebar';
  } else if (isSupportedPlatform) {
    statusElement.textContent = 'Fantasy platform detected. Navigate to a draft page to use ScoutAI.';
    statusElement.className = 'status info';
    toggleButton.textContent = 'Not Available';
  } else {
    statusElement.textContent = 'Navigate to ESPN or Yahoo Fantasy to use ScoutAI.';
    statusElement.className = 'status info';
    toggleButton.textContent = 'Not Available';
  }

  // Handle toggle button click
  toggleButton.addEventListener('click', async () => {
    if (isSupportedPlatform && isDraftPage) {
      try {
        await chrome.tabs.sendMessage(tab.id, { type: 'TOGGLE_SIDEBAR' });
        window.close();
      } catch (error) {
        statusElement.textContent = 'Error: Could not communicate with page. Please refresh the page.';
        statusElement.className = 'status error';
      }
    }
  });

  // Handle refresh button click
  refreshButton.addEventListener('click', async () => {
    if (isSupportedPlatform && isDraftPage) {
      try {
        await chrome.tabs.sendMessage(tab.id, { type: 'REFRESH_RECOMMENDATIONS' });
        statusElement.textContent = 'Refreshing recommendations...';
        statusElement.className = 'status info';
        
        // Reset status after a moment
        setTimeout(() => {
          statusElement.textContent = 'Draft page detected! Click the toggle button to open ScoutAI.';
          statusElement.className = 'status success';
        }, 2000);
      } catch (error) {
        statusElement.textContent = 'Error: Could not refresh recommendations.';
        statusElement.className = 'status error';
      }
    } else {
      statusElement.textContent = 'Please navigate to a draft page first.';
      statusElement.className = 'status error';
    }
  });
}); 