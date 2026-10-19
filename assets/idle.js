/* idle.ipe.rest — shared UI: light/dark toggle + mobile menu.
   The <head> of every page primes data-theme before first paint
   (stored choice wins, otherwise light — Davy 10-18: light by default). */
(function () {
  var root = document.documentElement;
  var LIGHT = '#f6f8fa', DARK = '#11151a';

  // ---- theme ----
  var btn = document.getElementById('themeBtn');
  var meta = document.querySelector('meta[name="theme-color"]');
  function current() { return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }
  function apply(theme, persist) {
    root.setAttribute('data-theme', theme);
    if (meta) meta.setAttribute('content', theme === 'dark' ? DARK : LIGHT);
    if (btn) {
      btn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
      // aria-label describes the action the button performs next
      btn.setAttribute('data-i18n-aria', theme === 'dark' ? 'aria_theme_to_light' : 'aria_theme_to_dark');
      var lbl = theme === 'dark' ? btn.getAttribute('data-label-light') : btn.getAttribute('data-label-dark');
      if (lbl) btn.setAttribute('aria-label', lbl);
      if (window.__applyAria) window.__applyAria(btn);
    }
    if (persist) { try { localStorage.setItem('idle-theme', theme); } catch (e) {} }
  }
  apply(current(), false);
  if (btn) btn.addEventListener('click', function () { apply(current() === 'dark' ? 'light' : 'dark', true); });

  // ---- mobile menu (≤760px) ----
  var menuBtn = document.getElementById('menuBtn');
  var nav = document.getElementById('primaryNav');
  if (menuBtn && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('is-open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    menuBtn.addEventListener('click', function () { setOpen(!nav.classList.contains('is-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); menuBtn.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!nav.classList.contains('is-open')) return;
      if (nav.contains(e.target) || menuBtn.contains(e.target)) return;
      setOpen(false);
    });
  }
})();
