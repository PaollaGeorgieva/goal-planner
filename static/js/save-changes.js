function enableEdit(span) {
  const text = span.innerText;
  const stepId = span.dataset.stepId;

  const input = document.createElement('input');
  input.type = 'text';
  input.value = text;
  input.className = 'edit-step-input';

  input.onblur = () => submitEdit(stepId, input.value, span);
  input.onkeydown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      input.blur();
    }
  };

  span.replaceWith(input);
  input.focus();
}

function submitEdit(stepId, newTitle, oldSpan) {
  fetch(`/steps/${stepId}/edit/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ title: newTitle }),
  })
  .then(response => {
    if (!response.ok) throw new Error("Update failed");
    return response.json();
  })
  .then(data => {
    const span = document.createElement('span');
    span.className = 'step-text';
    span.innerText = data.title;
    span.dataset.stepId = stepId;
    span.onclick = () => enableEdit(span);
    oldSpan.replaceWith(span);
  })
  .catch(err => {
    alert("Error updating step.");
    location.reload();  // fallback
  });
}

// CSRF helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}