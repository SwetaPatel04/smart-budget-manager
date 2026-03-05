const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  // Test directory
  testDir: './tests/e2e',
  
  // Run tests sequentially not in parallel
  workers: 1,
  
  // Retry failed tests once
  retries: 1,
  
  use: {
    // Base URL of our app
    baseURL: 'http://127.0.0.1:5000',
    
    // Take screenshot on failure
    screenshot: 'only-on-failure',
    
    // Slow down actions so we can see them
    actionTimeout: 10000,
  },
  
  // Only test on Chromium
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    }
  ]
});