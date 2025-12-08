document.addEventListener('DOMContentLoaded', function() {
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');

    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.innerHTML = "<i class='bx bx-eye-slash'></i>";
            } else {
                passwordInput.type = 'password';
                this.innerHTML = "<i class='bx bx-eye'></i>";
            }
        });
    });
});
