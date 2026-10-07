/* Shine micro-interactions. Visual only: nothing here reads or changes data.
   1. Count-up on metric figures (ease-out cubic), then one num-pop when it lands.
   2. window.shineToast(text): a short confirmation at the foot of the screen.
   Both stand down under prefers-reduced-motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Figures worth counting: the per-video numbers, the three agents, the scoreboard.
  var FIGURES = '.n .v, .agent .num, .scoreboard .big';
  var NUM = /^([^\d]*)(\d[\d,]*)(\.\d+)?(.*)$/;

  function countUp(el) {
    var text = el.textContent.trim();
    var m = NUM.exec(text);
    if (!m) return;
    var prefix = m[1], whole = m[2], frac = m[3] || '', suffix = m[4];
    var target = parseFloat(whole.replace(/,/g, '') + frac);
    if (!isFinite(target) || target === 0) return;
    var decimals = frac ? frac.length - 1 : 0;
    var grouped = whole.indexOf(',') !== -1;
    var dur = 1100 + Math.min(700, Math.log10(target + 1) * 180);
    var start = null;

    function fmt(v) {
      var s = decimals ? v.toFixed(decimals) : String(Math.round(v));
      if (grouped) {
        var parts = s.split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        s = parts.join('.');
      }
      return prefix + s + suffix;
    }

    el.textContent = fmt(0);
    function step(ts) {
      if (start === null) start = ts;
      var t = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = fmt(target * eased);
      if (t < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = text;
        el.style.display = el.style.display || 'inline-block';
        el.style.animation = 'num-pop .6s ease-out 1';
      }
    }
    requestAnimationFrame(step);
  }

  function run() {
    if (reduce) return;
    var els = document.querySelectorAll(FIGURES);
    for (var i = 0; i < els.length; i++) countUp(els[i]);
  }

  var toastEl = null, toastTimer = null;
  window.shineToast = function (text) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'shine-toast';
      toastEl.setAttribute('role', 'status');
      toastEl.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = text;
    toastEl.classList.remove('show');
    void toastEl.offsetWidth;  // restart the entrance animation
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2600);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
