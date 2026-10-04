/* Progressive enhancement: all study text and diagrams work without JavaScript. */
document.documentElement.classList.add('js-ready');
document.querySelectorAll('[data-diagram]').forEach(function (diagram) {
  diagram.querySelectorAll('[data-highlight]').forEach(function (button) {
    button.addEventListener('click', function () {
      var active = button.getAttribute('aria-pressed') !== 'true';
      diagram.querySelectorAll('[data-highlight]').forEach(function (other) {
        other.setAttribute('aria-pressed', String(active && other === button));
      });
      diagram.querySelectorAll('[data-pair]').forEach(function (cell) {
        cell.classList.toggle('selected', active && cell.dataset.pair === button.dataset.highlight);
      });
    });
  });
});
document.querySelectorAll('[data-print]').forEach(function (button) {
  button.addEventListener('click', function () { window.print(); });
});
