// Background service worker for ScoutAI Chrome extension

// Handle extension installation
chrome.runtime.onInstalled.addListener((details) => {
  console.log('ScoutAI extension installed:', details.reason);
  
  if (details.reason === 'install') {
    // Set default settings
    chrome.storage.local.set({
      enabled: true,
      apiUrl: 'http://localhost:8000',
      autoRefresh: true,
      refreshInterval: 30 // seconds
    });
  }
});

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('ScoutAI background received message:', request);
  
  switch (request.type) {
    case 'GET_DRAFT_STATE':
      // Forward to content script
      chrome.tabs.sendMessage(sender.tab!.id!, {
        type: 'EXTRACT_DRAFT_STATE'
      }, sendResponse);
      return true; // Keep message channel open for async response
      
    case 'API_REQUEST':
      // Handle API requests from content script
      handleAPIRequest(request.data)
        .then(sendResponse)
        .catch(error => sendResponse({ error: error.message }));
      return true;
      
    default:
      sendResponse({ error: 'Unknown message type' });
  }
});

// Handle API requests
async function handleAPIRequest(data: any) {
  try {
    const response = await fetch(`${data.url}`, {
      method: data.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...data.headers
      },
      body: data.body ? JSON.stringify(data.body) : undefined
    });
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('ScoutAI API request failed:', error);
    throw error;
  }
}

// Handle tab updates to check for draft pages
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    const url = new URL(tab.url);
    
    // Check if this is a supported fantasy platform
    if (url.hostname.includes('espn.com') || url.hostname.includes('yahoo.com')) {
      // Inject content script if not already injected
      chrome.scripting.executeScript({
        target: { tabId },
        files: ['content.js']
      }).catch(error => {
        console.log('ScoutAI: Content script already injected or failed:', error);
      });
    }
  }
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  if (tab.url && (tab.url.includes('espn.com') || tab.url.includes('yahoo.com'))) {
    // Send message to content script to toggle sidebar
    chrome.tabs.sendMessage(tab.id!, {
      type: 'TOGGLE_SIDEBAR'
    });
  } else {
    // Open popup for unsupported pages
    chrome.action.setPopup({ popup: 'popup.html' });
  }
});

// Handle storage changes
chrome.storage.onChanged.addListener((changes, namespace) => {
  console.log('ScoutAI storage changed:', changes, namespace);
  
  // Notify content scripts of settings changes
  chrome.tabs.query({}, (tabs) => {
    tabs.forEach(tab => {
      if (tab.url && (tab.url.includes('espn.com') || tab.url.includes('yahoo.com'))) {
        chrome.tabs.sendMessage(tab.id!, {
          type: 'SETTINGS_UPDATED',
          settings: changes
        }).catch(() => {
          // Ignore errors for tabs that don't have content scripts
        });
      }
    });
  });
});

console.log('ScoutAI background service worker loaded'); 