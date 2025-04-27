document.addEventListener('DOMContentLoaded', function () {
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const registerBtn = document.getElementById('registerBtn');

    function checkInputs() {
        if (emailField.value && passwordField.value) {
            registerBtn.disabled = false;
        } else {
            registerBtn.disabled = true;
        }
    }

    // Initialize button state based on data-enabled attribute
    if (registerBtn.getAttribute('data-enabled') === 'true') {
        registerBtn.removeAttribute('disabled');
    }

    // Add event listeners to input fields
    emailField.addEventListener('input', checkInputs);
    passwordField.addEventListener('input', checkInputs);
});
