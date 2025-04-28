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

    /**
     * Checks if all required form fields are filled
     * Enables or disables the submit button accordingly
     */
    function checkInputs() {
        let allFieldsFilled = emailField.value && passwordField.value;
        
        // If there's a select field (like on registration page), check that too
        if (selectField) {
            allFieldsFilled = allFieldsFilled && selectField.value;
        }
        
        submitBtn.disabled = !allFieldsFilled;
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
