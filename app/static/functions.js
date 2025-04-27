document.addEventListener('DOMContentLoaded', function () {
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const selectField = document.getElementById('role'); 
    const submitBtn = document.getElementById('submitBtn');

    function checkInputs() {
        let allFieldsFilled = emailField.value && passwordField.value;
        
      
        if (selectField) {
            allFieldsFilled = allFieldsFilled && selectField.value;
        }
        
        submitBtn.disabled = !allFieldsFilled;
    }

    if (submitBtn.getAttribute('data-enabled') === 'true') {
        submitBtn.removeAttribute('disabled');
    }

    emailField.addEventListener('input', checkInputs);
    passwordField.addEventListener('input', checkInputs);
    
   
    if (selectField) {
        selectField.addEventListener('change', checkInputs);
    }
    
    checkInputs();
});
