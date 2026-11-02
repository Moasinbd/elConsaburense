'use strict';
const menuData={
  raciones:[
    ['Croquetas de jamón (6 uds)','8,20 €','Croquetas tradicionales de jamón.'],
    ['Croquetas de pollo (6 uds)','7,90 €','Deliciosas croquetas de pollo.'],
    ['Croquetas de marisco (6 uds)','9,00 €','Croquetas con sabor a marisco.'],
    ['Delicias de pollo al ajillo (10 uds)','8,50 €','Bocados de pollo al ajillo.'],
    ['Ensaladilla rusa','8,50 €','Clásico de nuestra carta.'],
    ['Gazpacho o salmorejo','8,20 €','Una opción fresca para disfrutar.'],
    ['Patatas bravas','9,00 €','Patatas acompañadas de salsa brava.'],
    ['Patatas dos salsas (bravas, alioli)','10,20 €','Patatas para compartir con dos salsas.'],
    ['Calamares a la romana','12,60 €','Anillas de calamar rebozadas.'],
    ['Pincho de tortilla','4,60 €','Una porción de tortilla de patatas.']
  ],
  combinados:[
    ['Lomo, patatas y huevos','12,60 €','Lomo a la plancha con guarnición.'],
    ['Bacon, patatas y huevos','12,00 €','Bacon acompañado de huevos y patatas.'],
    ['Pica pollo','15,00 €','Pollo crujiente troceado.'],
    ['Lomo con patatas','9,60 €','Lomo a la plancha y patatas.'],
    ['Huevos rotos con jamón de bellota','18,50 €','Huevos y patatas con jamón.'],
    ['Pisto manchego con huevo','11,00 €','Verduras y huevo al estilo manchego.'],
    ['Salchipapas','8,20 €','Patatas fritas con salchichas.']
  ],
  hamburguesas:[
    ['Hamburguesa de ternera completa','12,00 €','Ternera, lechuga, tomate, queso, bacon, cebolla y huevo.'],
    ['Hamburguesa de pollo','9,60 €','Pollo con lechuga, tomate, cebolla y huevo.']
  ],
  bocadillos:[
    ['Bacon con queso o tomate','Montado 4,00 € · Bocadillo 5,50 €','Bacon a la plancha.'],
    ['Lomo con queso o tomate','Montado 4,00 € · Bocadillo 5,50 €','Lomo tierno a la plancha.'],
    ['Tortilla francesa','Montado 4,00 € · Bocadillo 5,50 €','Tortilla francesa hecha al momento.'],
    ['Tortilla de patatas','Montado 4,20 € · Bocadillo 5,80 €','El clásico de tortilla de patatas.'],
    ['Chorizo','Montado 4,00 € · Bocadillo 5,50 €','Sabor tradicional.'],
    ['Atún con tomate','Montado 4,20 € · Bocadillo 6,50 €','Atún acompañado de tomate.'],
    ['Jamón con tomate','Montado 4,20 € · Bocadillo 6,50 €','Jamón y tomate.'],
    ['Anchoas con tomate','Montado 4,20 € · Bocadillo 6,50 €','Anchoas y tomate.']
  ]
};
const $=id=>document.getElementById(id);
function showMenu(category){
  const wrapper=$('menu-items');if(!wrapper||!menuData[category])return;
  wrapper.replaceChildren(...menuData[category].map(([name,price,description])=>{
    const el=document.createElement('article');el.className='menu-item';
    const top=document.createElement('div');top.className='menu-item-top';
    const title=document.createElement('h3');title.textContent=name;
    const cost=document.createElement('span');cost.className='price';cost.textContent=price;
    const desc=document.createElement('p');desc.textContent=description;
    top.append(title,cost);el.append(top,desc);return el;
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