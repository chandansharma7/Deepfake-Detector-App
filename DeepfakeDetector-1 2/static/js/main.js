// Main JavaScript for the deepfake detector application

document.addEventListener('DOMContentLoaded', function() {
    // File input change handler
    const fileInput = document.getElementById('file-input');
    const fileLabel = document.querySelector('.custom-file-label');
    const uploadForm = document.getElementById('upload-form');
    const previewContainer = document.getElementById('preview-container');
    const submitBtn = document.getElementById('submit-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            // Update the file label with the selected file name
            const fileName = this.files[0]?.name || 'Choose file...';
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
            
            // Preview the selected file if it's an image
            if (this.files[0]) {
                const file = this.files[0];
                const fileType = file.type.split('/')[0];
                
                if (previewContainer) {
                    previewContainer.innerHTML = '';
                    
                    if (fileType === 'image') {
                        const preview = document.createElement('img');
                        preview.classList.add('file-preview', 'mt-3');
                        
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            preview.src = e.target.result;
                            previewContainer.appendChild(preview);
                        };
                        reader.readAsDataURL(file);
                    } else if (fileType === 'video') {
                        const preview = document.createElement('video');
                        preview.classList.add('file-preview', 'mt-3');
                        preview.controls = true;
                        
                        const source = document.createElement('source');
                        source.src = URL.createObjectURL(file);
                        source.type = file.type;
                        
                        preview.appendChild(source);
                        previewContainer.appendChild(preview);
                    }
                }
            }
        });
    }
    
    // Form submission handler
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            // Hide the submit button and show loading indicator
            if (submitBtn && loadingIndicator) {
                submitBtn.style.display = 'none';
                loadingIndicator.style.display = 'block';
            }
        });
    }
    
    // Initialize any tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggerList.length > 0) {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Make history table rows clickable
    const historyRows = document.querySelectorAll('.history-table tr[data-href]');
    historyRows.forEach(row => {
        row.addEventListener('click', () => {
            window.location.href = row.dataset.href;
        });
    });
    
    // Initialize confidence meter coloring
    const confidenceMeters = document.querySelectorAll('.confidence-meter-fill');
    confidenceMeters.forEach(meter => {
        const confidenceValue = parseFloat(meter.dataset.confidence || 0);
        meter.style.width = `${confidenceValue * 100}%`;
        
        if (confidenceValue >= 0.8) {
            meter.classList.add('high');
        } else if (confidenceValue >= 0.5) {
            meter.classList.add('medium');
        } else {
            meter.classList.add('low');
        }
    });
});

// Function to handle drag and drop file upload
function setupDragAndDrop() {
    const dropArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('file-input');
    
    if (dropArea && fileInput) {
        // Prevent default behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        // Highlight the drop area when drag over
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            dropArea.classList.add('border-primary');
            dropArea.classList.add('bg-light');
        }
        
        function unhighlight() {
            dropArea.classList.remove('border-primary');
            dropArea.classList.remove('bg-light');
        }
        
        // Handle dropped files
        dropArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length) {
                fileInput.files = files;
                // Trigger change event
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        }
    }
}

// Call drag and drop setup
document.addEventListener('DOMContentLoaded', setupDragAndDrop);
