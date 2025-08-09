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
  const listBtn = document.getElementById('list-view-btn');
  const thumbBtn = document.getElementById('thumb-view-btn');

  // --- Toggle View Function ---
  window.setLibraryView = (view) => {
    if (view === 'list') {
      docContainer.classList.remove('thumbnail-view');
      docContainer.classList.add('document-list-view');
      listBtn.classList.add('active');
      thumbBtn.classList.remove('active');
    } else {
      docContainer.classList.add('thumbnail-view');
      docContainer.classList.remove('document-list-view');
      thumbBtn.classList.add('active');
      listBtn.classList.remove('active');
    }
  };

  // --- Filter Documents ---
  window.filterDocuments = () => {
    const keyword = searchInput.value.toLowerCase();
    const category = categoryFilter.value.toLowerCase();
    const tag = tagFilter.value.toLowerCase();

    const cards = docContainer.querySelectorAll('.document-card');

    cards.forEach(card => {
      const title = card.dataset.title.toLowerCase();
      const author = card.dataset.author.toLowerCase();
      const docCategory = card.dataset.category.toLowerCase();
      const tags = card.dataset.tags.toLowerCase();

      const matchesKeyword = title.includes(keyword) || author.includes(keyword);
      const matchesCategory = category === '' || docCategory === category;
      const matchesTag = tag === '' || tags.includes(tag);

      card.style.display = (matchesKeyword && matchesCategory && matchesTag) ? '' : 'none';
    });
  };

  // ✅ Move default grid view AFTER definition
  setLibraryView('thumbnails');
});