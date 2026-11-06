# El Consaburense — Consuegra

Web responsive con carta, galería, agenda y reservas/eventos por WhatsApp Business directo.

## Contacto

- Dominio oficial: https://elconsaburense.moasin.dev/
- WhatsApp: https://wa.me/message/ACIXEAMQWNWME1
- Teléfono de llamadas: 925 09 71 73 (`tel:+34925097173`).

## Reservas y eventos

El visitante pulsa **Solicitar mesa por WhatsApp** o **Consultar evento por WhatsApp** para abrir el enlace corto oficial y escribir directamente. **No existe formulario, mensaje precargado, copia y pega obligatorio ni envío automático desde la web.** El restaurante contesta y confirma la disponibilidad.

La sección `#eventos` incluye cumpleaños, bautizos y comuniones, bodas, reuniones de grupo y catering, todos sujetos a disponibilidad. El sitio **no envía avisos a los tres números personales**; eso requeriría otra integración o dispositivos vinculados.

## Publicación

La fuente está en `public/` en `Moasinbd/elConsaburense`, rama `main`. GitHub Actions publica en `gh-pages` y Cloudflare Pages despliega la rama de producción; verificar la publicación en `elconsaburense.moasin.dev`. No habilitar `workers.dev`.

Antes de entregar: comprobar HTTPS y contenido del dominio, recepción en WhatsApp, privacidad y datos legales, carta e imágenes.

## Desarrollo

```sh
python3 -m http.server 8080 --directory public
```

Créditos de fotografía: [Créditos](public/creditos.html).

### Carrusel de imágenes fotorrealistas locales

Las 14 imágenes del carrusel se han generado con IA y optimizado en WebP. Están alojadas dentro de `public/media/carta-fotorealista/`, se incluyen en el repositorio y se sirven desde el mismo dominio, sin hotlinks externos. Son recreaciones visuales de los platos, no fotografías del restaurante. Los detalles y la presentación real pueden variar.
