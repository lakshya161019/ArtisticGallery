document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");

    form.addEventListener("submit", function (event) {
        let valid = true;

        // Clear previous error messages
        clearErrors();

        // Validate username
        if (!usernameInput.value) {
            showError(usernameError, "Username is required");
            valid = false;
        } else if (usernameInput.value.length < 8 || usernameInput.value.length > 20) {
            showError(usernameError, "Username must be between 8 and 20 characters");
            valid = false;
        }

        // Validate password
        if (!passwordInput.value) {
            showError(passwordError, "Password is required");
            valid = false;
        } else if (passwordInput.value.length < 8 || passwordInput.value.length > 20) {
            showError(passwordError, "Password must be between 8 and 20 characters");
            valid = false;
        }

        // Prevent form submission if validation fails
        if (!valid) {
            event.preventDefault();
        }
    });

    function showError(element, message) {
        element.textContent = message;
    }

    function clearErrors() {
        usernameError.textContent = '';
        passwordError.textContent = '';
    }
});
