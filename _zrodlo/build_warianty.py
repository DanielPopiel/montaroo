# -*- coding: utf-8 -*-
"""Dwie dodatkowe wersje strony „w budowie” do porównania:
  warianty/w2/  – „Montażownia”: ciemny ekran, podgląd filmu tnie się co beat, a znak (torba z joeyem)
                   skacze po klipach na osi czasu jak głowica odtwarzania.
  warianty/w3/  – „Klaps”: wielki klaps filmowy, który co takt się zamyka; przy każdym klapnięciu
                   joey wyskakuje z torby, a numer ujęcia rośnie.
Uruchom:  python _zrodlo/build_warianty.py
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'brand', 'logo', 'zrodlo'))
import mark

PRE = '../../'
CLIPS = ['st_489', 'st_401', 'st_145', 'st_240.5', 'st_473', 'mv']

def logo(variant='kolor'):
    s = open(os.path.join(ROOT, 'brand', 'logo', 'svg', f'montaroo-poziome-{variant}.svg'), encoding='utf-8').read()
    return re.sub(r'<title>.*?</title>', '', s).replace('<svg ', '<svg class="logo" role="img" aria-label="montaroo" ', 1)

FONTS = ''.join(
    f'@font-face{{font-family:{fam};font-weight:{w};font-display:swap;src:url({PRE}assets/fonts/{f}) format("woff2");unicode-range:{ur}}}'
    for fam, w, f, ur in [
        ('Gabarito', 800, 'gabarito-latin-800-normal.woff2', 'U+0000-00FF,U+2000-206F,U+2212'),
        ('Gabarito', 800, 'gabarito-latin-ext-800-normal.woff2', 'U+0100-024F'),
        ('Inter', 400, 'inter-latin-400-normal.woff2', 'U+0000-00FF,U+2000-206F,U+2212'),
        ('Inter', 400, 'inter-latin-ext-400-normal.woff2', 'U+0100-024F'),
        ('Inter', 600, 'inter-latin-600-normal.woff2', 'U+0000-00FF,U+2000-206F,U+2212'),
        ('Inter', 600, 'inter-latin-ext-600-normal.woff2', 'U+0100-024F')])

HEAD = lambda title, theme: f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>{title}</title><meta name="theme-color" content="{theme}">
<link rel="icon" href="{PRE}favicon.ico" sizes="any"><link rel="icon" href="{PRE}assets/favicon.svg" type="image/svg+xml">'''

def mark_parts(joey_col, pouch_col, stitch_col, stitch_cls=''):
    e = mark.ellipse_path(*mark.EAR1) + mark.ellipse_path(*mark.EAR2)
    tri = mark.rtri(mark.TRI, mark.TRIR)
    dashes = ''.join(f'<rect class="{stitch_cls}" x="{27 + i*10.8:.1f}" y="73.3" width="6.4" height="3.4" rx="1.7" fill="{stitch_col}"/>' for i in range(7))
    joey = f'<g class="ears"><path d="{e}" fill="{joey_col}"/></g><path d="{tri}" fill="{joey_col}"/>'
    pouch = f'<path d="{mark.pouch()}" fill="{pouch_col}"/>{dashes}'
    return joey, pouch

# ---------------------------------------------------------------- W2 Montażownia
def w2():
    BEAT = 0.6; N = len(CLIPS); LOOP = BEAT * N
    p = lambda t: f'{t / LOOP * 100:.3f}%'
    joey, pouch = mark_parts('#F4E9D6', '#E2642A', '#10251F')
    # podgląd: klip i widoczny w [i*BEAT, (i+1)*BEAT)
    view_kf = ''.join(
        f'@keyframes v{i}{{0%,{p(i*BEAT)}{{opacity:0}}{p(i*BEAT+0.001)},{p((i+1)*BEAT)}{{opacity:1}}{p((i+1)*BEAT+0.001)},100%{{opacity:0}}}}'
        for i in range(N))
    blk_kf = ''.join(
        f'@keyframes b{i}{{0%,{p(i*BEAT)}{{filter:saturate(.35) brightness(.7);transform:none}}{p(i*BEAT+0.02)}{{filter:none;transform:translateY(3px)}}{p(i*BEAT+0.12)},{p((i+1)*BEAT)}{{filter:none;transform:none}}{p((i+1)*BEAT+0.01)},100%{{filter:saturate(.35) brightness(.7)}}}}'
        for i in range(N))
    # znak przesuwa się po blokach: na początku każdego beatu ląduje na bloku i
    move = ''.join(f'{p(i*BEAT)}{{left:calc({i} * (100% / {N}) + 100% / {N} / 2)}}' for i in range(N))
    move_kf = f'@keyframes mv{{{move}100%{{left:calc({N-1} * (100% / {N}) + 100% / {N} / 2)}}}}'
    css = f'''{FONTS}
:root{{--noc:#10251F;--karta:#183730;--ochra:#E2642A;--zloto:#F2B544;--euk:#3E7C68;--piasek:#F4E9D6;--cichy:#CFC4AE;--beat:{BEAT}s;--loop:{LOOP:.1f}s}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%}}
body{{background:var(--noc);color:var(--piasek);font:400 16px/1.6 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;min-height:100vh}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:22px clamp(20px,5vw,56px)}}
.logo{{height:32px;width:auto;display:block}}
.pill{{font:600 12px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--noc);background:var(--zloto);padding:9px 12px;border-radius:99px}}
main{{flex:1;width:100%;max-width:1100px;margin:0 auto;padding:8px clamp(20px,5vw,56px) 36px;display:flex;flex-direction:column;align-items:center;text-align:center}}
h1{{font:800 clamp(40px,5.6vw,80px)/.93 Gabarito,sans-serif;letter-spacing:-.045em;margin:6px 0 16px}}
h1 em{{font-style:normal;color:var(--ochra)}}
.lead{{max-width:34em;color:var(--cichy);font-size:clamp(16px,1.5vw,19px);margin:0 0 28px}}
.editor{{width:100%;max-width:660px;background:var(--karta);border-radius:22px;padding:14px 14px 18px;box-shadow:0 40px 80px -40px #000}}
.bar{{display:flex;justify-content:space-between;align-items:center;font:600 12px/1 Inter,sans-serif;color:var(--cichy);padding:4px 6px 12px}}
.bar .dot{{display:inline-block;width:8px;height:8px;border-radius:9px;background:var(--ochra);margin-right:8px;animation:blink 1.2s steps(2) infinite}}
@keyframes blink{{50%{{opacity:.2}}}}
.tc{{font-variant-numeric:tabular-nums}}
.view{{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000}}
.view img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0}}
.view .place{{position:absolute;left:18px;bottom:16px;font:800 clamp(16px,2.4vw,26px)/1 Gabarito,sans-serif;letter-spacing:.02em;text-transform:uppercase;text-shadow:0 2px 12px #0008;border-left:3px solid var(--zloto);padding-left:10px}}
.tl{{position:relative;margin:18px 4px 0;height:140px}}
.blocks{{position:absolute;left:0;right:0;bottom:22px;height:44px;display:flex;gap:6px}}
.blocks span{{flex:1;border-radius:8px;background:center/cover;box-shadow:inset 0 0 0 2px #0003}}
.wave{{position:absolute;left:0;right:0;bottom:0;height:16px;display:flex;align-items:center;gap:2px}}
.wave i{{flex:1;background:var(--euk);border-radius:2px;height:var(--h);animation:pulse var(--beat) ease-out infinite}}
@keyframes pulse{{0%{{transform:scaleY(1.5);background:var(--zloto)}}40%,100%{{transform:scaleY(1)}}}}
.hopper{{position:absolute;bottom:64px;width:64px;height:64px;margin-left:-32px;animation:mv var(--loop) linear infinite;z-index:2}}
.hopper .jump{{width:100%;height:100%;animation:jump var(--beat) cubic-bezier(.3,.7,.4,1) infinite;transform-origin:50% 100%}}
@keyframes jump{{0%{{transform:translateY(0) scale(1.12,.84)}}12%{{transform:translateY(-10px) scale(.94,1.08)}}50%{{transform:translateY(-38px) scale(1)}}88%{{transform:translateY(-4px) scale(.98,1.04)}}100%{{transform:translateY(0) scale(1.12,.84)}}}}
.hopper svg{{width:100%;height:100%;overflow:visible}}
.ph{{position:absolute;bottom:14px;top:58px;width:2px;background:var(--zloto);margin-left:-1px;animation:mv var(--loop) linear infinite}}
.ears{{transform-box:fill-box;transform-origin:50% 100%;animation:ears calc(var(--beat)*2) ease-in-out infinite}}
@keyframes ears{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-10deg)}}}}
.note{{margin:26px 0 0;font-size:14px;color:var(--cichy)}}
footer{{padding:20px clamp(20px,5vw,56px) 28px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:14px;color:var(--cichy)}}
footer b{{font:800 16px/1.2 Gabarito,sans-serif;color:var(--piasek)}}
{view_kf}{blk_kf}{move_kf}
{''.join(f'.view img:nth-child({i+1}){{animation:v{i} var(--loop) steps(1,end) infinite}}.blocks span:nth-child({i+1}){{animation:b{i} var(--loop) infinite}}' for i in range(N))}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.view img:first-child{{opacity:1}}}}
'''
    places = ['Antelope Canyon', 'Monument Valley', 'Route 66', 'Grand Canyon', 'Bearizona', 'Monument Valley']
    imgs = ''.join(f'<img src="{PRE}assets/img/soon/c_{c}.jpg" alt="">' for c in CLIPS)
    # podpis miejsca zmienia się razem z klipem
    place_kf = ''.join(f'@keyframes pl{i}{{0%,{p(i*BEAT)}{{opacity:0}}{p(i*BEAT+0.001)},{p((i+1)*BEAT)}{{opacity:1}}{p((i+1)*BEAT+0.001)},100%{{opacity:0}}}}' for i in range(N))
    place_html = ''.join(f'<span class="place" style="opacity:0;animation:pl{i} var(--loop) steps(1,end) infinite">{n}</span>' for i, n in enumerate(places))
    blocks = ''.join(f'<span style="background-image:url({PRE}assets/img/soon/c_{c}.jpg)"></span>' for c in CLIPS)
    wave = ''.join(f'<i style="--h:{int(30+60*abs(__import__("math").sin(i*.7)*__import__("math").cos(i*.23)))}%"></i>' for i in range(72))
    hop_svg = f'<svg viewBox="8 4 112 120" aria-hidden="true">{joey}{pouch}</svg>'
    html = HEAD('Montaroo · coming soon (W2)', '#10251F') + f'''<style>{css}{place_kf}</style></head><body>
<header class="top"><a href="./">{logo('kolor-ciemne')}</a><span class="pill">Coming soon</span></header>
<main>
 <h1>Cutting it <em>to the beat.</em></h1>
 <p class="lead">Montaroo, the automatic travel film editor for Windows, is hopping in soon. Offline, on your PC, from the folder on your desktop to a film you’ll rewatch.</p>
 <div class="editor" aria-hidden="true">
  <div class="bar"><span><span class="dot"></span>USA 2026 · Grand Circle</span><span class="tc" id="tc">00:00:00:00</span></div>
  <div class="view">{imgs}{place_html}</div>
  <div class="tl"><div class="ph"></div><div class="hopper"><div class="jump">{hop_svg}</div></div><div class="blocks">{blocks}</div><div class="wave">{wave}</div></div>
 </div>
 <p class="note">Every cut lands on a beat. Every clip lands in the pouch. Launching soon.</p>
</main>
<footer><b>Hop from footage to film.</b><span>© 2026 Montaroo · montaroo.com</span></footer>
<script>(()=>{{const t0=performance.now(),el=document.getElementById('tc'),z=n=>String(n).padStart(2,'0');
const f=()=>{{const s=(performance.now()-t0)/1000,k=Math.floor(s);el.textContent='00:'+z(Math.floor(k/60)%60)+':'+z(k%60)+':'+z(Math.floor(s*25)%25);requestAnimationFrame(f)}};f()}})();</script>
</body></html>'''
    # wyrównanie podpisu miejsca: tylko jeden widoczny naraz
    html = html.replace('.view .place{', '.view .place{transition:none;')
    return html

# ---------------------------------------------------------------- W3 Klaps
def w3():
    LOOP = 2.4; SNAP = 1.75
    p = lambda t: f'{t / LOOP * 100:.2f}%'
    joey, pouch = mark_parts('#F4E9D6', '#E2642A', '#10251F')
    css = f'''{FONTS}
:root{{--noc:#10251F;--ochra:#E2642A;--zloto:#F2B544;--euk:#3E7C68;--piasek:#F4E9D6;--karta:#FBF6EC;--cichy:#3E5A50;--akcent:#B4471A;--loop:{LOOP}s}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%}}
body{{background:var(--ochra);color:var(--noc);font:400 16px/1.6 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;min-height:100vh;overflow-x:hidden}}
.top{{display:flex;justify-content:space-between;align-items:center;padding:22px clamp(20px,5vw,56px)}}
.logo{{height:32px;width:auto;display:block}}
main{{flex:1;width:100%;max-width:1200px;margin:0 auto;padding:8px clamp(20px,5vw,56px) 40px;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:center}}
.k{{font:600 13px/16px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin:0 0 18px}}
h1{{font:800 clamp(44px,6.2vw,88px)/.92 Gabarito,sans-serif;letter-spacing:-.045em;margin:0 0 22px}}
.lead{{font-size:clamp(17px,1.5vw,19px);max-width:30em;margin:0}}
.scene{{position:relative;width:100%;max-width:560px;justify-self:center;aspect-ratio:560/470}}
.slate{{position:absolute;left:0;right:0;bottom:0;top:16%;background:var(--noc);border-radius:18px;color:var(--piasek);padding:16% 7% 7%;box-shadow:0 30px 60px -30px #10251fcc;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:0;container-type:inline-size}}
.cell{{border-top:2px solid #f4e9d633;padding:2.6cqw 2.4cqw 0;display:flex;flex-direction:column;gap:.6cqw}}
.cell:nth-child(odd){{border-right:2px solid #f4e9d633}}
.cell small{{font:600 2.3cqw/1 Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#cfc4ae}}
.cell b{{font:800 6.6cqw/1 Gabarito,sans-serif;letter-spacing:-.02em}}
.cell b.take{{color:var(--zloto);font-variant-numeric:tabular-nums}}
.clap{{position:absolute;left:0;right:0;top:16%;height:13%;transform-origin:2.5% 100%;animation:clap var(--loop) cubic-bezier(.6,0,.8,.4) infinite;z-index:2}}
.clap .stick,.base{{position:absolute;inset:0;border-radius:12px 12px 4px 4px;background:repeating-linear-gradient(-60deg,var(--piasek) 0 28px,var(--noc) 28px 56px);box-shadow:inset 0 0 0 3px var(--noc)}}
.base{{top:16%;height:13%;bottom:auto;border-radius:6px;background:repeating-linear-gradient(60deg,var(--piasek) 0 28px,var(--noc) 28px 56px);z-index:1}}
@keyframes clap{{0%{{transform:rotate(0)}}{p(0.25)}{{transform:rotate(0)}}{p(1.1)}{{transform:rotate(-26deg)}}{p(SNAP-0.02)}{{transform:rotate(-26deg)}}{p(SNAP)}{{transform:rotate(0)}}{p(SNAP+0.06)}{{transform:rotate(-2.5deg)}}{p(SNAP+0.12)},100%{{transform:rotate(0)}}}}
.burst{{position:absolute;right:-2%;top:6%;width:22%;z-index:3;opacity:0;animation:burst var(--loop) infinite}}
@keyframes burst{{0%,{p(SNAP-0.01)}{{opacity:0;transform:scale(.6)}}{p(SNAP+0.03)}{{opacity:1;transform:scale(1)}}{p(SNAP+0.3)},100%{{opacity:0;transform:scale(1.15)}}}}
.shake{{position:absolute;inset:0;animation:shake var(--loop) infinite}}
@keyframes shake{{0%,{p(SNAP-0.01)},{p(SNAP+0.2)},100%{{transform:none}}{p(SNAP+0.04)}{{transform:translate(2px,3px)}}{p(SNAP+0.1)}{{transform:translate(-2px,-1px)}}}}
.mk{{position:absolute;right:5%;bottom:3%;width:21%;z-index:4}}
.mk svg{{width:100%;overflow:visible;display:block}}
.joey{{transform-box:view-box;transform-origin:64px 64px;animation:pop var(--loop) infinite}}
@keyframes pop{{0%,{p(0.55)}{{transform:translateY(0)}}{p(0.85)},{p(SNAP+0.02)}{{transform:translateY(56px)}}{p(SNAP+0.18)}{{transform:translateY(-8px) scaleY(1.06)}}{p(SNAP+0.32)}{{transform:translateY(1px)}}{p(SNAP+0.42)},100%{{transform:translateY(0)}}}}
.ears{{transform-box:fill-box;transform-origin:50% 100%;animation:ears var(--loop) infinite}}
@keyframes ears{{0%,{p(SNAP+0.3)}{{transform:rotate(0)}}{p(SNAP+0.42)}{{transform:rotate(-12deg)}}{p(SNAP+0.55)},100%{{transform:rotate(0)}}}}
footer{{padding:20px clamp(20px,5vw,56px) 28px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:14px}}
footer b{{font:800 16px/1.2 Gabarito,sans-serif}}
@media (max-width:860px){{main{{grid-template-columns:1fr}}.scene{{order:-1;max-width:460px}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.joey{{transform:none}}}}
'''
    mk = (f'<svg viewBox="0 0 128 128" aria-hidden="true"><defs><clipPath id="c3"><rect x="0" y="-60" width="128" height="126"/></clipPath></defs>'
          f'<g clip-path="url(#c3)"><g class="joey">{joey}</g></g>{pouch}</svg>')
    burst = ('<svg class="burst" viewBox="0 0 100 100" aria-hidden="true"><g stroke="#10251F" stroke-width="7" stroke-linecap="round">'
             '<path d="M20 60 L4 70"/><path d="M30 38 L14 26"/><path d="M52 30 L54 8"/><path d="M74 40 L92 26"/></g></svg>')
    html = HEAD('Montaroo · coming soon (W3)', '#E2642A') + f'''<style>{css}</style></head><body>
<header class="top"><a href="./">{logo('mono-ciemny')}</a><span style="font:600 13px Inter;letter-spacing:.14em;text-transform:uppercase">In production</span></header>
<main>
 <div class="scene" aria-hidden="true"><div class="shake">
  <div class="base"></div><div class="clap"><div class="stick"></div></div>{burst}
  <div class="slate">
   <div class="cell"><small>Production</small><b>montaroo</b></div>
   <div class="cell"><small>Scene</small><b>montaroo.com</b></div>
   <div class="cell"><small>Take</small><b class="take" id="take">1</b></div>
   <div class="cell"><small>Director</small><b>Joey</b></div>
   <div class="cell"><small>Roll</small><b>1,434 clips</b></div>
   <div class="cell"><small>Release</small><b>Soon</b></div>
  </div>
  <div class="mk">{mk}</div>
 </div></div>
 <div>
  <p class="k">Coming soon</p>
  <h1>Take 98.<br>Almost a wrap.</h1>
  <p class="lead">Montaroo, the automatic travel film editor for Windows, is in its final takes. Your clips go in, a film with a story comes out. Offline, on your PC.</p>
 </div>
</main>
<footer><b>Hop from footage to film.</b><span>© 2026 Montaroo · montaroo.com</span></footer>
<script>(()=>{{let n=90;const el=document.getElementById('take');
if(matchMedia('(prefers-reduced-motion: reduce)').matches){{el.textContent='98';return}}
el.textContent=n;setTimeout(function go(){{n=n<98?n+1:90;el.textContent=n;setTimeout(go,{int(LOOP*1000)})}},{int(SNAP*1000)});}})();</script>
</body></html>'''
    return html

for name, fn in (('w2', w2), ('w3', w3)):
    out = os.path.join(ROOT, 'warianty', name, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(fn())
    print('ok', out)
