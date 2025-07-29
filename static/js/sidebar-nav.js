
document.querySelectorAll('.sidebar-nav .nav-item').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    // Deactivate all
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(a => a.classList.remove('active'));
    document.querySelectorAll('.content .panel').forEach(p => p.classList.remove('active'));
    // Activate this
    link.classList.add('active');
    document.getElementById(link.dataset.target).classList.add('active');
  });
});
