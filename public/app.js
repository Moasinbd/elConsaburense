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
    const step=()=>foodCards.length>1?foodCards[1].offsetLeft-foodCards[0].offsetLeft:foodTrack.clientWidth;
    const updateFoodControls=()=>{
      const max=Math.max(0,foodTrack.scrollWidth-foodTrack.clientWidth);
      const index=Math.max(0,Math.min(foodCards.length-1,Math.round(foodTrack.scrollLeft/Math.max(1,step()))));
      if(foodPrev)foodPrev.disabled=foodTrack.scrollLeft<4;
      if(foodNext)foodNext.disabled=foodTrack.scrollLeft>max-4;
      if(foodCount)foodCount.textContent=String(index+1).padStart(2,'0')+' / '+String(foodCards.length).padStart(2,'0');
    };
    const moveFood=(dir)=>{
      const next=Math.max(0,Math.min(foodTrack.scrollWidth-foodTrack.clientWidth,foodTrack.scrollLeft+dir*step()));
      foodTrack.scrollTo({left:next,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    };
    foodPrev?.addEventListener('click',()=>moveFood(-1));
    foodNext?.addEventListener('click',()=>moveFood(1));
    foodTrack.addEventListener('scroll',updateFoodControls,{passive:true});
    foodTrack.addEventListener('keydown',event=>{
      if(event.key==='ArrowRight'){event.preventDefault();moveFood(1);}
      if(event.key==='ArrowLeft'){event.preventDefault();moveFood(-1);}
    });
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
  }

  document.querySelectorAll('.tab').forEach(tab=>tab.addEventListener('click',()=>showMenu(tab.dataset.category)));
  const nav=$('main-nav'),toggle=$('nav-toggle');
  toggle?.addEventListener('click',()=>{const expanded=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(expanded));toggle.setAttribute('aria-label',expanded?'Cerrar menú':'Abrir menú');nav.classList.toggle('is-open',expanded)});
  nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{nav.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');toggle?.setAttribute('aria-label','Abrir menú')}));
  const date=$('booking-date');if(date){const local=new Date(); const today=`${local.getFullYear()}-${String(local.getMonth()+1).padStart(2,'0')}-${String(local.getDate()).padStart(2,'0')}`;date.min=today;date.value=today}
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