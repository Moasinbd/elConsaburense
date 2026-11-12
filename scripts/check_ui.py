#!/usr/bin/env python3
"""Validación estática de UX y assets antes de publicar El Consaburense."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "public"
PAGES = [
    ROOT / "index.html",
    ROOT / "carta-para-llevar" / "index.html",
    ROOT / "arroces-asados-por-encargo" / "index.html",
    ROOT / "celebraciones" / "index.html",
]
errors = []

def ensure(condition: bool, explanation: str) -> None:
    if not condition:
        errors.append(explanation)

for page in PAGES:
    html = page.read_text(encoding="utf-8")
    prefix = "" if page.parent == ROOT else "../"
    for asset in ("motion.js", "motion.css"):
        ensure(f'{prefix}{asset}?v=20261111-2' in html, f"{page.name}: missing {asset}")
        ensure((ROOT / asset).is_file(), f"{asset}: asset missing")
    ensure("<main" in html and "</main>" in html, f"{page}: main landmark missing")
    ensure('href="https://wa.me/message/ACIXEAMQWNWME1"' in html or page != PAGES[0],
           f"{page}: WhatsApp reservation link missing")

homepage = PAGES[0].read_text(encoding="utf-8")
js = (ROOT / "app.js").read_text(encoding="utf-8")
motion = (ROOT / "motion.js").read_text(encoding="utf-8")
css = (ROOT / "motion.css").read_text(encoding="utf-8")

for marker in ("town-lightbox-prev", "town-lightbox-next", "town-lightbox-count",
               "hero-zamburinas", "hero-film-ambient", "food-track", "sol-launcher",
               "encargo-dialog", "nav-toggle"):
    ensure(f'id="{marker}"' in homepage, f"Homepage missing interactive element {marker}")
ensure("changeTownPhoto" in js and "touchend" in js and "ArrowRight" in js,
       "Town gallery navigation is incomplete")
ensure("closeMobileNav" in js and "event.key==='Escape'" in js,
       "Mobile navigation dismiss behavior is incomplete")
ensure("sol-pause-launcher" in js and ".sol-assistant.sol-pause-launcher" in (ROOT / "styles.css").read_text(encoding="utf-8"),
       "Floating assistant must not obstruct the video controls")
ensure("ambientDesktop.matches&&!saveData" in js,
       "Data-saving ambient video optimization missing")
ensure("backTop.hidden" in motion and "compareDocumentPosition" in motion,
       "Scroll navigation/progress implementation incomplete")
ensure(".back-to-top[hidden]" in css and "prefers-reduced-motion" in css,
       "Accessibility styles or hidden button style missing")
ensure('id="hero-film-ambient" autoplay' not in homepage,
       "Decorative video must not autoplay without JS controls")
ensure("media/consuegra/molinos.webp" in homepage,
       "Locally hosted Consuegra photo missing")
ensure(re.search(r'<video[^>]*id="hero-zamburinas"[^>]*autoplay', homepage) is not None,
       "Main video autoplay unexpectedly removed")
ensure("rel=\"canonical\"" in homepage, "Canonical homepage URL missing")

# Vídeo editorial: accesible, subtitulado por su propia cartelería y sin autoplay.
ensure('id="si-promo-video"' in homepage, "Falta el reproductor de la cooperativa")
ensure('media/san-isidro-presentacion.mp4' in homepage, "Falta vídeo de San Isidro")
ensure('media/san-isidro-presentacion.webp' in homepage, "Falta cartel del vídeo")
ensure('controls playsinline preload="metadata"' in homepage, "Vídeo no accesible en móvil")
ensure('Imágenes ambientales ilustrativas, no grabadas en las instalaciones' in homepage,
       "Falta advertencia sobre origen ilustrativo")
# Cooperativa San Isidro: contenido sin duplicar y galería controlable.
ensure(homepage.count('id="san-isidro-labrador"') == 1, "Cooperativa: sección duplicada")
ensure('Cooperativa<br><em>San Isidro Labrador</em>' in homepage,
       "Falta la identidad de la cooperativa")
for value in ("1958", "43", "215", "Consaburum", "Regates",
              "Airén", "Tempranillo", "roble americano y francés"):
    ensure(value in homepage, f"Falta un dato de la ficha turística: {value}")
ensure(homepage.count('si-btn si-btn-primary') == 1,
       "Cooperativa: debe haber un único botón principal")
ensure(homepage.count('www.consuegra.es/es/experiencias/actividades/cooperativa-san-isidro') >= 1,
       "Debe incluirse el enlace a la fuente oficial")
ensure(homepage.count('si-gallery-slide') == 4,
       "La galería debe ofrecer cuatro imágenes propias")
for control in ('si-gallery-prev','si-gallery-next','si-gallery-toggle','si-gallery-count'):
    ensure(f'id="{control}"' in homepage, f"Falta control de galería: {control}")
ensure('Fotografías ambientales ilustrativas, no de la cooperativa' in homepage,
       "La galería debe identificar honestamente las imágenes")
ensure('sin acuerdo publicitario formal' in homepage,
       "No atribuir patrocinios inexistentes")
ensure('Ver vídeo con controles' not in homepage and
       'Planifica tu visita' not in homepage and
       'Descubre a nuestros productores locales' not in homepage,
       "Persisten enlaces y redundancias evitables")
gallery_script = ROOT / "wine-gallery.js"
ensure(gallery_script.is_file() and "IntersectionObserver" in gallery_script.read_text(encoding="utf-8"),
       "Falta autoplay condicionado a la visibilidad")
ensure('wine-gallery.js?v=20261112-editorial-v5' in homepage,
       "El script de galería debe estar enlazado desde portada")
ensure('Gran Selección Plata' in homepage and 'Gran Selección Oro' in homepage,
       "Deben indicarse los reconocimientos históricos de Consaburum")
ensure('anteriores a 2015' in homepage and 'anteriores a 2016' in homepage,
       "Deben precisarse las categorías de los premios")
ensure('239 millones €' in homepage and 'provincia de Toledo' in homepage,
       "No debe atribuirse la inversión provincial a San Isidro")
ensure('guia.patatasanta.com/es/actividades-experiencias-enoturismo' in homepage,
       "Falta el recurso de enoturismo de Patata Santa")
ensure('Fotografías ambientales ilustrativas, no de la cooperativa' in homepage,
       "Las fotografías deben conservar una descripción fiel")
ensure('id="encargo-open"' in homepage and 'href="https://wa.me/message/ACIXEAMQWNWME1"' in homepage,
       "Deben seguir disponibles los encargos y WhatsApp")

ensure('id="booking-faq-title"' in homepage and 'class="booking-how"' in homepage,
       "Booking guidance and FAQ missing")
ensure("zamburinas-preparacion-ambiente-v1.mp4" in homepage,
       "Lightweight desktop ambient video is not linked")
ensure('rel="preconnect" href="https://upload.wikimedia.org"' not in homepage,
       "Unnecessary third-party preconnect is still configured")

if errors:
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    raise SystemExit(1)
print("OK: four pages, multimedia, interactive controls, accessibility and versioned assets")
