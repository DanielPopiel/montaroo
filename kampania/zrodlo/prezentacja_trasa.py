"""PREZENTACJA_trasa_skoku.html – makieta profilu IG + Reel + plan publikacji (jeden plik, obrazy w base64)."""
import base64, io, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trasa_lib import ROOT
D = os.path.join(ROOT, 'kampania', 'trasa')

def img64(path, w):
    im = Image.open(path).convert('RGB'); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=86); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def file64(path, mime): return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()
def font64(n): return file64(os.path.join(ROOT, 'brand', 'fonts', n), 'font/woff2')

POSTS = [  # (kafel, post, typ, hook, stan)
 (1, 6, 'Reel', '1,434 clips. Never watched.', 'okładka gotowa · Reel po nagraniach z aplikacji'),
 (2, 5, 'Reel', 'A kangaroo can clear 8 m in one hop.', 'gotowy (EN + PL)'),
 (3, 4, 'Reel', 'A joey stays in the pouch for 8 months.', 'okładka gotowa'),
 (4, 3, 'Reel', "Kangaroos don't hop backwards.", 'okładka gotowa'),
 (5, 2, 'Karuzela', '5 phones. 1 film.', 'okładka gotowa · przed/po z kadrów aplikacji'),
 (6, 1, 'Reel', 'A group of kangaroos is called a mob.', 'okładka gotowa'),
]
tiles = {t: img64(f'{D}/kafel-T{t}_post-{p}.png', 540) for t, p, *_ in POSTS}
covers = {t: img64(f'{D}/okladka-post-{p}_T{t}.png', 360) for t, p, *_ in POSTS}
avatar = file64(os.path.join(ROOT, 'brand', 'logo', 'png', 'montaroo-znak-kolor-ciemne-512.png'), 'image/png')
import subprocess
posters = {}
for L in ('en', 'pl'):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '5.2', '-i', f'{D}/reel-post-5_T2_{L}.mp4', '-frames:v', '1', f'/tmp/poster_{L}.png'])
    posters[L] = img64(f'/tmp/poster_{L}.png', 540)
v_en = file64(f'{D}/reel-post-5_T2_en.mp4', 'video/mp4'); v_pl = file64(f'{D}/reel-post-5_T2_pl.mp4', 'video/mp4')

reel_ico = '<svg viewBox="0 0 24 24" width="22" height="22"><path fill="#fff" d="M4 4h16v16H4z" opacity="0"/><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-width="2"/><path d="M10 9l5 3-5 3z" fill="#fff"/></svg>'
car_ico = '<svg viewBox="0 0 24 24" width="22" height="22"><rect x="7" y="3" width="14" height="14" rx="3" fill="none" stroke="#fff" stroke-width="2"/><path d="M4 7v12a2 2 0 0 0 2 2h12" fill="none" stroke="#fff" stroke-width="2"/></svg>'
grid = ''.join(f'<div class="tile"><img src="{tiles[t]}" alt=""><span class="ico">{reel_ico if typ=="Reel" else car_ico}</span>'
               f'<span class="ord">{p}</span></div>' for t, p, typ, *_ in POSTS)
rows = ''.join(f'<tr><td><b>{p}</b></td><td>T{t}</td><td>{typ}</td><td>„{h}”</td><td>{st}</td></tr>'
               for t, p, typ, h, st in sorted(POSTS, key=lambda x: x[1]))
covs = ''.join(f'<figure><img src="{covers[t]}" alt=""><figcaption>Post {p} · T{t}</figcaption></figure>'
               for t, p, *_ in sorted(POSTS, key=lambda x: x[1]))

html = f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Montaroo – siatka „Trasa skoku”</title><style>
@font-face{{font-family:G;font-weight:800;src:url({font64('gabarito-latin-800-normal.woff2')})}}
@font-face{{font-family:G;font-weight:800;src:url({font64('gabarito-latin-ext-800-normal.woff2')});unicode-range:U+0100-024F,U+201E}}
@font-face{{font-family:I;font-weight:400;src:url({font64('inter-latin-400-normal.woff2')})}}
@font-face{{font-family:I;font-weight:400;src:url({font64('inter-latin-ext-400-normal.woff2')});unicode-range:U+0100-024F,U+201E}}
@font-face{{font-family:I;font-weight:600;src:url({font64('inter-latin-600-normal.woff2')})}}
@font-face{{font-family:I;font-weight:600;src:url({font64('inter-latin-ext-600-normal.woff2')});unicode-range:U+0100-024F,U+201E}}
:root{{--ink:#10251F;--och:#E2642A;--gold:#F2B544;--euc:#3E7C68;--sand:#F4E9D6}}
*{{box-sizing:border-box;margin:0}}body{{font:400 16px/1.55 I,system-ui,sans-serif;background:var(--sand);color:var(--ink)}}
.wrap{{max-width:1180px;margin:0 auto;padding:56px 28px 96px}}
h1{{font:800 clamp(40px,6vw,76px)/.95 G;letter-spacing:-.035em}}h2{{font:800 34px/1.05 G;letter-spacing:-.02em;margin:0 0 18px}}
.k{{font:600 13px/1 I;letter-spacing:.14em;text-transform:uppercase;color:#B4471A;margin-bottom:14px}}
.lead{{max-width:640px;margin-top:18px;color:#3E5A50;font-size:18px}}
.top{{display:grid;grid-template-columns:420px 1fr;gap:56px;margin-top:56px;align-items:start}}
.phone{{background:#fff;border-radius:44px;padding:14px;box-shadow:0 30px 60px -30px #10251f66,0 0 0 1px #10251f14}}
.scr{{border-radius:32px;overflow:hidden;background:#fff;color:#111;font-family:system-ui,-apple-system,Segoe UI,sans-serif}}
.bar{{display:flex;justify-content:center;padding:14px 0 6px;font-weight:700;font-size:15px}}
.hd{{display:flex;gap:22px;align-items:center;padding:12px 16px}}.av{{width:80px;height:80px;border-radius:50%;background:var(--ink) url({avatar}) center/62% no-repeat;flex:none}}
.st{{display:flex;gap:18px;font-size:13px;text-align:center}}.st b{{display:block;font-size:16px}}
.bio{{padding:0 16px 12px;font-size:13px;line-height:1.4}}.bio a{{color:#00376b;font-weight:600}}
.btns{{display:flex;gap:6px;padding:0 16px 12px}}.btns span{{flex:1;background:#efefef;border-radius:8px;text-align:center;font-weight:600;font-size:13px;padding:7px}}
.tabs{{display:flex;border-top:1px solid #dbdbdb}}.tabs span{{flex:1;text-align:center;padding:9px;font-size:12px;color:#888}}.tabs span:first-child{{color:#111;border-bottom:1px solid #111}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}}.tile{{position:relative;aspect-ratio:3/4;overflow:hidden;background:var(--ink)}}
.tile img{{width:100%;height:100%;object-fit:cover;display:block}}.ico{{position:absolute;top:6px;right:6px;filter:drop-shadow(0 1px 2px #0008)}}
.ord{{position:absolute;inset:0;display:grid;place-items:center;font:800 64px G;color:var(--gold);background:#10251fcc;opacity:0;transition:.25s}}
body.ord-on .ord{{opacity:1}}
.tg{{margin-top:16px;display:inline-flex;gap:10px;align-items:center;font:600 14px I;background:var(--ink);color:var(--sand);border:0;border-radius:999px;padding:12px 20px;cursor:pointer}}
.card{{background:#fff8ec;border:1px solid #10251f1a;border-radius:20px;padding:26px 28px;margin-bottom:22px}}
.card p+p{{margin-top:10px}}.card ul{{padding-left:20px}}.card li+li{{margin-top:6px}}
.reels{{display:flex;gap:18px;flex-wrap:wrap}}.reels figure{{flex:1;min-width:220px}}video{{width:100%;border-radius:18px;background:var(--ink);display:block;aspect-ratio:9/16}}
figcaption{{font:600 13px I;margin-top:8px;color:#3E5A50}}
table{{width:100%;border-collapse:collapse;font-size:15px}}td,th{{text-align:left;padding:11px 10px;border-bottom:1px solid #10251f1a;vertical-align:top}}th{{font:600 12px I;letter-spacing:.1em;text-transform:uppercase;color:#3E5A50}}
.covers{{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}}.covers img{{width:100%;border-radius:12px;display:block}}
section{{margin-top:72px}}
@media (max-width:900px){{.top{{grid-template-columns:1fr}}.phone{{max-width:420px;margin:0 auto}}.covers{{grid-template-columns:repeat(3,1fr)}}table{{font-size:14px}}td:nth-child(5),th:nth-child(5){{display:none}}}}
</style></head><body><div class="wrap">
<p class="k">Montaroo · kampania · Instagram</p>
<h1>Siatka „Trasa skoku”</h1>
<p class="lead">Sześć Reeli, których okładki składają się w jedną panoramę. Joey skacze po przerywanej trasie od stosu nieobejrzanych klipów do stada („mob”). Każdy kafelek ma własny hook i działa też sam.</p>

<div class="top">
 <div><div class="phone"><div class="scr">
  <div class="bar">montarooapp</div>
  <div class="hd"><div class="av"></div><div class="st"><div><b>6</b>posts</div><div><b>0</b>followers</div><div><b>0</b>following</div></div></div>
  <div class="bio"><b>Montaroo</b><br>Hop from footage to film.<br>Turns your trip footage into a finished film. Offline, on Windows.<br><a>montaroo.com</a></div>
  <div class="btns"><span>Follow</span><span>Message</span></div>
  <div class="tabs"><span>▦</span><span>▶</span><span>☺</span></div>
  <div class="grid">{grid}</div>
 </div></div>
 <div style="text-align:center"><button class="tg" onclick="document.body.classList.toggle('ord-on')">Pokaż / ukryj kolejność publikacji</button></div></div>

 <div>
  <div class="card"><h2>Reel do posta 5 (gotowy)</h2><p style="color:#3E5A50;font-size:14px;margin:-6px 0 14px">Muzyka: własny podkład (remaster pierwszego bitu, A–F–C–G, 120 BPM), bez licencji zewnętrznych.</p>
   <div class="reels"><figure><video poster="{posters['en']}" src="{v_en}" controls loop muted playsinline></video><figcaption>EN · konto @montarooapp</figcaption></figure>
   <figure><video poster="{posters['pl']}" src="{v_pl}" controls loop muted playsinline></video><figcaption>PL · prywatne profile / reklamy</figcaption></figure></div></div>
  <div class="card"><h2>Jak publikować</h2><ul>
   <li><b>Od końca.</b> Instagram stawia najnowszy post w lewym górnym rogu, więc post 1 to kafelek T6 (prawy dolny), a post 6 to T1.</li>
   <li><b>Paczkami po 3.</b> Najpierw dolny rząd (posty 1–3), potem górny (4–6). Pełny rząd zawsze wygląda dobrze, nawet zanim reszta jest gotowa.</li>
   <li><b>Okładka:</b> przy publikacji Reela „Edytuj okładkę → Dodaj z rolki aparatu”, wybrać plik <i>okladka-post-N</i>. Kadr w siatce zostawić wyśrodkowany (3:4).</li>
   <li><b>Nie przypinać</b> postów, bo przypięte wskakują na początek i rozbijają panoramę.</li>
   <li>Kolejne Reele dokładamy po 3, a trasa idzie dalej, więc wzór się nie kończy.</li></ul></div>
 </div>
</div>

<section><h2>Plan sześciu postów</h2><div class="card" style="padding:8px 18px">
<table><tr><th>Post</th><th>Kafel</th><th>Typ</th><th>Hook</th><th>Stan</th></tr>{rows}</table></div>
<p style="color:#3E5A50;font-size:14px;margin-top:-6px">Fakty sprawdzone: skok ok. 8–9 m (rekord 12,8 m), joey kangura rudego opuszcza torbę na stałe po ok. 8 miesiącach (235 dni). Kangury potrafią się cofnąć tylko niezgrabnie, stąd ostrożne „don't hop backwards”.</p></section>

<section><h2>Okładki Reeli (1080×1920)</h2><div class="covers">{covs}</div></section>
</div></body></html>"""
open(f'{D}/PREZENTACJA_trasa_skoku.html', 'w').write(html)
print(len(html) // 1024, 'KB')
