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

La fuente está en `public/` en `Moasinbd/elConsaburense`, rama `main`. GitHub Actions publica una copia en `gh-pages`, pero **no actualiza automáticamente el Worker que actualmente atiende `elconsaburense.moasin.dev`**. La versión debe publicarse al servicio del dominio. No habilitar `workers.dev`.

Antes de entregar: comprobar HTTPS y contenido del dominio, recepción en WhatsApp, privacidad y datos legales, carta e imágenes.

## Desarrollo

```sh
python3 -m http.server 8080 --directory public
```

Créditos de fotografía: [Créditos](public/creditos.html).

### Fotografías reales en archivos locales

Las fotografías de referencia, procedentes de Pexels, están guardadas como imágenes WebP bajo `public/media/platos/`, dentro de GitHub. El carrusel apunta a rutas **locales**; no depende de descargas de terceros durante el despliegue. Créditos y fuente en `public/creditos.html`. Son fotos orientativas de platos similares, no fotos hechas en El Consaburense.
