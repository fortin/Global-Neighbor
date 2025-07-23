fileInput.addEventListener('change', (e) => {
  const filename = e.target.files[0]?.name || "";
  const titleField = document.querySelector('input[name="title"]');
  if (filename && titleField) {
    titleField.value = filename.replace(/\.[^/.]+$/, "");  // Remove extension
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const docContainer = document.getElementById('document-list-container');
  const searchInput = document.getElementById('library-search');
  const categoryFilter = document.getElementById('category-filter');
  const tagFilter = document.getElementById('tag-filter');

  window.setLibraryView = (view) => {
    if (view === 'list') {
      docContainer.classList.remove('thumbnail-view');
      docContainer.classList.add('document-list-view');
      document.getElementById('list-view-btn').classList.add('active');
      document.getElementById('thumb-view-btn').classList.remove('active');
    } else {
      docContainer.classList.add('thumbnail-view');
      docContainer.classList.remove('document-list-view');
      document.getElementById('thumb-view-btn').classList.add('active');
      document.getElementById('list-view-btn').classList.remove('active');
    }
  };

window.filterDocuments = () => {
  const keyword = searchInput.value.toLowerCase();
  const category = categoryFilter.value.toLowerCase();
  const tag = tagFilter.value.toLowerCase();

  const cards = docContainer.querySelectorAll('.document-card');

  cards.forEach(card => {
    const title = card.dataset.title.toLowerCase();
    const author = card.dataset.author.toLowerCase();  // Ensure data-author exists
    const docCategory = card.dataset.category.toLowerCase();
    const tags = card.dataset.tags.toLowerCase();

    const matchesKeyword = title.includes(keyword) || author.includes(keyword);
    const matchesCategory = category === '' || docCategory === category;
    const matchesTag = tag === '' || tags.includes(tag);

    if (matchesKeyword && matchesCategory && matchesTag) {
      card.style.display = '';
    } else {
      card.style.display = 'none';
    }
  });
};
});