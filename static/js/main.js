document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const generateBtn = document.getElementById('generateBtn');
    const spinner = generateBtn.querySelector('.spinner-border');
    const resultsSection = document.getElementById('resultsSection');
    const originalCode = document.getElementById('originalCode');
    const documentation = document.getElementById('documentation');
    const copyDocBtn = document.getElementById('copyDocBtn');
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');
    const errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
    const errorMessage = document.getElementById('errorMessage');

    // Add animation to file input when file is selected
    fileInput.addEventListener('change', function() {
        this.classList.add('bounce');
        setTimeout(() => this.classList.remove('bounce'), 500);
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            showError('Please select a file 📁');
            return;
        }

        // Show loading state with animation
        generateBtn.disabled = true;
        generateBtn.classList.add('pulse');
        spinner.classList.remove('d-none');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An error occurred');
            }

            // Hide results first
            resultsSection.style.display = 'none';

            // Update content
            originalCode.textContent = data.original_code;
            documentation.innerHTML = marked.parse(data.documentation);

            // Show results with animation
            resultsSection.style.display = 'flex';
            resultsSection.querySelectorAll('.card').forEach(card => {
                card.classList.add('fade-in');
            });

            // Highlight code
            Prism.highlightElement(originalCode);

        } catch (error) {
            showError(error.message + ' ❌');
        } finally {
            // Reset loading state
            generateBtn.disabled = false;
            generateBtn.classList.remove('pulse');
            spinner.classList.add('d-none');
        }
    });

    downloadPdfBtn.addEventListener('click', async function() {
        try {
            downloadPdfBtn.disabled = true;
            downloadPdfBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDF...';

            const response = await fetch('/download-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    documentation: documentation.innerText
                })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to generate PDF');
            }

            // Get the PDF blob
            const blob = await response.blob();

            // Create a download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'documentation.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Show success state
            downloadPdfBtn.innerHTML = '<i class="fas fa-check"></i> Downloaded! ✅';
            setTimeout(() => {
                downloadPdfBtn.innerHTML = '<i class="fas fa-file-pdf"></i> Download PDF';
                downloadPdfBtn.disabled = false;
            }, 2000);

        } catch (error) {
            showError('Error downloading PDF: ' + error.message + ' ❌');
            downloadPdfBtn.innerHTML = '<i class="fas fa-file-pdf"></i> Download PDF';
            downloadPdfBtn.disabled = false;
        }
    });

    copyDocBtn.addEventListener('click', function() {
        const docText = documentation.innerText;
        navigator.clipboard.writeText(docText).then(() => {
            copyDocBtn.classList.add('copy-success');
            copyDocBtn.innerHTML = '<i class="fas fa-check"></i> Copied! ✅';
            setTimeout(() => {
                copyDocBtn.classList.remove('copy-success');
                copyDocBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            }, 2000);
        });
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorToast.show();
    }
});