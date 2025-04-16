document.addEventListener("DOMContentLoaded", function () {
    // Search toggle
    const icon = document.getElementById("search-icon");
    const dropdown = document.getElementById("search-dropdown-container");
    if (icon && dropdown) {
        icon.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdown.classList.toggle("show");
        });
        document.addEventListener("click", function (e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove("show");
            }
        });
    }

    // Reply toggles
    document.querySelectorAll(".reply-toggle").forEach((btn) => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const replyId = this.dataset.replyId;
            const form = document.getElementById(`reply-form-${replyId}`);
            if (form) form.classList.toggle("hidden");
        });
    });

    // Delete confirmation
    const deleteModal = document.getElementById("deleteModal");
    if (deleteModal) {
        window.confirmDeletePost = () => (deleteModal.style.display = "block");
        window.closeDeleteModal = () => (deleteModal.style.display = "none");
    }

    // Initialize EasyMDE
    setTimeout(() => {
      document.querySelectorAll("textarea[id^='id_content']").forEach((el) => {
          if (!el.classList.contains("easymde-applied")) {
              new EasyMDE({
                  element: el,
                  forceSync: true,
                  spellChecker: false,
                  status: false,
                  toolbar: [
                      "bold", "italic", "heading", "|",
                      "quote", "unordered-list", "ordered-list", "|",
                      "link", "image", "|",
                      "preview", "side-by-side", "fullscreen", "|",
                      "guide"
                  ]
              });
              el.classList.add("easymde-applied");
          }
      });
}, 100);

function confirmDeletePost() {
    document.getElementById("deleteModal").style.display = "block";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_content") || document.getElementById("id_post-content");
    const preview = document.getElementById("markdown-preview");

    function updatePreview() {
      if (input && preview) {
        preview.innerHTML = marked.parse(input.value || "");
      }
    }

    if (input && preview) {
      input.addEventListener("input", updatePreview);
      updatePreview();

      window.togglePreview = function () {
        preview.classList.toggle("hidden");
        if (!preview.classList.contains("hidden")) {
          updatePreview();
        }
      };
    }
});

function togglePreview() {
    const textarea = document.getElementById("id_content");
    const preview = document.getElementById("markdown-preview");

    if (!textarea || !preview) return;

    const isHidden = preview.classList.contains("hidden");

    if (isHidden) {
      const markdownText = textarea.value;
      const html = marked.parse(markdownText);
      preview.innerHTML = html;
      preview.classList.remove("hidden");
    } else {
      preview.classList.add("hidden");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.querySelector("textarea[name='content']");
    const preview = document.getElementById("markdown-preview");

    if (textarea && preview) {
      textarea.addEventListener("input", () => {
        if (!preview.classList.contains("hidden")) {
          preview.innerHTML = marked.parse(textarea.value);
        }
      });
    }
});

function openModal(modalId, focusSelector = null) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');

    const focusTarget = focusSelector
      ? modal.querySelector(focusSelector)
      : modal.querySelector('input, button, textarea, [tabindex]:not([tabindex="-1"])');

    focusTarget?.focus();
    trapFocus(modal);
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
}

function trapFocus(modal) {
    const focusable = modal.querySelectorAll('a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), [tabindex]:not([tabindex="-1"])');
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    modal.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          last.focus();
          e.preventDefault();
        } else if (!e.shiftKey && document.activeElement === last) {
          first.focus();
          e.preventDefault();
        }
      }
    });
}

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      const openModals = document.querySelectorAll('.modal:not(.hidden)');
      openModals.forEach(modal => {
        modal.classList.add('hidden');
        modal.setAttribute('aria-hidden', 'true');
      });
    }
});