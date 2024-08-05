const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-upload');
const fileDetails = document.getElementById('file-details');
const fileName = document.getElementById('file-name');
const fileRemove = document.getElementById('file-remove');
const uploadButton = document.getElementById('upload-button');
const fileContent = document.getElementById('file-content');
const uploadForm = document.getElementById('upload-form');
const successMessage = document.getElementById('success-message');

uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', (event) => {
    event.preventDefault();
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        showFileDetails(files[0]);
    }
});

fileInput.addEventListener('change', (event) => {
    if (fileInput.files.length > 0) {
        showFileDetails(fileInput.files[0]);
    }
});

fileRemove.addEventListener('click', () => {
    fileInput.value = '';
    fileDetails.style.display = 'none';
    uploadButton.style.display = 'none';
    fileContent.innerHTML = '';
});

uploadButton.addEventListener('click', async (event) => {
    event.preventDefault();
    const file = fileInput.files[0];
    if (file && file.size > 50 * 1024 * 1024) { // 50MB limit
        alert('File size exceeds 50MB limit.');
    } else {
        const formData = new FormData(uploadForm);
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (result.message) {
            showSuccessMessage();
            displayFileContent(result.content);
            // Save the file content to local storage
            localStorage.setItem('uploadedFileContent', result.content);
        } else {
            alert(result.error);
        }
    }
});

function showFileDetails(file) {
    fileName.textContent = file.name;
    fileDetails.style.display = 'flex';
    uploadButton.style.display = 'block';
}

function showSuccessMessage() {
    successMessage.style.display = 'block';
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 1000);
}

function displayFileContent(content) {
    fileContent.textContent = content;
}
