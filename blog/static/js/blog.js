document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("tag-input");
    const suggestionBox = document.getElementById("tag-suggestions");
  
    let allTags = [];
    let activeIndex = -1;
  
    fetch("api/tags/")
      .then((res) => res.json())
      .then((data) => {
        allTags = data.tags || [];
      })
      .catch(() => {
        console.warn("Tag autocomplete: failed to fetch /api/tags/");
      });
  
    function updateSuggestions() {
      const raw = input.value;
      const typed = raw.split(",").pop().trim().toLowerCase();
      const selectedTags = raw
        .split(",")
        .map((t) => t.trim().toLowerCase())
        .filter(Boolean);
  
      suggestionBox.innerHTML = "";
      activeIndex = -1;
  
      if (!typed) {
        suggestionBox.classList.add("hidden");
        return;
      }
  
      const matches = allTags
        .filter(
          (tag) =>
            tag.toLowerCase().startsWith(typed) &&
            !selectedTags.includes(tag.toLowerCase())
        )
        .slice(0, 5);
  
      if (matches.length > 0) {
        matches.forEach((tag, index) => {
          const li = document.createElement("li");
          li.textContent = tag;
          li.className = "suggestion-item";
          li.setAttribute("role", "option");
          li.setAttribute("tabindex", "-1");
          if (index === 0) li.classList.add("active");
  
          li.addEventListener("click", () => applySuggestion(tag));
          suggestionBox.appendChild(li);
        });
        suggestionBox.classList.remove("hidden");
      } else {
        suggestionBox.classList.add("hidden");
      }
    }
  
    function applySuggestion(tag) {
      let parts = input.value.split(",");
      parts[parts.length - 1] = tag;
      input.value = parts.map((t) => t.trim()).join(", ") + ", ";
      suggestionBox.classList.add("hidden");
      input.focus();
    }
  
    input.addEventListener("input", updateSuggestions);
  
    input.addEventListener("keydown", (e) => {
      const items = suggestionBox.querySelectorAll(".suggestion-item");
      if (suggestionBox.classList.contains("hidden") || items.length === 0) return;
  
      if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (activeIndex >= 0 && items[activeIndex]) {
          applySuggestion(items[activeIndex].textContent);
        }
      }
  
      items.forEach((item, i) => {
        item.classList.toggle("active", i === activeIndex);
      });
    });
  
    document.addEventListener("click", (e) => {
      if (!suggestionBox.contains(e.target) && e.target !== input) {
        suggestionBox.classList.add("hidden");
      }
    });
  });
  
  // --- Appended second script (for #id_tags field) ---
  
  document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("id_tags");
    if (!input) return;
  
    const suggestionBox = document.createElement("div");
    suggestionBox.classList.add("tag-suggestions");
    suggestionBox.style.position = "absolute";
    suggestionBox.style.zIndex = "1000";
    suggestionBox.style.background = "#fff";
    suggestionBox.style.border = "1px solid #ccc";
    suggestionBox.style.borderRadius = "6px";
    suggestionBox.style.boxShadow = "0 2px 6px rgba(0,0,0,0.1)";
    suggestionBox.style.display = "none";
    suggestionBox.style.maxHeight = "200px";
    suggestionBox.style.overflowY = "auto";
  
    input.parentNode.appendChild(suggestionBox);
  
    input.addEventListener("input", async () => {
      const value = input.value.split(",").pop().trim();
      if (value.length === 0) {
        suggestionBox.style.display = "none";
        return;
      }
  
      try {
        const response = await fetch(`/api/tags/?q=${encodeURIComponent(value)}`);
        const tags = await response.json();
        suggestionBox.innerHTML = "";
  
        if (tags.length === 0) {
          suggestionBox.style.display = "none";
          return;
        }
  
        tags.forEach((tag) => {
          const item = document.createElement("div");
          item.textContent = tag;
          item.style.padding = "0.5rem";
          item.style.cursor = "pointer";

          item.addEventListener("click", () => {
            const parts = input.value.split(",");
            parts[parts.length - 1] = tag;
            input.value = parts.join(", ").replace(/\s+/, " ");
            suggestionBox.style.display = "none";
          });

          suggestionBox.appendChild(item);
        });

        const rect = input.getBoundingClientRect();
        suggestionBox.style.width = `${input.offsetWidth}px`;
        suggestionBox.style.display = "block";
      } catch (err) {
        console.error("Failed to fetch tags:", err);
      }
    });

    document.addEventListener("click", (e) => {
      if (!suggestionBox.contains(e.target) && e.target !== input) {
        suggestionBox.style.display = "none";
      }
    });
  });