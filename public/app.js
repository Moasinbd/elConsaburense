'use strict';
const menuData={
  raciones:[
    ['Croquetas de jamón (6 uds)','Croquetas tradicionales de jamón.'],
    ['Croquetas de pollo (6 uds)','Deliciosas croquetas de pollo.'],
    ['Croquetas de marisco (6 uds)','Croquetas con sabor a marisco.'],
    ['Delicias de pollo al ajillo (10 uds)','Bocados de pollo al ajillo.'],
    ['Ensaladilla rusa','Clásico de nuestra carta.'],
    ['Gazpacho o salmorejo','Una opción fresca para disfrutar.'],
    ['Patatas bravas','Patatas acompañadas de salsa brava.'],
    ['Patatas dos salsas (bravas, alioli)','Patatas para compartir con dos salsas.'],
    ['Calamares a la romana','Anillas de calamar rebozadas.'],
    ['Pincho de tortilla','Una porción de tortilla de patatas.']
  ],
  combinados:[
    ['Lomo, patatas y huevos','Lomo a la plancha con guarnición.'],
    ['Bacon, patatas y huevos','Bacon acompañado de huevos y patatas.'],
    ['Pica pollo','Pollo crujiente troceado.'],
    ['Lomo con patatas','Lomo a la plancha y patatas.'],
    ['Huevos rotos con jamón de bellota','Huevos y patatas con jamón.'],
    ['Pisto manchego con huevo','Verduras y huevo al estilo manchego.'],
    ['Salchipapas','Patatas fritas con salchichas.']
  ],
  hamburguesas:[
    ['Hamburguesa de ternera completa','Ternera, lechuga, tomate, queso, bacon, cebolla y huevo.'],
    ['Hamburguesa de pollo','Pollo con lechuga, tomate, cebolla y huevo.']
  ],
  bocadillos:[
    ['Bacon con queso o tomate','Bacon a la plancha.'],
    ['Lomo con queso o tomate','Lomo tierno a la plancha.'],
    ['Tortilla francesa','Tortilla francesa hecha al momento.'],
    ['Tortilla de patatas','El clásico de tortilla de patatas.'],
    ['Chorizo','Sabor tradicional.'],
    ['Atún con tomate','Atún acompañado de tomate.'],
    ['Jamón con tomate','Jamón y tomate.'],
    ['Anchoas con tomate','Anchoas y tomate.']
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
  });
  wrapper.setAttribute('aria-labelledby',`tab-${category}`);
}
document.addEventListener('DOMContentLoaded',()=>{
  showMenu('raciones');

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
  const nav=$('main-nav'),toggle=$('nav-toggle');
  toggle?.addEventListener('click',()=>{const expanded=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(expanded));toggle.setAttribute('aria-label',expanded?'Cerrar menú':'Abrir menú');nav.classList.toggle('is-open',expanded)});
  nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{nav.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');toggle?.setAttribute('aria-label','Abrir menú')}));
  const date=$('booking-date');if(date){const local=new Date(); const today=`${local.getFullYear()}-${String(local.getMonth()+1).padStart(2,'0')}-${String(local.getDate()).padStart(2,'0')}`;date.min=today;date.value=today}

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
  document.querySelectorAll('[data-agenda-booking]').forEach(link=>link.addEventListener('click',()=>{
    const day=link.dataset.bookingDate;
    if(date && day && day>=todayConsuegra && day>=date.min)date.value=day;
    const time=$('booking-time');
    if(time && link.dataset.bookingTime && [...time.options].some(option=>option.value===link.dataset.bookingTime)){
      time.value=link.dataset.bookingTime;
    }
    const result=$('booking-result');if(result)result.hidden=true;
  }));
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


  // Ampliación accesible de las imágenes del pueblo sin salir de El Consaburense.
  const townDialog=$('town-lightbox');
  const townDialogImage=$('town-lightbox-image');
  const townDialogTitle=$('town-lightbox-title');
  const townDialogMore=$('town-lightbox-more');
  const townClose=$('town-lightbox-close');
  let townLastTrigger=null;
  document.querySelectorAll('.town-gallery .town-card').forEach(card=>{
    const trigger=card.querySelector('.town-photo-open');
    const photo=trigger?.querySelector('img');
    const heading=card.querySelector('figcaption strong')?.textContent?.trim();
    const more=card.querySelector('a.town-more');
    trigger?.addEventListener('click',()=>{
      if(!townDialog||!photo||!townDialogImage||!townDialogTitle||!townDialogMore||!more)return;
      townLastTrigger=trigger;
      townDialogImage.src=photo.currentSrc||photo.src;
      townDialogImage.alt=photo.alt;
      townDialogTitle.textContent=heading||'Consuegra';
      townDialogMore.href=more.href;
      townDialogMore.setAttribute('aria-label','Saber más sobre '+(heading||'Consuegra')+' en la página oficial de Turismo');
      if(typeof townDialog.showModal==='function')townDialog.showModal();
      else window.open(photo.currentSrc||photo.src,'_blank','noopener,noreferrer');
    });
  });
  const closeTownDialog=()=>{if(townDialog?.open)townDialog.close()};
  townClose?.addEventListener('click',closeTownDialog);
  townDialog?.addEventListener('click',event=>{
    if(event.target===townDialog)closeTownDialog();
  });
  townDialog?.addEventListener('close',()=>{
    townDialogImage?.removeAttribute('src');
    townLastTrigger?.focus();
  });

  $('booking-form')?.addEventListener('submit',event=>{
    event.preventDefault(); const f=event.currentTarget;
    if(!f.reportValidity())return;
    const summary=[
      'SOLICITUD DE INFORMACIÓN — EL CONSABURENSE',
      'ATENCIÓN: este mensaje todavía NO se ha enviado al restaurante.',
      `Nombre: ${$('booking-name').value.trim()}`,
      `Teléfono: ${$('booking-phone').value.trim()}`,
      `Fecha: ${$('booking-date').value}`,
      `Hora deseada: ${$('booking-time').value}`,
      `Comensales: ${$('booking-guests').value}`,
      `Tipo: ${$('booking-type').value}`,
      `Observaciones: ${$('booking-notes').value.trim()||'Ninguna'}`,
      'Pendiente de disponibilidad y confirmación del establecimiento.'
    ].join('\n');
    $('booking-summary').value=summary;
    $('booking-result').hidden=false;
    $('copy-status').textContent='';
    $('booking-result').scrollIntoView({behavior:'smooth',block:'nearest'});
  });
  $('copy-summary')?.addEventListener('click',async()=>{
    const el=$('booking-summary');try{await navigator.clipboard.writeText(el.value);$('copy-status').textContent='Texto copiado. Recuerda que aún no se ha enviado al restaurante.'}
    catch(e){el.focus();el.select();$('copy-status').textContent='Selecciona el texto y cópialo manualmente.'}
  });
});