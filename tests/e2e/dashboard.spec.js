const { test, expect } = require('@playwright/test');

// Test user details
const TEST_USER = {
    username: 'playwrightuser',
    email: 'playwright@test.com',
    password: 'password123'
};

// Helper function to register user
async function registerUser(page) {
    await page.goto('/');
    await page.click('#show-register');
    await page.waitForSelector('#register-page:not(.hidden)');
    await page.fill('#reg-username', TEST_USER.username);
    await page.fill('#reg-email', TEST_USER.email);
    await page.fill('#reg-password', TEST_USER.password);
    await page.click('#register-btn');
    await page.waitForSelector('#login-page:not(.hidden)');
}

// Helper function to login
async function loginUser(page) {
    await page.goto('/');
    await page.fill('#login-email', TEST_USER.email);
    await page.fill('#login-password', TEST_USER.password);
    await page.click('#login-btn');
    await page.waitForSelector('#dashboard-section:not(.hidden)', { timeout: 10000 });
}

// ── TEST 1: Page Loads ────────────────────────────────
test('page loads with login form', async ({ page }) => {
    await page.goto('/');
    
    // Check page title
    await expect(page).toHaveTitle(/Smart Budget/);
    
    // Check login form is visible
    await expect(page.locator('#login-email')).toBeVisible();
    await expect(page.locator('#login-password')).toBeVisible();
    
    console.log('✅ Page loads correctly');
});

// ── TEST 2: Register ──────────────────────────────────
test('user can register successfully', async ({ page }) => {
    await page.goto('/');
    
    // Click register link
    await page.click('#show-register');
    
    await page.waitForSelector('#register-page:not(.hidden)');

    // Fill registration form
    await page.fill('#reg-username', TEST_USER.username);
    await page.fill('#reg-email', TEST_USER.email);
    await page.fill('#reg-password', TEST_USER.password);

    // Submit form
    await page.click('#register-btn');
    
    // Should show success and redirect to login
    await expect(page.locator('#login-email')).toBeVisible({ timeout: 10000 });
    
    console.log('✅ Registration works');
});

// ── TEST 3: Login Success ─────────────────────────────
test('user can login successfully', async ({ page }) => {
    await page.goto('/');
    
    // Fill login form
    await page.fill('#login-email', TEST_USER.email);
    await page.fill('#login-password', TEST_USER.password);
    
    // Submit
    await page.click('#login-btn');
    
    // Should see dashboard
    await expect(page.locator('#dashboard-section')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('text=Smart Budget Manager')).toBeVisible();
    
    console.log('✅ Login works');
});

// ── TEST 4: Login Failure ─────────────────────────────
test('login fails with wrong password', async ({ page }) => {
    await page.goto('/');
    
    // Fill with wrong password
    await page.fill('#login-email', TEST_USER.email);
    await page.fill('#login-password', 'wrongpassword');
    
    // Submit
    await page.click('#login-btn');
    
    // Should see error message
    await expect(page.locator('#login-error')).toBeVisible();
    
    console.log('✅ Login failure handled correctly');
});

// ── TEST 5: Add Expense ───────────────────────────────
test('user can add an expense', async ({ page }) => {
    // await page.goto('/');
    
    // // Login first
    // await page.fill('#login-email', TEST_USER.email);
    // await page.fill('#login-password', TEST_USER.password);
    // await page.click('text=Login');
    
    // // Wait for dashboard
    // await expect(page.locator('#dashboard-section')).toBeVisible();
    
    // Add expense
    await loginUser(page);
    await page.fill('#exp-title', 'Test Grocery');
    await page.fill('#exp-amount', '75.50');
    await page.selectOption('#exp-category', 'Food');
    await page.click('#add-expense-btn');
    
    // Should see success message
    await expect(page.locator('#add-success')).toBeVisible({ timeout: 10000 });
    
    console.log('✅ Add expense works');
});

// ── TEST 6: Expense in Table ──────────────────────────
test('expense appears in table after adding', async ({ page }) => {
    // await page.goto('/');
    
    // // Login
    // await page.fill('#login-email', TEST_USER.email);
    // await page.fill('#login-password', TEST_USER.password);
    // await page.click('text=Login');
    
    // Wait for dashboard
    // await expect(page.locator('#dashboard-section')).toBeVisible();
    
    // Check expense appears in table
    await loginUser(page);
    await expect(page.locator('text=Test Grocery')).toBeVisible({ timeout: 10000 });   

    console.log('✅ Expense appears in table');
});

// ── TEST 7: Stats Update ──────────────────────────────
test('stats update after adding expense', async ({ page }) => {
    // await page.goto('/');
    
    // // Login
    // await page.fill('#login-email', TEST_USER.email);
    // await page.fill('#login-password', TEST_USER.password);
    // await page.click('text=Login');
    
    // // Wait for dashboard
    // await expect(page.locator('#dashboard-section')).toBeVisible();
    
    // Check stats are not zero
    await loginUser(page);
    const totalAmount = await page.locator('#stat-total-amount').textContent();
    expect(totalAmount).not.toBe('$0');
    
    console.log('✅ Stats update correctly');
});

// ── TEST 8: Chart Visible ─────────────────────────────
test('spending chart is visible', async ({ page }) => {
    // await page.goto('/');
    
    // // Login
    // await page.fill('#login-email', TEST_USER.email);
    // await page.fill('#login-password', TEST_USER.password);
    // await page.click('text=Login');
    
    // // Wait for dashboard
    // await expect(page.locator('#dashboard-section')).toBeVisible();
    
    // Check chart canvas is visible
    await loginUser(page);
    await expect(page.locator('#categoryChart')).toBeVisible();    

    console.log('✅ Chart is visible');
});

// ── TEST 9: Delete Expense ────────────────────────────
test('user can delete an expense', async ({ page }) => {
    // await page.goto('/');
    
    // // Login
    // await page.fill('#login-email', TEST_USER.email);
    // await page.fill('#login-password', TEST_USER.password);
    // await page.click('text=Login');
    
    // // Wait for dashboard
    // await expect(page.locator('#dashboard-section')).toBeVisible();
    
    // // Add expense to delete
    // await page.fill('#exp-title', 'Expense to Delete');
    // await page.fill('#exp-amount', '10.00');
    // await page.click('text=Add Expense');
    
    // // Wait for it to appear
    // await expect(page.locator('text=Expense to Delete')).toBeVisible();
    
    // // Click delete on last row
    // const deleteButtons = page.locator('button:has-text("Delete")');
    // await deleteButtons.first().click();
    await loginUser(page);
    await page.fill('#exp-title', 'Expense to Delete');
    await page.fill('#exp-amount', '10.00');
    await page.click('#add-expense-btn');
    await expect(page.locator('text=Expense to Delete')).toBeVisible({ timeout: 10000 });
    const deleteButtons = page.locator('button:has-text("Delete")');
    await deleteButtons.first().click();
    console.log('✅ Delete expense works');
});

// ── TEST 10: Logout ───────────────────────────────────
test('user can logout', async ({ page }) => {
    // await page.goto('/');
    
    // // Login
    // await page.fill('#login-email', TEST_USER.email);
    // await page.fill('#login-password', TEST_USER.password);
    // await page.click('text=Login');
    
    // // Wait for dashboard
    // await expect(page.locator('#dashboard-section')).toBeVisible();
    
    // // Click logout
    // await page.click('text=Logout');
    
    // // Should see login page again
    // await expect(page.locator('#login-email')).toBeVisible();
    await loginUser(page);
    await page.click('#logout-btn');
    await expect(page.locator('#login-email')).toBeVisible({ timeout: 10000 });
    console.log('✅ Logout works');
});
