/**
 * Form validation functionality
 * This script handles dynamic form validation by enabling/disabling the submit button
 * based on whether all required fields are filled.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Get references to form elements
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const selectField = document.getElementById('role'); 
    const submitBtn = document.getElementById('submitBtn');
    const passwordTooltip = document.createElement('div'); // Tooltip element

    // Style the tooltip
    passwordTooltip.style.position = 'absolute';
    passwordTooltip.style.backgroundColor = '#f8d7da';
    passwordTooltip.style.color = '#721c24';
    passwordTooltip.style.padding = '5px';
    passwordTooltip.style.border = '1px solid #f5c6cb';
    passwordTooltip.style.borderRadius = '4px';
    passwordTooltip.style.fontSize = '12px';
    passwordTooltip.style.display = 'none'; // Hidden by default
    passwordTooltip.textContent = 'Password must be at least eight characters long.';
    document.body.appendChild(passwordTooltip);

    /**
     * Checks if all required form fields are filled
     * Enables or disables the submit button accordingly
     */
    function checkInputs() {
        let allFieldsFilled = emailField.value && passwordField.value;
        
        // Ensure password has at least 8 characters
        const isPasswordValid = passwordField.value.length >= 8;

        // If there's a select field (like on registration page), check that too
        if (selectField) {
            allFieldsFilled = allFieldsFilled && selectField.value;
        }
        
        // Update button state based on all conditions
        submitBtn.disabled = !(allFieldsFilled && isPasswordValid);

        // Show or hide tooltip based on password validity
        if (!isPasswordValid && passwordField.value) {
            const rect = passwordField.getBoundingClientRect();
            passwordTooltip.style.left = `${rect.left}px`;
            passwordTooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
            passwordTooltip.style.display = 'block';
        } else {
            passwordTooltip.style.display = 'none';
        }
    }

    // Initialize button state based on data attribute
    if (submitBtn.getAttribute('data-enabled') === 'true') {
        submitBtn.removeAttribute('disabled');
    }

    // Add input event listeners to form fields
    emailField.addEventListener('input', checkInputs);
    passwordField.addEventListener('input', checkInputs);
    
    // Add change listener to select field if it exists
    if (selectField) {
        selectField.addEventListener('change', checkInputs);
    }
    
    // Run initial check on page load
    checkInputs();
});