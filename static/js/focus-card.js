const checkbox = document.getElementById('focus-checkbox');
const feedback = document.getElementById('focus-feedback');
checkbox.addEventListener('change', function() {
feedback.style.opacity = checkbox.checked ? '1' : '0';
});