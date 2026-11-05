/* ==========================================================
   chaver.com SITE TOOLS (Nov 2026) — the one line each page loads.
   1. the "Find a verse" box in the menu bar (verse-search.js)
   2. printing for Torah unit pages and Mishnah chapter pages (print.css):
      a Print button beside the heading, and print rules that put only
      the heading and the table on paper.
   ========================================================== */
(function () {
  'use strict';
  var BASE = '/torah-weave/Admin/Assets/';

  /* 1. verse search */
  if (!document.querySelector('script[src="' + BASE + 'JS/verse-search.js"]')) {
    var vs = document.createElement('script');
    vs.src = BASE + 'JS/verse-search.js'; vs.defer = true;
    document.head.appendChild(vs);
  }

  /* 2. printing — only on unit pages and Mishnah chapter pages */
  var path = decodeURIComponent(location.pathname);
  var isUnit = /\/(hebrew-)?[a-z]+-unit-\d+\/(hebrew-)?[a-z]+-unit-\d+(\.html?)?$/i.test(path);
  var isChapter = /\/Mishnah-New\/Hebrew\/Text\/.+ Perek \d+[ab]?(\.html?)?$/i.test(path);
  if (!isUnit && !isChapter) return;

  var tables = document.querySelectorAll('table.scripture-table');
  var h1 = document.querySelector('main h1') || document.querySelector('h1');
  if (!tables.length || !h1) return;

  var css = BASE + 'CSS/print.css';
  if (!document.querySelector('link[href="' + css + '"]')) {
    var link = document.createElement('link'); link.rel = 'stylesheet'; link.href = css;
    document.head.appendChild(link);
  }

  /* mark what prints: the heading block (or the h1 alone) and every table */
  var heading = h1.closest('.unit-header-section') || h1;
  var keep = [heading].concat(Array.prototype.slice.call(tables));
  keep.forEach(function (el) {
    el.classList.add('pk');
    for (var p = el.parentElement; p && p !== document.documentElement; p = p.parentElement) p.classList.add('pk-path');
  });
  document.body.classList.add('print-ready');

  /* the button, right after the heading */
  var hebrew = /^he/i.test(document.documentElement.getAttribute('lang') || '');
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'print-button';
  btn.textContent = hebrew ? 'הדפסה' : 'Print';
  btn.setAttribute('aria-label', hebrew ? 'הדפסת הטבלה' : 'Print the table');
  btn.addEventListener('click', function () { window.print(); });
  heading.parentNode.insertBefore(btn, heading.nextSibling);
})();
