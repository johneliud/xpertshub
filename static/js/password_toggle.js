document.addEventListener('DOMContentLoaded', function() {
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');

    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Find the password input in the same parent container
            const container = this.parentElement;
            const passwordInput = container.querySelector('input[type="password"], input[type="text"]');
            
            if (passwordInput) {
                const icon = this.querySelector('i');
                
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.className = 'bx bx-eye-slash text-xl';
                } else {
                    passwordInput.type = 'password';
                    icon.className = 'bx bx-eye text-xl';
                }
            }
        });
    });
});
