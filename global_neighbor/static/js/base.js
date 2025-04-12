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
        });
    }, 100);
});

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