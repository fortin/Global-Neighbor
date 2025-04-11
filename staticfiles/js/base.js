document.addEventListener("DOMContentLoaded", function () {
    // Initialize EasyMDE for all visible textareas with id starting with id_content
    document.querySelectorAll("textarea[id^='id_content']").forEach(function (el) {
        new EasyMDE({
            element: el,
            forceSync: true,
            spellChecker: false,
            status: false,
            autosave: false,
            toolbar: [
                "bold", "italic", "heading", "|",
                "quote", "unordered-list", "ordered-list", "|",
                "link", "image", "|",
                "preview", "side-by-side", "fullscreen", "|",
                "guide"
            ]
        }, 100);
    });

    // Delete confirmation
    const deleteModal = document.getElementById("deleteModal");
    if (deleteModal) {
        window.confirmDeletePost = () => {
            deleteModal.style.display = "block";
        };
        window.closeDeleteModal = () => {
            deleteModal.style.display = "none";
        };
    }

    // Reply toggles
    document.querySelectorAll(".reply-toggle").forEach((btn) => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const replyId = this.dataset.replyId;
            const form = document.getElementById(`reply-form-${replyId}`);
            form.classList.toggle("hidden");
        });
    });
});

function confirmDeletePost() {
    document.getElementById("deleteModal").style.display = "block";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".reply-toggle").forEach((btn) => {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        const replyId = this.dataset.replyId;
        const form = document.getElementById(`reply-form-${replyId}`);
        form.classList.toggle("hidden");
        });
    });
});
