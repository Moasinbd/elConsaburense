/* Galería San Isidro: empieza con vídeo, después fotografías. Reproducción responsable. */
(() => {
  'use strict';
  const init = () => {
    const root = document.getElementById('si-gallery');
    if (!root) return;
    const slides = Array.from(root.querySelectorAll('.si-gallery-slide'));
    const video = root.querySelector('#si-promo-video');
    const prev = root.querySelector('#si-gallery-prev');
    const next = root.querySelector('#si-gallery-next');
    const toggle = root.querySelector('#si-gallery-toggle');
    const counter = root.querySelector('#si-gallery-count');
    const caption = root.querySelector('#si-gallery-title');
    if (slides.length < 2 || !video || !prev || !next || !toggle || !counter || !caption) return;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    const saveData = Boolean(navigator.connection && navigator.connection.saveData);
    let current = 0;
    let playing = !reduced.matches && !saveData;
    let inView = false;
    let hovered = false;
    let focused = false;
    let timer = null;
    let generation = 0;
    let touchStart = null;
    video.muted = true; // Los navegadores solo permiten autoplay sin sonido.
    video.playsInline = true;

    const clearTimer = () => {
      if (timer !== null) window.clearTimeout(timer);
      timer = null;
    };
    const canAuto = () => playing && inView && !document.hidden && !reduced.matches && !saveData;
    const syncToggle = () => {
      toggle.textContent = playing ? 'Ⅱ' : '▶';
      toggle.setAttribute('aria-label', playing ? 'Pausar carrusel automático' : 'Reanudar carrusel automático');
      toggle.setAttribute('aria-pressed', String(!playing));
    };
    const sync = () => {
      const isVideo = current === 0;
      slides.forEach((slide, index) => {
        const active = index === current;
        slide.classList.toggle('is-active', active);
        slide.setAttribute('aria-hidden', String(!active));
        if (slide.tagName === 'VIDEO') slide.tabIndex = active ? 0 : -1;
      });
      root.classList.toggle('is-video-active', isVideo);
      counter.textContent = String(current + 1).padStart(2, '0') +
        ' / ' + String(slides.length).padStart(2, '0');
      caption.textContent = slides[current].dataset.caption || 'Galería de vinos';
    };
    const stopVideo = () => {
      if (!video.paused) video.pause();
    };
    const schedule = () => {
      clearTimer();
      const run = ++generation;
      if (!canAuto()) { stopVideo(); return; }
      if (current === 0) {
        // No aplicar timeout de foto al vídeo; avanza con el evento ended.
        if (video.ended) video.currentTime = 0;
        const promise = video.play();
        if (promise && typeof promise.catch === 'function') {
          promise.catch(() => {
            // Con bloqueo del navegador, se conserva el póster y se avanza
            // a las fotos para no dejar la experiencia congelada.
            if (generation === run && current === 0 && canAuto()) {
              timer = window.setTimeout(() => show(1), 2800);
            }
          });
        }
        return;
      }
      if (hovered || focused) return;
      timer = window.setTimeout(() => show((current + 1) % slides.length), 5200);
    };
    const show = (index, manual = false) => {
      clearTimer();
      stopVideo();
      if (current === 0 && index !== 0) video.currentTime = 0;
      if (manual) playing = false;
      current = (index + slides.length) % slides.length;
      sync();
      syncToggle();
      schedule();
    };
    video.addEventListener('ended', () => {
      if (current === 0 && playing) show(1);
    });
    prev.addEventListener('click', () => show(current - 1, true));
    next.addEventListener('click', () => show(current + 1, true));
    toggle.addEventListener('click', () => {
      playing = !playing;
      if (playing && current === 0 && video.ended) video.currentTime = 0;
      syncToggle();
      schedule();
    });
    root.addEventListener('keydown', event => {
      if (event.target === video) return; // respetar controles nativos
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        show(current + (event.key === 'ArrowLeft' ? -1 : 1), true);
      }
    });
    root.addEventListener('touchstart', event => {
      if (event.target.closest('button') || event.target.closest('video')) return;
      touchStart = event.touches[0]?.clientX ?? null;
    }, {passive: true});
    root.addEventListener('touchend', event => {
      if (touchStart === null) return;
      const endX = event.changedTouches[0]?.clientX ?? touchStart;
      const distance = endX - touchStart;
      touchStart = null;
      if (Math.abs(distance) > 65) show(current + (distance < 0 ? 1 : -1), true);
    }, {passive: true});
    // El hover debe pausar las fotos, pero no interrumpir el vídeo.
    root.addEventListener('mouseenter', () => { hovered = true; if (current !== 0) schedule(); });
    root.addEventListener('mouseleave', () => { hovered = false; if (current !== 0) schedule(); });
    root.addEventListener('focusin', () => { focused = true; if (current !== 0) schedule(); });
    root.addEventListener('focusout', event => {
      if (event.relatedTarget && root.contains(event.relatedTarget)) return;
      focused = false;
      if (current !== 0) schedule();
    });
    document.addEventListener('visibilitychange', schedule);
    window.addEventListener('pagehide', () => { clearTimer(); stopVideo(); });
    const onMotionChange = () => {
      if (reduced.matches) playing = false;
      syncToggle();
      schedule();
    };
    if (typeof reduced.addEventListener === 'function') reduced.addEventListener('change', onMotionChange);
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        inView = entries.some(entry => entry.isIntersecting && entry.intersectionRatio >= .2);
        schedule();
      }, {threshold: [0, .2, .5]});
      observer.observe(root);
    } else {
      inView = true;
    }
    sync();
    syncToggle();
    schedule();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true});
  else init();
})();
