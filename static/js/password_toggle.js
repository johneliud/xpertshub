document.addEventListener('DOMContentLoaded', function() {
    // Get all toggle buttons
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Find the input field in the same container
            const container = this.parentElement;
            const input = container.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input && icon) {
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('bx-eye');
                    icon.classList.add('bx-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('bx-eye-slash');
                    icon.classList.add('bx-eye');
                }
            }
        });
    });
});
