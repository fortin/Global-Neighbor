document.addEventListener("DOMContentLoaded", function () {
  // Handle Sortable if present
  const categoryList = document.getElementById("category-list");
  if (typeof Sortable !== "undefined" && categoryList) {
    new Sortable(categoryList, {
      handle: ".category-card",
      animation: 150,
      onEnd: () => saveCategoryOrder(),
    });

    function getCurrentOrder() {
      const payload = [];
      document.querySelectorAll("#category-list .category-card").forEach((el, idx) => {
        const id = el.closest("li").dataset.id;
        payload.push({ id, order: idx });
      });
      return payload;
    }

    function saveCategoryOrder() {
      fetch(reorderUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ order: getCurrentOrder() }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) console.log("Order saved.");
          else alert("Failed to save order.");
        })
        .catch(() => alert("Failed to save order."));
    }
  }


  // Clickable category cards
  document.querySelectorAll(".clickable-card").forEach(card => {
    card.addEventListener("click", () => {
      const url = card.getAttribute("data-url");
      if (url) window.location.href = url;
    });
  });

  // Modals
  window.openCategoryModal = () => {
    document.getElementById("createCategoryModal")?.classList.remove("hidden");
  };

  window.closeCategoryModal = () => {
    document.getElementById("createCategoryModal")?.classList.add("hidden");
  };

  window.openDeleteModal = (postId) => {
    document.getElementById(`deleteModal-${postId}`)?.classList.remove("hidden");
  };

  window.closeDeleteModal = (postId) => {
    document.getElementById(`deleteModal-${postId}`)?.classList.add("hidden");
  };
});