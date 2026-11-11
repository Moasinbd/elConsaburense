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

# El documento A5 de sugerencias tiene 12 referencias y sus precios.
suggestion_names = ["Chorizo Criollo a la Parrilla","Nuestras Famosas Croquetas Caseras de Jamón Ibérico","Ensalada de Tomate de la Huerta con Ventresca","Huevo Roto Trufado sobre Cama de Patatas","Zamburiñas Selectas (al Ajillo o con Huevo y Patata)","Callos Tradicionales Consaburense","Carrillada Ibérica Estofada al Vino D.O.","Lomo de Rodaballo Salteado con Verduritas","Bacalao Confitado sobre Pisto Manchego","Chuletillas de Lechal Manchego Fritas","Entrecot de Ternera Mayor a la Parrilla","Solomillo de Vacuno (a la Plancha o al Ajillo Suave)"]
suggestion_prices = ["7,40 €","9,70 €","12,50 €","12,80 €","18,90 €","11,40 €","14,30 €","17,80 €","20,00 €","22,40 €","22,60 €","22,60 €"]
ensure('id="sugerencias"' in homepage and 'href="#sugerencias"' in homepage,
       "Suggestions must be accessible from the menu")
ensure(homepage.count('class="day-suggestion"') == 12,
       "Suggestions menu must contain exactly 12 dishes")
for dish in suggestion_names:
    ensure(dish in homepage, f"Missing menu suggestion: {dish}")
for price in suggestion_prices:
    ensure(price in homepage, f"Missing suggested price: {price}")
ensure("day-suggestions-starters" in homepage and "day-suggestions-mains" in homepage,
       "Suggestion groups are missing")
ensure('Información de alérgenos indicada en la carta' in homepage and 'contacto cruzado' in homepage,
       "Allergen information missing")
ensure('class="day-suggestion-price"' in homepage and 'day-suggestions-section' in (ROOT / "styles.css").read_text(encoding="utf-8"),
       "Suggestions menu styles missing")

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
