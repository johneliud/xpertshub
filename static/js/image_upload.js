document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('imageUploadArea');
    const fileInput = document.getElementById('id_image');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const fileName = document.getElementById('fileName');
    const removeBtn = document.getElementById('removeImage');

    if (!uploadArea || !fileInput) return;

    // Hide the default file input
    fileInput.style.display = 'none';
    fileInput.required = true;

    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target !== removeBtn && !removeBtn.contains(e.target)) {
            fileInput.click();
        }
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('border-purple-400', 'bg-purple-50');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Remove image
    if (removeBtn) {
        removeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            clearPreview();
        });
    }

    function handleFile(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        if (!validTypes.includes(file.type)) {
            alert('Please select a valid image file (JPG, PNG, GIF)');
            return;
        }

        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB');
            return;
        }

        // Create FileList and assign to input
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;

        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            fileName.textContent = file.name;
            uploadPlaceholder.classList.add('hidden');
            imagePreview.classList.remove('hidden');
            
            // Remove error styling if present
            uploadArea.classList.remove('border-red-400');
        };
        reader.readAsDataURL(file);
    }

    function clearPreview() {
        fileInput.value = '';
        previewImg.src = '';
        fileName.textContent = '';
        uploadPlaceholder.classList.remove('hidden');
        imagePreview.classList.add('hidden');
    }

    // Form validation
    const form = fileInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!fileInput.files.length) {
                e.preventDefault();
                uploadArea.classList.add('border-red-400');
                uploadArea.scrollIntoView({ behavior: 'smooth' });
                alert('Please upload a service image');
            }
        });
    }
});
