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

Las 24 imágenes del carrusel se han generado con IA y optimizado en WebP. Están alojadas dentro de `public/media/carta-fotorealista/`, se incluyen en el repositorio y se sirven desde el mismo dominio, sin hotlinks externos. Son recreaciones visuales de los platos, no fotografías del restaurante. Los detalles y la presentación real pueden variar.

## Campaña de encargos al entrar

El modal accesible `#encargo-dialog` aparece aproximadamente 1,3 segundos después de entrar **solo una vez por sesión de navegador** (mediante `sessionStorage`). Utiliza fotografías locales existentes de arroz meloso, cordero asado y pescado a la sal. Incluye llamada directa al 925 09 71 73 y contacto por WhatsApp Business para consultar entrega a domicilio o recogida. No tramita pedidos automáticamente ni garantiza servicio de reparto, horarios o precios. El visitante puede cerrar con X, Esc o clic en el fondo y reabrirlo desde «Ver especialidades» en la carta para llevar. Evitar eliminar este aviso de disponibilidad sin confirmar previamente el servicio real con el establecimiento.

## SEO local: primera fase (06/11/2026)

Se añaden:
- Metadatos únicos (title, description, Open Graph, Twitter y canonical) en portada y páginas de servicios.
- Datos estructurados JSON-LD `Restaurant` (dirección y teléfono confirmados, sin inventar horarios, valoraciones, precios ni reparto), más `WebPage` y `BreadcrumbList` en páginas de servicio.
- Sitemap `public/sitemap.xml` y declaración en `robots.txt`.
- Páginas HTML rastreables: `/carta-para-llevar/`, `/arroces-asados-por-encargo/`, `/celebraciones/`. El contenido se incluye en HTML para buscadores y visitantes sin JavaScript.
- Enlaces internos y promoción de encargos que no abre un modal automáticamente al aterrizar desde Google; el diálogo sigue disponible bajo clic en «Ver especialidades».
- Dimensiones explícitas para algunas imágenes existentes.

**Pendiente de completar fuera del repositorio:** verificar propiedad y sitemap en Google Search Console; medir indexación/Core Web Vitals; revisar ficha de Google Business Profile y horarios; añadir fotos reales del local y revisar textos legales. **No se anuncia reparto garantizado**: si se ofrece más adelante, se actualizan la página de encargos, el schema y la ficha del negocio.
