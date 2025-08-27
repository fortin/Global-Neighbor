console.log('library_upload_modal.js loaded');

// --- Upload Modal ---
function openUploadModal() {
  const modal = document.getElementById('uploadModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('active');
    
    // Force description field styling
    setTimeout(() => {
      forceDescriptionStyling();
    }, 100);
  }
}

// Function to force description field styling
function forceDescriptionStyling() {
  console.log('forceDescriptionStyling called');
  
  const descriptionTextarea = document.getElementById('id_description');
  const helpText = document.querySelector('.description-input-wrapper .help-text');
  const wrapper = document.querySelector('.description-input-wrapper');
  
  console.log('descriptionTextarea:', descriptionTextarea);
  console.log('helpText:', helpText);
  console.log('wrapper:', wrapper);
  
  if (descriptionTextarea) {
    console.log('Applying styles to textarea');
    descriptionTextarea.style.setProperty('width', '100%', 'important');
    descriptionTextarea.style.setProperty('display', 'block', 'important');
    descriptionTextarea.style.setProperty('box-sizing', 'border-box', 'important');
    descriptionTextarea.style.setProperty('margin-bottom', '0.5rem', 'important');
    descriptionTextarea.style.setProperty('float', 'none', 'important');
    descriptionTextarea.style.setProperty('max-width', '100%', 'important');
    descriptionTextarea.style.setProperty('min-width', '100%', 'important');
    console.log('Textarea styles applied');
  }
  
  if (helpText) {
    console.log('Applying styles to help text');
    helpText.style.setProperty('display', 'block', 'important');
    helpText.style.setProperty('margin-top', '0.5rem', 'important');
    helpText.style.setProperty('margin-bottom', '1rem', 'important');
    helpText.style.setProperty('color', '#666', 'important');
    helpText.style.setProperty('font-size', '0.9rem', 'important');
    helpText.style.setProperty('clear', 'both', 'important');
    helpText.style.setProperty('width', '100%', 'important');
    helpText.style.setProperty('float', 'none', 'important');
    console.log('Help text styles applied');
  }
  
  if (wrapper) {
    console.log('Applying styles to wrapper');
    wrapper.style.setProperty('position', 'relative', 'important');
    wrapper.style.setProperty('width', '100%', 'important');
    wrapper.style.setProperty('display', 'block', 'important');
    console.log('Wrapper styles applied');
  }
}

function openCategoryModal() {
  const modal = document.getElementById('categoryModal');
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('active');
  }
}

function closeCategoryModal() {
  const modal = document.getElementById('categoryModal');
  if (modal) {
    modal.classList.remove('active');
    modal.classList.add('hidden');
  }
}

// --- Description Modal ---
function toggleDescriptionModal() {
  const modal = document.getElementById('descriptionModal');
  const textarea = document.getElementById('descriptionModalTextarea');
  const mainTextarea = document.getElementById('id_description');
  
  if (modal && textarea && mainTextarea) {
    // Copy current content to modal
    textarea.value = mainTextarea.value;
    
    modal.classList.remove('hidden');
    modal.classList.add('active');
  }
}

function closeDescriptionModal() {
  const modal = document.getElementById('descriptionModal');
  if (modal) {
    modal.classList.remove('active');
    modal.classList.add('hidden');
  }
}

function saveDescription() {
  const modal = document.getElementById('descriptionModal');
  const textarea = document.getElementById('descriptionModalTextarea');
  const mainTextarea = document.getElementById('id_description');
  
  if (textarea && mainTextarea) {
    // Copy content back to main form
    mainTextarea.value = textarea.value;
  }
  
  closeDescriptionModal();
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
  const titleField = document.getElementById('id_title');

  let selectedFile = null;

  // Force description styling on page load
  forceDescriptionStyling();

  // Open file selector on drop area click
  dropArea.addEventListener('click', () => fileInput.click());

  // Handle file drop
  dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length === 0) return;

    selectedFile = e.dataTransfer.files[0];
    dropArea.innerHTML = `<p>Selected: ${selectedFile.name}</p>`;
    prepopulateTitle(selectedFile.name);
  });

  // Handle file selection
  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length === 0) return;

    selectedFile = e.target.files[0];
    dropArea.innerHTML = `<p>Selected: ${selectedFile.name}</p>`;
    prepopulateTitle(selectedFile.name);
  });

  // Handle form submission
  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      alert("Please select a file before uploading.");
      return;
    }

    if (!titleField.value.trim()) {
      alert("Please enter a title for the document.");
      return;
    }

    uploadButton.disabled = true;
    uploadButton.textContent = 'Uploading...';

    const formData = new FormData(uploadForm);
    formData.set('file', selectedFile);  // Ensure correct file is sent

    try {
      const response = await fetch(uploadForm.action, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        closeUploadModal();
        location.reload();
      } else {
        alert("Upload failed.");
        uploadButton.disabled = false;
        uploadButton.textContent = 'Upload';
      }
    } catch (error) {
      alert("An error occurred during upload.");
      uploadButton.disabled = false;
      uploadButton.textContent = 'Upload';
    }
  });

  function prepopulateTitle(filename) {
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

    try {
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
    } catch (error) {
      alert('Network error.');
    }
  });
});