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

    // Create error message elements
    const emailError = document.createElement('div');
    const passwordError = document.createElement('div');

    // Style error messages
    [emailError, passwordError].forEach(error => {
        error.style.color = 'red';
        error.style.fontSize = '12px';
        error.style.marginTop = '5px';
        error.style.display = 'none'; // Hidden by default
    });

    emailError.textContent = 'Please enter a valid email address.';
    passwordError.textContent = 'Password must be at least 8 characters long.';

    // Append error messages to the DOM
    emailField.parentNode.appendChild(emailError);
    passwordField.parentNode.appendChild(passwordError);

    /**
     * Checks if all required form fields are filled and valid
     * Enables or disables the submit button accordingly
     */
    function checkInputs() {
        let allFieldsFilled = emailField.value && passwordField.value;
        
        // Validate email format
        const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value);
        if (!emailValid && emailField.value) {
            emailError.style.display = 'block';
        } else {
            emailError.style.display = 'none';
        }

        // Ensure password has at least 8 characters
        const isPasswordValid = passwordField.value.length >= 8;
        if (!isPasswordValid && passwordField.value) {
            passwordError.style.display = 'block';
        } else {
            passwordError.style.display = 'none';
        }

        // If there's a select field (like on registration page), check that too
        if (selectField) {
            allFieldsFilled = allFieldsFilled && selectField.value;
        }
        
        // Update button state based on all conditions
        submitBtn.disabled = !(allFieldsFilled && emailValid && isPasswordValid);
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