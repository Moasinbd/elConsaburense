/* Galería editorial San Isidro: autoplay suave, manual, visible y accesible. */
(() => {
  'use strict';
  const init = () => {
    const root = document.getElementById('si-gallery');
    if (!root) return;
    const slides = [...root.querySelectorAll('.si-gallery-slide')];
    const previous = document.getElementById('si-gallery-prev');
    const next = document.getElementById('si-gallery-next');
    const toggle = document.getElementById('si-gallery-toggle');
    const counter = document.getElementById('si-gallery-count');
    const caption = document.getElementById('si-gallery-title');
    if (slides.length < 2 || !previous || !next || !toggle || !counter || !caption) return;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let current = 0;
    let playing = !reduceMotion.matches;
    let inView = false;
    let hovered = false;
    let focused = false;
    let interval = null;

    const draw = position => {
      current = (position + slides.length) % slides.length;
      slides.forEach((slide, i) => {
        const active = i === current;
        slide.classList.toggle('is-active', active);
        slide.setAttribute('aria-hidden', String(!active));
      });
      counter.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
      caption.textContent = slides[current].dataset.caption || 'Fotografía de vino';
    };
    const stop = () => {
      if (interval !== null) window.clearInterval(interval);
      interval = null;
    };
    const schedule = () => {
      stop();
      if (!playing || !inView || document.hidden || hovered || focused || reduceMotion.matches) return;
      interval = window.setInterval(() => draw(current + 1), 5700);
    };
    const syncToggle = () => {
      toggle.textContent = playing ? 'Ⅱ' : '▶';
      toggle.setAttribute('aria-label', playing ? 'Pausar galería automática' : 'Reanudar galería automática');
      toggle.setAttribute('aria-pressed', String(!playing));
    };
    const manuallyMove = step => {
      playing = false;
      draw(current + step);
      syncToggle();
      schedule();
    };
    previous.addEventListener('click', () => manuallyMove(-1));
    next.addEventListener('click', () => manuallyMove(1));
    toggle.addEventListener('click', () => {
      playing = !playing;
      syncToggle();
      schedule();
    });
    root.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        manuallyMove(event.key === 'ArrowLeft' ? -1 : 1);
      }
    });
    root.addEventListener('mouseenter', () => { hovered = true; schedule(); });
    root.addEventListener('mouseleave', () => { hovered = false; schedule(); });
    root.addEventListener('focusin', () => { focused = true; schedule(); });
    root.addEventListener('focusout', event => {
      if (event.relatedTarget && root.contains(event.relatedTarget)) return;
      focused = false;
      schedule();
    });
    document.addEventListener('visibilitychange', schedule);
    window.addEventListener('pagehide', stop);
    const onMotionChange = () => {
      if (reduceMotion.matches) playing = false;
      syncToggle();
      schedule();
    };
    if (typeof reduceMotion.addEventListener === 'function') {
      reduceMotion.addEventListener('change', onMotionChange);
    }
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        inView = entries.some(entry => entry.isIntersecting);
        schedule();
      }, {threshold:.16});
      observer.observe(root);
    } else {
      inView = true;
    }
    draw(0);
    syncToggle();
    schedule();
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, {once:true});
  } else init();
})();
