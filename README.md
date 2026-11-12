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

## SEO técnico: segunda fase (06/11/2026)

- Póster del vídeo de portada alojado localmente y precargado con `fetchpriority=high`. Las imágenes de introducción y ubicación usan fotografías locales de Consuegra.
- Imágenes Open Graph relevantes por página y tarjeta grande para redes sociales (recreaciones gastronómicas con texto alternativo descriptivo), además de `max-image-preview:large`.
- JSON-LD `Menu` con 6 categorías y 31 platos reales de la carta para llevar, sin inventar precios.
- `lastmod` en el sitemap y `scripts/check_seo.py` para validar automáticamente sitemap, canónicas, títulos, datos estructurados, enlaces internos y archivos antes de publicar.
- GitHub Actions utiliza el FFmpeg ya disponible en el runner y solo instala el paquete si falta, evitando `apt-get update` innecesarios.

La publicación/validación de Google Search Console **requiere que el propietario verifique el dominio**; subir el sitemap al sitio no equivale a enviarlo a Google. No se han inventado horarios, reparto, precios, valoraciones ni imágenes reales del restaurante.

## SEO local: tercera fase y futuro dominio

- Se añade `public/404.html` para que Cloudflare Pages sirva una verdadera respuesta 404 ante URLs inexistentes, evitando mostrar la portada como un posible *soft 404*. Incluye `noindex,follow` y enlaces útiles.
- Las seis fotografías decorativas de vinos se almacenan también en `public/media/vinos/` y se usan con rutas locales, evitando hotlinks de Pexels en tiempo de visita y descargas de esas fotos durante la CI.
- Se valida en `scripts/check_seo.py` que las seis imágenes existan, que la página de error tenga noindex y que la navegación de recuperación esté presente.
- **Dominio de destino previsto:** `elconsaburense.com`. Hasta que el propietario confirme el registro y la conexión HTTPS del dominio, **no sustituir todavía las URL canónicas ni el sitemap de `elconsaburense.moasin.dev`**. Entonces actualizar los 4 canonicals, el `Restaurant.url` y `hasMenu`, los datos de WebPage/BreadcrumbList, Open Graph, sitemap y robots; configurar redirecciones 301 uno a uno desde el subdominio provisional, actualizar el perfil de Google y verificar el dominio final en Search Console.
- No se ha creado ni modificado ningún TXT DNS para Search Console.
 
## Animaciones y transiciones (10/11/2026)

- `public/motion.css` y `public/motion.js`: efectos propios de entrada al desplazarse con IntersectionObserver, aparicion escalonada de tarjetas, microinteracciones al pasar el raton y barra de progreso discreta.
- El menu de la portada cambia con una transicion breve y la navegacion destaca la seccion visible. El video original y el carrusel mantienen su logica.
- Se aplican a portada y las tres paginas SEO de servicios. Se respeta `prefers-reduced-motion`, se mantiene el contenido visible sin JavaScript y no se anaden librerias ni recursos externos.

## Segunda fase de mejoras visuales y de uso (11/11/2026)

- La galería de Consuegra admite botones anterior/siguiente, contador, flechas del teclado y deslizamiento lateral en móvil. Conserva las fuentes oficiales de cada monumento y devuelve el foco al cerrar.
- Se incorpora el botón «Subir», con posición opuesta a la asistente Sol. El menú destaca la sección activa según el orden del documento.
- Las pestañas de categorías admiten flechas izquierda/derecha, Inicio y Fin. El menú móvil se puede cerrar con Escape o tocando fuera.
- En móvil y con ahorro de datos no se reproduce una segunda copia ambiental del vídeo de portada; se mantiene el vídeo principal y el carrusel de platos.
- La imagen de molinos de la agenda ahora se carga desde la biblioteca local. No se han añadido librerías de terceros.

## Experiencia de reservas y rendimiento (11/11/2026)

- Se conservan los enlaces directos de WhatsApp Business y las consultas de disponibilidad; se explica el proceso de reserva en tres pasos y se añaden respuestas desplegables sin recopilar datos personales desde la web.
- El segundo vídeo decorativo de escritorio utiliza ahora una versión más ligera (320×568, sin audio). Se conserva el original vertical para la imagen principal, sin deformaciones.
- El vídeo corporativo secundario se compone con fotografías locales y ya no exige descargar imágenes de Wikimedia durante su creación.
- La página no debe afirmar disponibilidad, horarios, precio ni servicio de reparto sin confirmación del restaurante.
- **Fotos reales:** se requiere material autorizado del establecimiento. Las imágenes gastronómicas actuales siguen identificándose como recreaciones; no convertirlas en fotos auténticas.
- **Despliegue automático:** el workflow contempla sincronización y verificación de Cloudflare Pages si se configuran `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID` como secretos de GitHub Actions. Sin ellos se publica en `gh-pages` y aparece una advertencia; no se expone ninguna credencial en el repositorio.
- **Dominio final:** las URL de `elconsaburense.com` solo se activarán cuando el dominio esté registrado, asignado al proyecto Pages y su HTTPS confirmado.

## Galería de fotografías reales (opt-in)

- Subir fotos autorizadas a `public/media/fotos-reales/` en WebP/JPG/PNG.
- Añadir sus fichas a `public/media/fotos-reales/manifest.json`: `{"photos":[{"file":"salon.webp","title":"Nuestro salón","alt":"Vista real del comedor de El Consaburense","credit":"El Consaburense"}]}`.
- El paso `scripts/build_real_gallery.py` comprueba los archivos, créditos y texto alternativo; solo crea una sección visible cuando hay fotografías verificadas. El manifiesto permanece vacío por defecto.
- No incluir imágenes de personas identificables sin los permisos pertinentes. Usar títulos, descripción y créditos fieles; no etiquetar imágenes generadas con IA como fotografías auténticas.

## Carta de sugerencias (documento A5 del restaurante, noviembre de 2026)

- Se ha integrado una sección editorial `#sugerencias` justo después de `#carta` y antes de `#para-llevar`.
- Contiene las 12 sugerencias, divididas en `Entrantes y para compartir` (5) y `Guisos, pescados y carnes` (7), con los precios del archivo entregado.
- La carta general sigue sin precios, según lo solicitado anteriormente. Los precios aparecen **solo en la sección de sugerencias** por estar indicados en el documento.
- Los alérgenos son los símbolos marcados en el archivo de origen. No se han inferido alérgenos ausentes; se invita a consultar al personal por intolerancias, contacto cruzado y disponibilidad.
- La sección tiene acceso desde el encabezado de la carta, y contacto por WhatsApp y teléfono. No se añaden imágenes de platos sin referencias autorizadas.
- Para actualizar las sugerencias más adelante, modificar el bloque `day-suggestions-section` de `public/index.html` y el listado validado en `scripts/check_ui.py`.

## Bodega de confianza: Cooperativa San Isidro Labrador (Consuegra)

- Actualización del diseño editorial en `public/index.html#san-isidro-labrador` con estética borgoña, fotografía ambiental de viñedos (licenciada ya en el repositorio), datos históricos, selección varietal, marcas, y enlaces oficiales.
- La fuente principal de datos es Turismo de Consuegra: https://www.consuegra.es/es/experiencias/actividades/cooperativa-san-isidro
- Según la ficha: fundación el 17 de septiembre de 1958 con 43 socios, 215 socios recogidos en la ficha, capacidad de elaboración de 18 millones kg de uva, última ampliación en 2016, variedades blancas Airén, Sauvignon Blanc, Verdejo y Macabeo; tintas Garnacha, Tempranillo y Syrah; barricas de roble francés y americano.
- Las marcas de la cooperativa son Consaburum (Vinos de la Tierra de Castilla) y Regates (vino sin IGP/DOP). Mencionar estas marcas **no garantiza que ambas estén disponibles en el restaurante**.
- Se afirma la compra de vinos a la cooperativa, según la información facilitada por el restaurante. No se afirma patrocinio, exclusividad ni colaboración comercial formal.
- La fotografía se presenta explícitamente como viñedo ambiental ilustrativo, sin atribuirla a la cooperativa. Las fotografías de sus instalaciones y productos deben obtener autorización antes de replicarse. Se enlaza directamente su ficha oficial y su teléfono publicado.
- Criterio comercial: transmitir valor de marca y promoción genuina para abrir una futura colaboración, sin convertir el sitio del restaurante en una oferta publicitaria propia.
