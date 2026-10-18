/* idle.ipe.rest site.js v1 · 2026-10-18
   1) Theme: light is the default on every first visit (system setting ignored). The header toggle writes localStorage "idle-theme".
      The matching pre-paint snippet in each <head> sets data-theme before first paint (no flash). All storage access is try/catch.
   2) Language: EN/KO static pages. A saved choice (localStorage ipe_lang) or an old ?lang=ko link sends English pages to /ko/.
   3) Drawer (<=760): close button receives focus on open; Esc / scrim / resize close; Tab is trapped.
   4) Journal list: topic chips filter the cards. */
(function () {
  var KEY = 'idle-theme', root = document.documentElement;
  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function write(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var btn = document.querySelector('.theme-btn');
  var meta = document.querySelector('meta[name="theme-color"]');
  var ko = root.lang === 'ko';
  function apply(t) {
    root.setAttribute('data-theme', t);
    if (meta) meta.setAttribute('content', t === 'dark' ? '#0d1117' : '#fbfaf4');
    if (!btn) return;
    btn.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
    btn.setAttribute('aria-label', t === 'dark' ? (ko ? '라이트 테마로 전환' : 'Switch to light theme') : (ko ? '다크 테마로 전환' : 'Switch to dark theme'));
    btn.setAttribute('title', t === 'dark' ? (ko ? '밝은 테마' : 'Light theme') : (ko ? '밤 테마' : 'Night theme'));
  }
  apply(read() === 'dark' ? 'dark' : 'light');
  if (btn) btn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    apply(next); write(next);
  });
})();

(function () {
  var sels = document.querySelectorAll('select.lang');
  if (!sels.length) return;
  var KEY = 'ipe_lang';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var isKo = document.documentElement.lang === 'ko';
  if (!isKo) {
    var q = (location.search.match(/[?&]lang=([a-z]{2})/) || [])[1];
    if (q === 'ko' || (!q && get() === 'ko')) { location.replace(sels[0].getAttribute('data-ko') + location.hash); return; }
  }
  Array.prototype.forEach.call(sels, function (sel) {
    sel.addEventListener('change', function () {
      set(sel.value);
      location.href = sel.getAttribute('data-' + sel.value) + location.hash;
    });
  });
})();

(function () {
  var btn = document.querySelector('.menu-btn'), drawer = document.getElementById('drawer'), scrim = document.querySelector('.scrim');
  if (!btn || !drawer) return;
  var close = drawer.querySelector('.drawer-close');
  function focusables() { return drawer.querySelectorAll('a[href],button,select'); }
  function open() {
    drawer.classList.add('is-open'); scrim.classList.add('is-open');
    drawer.removeAttribute('inert'); drawer.setAttribute('aria-hidden', 'false');
    btn.setAttribute('aria-expanded', 'true'); document.body.classList.add('drawer-lock');
    /* the drawer is not focusable until its visibility transition has started, so retry for ~0.5s */
    var tries = 0;
    (function focusClose() {
      close.focus();
      if (document.activeElement !== close && drawer.classList.contains('is-open') && tries++ < 12) setTimeout(focusClose, 40);
    })();
  }
  function shut(restore) {
    drawer.classList.remove('is-open'); scrim.classList.remove('is-open');
    drawer.setAttribute('inert', ''); drawer.setAttribute('aria-hidden', 'true');
    btn.setAttribute('aria-expanded', 'false'); document.body.classList.remove('drawer-lock');
    if (restore !== false) btn.focus();
  }
  btn.addEventListener('click', open);
  close.addEventListener('click', function () { shut(); });
  scrim.addEventListener('click', function () { shut(); });
  document.addEventListener('keydown', function (e) {
    if (!drawer.classList.contains('is-open')) return;
    if (e.key === 'Escape') { shut(); return; }
    if (e.key === 'Tab') {
      var f = focusables(), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  window.matchMedia('(min-width:761px)').addEventListener('change', function (m) { if (m.matches) shut(false); });
})();

(function () {
  var chips = document.querySelectorAll('.chip[data-filter]');
  if (!chips.length) return;
  var items = document.querySelectorAll('[data-tag]');
  Array.prototype.forEach.call(chips, function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      Array.prototype.forEach.call(chips, function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      Array.prototype.forEach.call(items, function (el) { el.hidden = !!f && el.getAttribute('data-tag') !== f; });
    });
  });
})();
