document.querySelectorAll('.reply-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = document.getElementById(btn.dataset.target);
      target.style.display = target.style.display === 'none' ? 'block' : 'none';
    });
  });
