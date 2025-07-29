document.addEventListener('DOMContentLoaded', function() {
      const navToggle = document.querySelector('.nav-toggle');
      const navLinks = document.querySelector('.nav-links');

      navToggle.addEventListener('click', function() {
        navLinks.classList.toggle('open');
      });

      document.addEventListener('click', function(event) {
        if (!navLinks.contains(event.target) && !navToggle.contains(event.target)) {
          navLinks.classList.remove('open');
        }
      });
    });