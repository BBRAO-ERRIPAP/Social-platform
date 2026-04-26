document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 4 seconds
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      bootstrap.Alert.getOrCreateInstance(alert).close();
    }, 4000);
  });

  // Character counter for post textarea
  const textarea = document.querySelector('textarea[name="content"]');
  if (textarea) {
    const max = 2000;
    const counter = document.createElement('small');
    counter.className = 'text-muted d-block text-end';
    counter.textContent = `0 / ${max}`;
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);
    textarea.addEventListener('input', function () {
      const len = this.value.length;
      counter.textContent = `${len} / ${max}`;
      counter.style.color = len > max * 0.9 ? '#dc3545' : '';
    });
  }
});