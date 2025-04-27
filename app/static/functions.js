document.addEventListener('DOMContentLoaded', function () {
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const selectField = document.getElementById('role'); // Cambiado de 'selectId' a 'role'
    const submitBtn = document.getElementById('submitBtn');

    function checkInputs() {
        let allFieldsFilled = emailField.value && passwordField.value;
        
        // Solo verificar el select si existe en este formulario
        if (selectField) {
            allFieldsFilled = allFieldsFilled && selectField.value;
        }
        
        submitBtn.disabled = !allFieldsFilled;
    }

    // Initialize button state based on data-enabled attribute
    if (submitBtn.getAttribute('data-enabled') === 'true') {
        submitBtn.removeAttribute('disabled');
    }

    // Add event listeners to input fields
    emailField.addEventListener('input', checkInputs);
    passwordField.addEventListener('input', checkInputs);
    
    // Solo añadir event listener al select si existe
    if (selectField) {
        selectField.addEventListener('change', checkInputs);
    }
    
    // Verificar estado inicial
    checkInputs();
});
