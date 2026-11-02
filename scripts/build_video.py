#!/usr/bin/env python3
"""Genera el vídeo promocional de 15 s sin tokens externos."""
import base64, io, os, pathlib, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'public'/'media'; OUT.mkdir(parents=True,exist_ok=True)
URLS=[
 ('Consuegra y sus molinos','https://upload.wikimedia.org/wikipedia/commons/e/e0/Windmills_and_castle_of_Consuegra_%287079301421%29.jpg'),
 ('Castillo de la Muela','https://upload.wikimedia.org/wikipedia/commons/9/9d/Castillo_de_Consuegra.jpg'),
 ('Pisto manchego','https://upload.wikimedia.org/wikipedia/commons/8/81/Pisto_manchego.jpg'),
 ('Croquetas tradicionales','https://upload.wikimedia.org/wikipedia/commons/2/2c/Croquetas_de_jam%C3%B3n_-_lacestabar.jpg'),
 ('El Consaburense | Tradición y sabor','')]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; font2='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
slides=[]
for i,(name,url) in enumerate(URLS):
    try:
        if not url: raise ValueError('Final with brand')
        req=urllib.request.Request(url,headers={'User-Agent':'ElConsaburenseWebsite/1.0 (contact: website)'}); 
        with urllib.request.urlopen(req,timeout=18) as response: raw=response.read(16000000)
        im=Image.open(io.BytesIO(raw)).convert('RGB'); im=ImageOps.fit(im,(960,540),method=Image.Resampling.LANCZOS)
        print('Photo OK',name)
    except Exception as exc:
        print('Image fallback',name,str(exc))
        im=Image.new('RGB',(960,540),(100+i*10,58+i*4,28)); d=ImageDraw.Draw(im)
        for y in range(540):
            v=int(y/540*40);d.line((0,y,960,y),fill=(115+v//2,60+v//3,29+v//4))
    d=ImageDraw.Draw(im,'RGBA');d.rectangle((0,340,960,540),fill=(15,10,7,168))
    d.text((54,402),name,font=ImageFont.truetype(font,33),fill='white')
    d.text((56,455),'CONSUEGRA · TOLEDO · CASTILLA-LA MANCHA',font=ImageFont.truetype(font2,17),fill=(246,216,176))
    # El logotipo se mantiene exclusivamente en la cabecera de la web.
    path=OUT/f'frame-{i}.jpg';im.save(path,quality=85);slides.append(path)
# Cinco segmentos consecutivos de tres segundos producen un vídeo de 15s.
inputs=[]
for path in slides: inputs+=['-loop','1','-framerate','24','-t','3','-i',str(path)]
filter_complex=''.join(f'[{i}:v]scale=960:540,setsar=1,format=yuv420p[v{i}];' for i in range(len(slides)))
filter_complex+=''.join(f'[v{i}]' for i in range(len(slides)))+f'concat=n={len(slides)}:v=1:a=0,format=yuv420p[v]'
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',*inputs,'-filter_complex',filter_complex,'-map','[v]','-c:v','libx264','-preset','veryfast','-crf','25','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(OUT/'consaburense-15s.mp4')]
subprocess.run(cmd,check=True)
for p in slides:p.unlink()
print('GENERATED',OUT/'consaburense-15s.mp4')
