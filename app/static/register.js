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

emailField.addEventListener('input', checkInputs);
passwordField.addEventListener('input', checkInputs);
