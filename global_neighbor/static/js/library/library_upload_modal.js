// --- Upload Modal ---
function openUploadModal() {
  const modal = document.getElementById('uploadModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('active');
  }
}

function closeUploadModal() {
  const modal = document.getElementById('uploadModal');
  if (modal) {
    modal.classList.remove('active');
    modal.classList.add('hidden');
  }
}

// --- CSRF ---
function getCSRFToken() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
  return csrfToken ? csrfToken.value : '';
}

// --- Prevent Drag & Drop Opening PDFs ---
document.addEventListener('dragover', (e) => e.preventDefault());
document.addEventListener('drop', (e) => e.preventDefault());

// --- Upload Modal Logic ---
document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('dropArea');
  const fileInput = document.getElementById('fileInput');
  const uploadForm = document.getElementById('uploadForm');
  const uploadButton = uploadForm.querySelector('button[type="submit"]');

  let selectedFile = null;

  dropArea.addEventListener('click', () => fileInput.click());

  dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    selectedFile = e.dataTransfer.files[0];
    dropArea.innerHTML = `<p>Selected: ${selectedFile.name}</p>`;
    prepopulateTitle(selectedFile.name);
  });

  fileInput.addEventListener('change', (e) => {
    selectedFile = e.target.files[0];
    dropArea.innerHTML = `<p>Selected: ${selectedFile.name}</p>`;
    prepopulateTitle(selectedFile.name);
  });

  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }

    uploadButton.disabled = true;
    uploadButton.textContent = 'Uploading...';

    const formData = new FormData(uploadForm);
    formData.append('file', selectedFile);

    const response = await fetch(uploadForm.action, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      alert("Upload successful!");
      closeUploadModal();
      location.reload();
    } else {
      alert("Upload failed.");
      uploadButton.disabled = false;
      uploadButton.textContent = 'Upload';
    }
  });

  function prepopulateTitle(filename) {
    const titleField = document.getElementById('id_title');
    if (titleField && filename) {
      titleField.value = filename.replace(/\.[^/.]+$/, '');  // Strip extension
    }
  }
});

// --- Category Manager ---
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('addCategoryForm');
  const nameInput = document.getElementById('newCategoryName');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = nameInput.value.trim();
    if (!name) return alert('Please enter a category name.');

    const csrfToken = getCSRFToken();

    const response = await fetch('/library/categories/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ name: name })
    });

    if (response.ok) {
      location.reload();
    } else {
      alert('Error adding category.');
    }
  });
});
