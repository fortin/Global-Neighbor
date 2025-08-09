document.addEventListener("DOMContentLoaded", () => {
  const uploadArea = document.getElementById("upload-area");
  const fileInput = document.getElementById("file-input");
  console.log("library_upload.js loaded");

  uploadArea.addEventListener("click", () => {
      console.log("Upload area clicked");
      fileInput.click();
  });

  fileInput.addEventListener("change", () => {
      console.log("File selected:", fileInput.files[0]?.name);
  });

  if (!uploadArea || !fileInput) return;

  // Clicking the box opens file picker
  uploadArea.addEventListener("click", () => {
    fileInput.click();
  });

  // Optional: highlight box on dragover
  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
  });

  uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
  });

  // Handle dropped files
  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  });

  // Handle manual file selection
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });

  console.log("File selected from picker:", fileInput.files[0]?.name);

function handleFileUpload(file) {
  console.log("Uploading file:", file.name);

  uploadArea.innerHTML = `<p>Uploading "${file.name}"...</p>`;

  const formData = new FormData();
  formData.append('document', file);

  fetch('/library/upload/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCSRFToken(),  // ensure this is defined (see below)
    },
  })
    .then(response => {
      console.log('Upload response:', response.status);
      if (response.ok) {
        uploadArea.innerHTML = `<p>Upload complete!</p>`;
        location.reload();  // optional
      } else {
        uploadArea.innerHTML = `<p>Upload failed.</p>`;
      }
    })
    .catch(error => {
      console.error('Upload error:', error);
      uploadArea.innerHTML = `<p>Upload failed (network error).</p>`;
    });
}
});

function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}