document.addEventListener("DOMContentLoaded", () => {
  const categoryList = document.getElementById("category-list");

  // Make categories draggable with SortableJS
  new Sortable(categoryList, {
    handle: ".category-card", // The element used to drag
    animation: 150, // Smooth animation when moving
    onEnd: () => saveCategoryOrder(), // Automatically save on change
  });

  // Function to collect the current order
  function getCurrentOrder() {
    const payload = [];
    document.querySelectorAll("#category-list .category-card").forEach((categoryEl, index) => {
      const categoryId = categoryEl.closest("li").dataset.id;
      payload.push({ id: categoryId, order: index });
    });
    return payload;
  }

  // Function to save the category order
  function saveCategoryOrder() {
    const payload = getCurrentOrder();

    fetch(reorderUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ order: payload }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          console.log("Category order saved successfully!");
        } else {
          alert("Failed to save order.");
        }
      })
      .catch(() => alert("Failed to save order."));
  }
});


// Optional: close when clicking outside the modal
window.onclick = function (event) {
  const modal = document.getElementById("createCategoryModal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("id_post-content");
  const preview = document.getElementById("markdown-preview");

  function updatePreview() {
    preview.innerHTML = marked.parse(input.value || "");
  }

  if (input && preview) {
    input.addEventListener("input", updatePreview);
    updatePreview();
  }

  // 🔧 GLOBAL toggle function
  window.togglePreview = function () {

   if (!input || !preview) return;

    preview.classList.toggle("hidden");

    if (!preview.classList.contains("hidden")) {
      preview.innerHTML = marked.parse(input.value || "");
    }
  };

  // Clickable category cards
  document.querySelectorAll(".clickable-card").forEach(card => {
    card.addEventListener("click", () => {
      const url = card.getAttribute("data-url");
      if (url) window.location.href = url;
    });
  });
});

function togglePreview() {
  const textarea = document.getElementById("id_content");
  const preview = document.getElementById("markdown-preview");
  if (preview.classList.contains("hidden")) {
    preview.innerHTML = marked.parse(textarea.value);
    preview.classList.remove("hidden");
  } else {
    preview.classList.add("hidden");
  }
}

// Live update as you type (optional)
document.getElementById("id_content").addEventListener("input", function () {
  const preview = document.getElementById("markdown-preview");
  if (!preview.classList.contains("hidden")) {
    preview.innerHTML = marked.parse(this.value);
  }
});


function togglePreview() {
  const textarea = document.getElementById("id_content");
  const preview = document.getElementById("markdown-preview");
  if (preview.classList.contains("hidden")) {
    preview.innerHTML = marked.parse(textarea.value);
    preview.classList.remove("hidden");
  } else {
    preview.classList.add("hidden");
  }
}

document.getElementById("id_content").addEventListener("input", function () {
  const preview = document.getElementById("markdown-preview");
  if (!preview.classList.contains("hidden")) {
    preview.innerHTML = marked.parse(this.value);
  }
});

function openCategoryModal() {
  document.getElementById("createCategoryModal").classList.remove("hidden");
}

function closeCategoryModal() {
  document.getElementById("createCategoryModal").classList.add("hidden");
}
