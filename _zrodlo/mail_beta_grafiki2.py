"""Grafiki do wariantów 6–10 maila powitalnego (kontynuacja mail_beta_grafiki.py). python _zrodlo/mail_beta_grafiki2.py <katalog_z_klatkami>"""
import sys, os
sys.argv += [] ; K = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
import importlib.util
spec = importlib.util.spec_from_file_location('g1', os.path.join(os.path.dirname(__file__), 'mail_beta_grafiki.py'))
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = f'{R}/assets/mail'
FONTS = f'file://{R}/assets/fonts'; LOGO = f'file://{R}/brand/logo/png/montaroo-poziome-kolor-ciemne.png'
from playwright.sync_api import sync_playwright
from PIL import Image
BASE = f"""<meta charset="utf-8"><style>
@font-face{{font-family:G;src:url({FONTS}/gabarito-latin-ext-800-normal.woff2)}}@font-face{{font-family:G;src:url({FONTS}/gabarito-latin-800-normal.woff2)}}
@font-face{{font-family:I;font-weight:400;src:url({FONTS}/inter-latin-ext-400-normal.woff2)}}@font-face{{font-family:I;font-weight:400;src:url({FONTS}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:I;font-weight:600;src:url({FONTS}/inter-latin-ext-600-normal.woff2)}}@font-face{{font-family:I;font-weight:600;src:url({FONTS}/inter-latin-600-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;font-family:I,sans-serif;background:#10251F}}</style>"""
def render(pg, html, h, name):
    pg.set_viewport_size({'width': 1200, 'height': h}); tmp = f'{OUT}/_tmp.html'
    open(tmp, 'w', encoding='utf-8').write(BASE + html); pg.goto('file://' + tmp); pg.wait_for_timeout(600); os.remove(tmp)
    pg.screenshot(path=f'{OUT}/{name}.png'); Image.open(f'{OUT}/{name}.png').convert('RGB').save(f'{OUT}/{name}.jpg', quality=84, optimize=True); os.remove(f'{OUT}/{name}.png')

# ikony SVG (bez emoji – nie każdy system je ma)
PHONE = '<svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="#F2B544" stroke-width="1.6"><rect x="6" y="2" width="12" height="20" rx="2.5"/><circle cx="12" cy="18" r="1"/></svg>'
CAM = '<svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="#F2B544" stroke-width="1.6"><rect x="3" y="6" width="18" height="13" rx="2.5"/><circle cx="14" cy="12.5" r="3.6"/><rect x="5" y="8" width="3" height="2"/></svg>'
DRONE = '<svg width="90" height="90" viewBox="0 0 24 24" fill="none" stroke="#F2B544" stroke-width="1.6"><rect x="9" y="10" width="6" height="4" rx="1"/><path d="M9 11 5 7M15 11l4-4M9 13l-4 4M15 13l4 4"/><circle cx="5" cy="7" r="2.4"/><circle cx="19" cy="7" r="2.4"/><circle cx="5" cy="17" r="2.4"/><circle cx="19" cy="17" r="2.4"/></svg>'
M6 = f"""<div style="height:400px;padding:50px 70px;color:#F4E9D6">
<div style="font:600 20px I;letter-spacing:.2em;color:#3E7C68">JEDNO PYTANIE</div>
<div style="font:800 84px/1 G;margin:14px 0 44px">Czym nagrywasz?</div>
<div style="display:flex;gap:28px">{''.join(f'<div style="flex:1;border:2px solid #F2B54466;border-radius:22px;padding:30px;display:flex;align-items:center;gap:22px">{ic}<span style="font:800 40px G">{t}</span></div>' for ic,t in [(PHONE,'Telefon'),(CAM,'GoPro'),(DRONE,'Dron')])}</div></div>"""

def frame(f, lab, n):
    return f'<div style="flex:1;position:relative"><img src="file://{K}/{f}" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:6px"><div style="font:600 17px I;letter-spacing:.16em;color:#F2B544;margin-top:14px">ROZDZIAŁ {n}</div><div style="font:800 30px G;color:#F4E9D6">{lab}</div></div>'
holes = '<div style="height:26px;background:repeating-linear-gradient(90deg,transparent 0 18px,#F4E9D6 18px 36px,transparent 36px 54px);opacity:.25;border-radius:4px"></div>'
M7 = f"""<div style="height:500px;padding:40px 50px"><div style="background:#0a1814;border-radius:18px;padding:22px 28px">{holes}
<div style="display:flex;gap:24px;margin:22px 0">{frame('g3.8.jpg','W drodze',1)}{frame('g7.2.jpg','Grand Canyon',2)}{frame('f16.jpg','Monument Valley',3)}</div>{holes}</div>
<div style="font:600 21px I;color:#F4E9D6b0;margin-top:22px">Rozdziały z prawdziwego filmu, który ułożył Montaroo – plansze dodał sam.</div></div>"""

M9 = f"""<div style="position:relative;height:675px;overflow:hidden"><img src="file://{K}/f16.jpg" style="width:1200px;display:block;filter:brightness(.82)">
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><div style="width:170px;height:170px;border-radius:50%;background:#E2642A;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 50px #0008"><svg width="70" height="70" viewBox="0 0 24 24"><path d="M7 4v16l14-8z" fill="#10251F"/></svg></div></div>
<div style="position:absolute;right:34px;bottom:34px;background:#10251FE6;color:#F4E9D6;font:600 24px I;padding:10px 18px;border-radius:10px">▶ 0:20 · zmontowane w Montaroo</div></div>"""

M10 = f"""<div style="height:440px;padding:40px 90px;color:#F4E9D6;display:flex;align-items:center;gap:70px">
<div style="font:800 300px/0.85 G;color:#E2642A">20</div>
<div><div style="font:600 20px I;letter-spacing:.2em;color:#3E7C68">PIERWSZA RUNDA TESTÓW</div>
<div style="font:800 66px/1.02 G;margin:14px 0 30px">miejsc dla osób<br>z listy</div>
<div style="display:flex;gap:10px">{''.join('<span style="width:26px;height:26px;border-radius:50%;border:3px solid #F2B544"></span>' for _ in range(10))}</div>
<div style="display:flex;gap:10px;margin-top:10px">{''.join('<span style="width:26px;height:26px;border-radius:50%;border:3px solid #F2B544"></span>' for _ in range(10))}</div></div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    render(pg, M6, 400, 'm6-pytanie'); render(pg, M7, 500, 'm7-rozdzialy'); render(pg, M9, 675, 'm9-play'); render(pg, M10, 440, 'm10-miejsca')
    b.close()
Image.open(f'{OUT}/m9-play.jpg').resize((560, 315)).save(f'{OUT}/m8-miniatura.jpg', quality=84)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}')//1024, 'KB')
