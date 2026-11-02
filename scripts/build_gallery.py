#!/usr/bin/env python3
"""Descarga fotos gastronómicas libres y guarda WebP locales para que el carrusel sea fiable."""
import io, pathlib, time, urllib.request
from PIL import Image, ImageOps
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"public"/"media"/"platos"
OUT.mkdir(parents=True,exist_ok=True)
HTML=ROOT/"public"/"index.html"
photos=[{"id":"33389174","slug":"croquetas-tapas"},{"id":"28490816","slug":"patatas-bravas"},{"id":"20887639","slug":"ensaladilla-rusa"},{"id":"21327969","slug":"tortilla-patatas"},{"id":"27565825","slug":"calamares-romana"},{"id":"15146199","slug":"hamburguesa-ternera"}]
html=HTML.read_text(encoding="utf-8")
for p in photos:
    source=f'https://images.pexels.com/photos/{p["id"]}/pexels-photo-{p["id"]}.jpeg?auto=compress&cs=tinysrgb&w=1280'
    target=OUT/(p["slug"]+".webp")
    for attempt in range(3):
        try:
            req=urllib.request.Request(source,headers={"User-Agent":"Mozilla/5.0 (compatible; ElConsaburense/1.0)","Accept":"image/avif,image/webp,image/*,*/*;q=0.8"})
            with urllib.request.urlopen(req,timeout=20) as response: data=response.read(9000000)
            with Image.open(io.BytesIO(data)) as src:
                im=ImageOps.fit(src.convert("RGB"),(960,780),method=Image.Resampling.LANCZOS,centering=(.5,.48))
            im.save(target,"WEBP",quality=83,method=5)
            if target.stat().st_size<4000: raise ValueError("archivo de imagen demasiado pequeño")
            html=html.replace('src="'+source.replace('&','&amp;')+'"','src="media/platos/'+p["slug"]+'.webp"')
            print("FOTO OK",p["slug"],target.stat().st_size,flush=True)
            break
        except Exception as exc:
            print("Descarga fallida",p["slug"],str(exc)[:160],flush=True)
            if attempt<2:time.sleep(2+attempt)
    else:
        print("FOTO EXTERNA",p["slug"],flush=True)
HTML.write_text(html,encoding="utf-8")
