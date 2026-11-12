#!/usr/bin/env python3
"""Vídeo editorial de San Isidro Labrador. Usa imágenes ambientales autorizadas
del repositorio, no fotografías de las instalaciones reales de la cooperativa."""
from pathlib import Path
import math, struct, subprocess, tempfile, wave
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
OUT = PUBLIC / "media"
OUT.mkdir(exist_ok=True, parents=True)
VIDEO = OUT / "san-isidro-presentacion.mp4"
POSTER = OUT / "san-isidro-presentacion.webp"
W, H, FPS = 1280, 720, 24
DURATION, TRANSITION = 5.7, 0.7
TOTAL = 6*DURATION - 5*TRANSITION
SCENES = [
    ("EL PAISAJE DE LA MANCHA", ("CONSUEGRA,", "TIERRA DE VINO"),
     "Una historia ligada a nuestra tierra", "media/consuegra/molinos.webp"),
    ("1958 · EL ORIGEN", ("43 VITICULTORES.", "UN MISMO SUEÑO."),
     "Así nació la Cooperativa San Isidro Labrador", "media/vinos/castillo-consuegra.webp"),
    ("TRADICIÓN COOPERATIVA", ("CADA VENDIMIA", "CUENTA"),
     "Generaciones dedicadas al cultivo de la vid", "media/vinos/finca-antigua.webp"),
    ("OFICIO Y DEDICACIÓN", ("TIEMPO, CUIDADO", "Y PACIENCIA"),
     "Elaboración y crianza en barricas de roble", "media/vinos/calderico.webp"),
    ("VINOS DE NUESTRA TIERRA", ("CONSABURUM",),
     "Un nombre que nace en Consuegra", "media/vinos/ojos-guadiana.webp"),
    ("EL CONSABURENSE PRESENTA", ("DE NUESTRA TIERRA", "A TU MESA"),
     "Tradición y sabor · Consuegra, Toledo", "media/vinos/altovela.webp"),
]

def font(size, serif=False, bold=False):
    name = ("DejaVuSerif" if serif else "DejaVuSans") + ("-Bold" if bold else "")
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name + ".ttf", size)

def tracked(draw, xy, text, face, color, spacing=3):
    x, y = xy
    for char in text:
        draw.text((x, y), char, fill=color, font=face, anchor="lt")
        x += draw.textlength(char, font=face) + spacing

def render_scene(i, destination):
    eyebrow, titles, subtitle, photo_path = SCENES[i]
    photo = PUBLIC / photo_path
    if not photo.is_file():
        raise FileNotFoundError(str(photo))
    with Image.open(photo) as picture:
        base = ImageOps.fit(ImageOps.exif_transpose(picture).convert("RGB"),
                            (W, H), method=Image.Resampling.LANCZOS,
                            centering=(.49, .46)).convert("RGBA")
    alpha = Image.new("L", (W, 1))
    alpha.putdata([int(200*(1-(x/W)**.62)+55) for x in range(W)])
    shade = Image.new("RGBA", (W, H), (17, 9, 17, 0))
    shade.putalpha(alpha.resize((W, H)))
    base = Image.alpha_composite(base, shade)
    dim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ramp = Image.new("L", (1, H))
    ramp.putdata([int(53+65*abs((y-H/2)/(H/2))**2) for y in range(H)])
    dim.putalpha(ramp.resize((W, H)))
    base = Image.alpha_composite(base, dim)
    draw = ImageDraw.Draw(base)
    gold, white, ivory = (230,188,129,255), (255,248,235,255), (240,218,196,255)
    tracked(draw, (76,43), "EL CONSABURENSE", font(18,bold=True), white, 4)
    draw.line((76,82,430,82), fill=gold, width=2)
    tracked(draw, (78,219), eyebrow, font(18,bold=True), gold)
    size = 91 if i==4 else 77 if max(map(len,titles)) < 21 else 66
    face = font(size,serif=True,bold=True)
    while any(draw.textbbox((0,0), line,font=face)[2] > 1080 for line in titles):
        size -= 3
        face = font(size,serif=True,bold=True)
    top = 277 if len(titles)>1 else 318
    for line_no, line in enumerate(titles):
        draw.text((72,top+line_no*(size+15)),line,font=face,fill=white,
                  stroke_width=1,stroke_fill=(17,9,15,180))
    sy = min(564,top+len(titles)*(size+15)+14)
    draw.line((77,sy-20,146,sy-20),fill=gold,width=3)
    draw.text((78,sy),subtitle,fill=ivory,font=font(23))
    draw.text((78,663),"IMÁGENES AMBIENTALES · NO SON FOTOGRAFÍAS DE LA COOPERATIVA",
              fill=(239,226,205,235),font=font(13))
    draw.text((1106,663),f"{i+1:02d} / 06",fill=gold,font=font(15,bold=True))
    draw.line((75,692,1205,692),fill=(236,206,164,130),width=2)
    draw.line((75,692,75+int(1130*(i+1)/6),692),fill=gold,width=3)
    rgb = base.convert("RGB")
    rgb.save(destination,optimize=True)
    return rgb

def soundtrack(destination):
    rate = 22050
    melody = [329.63,369.99,440,392,293.66,329.63,369.99,
              293.66,277.18,329.63,293.66,246.94,329.63,220]
    chords = [(146.83,185,220), (174.61,220,261.63),
              (130.81,164.81,196), (146.83,220,293.66)]
    length = TOTAL+.25
    with wave.open(str(destination),"wb") as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(rate)
        buf = bytearray()
        for idx in range(int(length*rate)):
            t = idx/rate
            chord = chords[min(3,int(t//7.75))]
            bed = sum(math.sin(2*math.pi*f*t+.05*math.sin(t*.23))*.11 for f in chord)
            j = int(t//2.1); dt = t-j*2.1
            pitch = melody[min(len(melody)-1,j)]
            pluck = (math.sin(2*math.pi*pitch*dt)+.21*math.sin(4*math.pi*pitch*dt))*.18*math.exp(-2.4*dt)
            fade = min(1,t/1.7,max(0,(length-t)/2.1))
            amp = max(-1,min(1,(bed+pluck)*fade))
            buf.extend(struct.pack("<h",int(amp*24000)))
            if len(buf)>65536:
                wav.writeframes(buf); buf.clear()
        if buf: wav.writeframes(buf)

def main():
    with tempfile.TemporaryDirectory(prefix="san-isidro-") as temporary:
        temp = Path(temporary)
        inputs = []
        for idx in range(6):
            png = temp/f"scene-{idx}.png"
            image = render_scene(idx,png)
            inputs.append(png)
            if idx == 0:
                poster = image.copy()
                d = ImageDraw.Draw(poster,"RGBA")
                d.ellipse((1120,500,1220,600),fill=(48,23,28,185),
                          outline=(235,194,139,235),width=3)
                d.polygon([(1159,526),(1159,576),(1196,551)],fill=(255,248,231,245))
                poster.save(POSTER,format="WEBP",quality=86,method=6)
        music = temp/"ambient-original.wav"
        soundtrack(music)
        command = ["ffmpeg","-hide_banner","-loglevel","warning","-nostdin","-y"]
        for path in inputs:
            command += ["-loop","1","-framerate",str(FPS),
                        "-t",str(DURATION),"-i",str(path)]
        command += ["-i",str(music)]
        filters = []
        for idx in range(6):
            nframes = round(DURATION*FPS)
            sweep = "n" if idx%2==0 else f"({nframes}-n)"
            filters.append(
                f"[{idx}:v]scale=1350:760:flags=lanczos,"
                f"crop=1280:720:x='(iw-ow)*{sweep}/{nframes}':y='(ih-oh)/2',"
                f"format=yuv420p,setpts=PTS-STARTPTS,fps={FPS},"
                f"settb=expr=1/{FPS}[v{idx}]")
        last = "v0"
        for idx in range(1,6):
            out = f"fx{idx}"
            offset = idx*(DURATION-TRANSITION)
            filters.append(f"[{last}][v{idx}]xfade=transition=fade:"
                           f"duration={TRANSITION}:offset={offset:.3f}[{out}]")
            last = out
        command += ["-filter_complex",";".join(filters),"-map",f"[{last}]",
                    "-map","6:a:0","-c:v","libx264","-preset","veryfast",
                    "-crf","23","-profile:v","high","-level","3.1",
                    "-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-b:a","112k",
                    "-t",f"{TOTAL:.3f}","-movflags","+faststart",str(VIDEO)]
        print("Generating San Isidro film...",flush=True)
        subprocess.run(command,check=True)
    assert VIDEO.stat().st_size>50000 and POSTER.stat().st_size>20000
    print(f"San Isidro film ready: {VIDEO.stat().st_size} bytes, {TOTAL:.1f} s",flush=True)

if __name__ == "__main__":
    main()
