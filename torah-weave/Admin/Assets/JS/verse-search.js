/* ==========================================================
   chaver.com VERSE SEARCH — the "Find a verse or Mishnah chapter" box in
   the menu bar (Nov 2026). Type a Torah reference (Genesis 22:3, Gen 22,
   בראשית כב ג) and go to the literary unit that contains it — English pages
   to the English unit page, Hebrew pages to the Hebrew one; or a Mishnah
   chapter (Berakhot 2, Avot 1:1, ברכות ב) and go to its chapter page.
   Data, loaded only when the box is used: /torah-weave/api/by-verse.json
   and /torah-weave/Admin/Assets/JS/mishnah-chapters.json.
   Chapter lengths below follow the Hebrew verse numbering used on the site
   (checked: 5,846 verses).
   Styles: /torah-weave/Admin/Assets/CSS/verse-search.css
   ========================================================== */
(function () {
  'use strict';

  var CHAPTER_LENGTHS = {"Genesis":[31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,54,33,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26],"Exodus":[22,25,22,31,23,30,29,28,35,29,10,51,22,31,27,36,16,27,25,23,37,30,33,18,40,37,21,43,46,38,18,35,23,35,35,38,29,31,43,38],"Leviticus":[17,16,17,35,26,23,38,36,24,20,47,8,59,57,33,34,16,30,37,27,24,33,44,23,55,46,34],"Numbers":[54,34,51,49,31,27,89,26,23,36,35,16,33,45,41,35,28,32,22,29,35,41,30,25,18,65,23,31,39,17,54,42,56,29,34,13],"Deuteronomy":[46,37,29,49,30,25,26,20,29,22,32,31,19,29,23,22,20,22,21,20,23,29,26,22,19,19,26,69,28,20,30,52,29,12]};

  var BOOKS = [
    { key: 'Genesis', he: 'בראשית', names: ['genesis', 'gen', 'ge', 'gn', 'bereshit', 'bereishit', 'breishit', 'bereshith', 'בראשית'] },
    { key: 'Exodus', he: 'שמות', names: ['exodus', 'exod', 'exo', 'ex', 'shemot', 'shmot', 'shemoth', 'שמות'] },
    { key: 'Leviticus', he: 'ויקרא', names: ['leviticus', 'levit', 'lev', 'lv', 'le', 'vayikra', 'vayiqra', 'wayiqra', 'ויקרא'] },
    { key: 'Numbers', he: 'במדבר', names: ['numbers', 'numb', 'num', 'nu', 'nm', 'bamidbar', 'bemidbar', 'במדבר'] },
    { key: 'Deuteronomy', he: 'דברים', names: ['deuteronomy', 'deut', 'deu', 'dt', 'devarim', 'dvarim', 'דברים'] }
  ];

  var HEB = { 'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,'כ':20,'ך':20,'ל':30,'מ':40,'ם':40,'נ':50,'ן':50,'ס':60,'ע':70,'פ':80,'ף':80,'צ':90,'ץ':90,'ק':100 };

  function toNumber(tok) {
    if (/^\d+$/.test(tok)) return parseInt(tok, 10);
    if (/^[א-ת]+$/.test(tok)) {
      var n = 0;
      for (var i = 0; i < tok.length; i++) { if (!HEB[tok[i]]) return null; n += HEB[tok[i]]; }
      return n;
    }
    return null;
  }

  /* Read a reference. Returns {book, chapter, verse|null} or null. */
  function parse(input) {
    var s = String(input || '')
      .replace(/[֑-ׇ]/g, '')          /* vowel points and accents */
      .replace(/[״׳"'`’]/g, '')                 /* gershayim, geresh, quotes */
      .replace(/[‐-―]/g, '-')          /* dashes */
      .toLowerCase().replace(/\s+/g, ' ').trim();
    s = s.replace(/^(ספר|sefer|the book of|book of)\s+/, '');
    var all = [];
    BOOKS.forEach(function (b) { b.names.forEach(function (n) { all.push({ name: n, book: b }); }); });
    all.sort(function (a, b) { return b.name.length - a.name.length; });
    var found = null, rest = '';
    for (var i = 0; i < all.length; i++) {
      var n = all[i].name;
      if (s.indexOf(n) === 0) {
        var next = s.charAt(n.length);
        if (next === '' || /[\s.:,\d-]/.test(next)) { found = all[i].book; rest = s.slice(n.length); break; }
      }
    }
    if (!found) return null;
    rest = rest.replace(/\b(chapter|chap|ch|verses|verse|vv|v)\b\.?/g, ' ')
               .replace(/(^|\s)(פרק|פסוקים|פסוק)(?=\s|$)/g, ' ')
               .replace(/[.:,;]/g, ' ').trim();
    if (!rest) return null;
    var toks = rest.split(/[\s-]+/).filter(Boolean);
    var ch = toNumber(toks[0]);
    if (ch === null) return null;
    var v = toks.length > 1 ? toNumber(toks[1]) : null;
    if (toks.length > 1 && v === null) return null;
    return { book: found.key, chapter: ch, verse: v };
  }

  /* Find the unit(s) for a parsed reference in the by-verse data. */
  function resolve(ref, data) {
    var info = data.books[ref.book];
    var lens = CHAPTER_LENGTHS[ref.book];
    if (!info || ref.chapter < 1 || ref.chapter > lens.length) return { error: 'chapter', ref: ref };
    if (ref.verse === null) {
      var nums = (data.by_chapter[ref.book] || {})[String(ref.chapter)] || [];
      var units = info.ranges.filter(function (r) { return nums.indexOf(r.unit) !== -1; });
      return units.length ? { units: units, book: ref.book } : { error: 'chapter', ref: ref };
    }
    if (ref.verse < 1 || ref.verse > lens[ref.chapter - 1]) return { error: 'verse', ref: ref, max: lens[ref.chapter - 1] };
    var key = ref.chapter * 1000 + ref.verse;
    for (var i = 0; i < info.ranges.length; i++) {
      var r = info.ranges[i];
      if (r.start.chapter * 1000 + r.start.verse <= key && key <= r.end.chapter * 1000 + r.end.verse) {
        return { units: [r], book: ref.book };
      }
    }
    /* A verse inside the chapter that no range lists (Exodus 20:23, whose printed
       number is unreadable in the edition, is listed only by its unit's chapter):
       take the unit that ends in this chapter. */
    var inChapter = (data.by_chapter[ref.book] || {})[String(ref.chapter)] || [];
    var last = info.ranges.filter(function (r) { return inChapter.indexOf(r.unit) !== -1 && r.end.chapter === ref.chapter; });
    if (last.length) return { units: [last[last.length - 1]], book: ref.book };
    return { error: 'verse', ref: ref, max: lens[ref.chapter - 1] };
  }

  /* ---------- Mishnah ---------- */
  /* Fold small spelling differences: Latin kh/ch, tz/ts and doubled letters
     ('Berachot', 'Berakhot'); Hebrew final letters and doubled ו/י ('כלאים',
     'כלאיים'). Other variants are listed by name in mishnah-chapters.json. */
  function fold(s) {
    s = String(s).toLowerCase().replace(/[֑-ׇ]/g, '').replace(/[״׳"'`’.\-]/g, '').replace(/\s+/g, '');
    if (/[א-ת]/.test(s)) {
      return s.replace(/ך/g, 'כ').replace(/ם/g, 'מ').replace(/ן/g, 'נ').replace(/ף/g, 'פ').replace(/ץ/g, 'צ').replace(/([וי])\1+/g, '$1');
    }
    return s.replace(/kh|ch/g, 'h').replace(/tz|ts/g, 'z').replace(/(.)\1+/g, '$1');
  }

  /* Read a Mishnah reference. Returns {tractate, chapter|null, part|null} or null. */
  function parseMishnah(input, index) {
    var s = String(input || '').replace(/[֑-ׇ]/g, '').toLowerCase()
      .replace(/[‐-―]/g, '-').replace(/[:,;]/g, ' ').replace(/\s+/g, ' ').trim();
    s = s.replace(/^((mishnah|mishna|m\.|tractate|masechet|massekhet|masekhet|משנה|מסכת)\s+)+/, '');
    var toks = s.split(' ').filter(Boolean);
    if (!index._folded) {
      index.tractates.forEach(function (tr) { tr._f = tr.names.map(fold); });
      index._folded = true;
    }
    for (var k = toks.length; k >= 1; k--) {
      var name = fold(toks.slice(0, k).join(' '));
      var hit = null;
      for (var i = 0; i < index.tractates.length && !hit; i++) {
        if (index.tractates[i]._f.indexOf(name) !== -1) hit = index.tractates[i];
      }
      if (!hit) continue;
      var rest = toks.slice(k).join(' ').replace(/\./g, ' ').split(/[\s-]+/).filter(function (x) {
        return x && !/^(פרק|משנה|chapter|chap|ch|mishnah|mishna)$/.test(x);
      });
      if (!rest.length) return { tractate: hit, chapter: null, part: null };
      if (rest.length > 2) return null;
      var part = null, first = rest[0];
      var m = /^(\d+)([ab])$/.exec(first);
      if (m) { first = m[1]; part = m[2]; }
      var ch = toNumber(first);
      if (ch === null) return null;
      if (rest.length === 2 && toNumber(rest[1]) === null) {
        if (/^[ab]$/.test(rest[1]) && !part) part = rest[1]; else return null;
      }
      return { tractate: hit, chapter: ch, part: part };
    }
    return null;
  }

  /* Find the page(s) for a parsed Mishnah reference. */
  function resolveMishnah(ref) {
    var tr = ref.tractate;
    var last = tr.chapters[tr.chapters.length - 1].n;
    if (ref.chapter === null) {
      return tr.list ? { url: tr.list } : { list: tr.chapters, tractate: tr };
    }
    var hits = tr.chapters.filter(function (c) { return c.n === ref.chapter; });
    if (!hits.length) return { error: 'mishnah-chapter', tractate: tr, max: last };
    if (hits.length > 1 && ref.part) hits = hits.filter(function (c) { return c.part === ref.part; });
    return hits.length === 1 ? { url: hits[0].url } : { list: hits, tractate: tr };
  }

  function unitUrl(book, slug, n, hebrew) {
    return hebrew
      ? '/torah-weave/' + book + '/hebrew-' + slug + '-unit-' + n + '/hebrew-' + slug + '-unit-' + n
      : '/torah-weave/' + book + '/' + slug + '-unit-' + n + '/' + slug + '-unit-' + n;
  }

  /* Exposed for testing. */
  var api = { parse: parse, resolve: resolve, unitUrl: unitUrl, CHAPTER_LENGTHS: CHAPTER_LENGTHS,
              parseMishnah: parseMishnah, resolveMishnah: resolveMishnah, fold: fold };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; return; }
  window.ChaverVerseSearch = api;

  /* ---------- the box ---------- */
  var row = document.querySelector('header.site-header .nav-row');
  if (!row || row.querySelector('.verse-search')) return;

  var root = document.documentElement;
  var hebrew = /^he/i.test(root.getAttribute('lang') || '') || (root.getAttribute('dir') || '').toLowerCase() === 'rtl';
  var T = hebrew ? {
    label: 'חיפוש פסוק או פרק משנה', placeholder: 'פסוק או פרק משנה', go: 'חיפוש',
    help: 'נסו למשל: בראשית כב ג, שמות כ, או משנה אבות א',
    mchapter: function (tr, m) { return 'במסכת ' + tr.he + ' ' + m + ' פרקים. '; },
    mlist: function (tr) { return 'פרקי מסכת ' + tr.he + ':'; },
    mlabel: function (tr, c) { return tr.he + ' פרק ' + c.he + (c.part ? (c.part === 'a' ? ', חלק א' : ', חלק ב') : ''); },
    chapter: 'אין פרק כזה. ', verse: function (b, c, m) { return 'בפרק זה ' + m + ' פסוקים. '; },
    choose: 'הפרק מתחלק בין יחידות:', unit: 'יחידה', fail: 'החיפוש אינו זמין כרגע. נסו שוב מאוחר יותר.'
  } : {
    label: 'Find a verse or Mishnah chapter', placeholder: 'Verse or Mishnah, e.g. Gen 22:3, Avot 1', go: 'Go',
    help: 'Try a reference such as Genesis 22:3, Exodus 20, or Mishnah Avot 1.',
    mchapter: function (tr, m) { return 'Tractate ' + tr.en + ' has ' + m + ' chapters. '; },
    mlist: function (tr) { return 'Chapters of tractate ' + tr.en + ':'; },
    mlabel: function (tr, c) { return 'Mishnah ' + tr.en + ' ' + c.n + (c.part || ''); },
    chapter: 'There is no such chapter. ', verse: function (b, c, m) { return b + ' ' + c + ' has ' + m + ' verses in the Hebrew numbering used on this site. '; },
    choose: 'This chapter spans more than one unit:', unit: 'Unit', fail: 'The verse search is not available right now. Please try again later.'
  };

  var css = '/torah-weave/Admin/Assets/CSS/verse-search.css';
  if (!document.querySelector('link[href="' + css + '"]')) {
    var link = document.createElement('link'); link.rel = 'stylesheet'; link.href = css;
    document.head.appendChild(link);
  }

  var form = document.createElement('form');
  form.className = 'verse-search'; form.setAttribute('role', 'search');
  var input = document.createElement('input');
  input.type = 'search'; input.name = 'ref'; input.placeholder = T.placeholder;
  input.setAttribute('aria-label', T.label); input.autocomplete = 'off'; input.spellcheck = false;
  input.setAttribute('dir', 'auto');
  var button = document.createElement('button');
  button.type = 'submit'; button.textContent = T.go;
  var panel = document.createElement('div');
  panel.className = 'verse-search-panel'; panel.setAttribute('role', 'status'); panel.setAttribute('aria-live', 'polite');
  panel.hidden = true;
  form.appendChild(input); form.appendChild(button); form.appendChild(panel);
  var brand = row.querySelector('.nav-brand');
  if (brand && brand.nextSibling) row.insertBefore(form, brand.nextSibling); else row.appendChild(form);

  var dataPromise = null;
  function load() {
    if (!dataPromise) {
      dataPromise = fetch('/torah-weave/api/by-verse.json').then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status); return r.json();
      });
      dataPromise.catch(function () { dataPromise = null; });
    }
    return dataPromise;
  }
  input.addEventListener('focus', function () { load().catch(function () {}); }, { once: true });

  var mishnahPromise = null;
  function loadMishnah() {
    if (!mishnahPromise) {
      mishnahPromise = fetch('/torah-weave/Admin/Assets/JS/mishnah-chapters.json').then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status); return r.json();
      });
      mishnahPromise.catch(function () { mishnahPromise = null; });
    }
    return mishnahPromise;
  }
  function chooser(head, items) {
    var p = document.createElement('p'); p.textContent = head;
    var ul = document.createElement('ul');
    items.forEach(function (it) {
      var li = document.createElement('li'); var a = document.createElement('a');
      a.href = encodeURI(it.url); a.textContent = it.text; li.appendChild(a); ul.appendChild(li);
    });
    show([p, ul]);
  }

  function show(nodes) {
    panel.innerHTML = '';
    nodes.forEach(function (n) { panel.appendChild(n); });
    panel.hidden = false;
  }
  function message(text) { var p = document.createElement('p'); p.textContent = text; show([p]); }
  function hide() { panel.hidden = true; panel.innerHTML = ''; }

  function label(book, r) {
    var info = window.__vsData.books[book];
    return hebrew
      ? info.book_he + ' ' + T.unit + ' ' + r.unit + ' (' + r.verses_he + ')'
      : book + ' ' + T.unit + ' ' + r.unit + ': ' + r.title + ' (' + r.verses.replace(book + ' ', '') + ')';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ref = parse(input.value);
    if (!ref) {
      var typed = input.value;
      loadMishnah().then(function (idx) {
        var mref = parseMishnah(typed, idx);
        if (!mref) { message(T.help); return; }
        var res = resolveMishnah(mref);
        if (res.error) { message(T.mchapter(res.tractate, res.max) + T.help); return; }
        if (res.url) { window.location.href = encodeURI(res.url); return; }
        chooser(T.mlist(res.tractate), res.list.map(function (c) { return { url: c.url, text: T.mlabel(res.tractate, c) }; }));
      }).catch(function () { message(T.fail); });
      return;
    }
    load().then(function (data) {
      window.__vsData = data;
      var res = resolve(ref, data);
      if (res.error === 'chapter') { message(T.chapter + T.help); return; }
      if (res.error === 'verse') { message(T.verse(hebrew ? BOOKS.filter(function (b) { return b.key === ref.book; })[0].he : ref.book, ref.chapter, res.max) + T.help); return; }
      var slug = data.books[res.book].slug;
      if (res.units.length === 1) { window.location.href = unitUrl(res.book, slug, res.units[0].unit, hebrew); return; }
      var head = document.createElement('p'); head.textContent = T.choose;
      var ul = document.createElement('ul');
      res.units.forEach(function (r) {
        var li = document.createElement('li'); var a = document.createElement('a');
        a.href = unitUrl(res.book, slug, r.unit, hebrew); a.textContent = label(res.book, r);
        li.appendChild(a); ul.appendChild(li);
      });
      show([head, ul]);
    }).catch(function () { message(T.fail); });
  });

  input.addEventListener('keydown', function (e) { if (e.key === 'Escape') { hide(); input.blur(); } });
  input.addEventListener('input', function () { if (!panel.hidden) hide(); });
  document.addEventListener('click', function (e) { if (!form.contains(e.target)) hide(); });
})();
