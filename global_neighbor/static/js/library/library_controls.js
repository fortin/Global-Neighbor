document.addEventListener('DOMContentLoaded', () => {
  // --- Autofill title from chosen file ---
  const fileInput =
    document.querySelector('input[type="file"][name="file"]') ||
    document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      const filename = e.target.files && e.target.files[0] ? e.target.files[0].name : '';
      const titleField = document.querySelector('input[name="title"]');
      if (filename && titleField) {
        const base = filename.replace(/\.[^.]+$/, '');           // remove extension
        titleField.value = base.replace(/[_-]+/g, ' ').trim();   // prettify
      }
    });
  }

  const docContainer   = document.getElementById('document-list-container');
  const searchInput    = document.getElementById('library-search');
  const categoryFilter = document.getElementById('category-filter');
  const tagFilter      = document.getElementById('tag-filter');
  const listBtn        = document.getElementById('list-view-btn');
  const thumbBtn       = document.getElementById('thumb-view-btn');

  if (!docContainer) return; // nothing to do

  // --- Toggle View Function (kept global for onclicks) ---
  window.setLibraryView = (view) => {
    if (view === 'list') {
      docContainer.classList.remove('thumbnail-view');
      docContainer.classList.add('document-list-view');
      listBtn && listBtn.classList.add('active');
      thumbBtn && thumbBtn.classList.remove('active');
    } else {
      docContainer.classList.add('thumbnail-view');
      docContainer.classList.remove('document-list-view');
      thumbBtn && thumbBtn.classList.add('active');
      listBtn && listBtn.classList.remove('active');
    }
  };

  // --- Filter Documents (kept global for oninput/onchange) ---
  window.filterDocuments = () => {
    const keyword  = (searchInput?.value || '').toLowerCase();
    const category = (categoryFilter?.value || '').toLowerCase();
    const tag      = (tagFilter?.value || '').toLowerCase();

    const cards = docContainer.querySelectorAll('.document-card');
    cards.forEach((card) => {
      const title       = (card.dataset.title || '').toLowerCase();
      const author      = (card.dataset.author || '').toLowerCase();
      const docCategory = (card.dataset.category || '').toLowerCase();
      const tags        = (card.dataset.tags || '').toLowerCase();

      const matchesKeyword  = !keyword  || title.includes(keyword) || author.includes(keyword);
      const matchesCategory = !category || docCategory === category;
      const matchesTag      = !tag      || tags.includes(tag);

      card.style.display = (matchesKeyword && matchesCategory && matchesTag) ? '' : 'none';
    });
  };

  // --- Apply ?tag=... from URL AFTER defining filterDocuments ---
  try {
    const params = new URLSearchParams(window.location.search);
    const tagParam = params.get('tag');
    if (tagParam && tagFilter) {
      tagFilter.value = tagParam;
    }
  } catch (_) {}

  // Initial state
  setLibraryView('thumbnails');
  filterDocuments();
});