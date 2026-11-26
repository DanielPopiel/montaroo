"""Grafiki do 5 wariantów maila powitalnego (rekrutacja testerów bety).
Wejście: klatki z assets/video (probka-usa.mp4, film-20s-16x9.mp4) wyciągnięte ffmpegiem + assets/historia/kafle.jpg.
Wyjście: assets/mail/m1..m5. Bez AI, 0 kredytów.  python _zrodlo/mail_beta_grafiki.py <katalog_z_klatkami>"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
OUT = f'{R}/assets/mail'; os.makedirs(OUT, exist_ok=True)
FONTS = f'file://{R}/assets/fonts'
LOGO = f'file://{R}/brand/logo/png/montaroo-poziome-kolor-ciemne.png'
BASE = f"""<style>
@font-face{{font-family:G;src:url({FONTS}/gabarito-latin-ext-800-normal.woff2)}}@font-face{{font-family:G;src:url({FONTS}/gabarito-latin-800-normal.woff2)}}
@font-face{{font-family:I;font-weight:400;src:url({FONTS}/inter-latin-ext-400-normal.woff2)}}@font-face{{font-family:I;font-weight:400;src:url({FONTS}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:I;font-weight:600;src:url({FONTS}/inter-latin-ext-600-normal.woff2)}}@font-face{{font-family:I;font-weight:600;src:url({FONTS}/inter-latin-600-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;font-family:I,sans-serif}}</style>"""

def render(pg, html, h, name):
    pg.set_viewport_size({'width': 1200, 'height': h})
    tmp = f'{OUT}/_tmp.html'; open(tmp, 'w', encoding='utf-8').write('<meta charset="utf-8">' + BASE + html)
    pg.goto('file://' + tmp); pg.wait_for_timeout(600); os.remove(tmp)
    pg.screenshot(path=f'{OUT}/{name}.png')
    Image.open(f'{OUT}/{name}.png').convert('RGB').save(f'{OUT}/{name}.jpg', quality=84, optimize=True)
    os.remove(f'{OUT}/{name}.png')

# 1 – karta pokładowa
M1 = f"""<div style="height:600px;background:#10251F;display:flex;align-items:center;justify-content:center">
<div style="width:1080px;height:470px;display:flex;filter:drop-shadow(0 30px 40px #0007)">
 <div style="flex:1;background:#FFFBF4;border-radius:28px 0 0 28px;padding:44px 52px;position:relative;color:#10251F">
  <div style="display:flex;justify-content:space-between;align-items:center"><img src="{LOGO.replace('-ciemne','')}" style="height:44px"><span style="font:600 18px I;letter-spacing:.2em;color:#3E7C68">KARTA POKŁADOWA · BETA</span></div>
  <div style="display:flex;align-items:center;gap:36px;margin-top:46px">
   <div><div style="font:600 17px I;letter-spacing:.16em;color:#3E7C68">Z</div><div style="font:800 92px/1 G">FOLDER</div><div style="font:400 19px I;color:#555">1 434 nagrania</div></div>
   <div style="flex:1;height:3px;background:repeating-linear-gradient(90deg,#E2642A 0 14px,transparent 14px 26px);position:relative"><span style="position:absolute;left:50%;top:-30px;transform:translateX(-50%);font-size:46px">🦘</span></div>
   <div style="text-align:right"><div style="font:600 17px I;letter-spacing:.16em;color:#3E7C68">DO</div><div style="font:800 92px/1 G;color:#E2642A">FILM</div><div style="font:400 19px I;color:#555">z muzyką i mapą</div></div>
  </div>
  <div style="display:flex;gap:56px;margin-top:52px">
   {''.join(f'<div><div style="font:600 15px I;letter-spacing:.16em;color:#3E7C68">{a}</div><div style="font:800 34px G;margin-top:4px">{b}</div></div>' for a,b in [('LOT','MTR 001'),('MIEJSCE','Tester'),('BRAMKA','Windows'),('KLASA','Beta')])}
  </div>
 </div>
 <div style="width:250px;background:#F2B544;border-radius:0 28px 28px 0;border-left:4px dashed #10251F55;padding:44px 30px;color:#10251F;display:flex;flex-direction:column;justify-content:space-between">
  <div><div style="font:600 15px I;letter-spacing:.16em">PASAŻER</div><div style="font:800 34px/1.1 G;margin-top:6px">Ty</div></div>
  <div style="height:120px;background:repeating-linear-gradient(90deg,#10251F 0 3px,transparent 3px 6px,#10251F 6px 7px,transparent 7px 12px,#10251F 12px 16px,transparent 16px 19px)"></div>
  <div style="font:600 15px I;letter-spacing:.12em">MIEJSC: 20</div>
 </div></div></div>"""

# 4 – kadr z opisami
M4 = f"""<div style="height:760px;background:#10251F;padding:40px 60px;color:#F4E9D6">
<div style="position:relative;border-radius:20px;overflow:hidden"><img src="file://{K}/p8.jpg" style="width:1080px;display:block">
 {''.join(f'<div style="position:absolute;{pos};display:flex;align-items:center;gap:12px"><span style="width:44px;height:44px;border-radius:50%;background:#E2642A;color:#10251F;font:800 24px/44px G;text-align:center">{n}</span><span style="background:#10251FE6;padding:10px 16px;border-radius:10px;font:600 20px I">{t}</span></div>' for n,t,pos in [(1,'Plansza miejsca – sama z GPS','left:430px;bottom:66px'),(2,'Najlepsze ujęcie – wybrane automatycznie','left:40px;top:40px'),(3,'Cięcie w rytm muzyki','right:40px;top:200px')])}
</div>
<div style="font:600 21px I;margin-top:22px;color:#F2B544;letter-spacing:.04em">Kadr z filmu z naszego road tripu po USA, zmontowanego w Montaroo.</div></div>"""

# 5 – przed / po
files = ['VID_20261019_071422.mp4','VID_20261019_071509.mp4','DJI_0042.MP4','GX010188.MP4','VID_20261019_081133.mp4','IMG_4471.MOV','DJI_0043.MP4','VID_20261019_093027.mp4','GX010189.MP4','VID_20261019_101544.mp4','IMG_4472.MOV','VID_20261019_112301.mp4']
M5 = f"""<div style="height:600px;display:flex;background:#10251F">
<div style="width:560px;padding:40px 30px 40px 40px;position:relative">
 <div style="font:800 30px G;color:#F2B544;margin-bottom:16px">PRZED</div>
 <div style="background:#fff;border-radius:10px;height:470px;overflow:hidden;font:400 17px I;color:#222">
  <div style="background:#eef1f5;padding:12px 16px;font:600 16px I;color:#333">📁 USA 2026 › Dzień 6</div>
  {''.join(f'<div style="padding:7px 16px;display:flex;gap:10px;border-bottom:1px solid #f0f0f0"><span>🎞️</span>{f}</div>' for f in files)}
 </div></div>
<div style="width:80px;display:flex;align-items:center;justify-content:center;font:800 64px G;color:#E2642A">→</div>
<div style="flex:1;padding:40px 40px 40px 10px">
 <div style="font:800 30px G;color:#F2B544;margin-bottom:16px">PO</div>
 <img src="file://{K}/p8.jpg" style="width:520px;height:470px;object-fit:cover;object-position:left center;border-radius:10px;display:block"></div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    render(pg, M1, 600, 'm1-karta'); render(pg, M4, 760, 'm4-kadr'); render(pg, M5, 600, 'm5-przed-po')
    b.close()

# 3 – zdjęcie do listu (polaroidy z filmu)
Image.open(f'{K}/p37.jpg').crop((0, 60, 1920, 1020)).resize((1200, 600)).save(f'{OUT}/m3-list.jpg', quality=84)

# 2 – GIF: siatka nagrań zbiega się w jeden kadr filmu
kaf = Image.open(f'{R}/assets/historia/kafle.jpg').convert('RGB')
W, H = 600, 338
tw, th = kaf.width // 16 if kaf.width >= 4000 else 128, 0
cols, rows = 16, 7
cw, ch = kaf.width / cols, kaf.height / rows
tiles = [kaf.crop((int(c*cw), int(r*ch), int((c+1)*cw), int((r+1)*ch))) for r in range(rows) for c in range(cols)][:110]
film = Image.open(f'{K}/f16.jpg').convert('RGB').resize((W, H))
try:
    fg = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except Exception:
    fg = ImageFont.load_default()
def label(im, txt):
    d = ImageDraw.Draw(im); tw_ = d.textlength(txt, font=fg)
    d.rounded_rectangle((W/2-tw_/2-18, H-62, W/2+tw_/2+18, H-16), 12, fill=(16, 37, 31))
    d.text((W/2-tw_/2, H-56), txt, font=fg, fill=(242, 181, 68)); return im
frames, durs = [], []
gc, gr = 11, 10; sw, sh = W / gc, H / gr
def grid(scale=1.0, alpha=1.0):
    im = Image.new('RGB', (W, H), (16, 37, 31))
    for i, t in enumerate(tiles[:gc*gr]):
        c, r = i % gc, i // gc
        cx, cy = (c+.5)*sw, (r+.5)*sh
        cx = W/2 + (cx-W/2)*scale; cy = H/2 + (cy-H/2)*scale
        w, h = max(1, int(sw*scale-2)), max(1, int(sh*scale-2))
        im.paste(t.resize((w, h)), (int(cx-w/2), int(cy-h/2)))
    return im
g0 = label(grid(), '1 434 nagrania')
frames.append(g0); durs.append(1400)
for k in range(1, 9):
    s = 1 - k/9
    frames.append(Image.blend(grid(s), film, k/9 * .9)); durs.append(80)
frames.append(label(film.copy(), '→ jeden film')); durs.append(2600)
pal = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for f in frames]
pal[0].save(f'{OUT}/m2-folder-film.gif', save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}')//1024, 'KB')
