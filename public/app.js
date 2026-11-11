'use strict';
const menuData={
  entrantes:[
    ['Ensaladilla rusa casera','Un clásico de nuestra cocina.'],
    ['Calamares a la romana','Crujientes y recién preparados.'],
    ['Croquetas caseras de jamón ibérico','Cremosas, con jamón ibérico.'],
    ['Croquetas caseras de gamba roja','Sabor intenso a mar.'],
    ['Verduritas fritas con langostinos','Una combinación de verduras y marisco.']
  ],
  guisos:[
    ['Callos a la madrileña','Receta tradicional.'],
    ['Fabada asturiana con compango','Guiso asturiano de cuchara.'],
    ['Albóndigas caseras en salsa','Sabor de cocina de siempre.'],
    ['Suquet de langostinos con almejas','Guiso marinero.']
  ],
  carnes:[
    ['Chuletitas de lechal manchego','Producto tradicional manchego.'],
    ['Entrecot de vacuno mayor a la plancha','Carne a la plancha.'],
    ['Solomillo de vacuno al ajillo suave','Con un toque de ajo.'],
    ['Solomillo a la plancha o a la pimienta','A elegir la preparación.'],
    ['Cachopín asturiano con patatas','Especialidad asturiana con guarnición.']
  ],
  encargos:[
    ['Arroz a banda','Especial por encargo.'],
    ['Arroz negro','Especial por encargo.'],
    ['Arroz meloso','Especial por encargo.'],
    ['Asado de cordero','Consultar encargo y disponibilidad.'],
    ['Asado de lechal','Consultar encargo y disponibilidad.'],
    ['Cochinillo asado','Consultar encargo y disponibilidad.'],
    ['Pescados frescos a la plancha, al horno o a la sal','Consultar pescado disponible y preparación.']
  ],
  peques:[
    ['Fingers de pollo crujientes','Para los más pequeños.'],
    ['Hamburguesa completa con patatas','Con guarnición.'],
    ['Pollo frito con patatas','Crujiente y sabroso.'],
    ['Tortilla de patatas mini','El clásico en formato pequeño.']
  ],
  postres:[
    ['Tarta de chocolate fondant','Para amantes del chocolate.'],
    ['Brownie casero con nueces','Chocolate y nueces.'],
    ['Tatín de manzana tradicional','Tarta de manzana invertida.'],
    ['Tarta de queso cremosa','Un postre irresistible.'],
    ['Compota de manzana casera','Dulce tradicional.'],
    ['Helados variados de la casa','Consultar sabores disponibles.']
  ]
};
const $=id=>document.getElementById(id);
function showMenu(category){
  const wrapper=$('menu-items');if(!wrapper||!menuData[category])return;
  wrapper.replaceChildren(...menuData[category].map(([name,description])=>{
    const el=document.createElement('article');el.className='menu-item';
    const top=document.createElement('div');top.className='menu-item-top';
    const title=document.createElement('h3');title.textContent=name;
    const desc=document.createElement('p');desc.textContent=description;
    top.append(title);el.append(top,desc);return el;
  }));
  document.querySelectorAll('.tab').forEach(tab=>{
    const active=tab.dataset.category===category;
    tab.classList.toggle('is-active',active);
    tab.setAttribute('aria-selected',String(active));
    tab.tabIndex=active?0:-1;
  });
  wrapper.setAttribute('aria-labelledby',`tab-${category}`);
}
document.addEventListener('DOMContentLoaded',()=>{
  showMenu('entrantes');


  // Portada: el vídeo de unos 20 segundos se reproduce una sola vez y luego se muestran
  // automáticamente las 24 imágenes del carrusel que ya existe en la carta.
  const hero=$('video-zamburinas');
  const film=$('hero-zamburinas');
  const ambient=$('hero-film-ambient');
  const filmPlay=$('hero-zamburinas-play');
  const filmAudio=$('hero-zamburinas-audio');
  const filmReplay=$('hero-film-replay');
  const filmPrev=$('hero-film-prev');
  const filmNext=$('hero-film-next');
  const filmPhase=$('hero-film-phase');
  const filmLabel=$('hero-film-feature-label');
  const filmTitle=$('hero-film-feature-title');
  const galleryA=$('hero-film-slide-a');
  const galleryB=$('hero-film-slide-b');
  if(hero&&film&&ambient&&filmPlay&&filmAudio&&filmReplay&&filmPrev&&filmNext&&filmPhase&&filmLabel&&filmTitle&&galleryA&&galleryB){
    const cards=[...document.querySelectorAll('#food-track .food-card')];
    const photographs=cards.map(card=>({
      src:card.querySelector('img')?.getAttribute('src')||'',
      title:card.querySelector('figcaption strong')?.textContent?.trim()||'Nuestra carta'
    })).filter(item=>item.src);
    const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const ambientDesktop=window.matchMedia('(min-width:681px)');
    const saveData=Boolean(navigator.connection?.saveData);
    let galleryMode=false;
    let slideIndex=0;
    let activeSlide=galleryA;
    let userPaused=reduceMotion;
    let isVisible=true;
    let slideTimer=null;
    let slideChangeId=0;
    const slideDelay=4700;
    const filmPlayIcon=filmPlay.querySelector('.hero-film__play-icon');
    const filmPlayLabel=filmPlay.querySelector('.hero-film__play-label');
    const filmAudioLabel=filmAudio.querySelector('.hero-film__audio-label');
    const cancelSlideTimer=()=>{if(slideTimer!==null){window.clearTimeout(slideTimer);slideTimer=null;}};
    const updateControls=()=>{
      const playing=galleryMode?!userPaused:!film.paused;
      const verb=playing?'Pausar':'Reproducir';
      filmPlay.setAttribute('aria-label',verb+(galleryMode?' carrusel de fotos':' vídeo de portada'));
      filmPlay.setAttribute('aria-pressed',String(!playing));
      if(filmPlayIcon)filmPlayIcon.textContent=playing?'Ⅱ':'▶';
      if(filmPlayLabel)filmPlayLabel.textContent=verb;
      filmAudio.hidden=galleryMode;
      filmReplay.hidden=!galleryMode;
      filmNext.hidden=!galleryMode;
      filmPrev.hidden=!galleryMode;
      const audioVerb=film.muted?'Activar sonido':'Silenciar';
      filmAudio.setAttribute('aria-label',audioVerb+' del vídeo');
      filmAudio.setAttribute('aria-pressed',String(!film.muted));
      if(filmAudioLabel)filmAudioLabel.textContent=film.muted?'Sonido':'Silenciar';
    };
    const stopVideos=()=>{film.pause();ambient.pause();};
    const startVideos=()=>{
      if(galleryMode||userPaused||document.hidden||!isVisible)return;
      const attempt=film.play();
      if(attempt&&typeof attempt.catch==='function')attempt.catch(()=>updateControls());
      // Mantener el vídeo principal. Evitar segunda reproducción en móvil y ahorro de datos.
      if(ambientDesktop.matches&&!saveData){
        const backgroundAttempt=ambient.play();
        if(backgroundAttempt&&typeof backgroundAttempt.catch==='function')backgroundAttempt.catch(()=>{});
      }else ambient.pause();
    };
    const scheduleSlide=()=>{
      cancelSlideTimer();
      if(!galleryMode||userPaused||document.hidden||!isVisible||reduceMotion||photographs.length<2)return;
      slideTimer=window.setTimeout(()=>showSlide((slideIndex+1)%photographs.length),slideDelay);
    };
    const showSlide=index=>{
      if(!photographs.length)return;
      const chosen=(index+photographs.length)%photographs.length;
      const photo=photographs[chosen];
      const nextImage=activeSlide===galleryA?galleryB:galleryA;
      const serial=++slideChangeId;
      const swap=()=>{
        if(serial!==slideChangeId||!galleryMode)return;
        nextImage.classList.add('is-active');
        activeSlide.classList.remove('is-active');
        activeSlide=nextImage;
        slideIndex=chosen;
        filmPhase.textContent='FOTO '+String(chosen+1).padStart(2,'0')+' / '+String(photographs.length).padStart(2,'0');
        filmLabel.textContent='Descubre nuestra carta · Imágenes ilustrativas';
        filmTitle.textContent=photo.title;
        scheduleSlide();
      };
      nextImage.onload=null;
      nextImage.onerror=null;
      if(nextImage.getAttribute('src')!==photo.src)nextImage.setAttribute('src',photo.src);
      if(nextImage.complete&&nextImage.naturalWidth>0){swap();}
      else{
        nextImage.onload=swap;
        nextImage.onerror=()=>{if(serial===slideChangeId){slideIndex=chosen;scheduleSlide();}};
      }
    };
    const showGallery=()=>{
      if(galleryMode)return;
      stopVideos();
      galleryMode=true;
      userPaused=reduceMotion;
      hero.classList.add('hero-film--gallery');
      activeSlide=galleryA;
      galleryA.classList.add('is-active');
      galleryB.classList.remove('is-active');
      slideIndex=0;
      const first=photographs[0];
      if(first){
        galleryA.src=first.src;
        filmLabel.textContent='Descubre nuestra carta · Imágenes ilustrativas';
        filmTitle.textContent=first.title;
        filmPhase.textContent='FOTO 01 / '+String(photographs.length).padStart(2,'0');
      }else{
        filmLabel.textContent='Descubre nuestra cocina';
        filmTitle.textContent='Sabores para compartir';
        filmPhase.textContent='GALERÍA';
      }
      updateControls();
      scheduleSlide();
    };
    const replay=()=>{
      ++slideChangeId;
      cancelSlideTimer();
      galleryMode=false;
      userPaused=false;
      hero.classList.remove('hero-film--gallery');
      filmLabel.textContent='En nuestra cocina · 20 segundos aprox.';
      filmTitle.textContent='Zamburiñas con patatas y huevos';
      filmPhase.textContent='VÍDEO · 20 S';
      film.currentTime=0;
      try{ambient.currentTime=0;}catch(_error){}
      film.muted=true;
      updateControls();
      startVideos();
    };
    film.addEventListener('ended',showGallery);
    film.addEventListener('error',showGallery);
    film.addEventListener('play',updateControls);
    film.addEventListener('pause',updateControls);
    film.addEventListener('volumechange',updateControls);
    film.addEventListener('timeupdate',()=>{
      if(!ambient.paused&&ambient.readyState>=1&&Math.abs(ambient.currentTime-film.currentTime)>.5){
        try{ambient.currentTime=film.currentTime;}catch(_error){}
      }
    });
    filmPlay.addEventListener('click',()=>{
      userPaused=!userPaused;
      if(galleryMode){scheduleSlide();}
      else if(userPaused){stopVideos();}
      else{startVideos();}
      updateControls();
    });
    filmAudio.addEventListener('click',()=>{
      film.muted=!film.muted;
      if(!film.muted&&film.paused){userPaused=false;startVideos();}
      updateControls();
    });
    window.addEventListener('resize',()=>{
      if(!ambientDesktop.matches||saveData)ambient.pause();
      else startVideos();
    },{passive:true});
    filmReplay.addEventListener('click',replay);
    filmNext.addEventListener('click',()=>showSlide(slideIndex+1));
    filmPrev.addEventListener('click',()=>showSlide(slideIndex-1));
    document.addEventListener('visibilitychange',()=>{
      if(document.hidden){stopVideos();cancelSlideTimer();}
      else if(galleryMode){scheduleSlide();}
      else{startVideos();}
      updateControls();
    });
    if('IntersectionObserver' in window){
      const observer=new IntersectionObserver(entries=>{
        isVisible=entries.some(entry=>entry.isIntersecting);
        if(!isVisible){stopVideos();cancelSlideTimer();}
        else if(galleryMode){scheduleSlide();}
        else{startVideos();}
        updateControls();
      },{threshold:.12});
      observer.observe(hero);
    }
    if(reduceMotion){film.autoplay=false;ambient.autoplay=false;stopVideos();}
    else{startVideos();}
    updateControls();
  }

  const foodTrack=$('food-track');
  if(foodTrack){
    const foodCards=[...foodTrack.querySelectorAll('.food-card')];
    const foodPrev=$('food-prev'),foodNext=$('food-next'),foodCount=$('food-count');
    const autoToggle=$('food-autoplay-toggle');
    const foodShowcase=foodTrack.closest('.food-showcase');
    const motionPreference=window.matchMedia('(prefers-reduced-motion: reduce)');
    const FOOD_AUTO_INTERVAL=4800;
    const FOOD_INTERACTION_COOLDOWN=12000;
    let autoPaused=motionPreference.matches;
    let foodInView=!('IntersectionObserver' in window);
    let foodHovered=false;
    let lastManualInteraction=0;
    let lastAutoAdvance=Date.now();
    let isAutoScrolling=false;
    let autoScrollReset=null;

    const step=()=>foodCards.length>1?foodCards[1].offsetLeft-foodCards[0].offsetLeft:foodTrack.clientWidth;
    const updateFoodControls=()=>{
      const max=Math.max(0,foodTrack.scrollWidth-foodTrack.clientWidth);
      const index=Math.max(0,Math.min(foodCards.length-1,Math.round(foodTrack.scrollLeft/Math.max(1,step()))));
      if(foodPrev)foodPrev.disabled=foodTrack.scrollLeft<4;
      if(foodNext)foodNext.disabled=foodTrack.scrollLeft>max-4;
      if(foodCount)foodCount.textContent=String(index+1).padStart(2,'0')+' / '+String(foodCards.length).padStart(2,'0');
    };
    const noteFoodInteraction=()=>{
      lastManualInteraction=Date.now();
      lastAutoAdvance=Date.now();
      isAutoScrolling=false;
    };
    const moveFood=(dir)=>{
      const next=Math.max(0,Math.min(foodTrack.scrollWidth-foodTrack.clientWidth,foodTrack.scrollLeft+dir*step()));
      foodTrack.scrollTo({left:next,behavior:motionPreference.matches?'auto':'smooth'});
    };
    const updateAutoToggle=()=>{
      if(!autoToggle)return;
      const label=autoPaused?'Reanudar avance automático de los platos':'Pausar avance automático de los platos';
      autoToggle.setAttribute('aria-label',label);
      autoToggle.title=label;
      const icon=autoToggle.querySelector('span');
      if(icon)icon.textContent=autoPaused?'▶':'Ⅱ';
      autoToggle.setAttribute('aria-pressed',String(autoPaused));
    };
    foodPrev?.addEventListener('click',()=>{
      noteFoodInteraction();
      moveFood(-1);
    });
    foodNext?.addEventListener('click',()=>{
      noteFoodInteraction();
      moveFood(1);
    });
    autoToggle?.addEventListener('click',()=>{
      autoPaused=!autoPaused;
      if(autoPaused)noteFoodInteraction();
      else{
        lastManualInteraction=0;
        lastAutoAdvance=Date.now();
      }
      updateAutoToggle();
    });
    foodTrack.addEventListener('scroll',()=>{
      updateFoodControls();
      // Los desplazamientos manuales reinician la espera; los automáticos no.
      if(!isAutoScrolling)noteFoodInteraction();
    },{passive:true});
    foodTrack.addEventListener('pointerdown',noteFoodInteraction,{passive:true});
    foodTrack.addEventListener('wheel',noteFoodInteraction,{passive:true});
    foodTrack.addEventListener('keydown',event=>{
      if(event.key==='ArrowRight'){event.preventDefault();noteFoodInteraction();moveFood(1);}
      if(event.key==='ArrowLeft'){event.preventDefault();noteFoodInteraction();moveFood(-1);}
    });
    foodShowcase?.addEventListener('pointerenter',event=>{
      if(event.pointerType==='mouse')foodHovered=true;
    });
    foodShowcase?.addEventListener('pointerleave',event=>{
      if(event.pointerType==='mouse'){
        foodHovered=false;
        lastAutoAdvance=Date.now();
      }
    });
    foodShowcase?.addEventListener('focusin',noteFoodInteraction);
    document.addEventListener('visibilitychange',()=>{
      if(!document.hidden)lastAutoAdvance=Date.now();
    });
    if('IntersectionObserver' in window){
      const observer=new IntersectionObserver(entries=>{
        const wasVisible=foodInView;
        foodInView=entries.some(entry=>entry.isIntersecting);
        if(foodInView&&!wasVisible)lastAutoAdvance=Date.now();
      },{threshold:0.25});
      observer.observe(foodTrack);
    }
    // Avanza una tarjeta cada 4,8 s, solo si se ve y no hay interacción reciente.
    if(foodCards.length>1){
      window.setInterval(()=>{
        const now=Date.now();
        const max=Math.max(0,foodTrack.scrollWidth-foodTrack.clientWidth);
        if(autoPaused||document.hidden||!foodInView||foodHovered||max<8)return;
        if(now-lastAutoAdvance<FOOD_AUTO_INTERVAL)return;
        if(lastManualInteraction&&now-lastManualInteraction<FOOD_INTERACTION_COOLDOWN)return;
        const next=foodTrack.scrollLeft>=max-8?0:Math.min(max,foodTrack.scrollLeft+step());
        lastAutoAdvance=now;
        isAutoScrolling=true;
        foodTrack.scrollTo({left:next,behavior:motionPreference.matches?'auto':'smooth'});
        window.clearTimeout(autoScrollReset);
        autoScrollReset=window.setTimeout(()=>{
          isAutoScrolling=false;
          updateFoodControls();
        },1250);
      },500);
    }
    window.addEventListener('resize',updateFoodControls,{passive:true});
    foodCards.forEach(card=>{
      const img=card.querySelector('img');
      img?.addEventListener('error',()=>{
        if(img.dataset.fallbackTried!=='yes'&&img.dataset.original&&img.src!==img.dataset.original){
          img.dataset.fallbackTried='yes';img.src=img.dataset.original;
        }else{img.classList.add('food-image-error');}
      });
    });
    updateFoodControls();
    updateAutoToggle();
  }

  document.querySelectorAll('.tab').forEach(tab=>tab.addEventListener('click',()=>showMenu(tab.dataset.category)));
  // Teclado: flechas, Inicio y Fin para cambiar categorías de la carta.
  const menuTabs=[...document.querySelectorAll('.menu-tabs [role="tab"]')];
  document.querySelector('.menu-tabs[role="tablist"]')?.addEventListener('keydown',event=>{
    const current=menuTabs.indexOf(document.activeElement);
    if(current===-1)return;
    let next=current;
    if(event.key==='ArrowRight')next=(current+1)%menuTabs.length;
    else if(event.key==='ArrowLeft')next=(current-1+menuTabs.length)%menuTabs.length;
    else if(event.key==='Home')next=0;
    else if(event.key==='End')next=menuTabs.length-1;
    else return;
    event.preventDefault();
    menuTabs[next].focus();
    showMenu(menuTabs[next].dataset.category);
  });
  const nav=$('main-nav'),toggle=$('nav-toggle');
  const closeMobileNav=(restoreFocus=false)=>{
    if(!nav?.classList.contains('is-open'))return;
    nav.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded','false');
    toggle?.setAttribute('aria-label','Abrir menú');
    if(restoreFocus)toggle?.focus();
  };
  toggle?.addEventListener('click',()=>{
    if(toggle.getAttribute('aria-expanded')==='true')closeMobileNav();
    else {
      toggle.setAttribute('aria-expanded','true');
      toggle.setAttribute('aria-label','Cerrar menú');
      nav?.classList.add('is-open');
    }
  });
  nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>closeMobileNav()));
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&nav?.classList.contains('is-open')){
      event.preventDefault();closeMobileNav(true);
    }
  });
  document.addEventListener('pointerdown',event=>{
    if(nav?.classList.contains('is-open')&&!nav.contains(event.target)&&!toggle?.contains(event.target))closeMobileNav();
  });

  // Agenda local. Las fechas pasadas se ocultan automáticamente en zona horaria de Consuegra.
  const parts=new Intl.DateTimeFormat('es-ES',{timeZone:'Europe/Madrid',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
  const datePiece=type=>parts.find(part=>part.type===type)?.value||'00';
  const todayConsuegra=datePiece('year')+'-'+datePiece('month')+'-'+datePiece('day');
  const agendaCards=[...document.querySelectorAll('.agenda-card[data-ends]')];
  agendaCards.forEach(card=>{
    card.hidden=card.dataset.ends<todayConsuegra;
  });
  if(agendaCards.length && agendaCards.every(card=>card.hidden)){
    const empty=$('agenda-no-events');if(empty)empty.hidden=false;
  }
  const fairDays={
    '20':{heading:'Domingo 20 · Víspera patronal',events:[
      ['12:00','Chupinazo en la Plaza de España.'],
      ['12:00–14:00','Gigantes y cabezudos por Plaza de España y calle del Arco.'],
      ['00:00','Orquesta Danubios en la Plaza de España.']
    ]},
    '21':{heading:'Lunes 21 · Día del Cristo de la Vera Cruz',events:[
      ['09:00','Diana musical por las calles de Consuegra.'],
      ['19:00','Procesión del Santísimo Cristo de la Vera Cruz.'],
      ['23:00','Fuegos artificiales junto al río Amarguillo.']
    ]},
    '22':{heading:'Martes 22 · Día del Ausente',events:[
      ['12:00–15:00','Parque infantil de hinchables en Plaza de España.'],
      ['19:30–21:30','Franja de atracciones con menor intensidad sonora y lumínica.'],
      ['23:00','Orquesta Séptima Avenida en la Plaza de España.']
    ]},
    '23':{heading:'Miércoles 23 · Día del Niño',events:[
      ['11:30','Bueyada infantil por la calle del Arco.'],
      ['12:00–15:00','Juegos de habilidad y puntería en Plaza de España.'],
      ['23:00','Orquesta Jenasan en la Plaza de España.']
    ]},
    '24':{heading:'Jueves 24 · Día del Mayor',events:[
      ['10:00','Desayuno popular para mayores en Plaza de España.'],
      ['12:30','Bingo musical para mayores en Plaza de España.'],
      ['23:00','Orquesta Mambo Show en Plaza de España.']
    ]},
    '25':{heading:'Viernes 25 · Fin de feria',events:[
      ['12:00–15:00','Jornada infantil de multiaventura en Plaza de España.'],
      ['23:00','Fuegos artificiales en el entorno del molino Bolero.'],
      ['23:30','Fiesta de cierre con DJ locales en la carpa municipal.']
    ]}
  };
  const dayButtons=[...document.querySelectorAll('[data-fair-day]')];
  const chooseFairDay=(day)=>{
    const info=fairDays[day];if(!info)return;
    dayButtons.forEach(button=>{
      const isActive=button.dataset.fairDay===day;
      button.classList.toggle('is-active',isActive);
      button.setAttribute('aria-pressed',String(isActive));
    });
    const heading=$('fair-day-heading'),list=$('fair-day-activities');
    if(heading)heading.textContent=info.heading;
    if(list)list.replaceChildren(...info.events.map(([hour,description])=>{
      const li=document.createElement('li');li.className='fair-activity';
      const time=document.createElement('time');time.textContent=hour;
      const activity=document.createElement('span');activity.textContent=description;
      li.append(time,activity);
      return li;
    }));
  };
  dayButtons.forEach(button=>button.addEventListener('click',()=>chooseFairDay(button.dataset.fairDay)));


  // Galería de monumentos con flechas, contador y deslizamiento en móvil.
  const townDialog=$('town-lightbox');
  const townDialogImage=$('town-lightbox-image');
  const townDialogTitle=$('town-lightbox-title');
  const townDialogMore=$('town-lightbox-more');
  const townClose=$('town-lightbox-close');
  const townPrev=$('town-lightbox-prev'),townNext=$('town-lightbox-next'),townCount=$('town-lightbox-count');
  const townPhotos=[...document.querySelectorAll('.town-gallery .town-card')].map(card=>({
    trigger:card.querySelector('.town-photo-open'),
    photo:card.querySelector('.town-photo-open img'),
    heading:card.querySelector('figcaption strong')?.textContent?.trim()||'Consuegra',
    more:card.querySelector('a.town-more')
  })).filter(item=>item.trigger&&item.photo&&item.more);
  let townIndex=0,townLastTrigger=null;
  const renderTownPhoto=()=>{
    const item=townPhotos[townIndex];
    if(!item||!townDialogImage||!townDialogTitle||!townDialogMore)return;
    townDialogImage.src=item.photo.currentSrc||item.photo.src;
    townDialogImage.alt=item.photo.alt;
    townDialogTitle.textContent=item.heading;
    townDialogMore.href=item.more.href;
    townDialogMore.setAttribute('aria-label','Saber más sobre '+item.heading+' en Turismo de Consuegra');
    if(townCount)townCount.textContent=String(townIndex+1).padStart(2,'0')+' / '+String(townPhotos.length).padStart(2,'0');
    if(townPrev)townPrev.disabled=townPhotos.length<2;
    if(townNext)townNext.disabled=townPhotos.length<2;
  };
  const changeTownPhoto=step=>{
    if(townPhotos.length<2||!townDialog?.open)return;
    townIndex=(townIndex+step+townPhotos.length)%townPhotos.length;
    renderTownPhoto();
  };
  townPhotos.forEach((item,index)=>item.trigger.addEventListener('click',()=>{
    if(!townDialog||townDialog.open)return;
    townLastTrigger=item.trigger;townIndex=index;renderTownPhoto();
    if(typeof townDialog.showModal==='function')townDialog.showModal();
    else window.open(item.photo.currentSrc||item.photo.src,'_blank','noopener,noreferrer');
  }));
  townPrev?.addEventListener('click',()=>changeTownPhoto(-1));
  townNext?.addEventListener('click',()=>changeTownPhoto(1));
  townDialog?.addEventListener('keydown',event=>{
    if(!townDialog.open)return;
    if(event.key==='ArrowLeft'){event.preventDefault();changeTownPhoto(-1);}
    if(event.key==='ArrowRight'){event.preventDefault();changeTownPhoto(1);}
  });
  let townTouchStart=null;
  townDialogImage?.addEventListener('touchstart',event=>{
    if(event.touches.length===1)townTouchStart={x:event.touches[0].clientX,y:event.touches[0].clientY};
  },{passive:true});
  townDialogImage?.addEventListener('touchend',event=>{
    if(!townTouchStart||!event.changedTouches.length)return;
    const dx=event.changedTouches[0].clientX-townTouchStart.x;
    const dy=event.changedTouches[0].clientY-townTouchStart.y;
    townTouchStart=null;
    if(Math.abs(dx)>=55&&Math.abs(dx)>Math.abs(dy)*1.3)changeTownPhoto(dx<0?1:-1);
  },{passive:true});
  const closeTownDialog=()=>{if(townDialog?.open)townDialog.close();};
  townClose?.addEventListener('click',closeTownDialog);
  townDialog?.addEventListener('click',event=>{if(event.target===townDialog)closeTownDialog();});
  townDialog?.addEventListener('close',()=>{
    townDialogImage?.removeAttribute('src');
    townLastTrigger?.focus();townLastTrigger=null;
  });

  // Sol orienta a los visitantes; las respuestas de WhatsApp son humanas.
  const solLauncher=$('sol-launcher'),solPanel=$('sol-panel'),solClose=$('sol-close');
  const setSolOpen=open=>{if(!solLauncher||!solPanel)return;solPanel.hidden=!open;solLauncher.setAttribute('aria-expanded',String(open));};
  solLauncher?.addEventListener('click',()=>setSolOpen(solPanel.hidden));
  solClose?.addEventListener('click',()=>{setSolOpen(false);solLauncher?.focus();});
  document.querySelectorAll('[data-sol-close]').forEach(a=>a.addEventListener('click',()=>setSolOpen(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&solPanel&&!solPanel.hidden){setSolOpen(false);solLauncher?.focus();}});

  // Especialidades por encargo: se muestra una sola vez por sesión, con cierre estándar de dialog.
  const encargoDialog=$('encargo-dialog');
  const encargoClose=$('encargo-close');
  const encargoOpen=$('encargo-open');
  const encargoSessionKey='consaburense-encargos-intro-v1';
  let encargoLastTrigger=null;
  const openEncargo=(trigger=null)=>{
    if(!encargoDialog||encargoDialog.open)return;
    if($('town-lightbox')?.open)return; // No superponer dos diálogos.
    encargoLastTrigger=trigger;
    if(typeof encargoDialog.showModal==='function'){
      encargoDialog.showModal();
      try{sessionStorage.setItem(encargoSessionKey,'seen');}catch(_e){}
    }
  };
  const closeEncargo=()=>{if(encargoDialog?.open)encargoDialog.close();};
  encargoOpen?.addEventListener('click',()=>openEncargo(encargoOpen));
  encargoClose?.addEventListener('click',closeEncargo);
  encargoDialog?.addEventListener('click',event=>{if(event.target===encargoDialog)closeEncargo();});
  encargoDialog?.addEventListener('close',()=>{
    if(encargoLastTrigger?.isConnected)encargoLastTrigger.focus();
    encargoLastTrigger=null;
  });
  document.querySelectorAll('[data-encargo-dismiss]').forEach(a=>a.addEventListener('click',closeEncargo));
  // La promoción se abre solo al pulsar «Ver especialidades»; no tapa el contenido al llegar desde Google.

});
