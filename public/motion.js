/* Movimiento progresivo de El Consaburense. Sin dependencias ni desplazamientos forzados. */
(() => {
  'use strict';
  const init = () => {
    const prefersLessMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const header = document.querySelector('.header');
    const navLinks = [...document.querySelectorAll('#main-nav > a[href^="#"]')];
    const targets = navLinks.map(link => {
      const id = link.getAttribute('href').slice(1);
      return { link, section:document.getElementById(id) };
    }).filter(item => item.section).sort((a,b)=>{
      if(a.section===b.section)return 0;
      return a.section.compareDocumentPosition(b.section)&Node.DOCUMENT_POSITION_FOLLOWING?-1:1;
    });
    const progress = document.createElement('div');
    progress.className = 'reading-progress';
    progress.setAttribute('aria-hidden','true');
    document.body.append(progress);
    const backTop=document.createElement('button');
    backTop.type='button';
    backTop.className='back-to-top';
    backTop.hidden=true;
    backTop.setAttribute('aria-label','Volver al principio de la página');
    const arrow=document.createElement('span');
    arrow.textContent='↑';arrow.setAttribute('aria-hidden','true');
    const label=document.createElement('span');
    label.className='back-to-top__label';label.textContent='Subir';
    backTop.append(arrow,label);
    backTop.addEventListener('click',()=>window.scrollTo({
      top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'
    }));
    document.body.append(backTop);

    // Un unico calculo por fotograma: barra de lectura y enlace activo.
    let framePending = false;
    const syncPosition = () => {
      framePending = false;
      const available = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
      const ratio = available ? Math.min(1, Math.max(0, window.scrollY / available)) : 0;
      progress.style.transform = 'scaleX(' + ratio.toFixed(4) + ')';
      backTop.hidden=window.scrollY<Math.max(620,window.innerHeight*.8);
      if (!targets.length) return;
      const marker = (header ? header.getBoundingClientRect().height : 80)
        + Math.min(window.innerHeight * .31, 225);
      let active = window.scrollY < 80 ? 'inicio' : '';
      for (const item of targets) {
        if (item.section.getBoundingClientRect().top <= marker) active = item.section.id;
      }
      for (const item of targets) {
        const selected = item.section.id === active;
        item.link.classList.toggle('is-current', selected);
        if (selected) item.link.setAttribute('aria-current','location');
        else item.link.removeAttribute('aria-current');
      }
    };
    const queuePosition = () => {
      if (framePending) return;
      framePending = true;
      window.requestAnimationFrame(syncPosition);
    };
    window.addEventListener('scroll', queuePosition, {passive:true});
    window.addEventListener('resize', queuePosition, {passive:true});
    window.addEventListener('pageshow', queuePosition);
    queuePosition();

    // Contenido siempre visible si faltan las APIs o se prefiere menos movimiento.
    if (prefersLessMotion || !('IntersectionObserver' in window)) return;
    const selectors = [
      '.intro-visual','.intro-copy','.section-heading','.food-showcase',
      '.menu-tabs','#menu-items','.takeaway-identity','.takeaway-action',
      '.wine-intro > *','.wine-card','.events-grid > .event-card',
      '.reviews-top','.review-card','.town-card',
      '.agenda-heading','.agenda-showcase','.agenda-events-heading',
      '.agenda-next-grid > .agenda-card','.booking-quick-card',
      '.location-grid > div','.seo-section-heading','.seo-card',
      '.seo-menu-group','.seo-cta-inner'
    ];
    const gridCard = '.wine-card,.event-card,.review-card,.town-card,.agenda-card,.booking-quick-card,.seo-card';
    const fromLeft = '.intro-visual,.location-visual,.agenda-showcase,.seo-cta-inner';
    const fromRight = '.intro-copy,.takeaway-action';
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }, {threshold:.07, rootMargin:'0px 0px -6% 0px'});

    for (const node of document.querySelectorAll(selectors.join(','))) {
      if (node.closest('[hidden],dialog,[aria-hidden="true"]')) continue;
      const rect = node.getBoundingClientRect();
      if (!rect.height || !rect.width) continue;
      // No esconder contenido que ya esta a la vista, ni al restaurar la posicion.
      if (rect.bottom <= 0 || rect.top < window.innerHeight * .78) continue;
      if (node.matches(gridCard)) {
        const siblings = [...node.parentElement.children].filter(el => el.matches(gridCard));
        const order = siblings.indexOf(node) % 3;
        if (order) node.classList.add('motion-delay-' + order);
      }
      if (node.matches(fromLeft)) node.dataset.motionAxis = 'left';
      else if (node.matches(fromRight)) node.dataset.motionAxis = 'right';
      node.classList.add('motion-item');
      observer.observe(node);
    }
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, {once:true});
  } else {
    init();
  }
})();
