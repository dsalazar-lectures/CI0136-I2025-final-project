class FileUploadWidget {
    constructor(options = {}) {
        this.options = {
            serverUrl: options.serverUrl || '/upload',
            buttonText: options.buttonText || 'Subir archivo',
            buttonClass: options.buttonClass || 'btn btn-primary',
            uploadType: options.uploadType || 'attachment', // 'profile_picture' or 'attachment'
            onSuccess: options.onSuccess || this.defaultSuccessHandler,
            onError: options.onError || this.defaultErrorHandler,
            autoRender: options.autoRender !== false,
            multiple: options.multiple || false,
            accept: options.accept || this.getAcceptString(options.uploadType),
            ...options
        };
        
        this.fileInput = null;
        this.button = null;
        
        if (this.options.autoRender && !options.floating) {
            this.render();
        }
    }

    getAcceptString(uploadType) {
        if (uploadType === 'profile_picture') {
            return 'image/*';
        }
        return '*/*'; // Accept all files for general attachments
    }

    render(container) {
        // Create hidden file input
        this.fileInput = document.createElement('input');
        this.fileInput.type = 'file';
        this.fileInput.style.display = 'none';
        this.fileInput.accept = this.options.accept;
        this.fileInput.multiple = this.options.multiple;
        
        // Create visible button
        this.button = document.createElement('button');
        this.button.type = 'button';
        this.button.textContent = this.options.buttonText;
        this.button.className = this.options.buttonClass;
        
        // Handle file selection
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                this.uploadFile(e.target.files[0]);
            }
        });
        
        // Handle button click
        this.button.addEventListener('click', (e) => {
            e.preventDefault();
            this.fileInput.click();
        });
        
        // Append to container or body
        if (container) {
            if (typeof container === 'string') {
                container = document.querySelector(container);
            }
            if (container) {
                container.appendChild(this.button);
                container.appendChild(this.fileInput);
            }
        } else {
            document.body.appendChild(this.button);
            document.body.appendChild(this.fileInput);
        }
        
        return this.button;
    }

    async uploadFile(file) {
        if (!file) {
            this.options.onError('Ningún archivo seleccionado');
            return;
        }

        try {
            // Show loading state
            const originalText = this.button.textContent;
            this.button.disabled = true;
            this.button.textContent = 'Subiendo archivo...';

            // Create form data
            const formData = new FormData();
            formData.append('file', file);
            formData.append('upload_type', this.options.uploadType);

            // Upload file
            const response = await fetch(`${this.options.serverUrl}/file`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.options.onSuccess(result.file);
            } else {
                this.options.onError(result.error || 'Subida fallida');
            }
        } catch (error) {
            this.options.onError('Error de red: ' + error.message);
        } finally {
            // Restore button state
            if (this.button) {
                this.button.disabled = false;
                this.button.textContent = this.options.buttonText;
            }
        }
    }

    defaultSuccessHandler(file) {
        console.log('Archivo subido exitosamente:', file);
        alert(`Archivo "${file.original_name || file.name}" subido exitosamente.`);
    }

    defaultErrorHandler(error) {
        console.error('Fallo al subir:', error);
        alert(`Fallo al subir: ${error}`);
    }

    destroy() {
        if (this.button && this.button.parentNode) {
            this.button.parentNode.removeChild(this.button);
        }
        if (this.fileInput && this.fileInput.parentNode) {
            this.fileInput.parentNode.removeChild(this.fileInput);
        }
    }

    // Static method to create profile picture uploader
    static createProfileUploader(options = {}) {
        return new FileUploadWidget({
            uploadType: 'profile_picture',
            buttonText: ' Subir foto de perfil',
            accept: 'image/*',
            autoRender: false,
            ...options
        });
    }

    // Static method to create attachment uploader  
    static createAttachmentUploader(options = {}) {
        return new FileUploadWidget({
            uploadType: 'attachment',
            buttonText: 'Subir archivo',
            autoRender: false,
            ...options
        });
    }
}

// Make it available globally
window.FileUploadWidget = FileUploadWidget;

// Auto-create widgets from data attributes
document.addEventListener('DOMContentLoaded', () => {
    const autoElements = document.querySelectorAll('[data-upload-widget]');
    autoElements.forEach(element => {
        const options = {
            buttonText: element.getAttribute('data-text') || 'Subir archivo',
            serverUrl: element.getAttribute('data-server-url') || '/upload',
            uploadType: element.getAttribute('data-upload-type') || 'attachment'
        };
        
        const widget = new FileUploadWidget(options);
        widget.render(element);
    });
});
