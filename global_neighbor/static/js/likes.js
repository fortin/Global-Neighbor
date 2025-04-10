document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".like-form").forEach((form) => {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
  
        const url = form.action;
        const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value;
        const button = form.querySelector(".like-button");
  
        fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((res) => {
            const contentType = res.headers.get("content-type") || "";
            console.log("Response content type:", contentType);
            if (!res.ok || !contentType.includes("application/json")) {
              throw new Error("Invalid JSON response");
            }
            return res.json();
          })
          .then((data) => {
            console.log("Like toggle success:", data);
            button.querySelector(".like-text").textContent = data.liked ? "Unlike" : "Like";
            button.querySelector(".like-count").textContent = data.likes_count ?? "0";
          })
          .catch((err) => {
            console.error("Like toggle failed:", err);
            if (err.message === "Invalid JSON response") {
              alert("Login required or bad server response.");
            } else {
              alert("Something went wrong — check console.");
            }
          });
      });
    });
});