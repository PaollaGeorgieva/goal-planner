const checkbox = document.getElementById('focus-checkbox');
const feedback = document.getElementById('focus-feedback');
const userId = window.userId; // от шаблона
const prefix = 'focus-';
const today = new Date().toISOString().slice(0, 10);
const storageKey = `${prefix}${userId}-${today}`;

function init() {
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key.startsWith(`${prefix}${userId}-`) && key !== storageKey) {
      localStorage.removeItem(key);
      i--;
    }
  }

  if (localStorage.getItem(storageKey) === '1') {
    checkbox.checked = true;
    checkbox.disabled = true;
    feedback.style.opacity = '0';
  }
}

checkbox.addEventListener('change', () => {
  if (checkbox.checked) {
    localStorage.setItem(storageKey, '1');
    feedback.style.opacity = '1';
    checkbox.disabled = true;
  } else {
    localStorage.removeItem(storageKey);
    feedback.style.opacity = '0';
  }
});

init();
