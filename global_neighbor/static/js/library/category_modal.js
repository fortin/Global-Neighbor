function openCategoryModal() {
  const modal = document.getElementById('categoryModal');
  modal.classList.remove('hidden');
  modal.setAttribute('aria-hidden', 'false');
  modal.classList.add('active');
}

function closeCategoryModal() {
  const modal = document.getElementById('categoryModal');
  modal.classList.add('hidden');
  modal.setAttribute('aria-hidden', 'true');
  modal.classList.remove('active');
}

function deleteCategory(categoryId) {
  if (!confirm("Are you sure you want to delete this category?")) return;

  fetch(`/library/categories/delete/${categoryId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
    }
  }).then(response => {
    if (response.ok) {
      location.reload();
    } else {
      alert("Error deleting category.");
    }
  });
}

function getCSRFToken() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
  return csrfToken ? csrfToken.value : '';
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('addCategoryForm');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('newCategoryName').value.trim();
    if (!name) return;

    fetch('/library/categories/add/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: name })
    }).then(response => {
      if (response.ok) {
        location.reload();
      } else {
        alert("Error adding category.");
      }
    });
  });
});