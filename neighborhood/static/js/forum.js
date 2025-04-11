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

function openCategoryModal() {
  document.getElementById("createCategoryModal").style.display = "block";
}
function closeCategoryModal() {
  document.getElementById("createCategoryModal").style.display = "none";
}

// Optional: close when clicking outside the modal
window.onclick = function (event) {
  const modal = document.getElementById("createCategoryModal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
};