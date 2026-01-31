/**
 * Image preview for flavor photo upload.
 * Shows selected image before form submission.
 */
document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.querySelector('input[type="file"][name="photo"]');
    if (!photoInput) return;

    // Find or create preview container
    const previewContainer = document.getElementById('photo-preview-container');

    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file || !file.type.startsWith('image/')) {
            // Clear preview if no valid image
            if (previewContainer) {
                const preview = previewContainer.querySelector('#photo-preview');
                if (preview) preview.remove();
            }
            return;
        }

        const reader = new FileReader();
        reader.onload = function(event) {
            let preview = document.getElementById('photo-preview');
            if (!preview) {
                preview = document.createElement('img');
                preview.id = 'photo-preview';
                preview.className = 'mt-3 rounded-lg max-w-full';
                preview.style.maxHeight = '200px';
                preview.style.objectFit = 'contain';
                if (previewContainer) {
                    previewContainer.appendChild(preview);
                }
            }
            preview.src = event.target.result;
            preview.alt = 'Podglad zdjecia';
        };
        reader.readAsDataURL(file);
    });
});
