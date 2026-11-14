# -*- coding: utf-8 -*-
"""Strona „w budowie” montaroo.com (EN: index.html, PL: pl/index.html).
Animacja 7,2 s w pętli: klipy z wyjazdu skaczą do torby (każdy = jeden szew),
na końcu joey w kasku wyskakuje z torby. Pod sceną oś czasu z głowicą jak w programie do montażu.
Uruchom z katalogu repozytorium:  python _zrodlo/build_soon.py
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'brand', 'logo', 'zrodlo'))
import mark  # geometria znaku (siatka 128)

LOOP = 7.2
CLIPS = ['st_489', 'st_401', 'st_145', 'st_240.5', 'st_473', 'mv']
N = len(CLIPS)
START, STEP, FLY = 0.35, 0.58, 0.62          # s: pierwszy skok, odstęp, czas lotu
LAND = [START + i * STEP + FLY for i in range(N)]
POP = LAND[-1] + 0.35                         # joey wyskakuje
DOWN = LOOP - 0.55                            # joey chowa się

def pct(t): return f'{t / LOOP * 100:.2f}%'

def keyframes():
    css = []
    for i in range(N):
        t0 = START + i * STEP; t1 = t0 + FLY
        css.append(f'''@keyframes clip{i}{{0%,{pct(max(0,t0-0.25))}{{offset-distance:0%;opacity:0;transform:scale(.9) rotate(-8deg)}}
{pct(max(0,t0-0.05))}{{offset-distance:0%;opacity:1;transform:scale(1) rotate(-6deg)}}
{pct(t0+FLY*0.5)}{{opacity:1;transform:scale(.92) rotate(8deg)}}
{pct(t1)}{{offset-distance:100%;opacity:1;transform:scale(.62) rotate(14deg)}}
{pct(t1+0.01)},100%{{offset-distance:100%;opacity:0;transform:scale(.62)}}}}''')
        css.append(f'''@keyframes st{i}{{0%,{pct(t1-0.01)}{{fill:var(--szew)}}{pct(t1)},{pct(DOWN+0.3)}{{fill:var(--zloto)}}{pct(DOWN+0.45)},100%{{fill:var(--szew)}}}}''')
    # torba podskakuje przy każdym lądowaniu
    bumps = ['0%{transform:none}']
    for t in LAND:
        bumps += [f'{pct(t-0.02)}{{transform:none}}', f'{pct(t+0.06)}{{transform:scaleY(.93) scaleX(1.03)}}', f'{pct(t+0.2)}{{transform:none}}']
    bumps += [f'{pct(POP-0.05)}{{transform:none}}', f'{pct(POP+0.08)}{{transform:scaleY(.88) scaleX(1.05)}}', f'{pct(POP+0.28)}{{transform:none}}', '100%{transform:none}']
    css.append('@keyframes bump{' + ''.join(bumps) + '}')
    css.append(f'''@keyframes pop{{0%,{pct(POP)}{{transform:translateY(58px) scaleY(1)}}
{pct(POP+0.16)}{{transform:translateY(-9px) scaleY(1.08)}}
{pct(POP+0.32)}{{transform:translateY(2px) scaleY(.96)}}
{pct(POP+0.46)},{pct(DOWN)}{{transform:translateY(0) scaleY(1)}}
{pct(DOWN+0.35)},100%{{transform:translateY(58px)}}}}''')
    css.append(f'''@keyframes hat{{0%,{pct(POP+0.5)}{{transform:rotate(0)}}{pct(POP+0.62)}{{transform:rotate(-9deg)}}{pct(POP+0.78)}{{transform:rotate(5deg)}}{pct(POP+0.92)},100%{{transform:rotate(0)}}}}''')
    css.append(f'''@keyframes ears{{0%,{pct(POP+1.2)}{{transform:rotate(0)}}{pct(POP+1.3)}{{transform:rotate(-12deg)}}{pct(POP+1.42)}{{transform:rotate(6deg)}}{pct(POP+1.55)},100%{{transform:rotate(0)}}}}''')
    css.append(f'''@keyframes bubble{{0%,{pct(POP+0.45)}{{opacity:0;transform:translateY(8px) scale(.8)}}{pct(POP+0.65)},{pct(DOWN-0.1)}{{opacity:1;transform:none}}{pct(DOWN+0.1)},100%{{opacity:0;transform:translateY(6px) scale(.9)}}}}''')
    css.append(f'''@keyframes head{{0%{{left:0%}}100%{{left:100%}}}}''')
    # bloki na osi czasu zapalają się przy lądowaniu
    for i, t in enumerate(LAND):
        css.append(f'@keyframes tl{i}{{0%,{pct(t-0.01)}{{opacity:.28}}{pct(t)},{pct(DOWN+0.3)}{{opacity:1}}{pct(DOWN+0.45)},100%{{opacity:.28}}}}')
    return '\n'.join(css)

def joey_svg(joey_col='#10251F'):
    s = 3.1; tx = 300 - 64 * s; ty = 414 - 120 * s
    e1 = mark.ellipse_path(*mark.EAR1); e2 = mark.ellipse_path(*mark.EAR2)
    tri = mark.rtri(mark.TRI, mark.TRIR)
    hat = ('<g class="hat"><path d="M41 31 C41 17 69 15 72 30 Z" fill="#F2B544"/>'
           '<rect x="35" y="28.6" width="42" height="5" rx="2.5" fill="#F2B544"/>'
           '<path d="M55.5 17.6 C57 21 57.6 25 57.4 29" stroke="#10251F" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".55"/></g>')
    joey = (f'<g class="joey"><g class="ears"><path d="{e1}{e2}" fill="{joey_col}"/></g>'
            f'<path d="{tri}" fill="{joey_col}"/>{hat}</g>')
    pouch = mark.pouch()
    dashes = ''.join(f'<rect class="st st{i}" x="{27 + i*12.6:.1f}" y="73.4" width="7.4" height="3.6" rx="1.8"/>' for i in range(N))
    back = (f'<svg class="layer back" viewBox="0 0 600 420" aria-hidden="true"><defs><clipPath id="jc"><rect x="0" y="-60" width="128" height="126"/></clipPath></defs>'
            f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s})"><g clip-path="url(#jc)">{joey}</g></g></svg>')
    front = (f'<svg class="layer front" viewBox="0 0 600 420" aria-hidden="true"><g transform="translate({tx:.1f} {ty:.1f}) scale({s})">'
             f'<g class="pouch"><path d="{pouch}" fill="#E2642A"/>{dashes}</g></g></svg>')
    return back, front

T = {
 'en': dict(lang='en', pre='', other='pl/', other_label='PL', title='Montaroo · coming soon',
            desc='Montaroo, the automatic travel film editor for Windows, is launching soon. Offline, on your PC.',
            pile='1,434 clips', bubble='Almost cut!', k='Coming soon', h='Our joey is still in the edit.',
            p='Montaroo turns the clips from your trip into a film with chapters, music and a story. Offline, on your Windows PC. Launching soon.',
            status='Rendering montaroo.com', note='The last 2% always take the longest.', tagline='Hop from footage to film.', legal='<a href="/privacy/">Privacy</a> · <a href="/eula/">EULA</a>'),
 'pl': dict(lang='pl', pre='../', other='../', other_label='EN', title='Montaroo · już wkrótce',
            desc='Montaroo, automatyczny montaż filmów z podróży na Windows, startuje wkrótce. Offline, na twoim komputerze.',
            pile='1 434 nagrania', bubble='Prawie zmontowane!', k='Już wkrótce', h='Joey jeszcze montuje.',
            p='Montaroo zamienia nagrania z wyjazdu w film z rozdziałami, muzyką i historią. Offline, na twoim komputerze z Windows. Startujemy wkrótce.',
            status='Montujemy montaroo.com', note='Ostatnie 2% zawsze trwa najdłużej.', tagline='Od nagrań do filmu jednym skokiem.', legal='<a href="/pl/prywatnosc/">Prywatność</a> · <a href="/pl/licencja/">Licencja</a>'),
}

CSS_BASE = r'''
@font-face{font-family:Gabarito;font-weight:800;font-display:swap;src:url(PRE/assets/fonts/gabarito-latin-800-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F,U+2212}
@font-face{font-family:Gabarito;font-weight:800;font-display:swap;src:url(PRE/assets/fonts/gabarito-latin-ext-800-normal.woff2) format("woff2");unicode-range:U+0100-024F}
@font-face{font-family:Inter;font-weight:400;font-display:swap;src:url(PRE/assets/fonts/inter-latin-400-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F,U+2212}
@font-face{font-family:Inter;font-weight:400;font-display:swap;src:url(PRE/assets/fonts/inter-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+0100-024F}
@font-face{font-family:Inter;font-weight:600;font-display:swap;src:url(PRE/assets/fonts/inter-latin-600-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F,U+2212}
@font-face{font-family:Inter;font-weight:600;font-display:swap;src:url(PRE/assets/fonts/inter-latin-ext-600-normal.woff2) format("woff2");unicode-range:U+0100-024F}
:root{--noc:#10251F;--ochra:#E2642A;--zloto:#F2B544;--euk:#3E7C68;--piasek:#F4E9D6;--karta:#FBF6EC;--cichy:#3E5A50;--akcent:#B4471A;--szew:#F4E9D6;--loop:LOOPs}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{background:var(--piasek);color:var(--noc);font:400 16px/1.6 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;min-height:100vh;overflow-x:hidden}
a{color:var(--noc)}
:focus-visible{outline:3px solid var(--zloto);outline-offset:3px;border-radius:4px}
.top{display:flex;justify-content:space-between;align-items:center;padding:22px clamp(20px,5vw,56px)}
.top .logo{height:32px;width:auto;display:block}
.lang{font:600 14px/1 Inter,sans-serif;text-decoration:none;padding:12px 14px;border-radius:8px;box-shadow:inset 0 0 0 1px #10251f24}
.lang:hover{background:var(--karta)}
main{flex:1;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:center;gap:clamp(24px,5vw,72px);max-width:1240px;width:100%;margin:0 auto;padding:12px clamp(20px,5vw,56px) 40px}
.k{font:600 13px/16px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--akcent);margin:0 0 18px}
h1{font:800 clamp(44px,6vw,84px)/.93 Gabarito,"Arial Rounded MT Bold",sans-serif;letter-spacing:-.045em;margin:0 0 24px}
.lead{font-size:clamp(17px,1.5vw,19px);line-height:1.55;max-width:31em;margin:0 0 30px}
.status{max-width:420px}
.status-row{display:flex;justify-content:space-between;font:600 14px/1 Inter,sans-serif;margin-bottom:10px;gap:12px}
.status-row .tc{font-variant-numeric:tabular-nums;color:var(--cichy);font-weight:400}
.bar{height:10px;border-radius:99px;background:#10251f14;overflow:hidden}
.bar i{display:block;height:100%;width:0;background:var(--ochra);border-radius:99px}
.note{font-size:14px;color:var(--cichy);margin:10px 0 0}
.stagewrap{position:relative;width:100%;max-width:600px;justify-self:center}
.stage{position:relative;width:600px;height:420px;transform-origin:0 0;transform:scale(var(--s,1))}
.sizer{width:100%;aspect-ratio:600/420}
.stagewrap .stage{position:absolute;left:0;top:0}
.layer{position:absolute;inset:0;width:600px;height:420px;overflow:visible}
.front{z-index:3}.back{z-index:1}
.joey{transform-box:view-box;transform-origin:64px 64px;animation:pop var(--loop) infinite}
.hat{transform-box:fill-box;transform-origin:20% 100%;animation:hat var(--loop) infinite}
.ears{transform-box:fill-box;transform-origin:50% 100%;animation:ears var(--loop) infinite}
.pouch{transform-box:fill-box;transform-origin:50% 0;animation:bump var(--loop) infinite}
.st{fill:var(--szew)}
.pile{position:absolute;left:8px;top:118px;width:128px;height:72px;z-index:0}
.pile span{position:absolute;inset:0;border-radius:10px;background:var(--noc);box-shadow:0 0 0 3px var(--piasek)}
.pile span:nth-child(1){transform:translate(-8px,10px) rotate(-9deg);opacity:.35}
.pile span:nth-child(2){transform:translate(-4px,5px) rotate(-4deg);opacity:.6}
.pile span:nth-child(3){background:var(--noc) url(PRE/assets/img/soon/c_mv.jpg) center/cover}
.pile b{position:absolute;left:0;right:0;top:calc(100% + 18px);text-align:center;font:600 13px/1.2 Inter,sans-serif;color:var(--cichy)}
.clip{position:absolute;left:0;top:0;width:128px;height:72px;border-radius:10px;background:var(--noc) center/cover;box-shadow:0 0 0 3px var(--piasek),0 10px 22px -12px #10251f99;z-index:2;
 offset-path:path("M72 154 C 150 -70, 280 -40, 300 300");offset-rotate:0deg;offset-anchor:50% 50%;opacity:0}
.bubble{position:absolute;left:404px;top:58px;z-index:4;background:var(--noc);color:var(--piasek);font:600 15px/1 Inter,sans-serif;padding:12px 14px;border-radius:14px 14px 14px 4px;white-space:nowrap;animation:bubble var(--loop) infinite;opacity:0}
.timeline{position:relative;margin:6px 34px 0;height:46px;z-index:5}
.track{position:absolute;left:0;right:0;top:8px;height:26px;display:flex;gap:4px}
.track span{flex:1;border-radius:6px;background:var(--euk);opacity:.28}
.track span:nth-child(odd){background:var(--ochra)}
.ticks{position:absolute;left:0;right:0;top:38px;height:6px;background:repeating-linear-gradient(90deg,#10251f55 0 2px,transparent 2px 25%)}
.ph{position:absolute;top:0;bottom:0;left:0;width:0;z-index:2;animation:head var(--loop) linear infinite}
.ph::before{content:"";position:absolute;left:-1px;top:0;bottom:0;width:2px;background:var(--noc)}
.ph::after{content:"";position:absolute;left:-7px;top:-6px;width:14px;height:10px;background:var(--noc);clip-path:polygon(0 0,100% 0,50% 100%)}
footer{padding:20px clamp(20px,5vw,56px) 28px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:14px;color:var(--cichy)}
footer b{font:800 16px/1.2 Gabarito,sans-serif;color:var(--noc)}
footer a{color:var(--cichy);text-underline-offset:3px}footer a:hover{color:var(--noc)}
@media (max-width:860px){
 main{grid-template-columns:1fr;padding-top:0}
 .stagewrap{order:-1;max-width:520px}
 .text{text-align:center}
 .lead{margin-left:auto;margin-right:auto}
 .status{max-width:440px;margin:0 auto}
 .note{text-align:center}
 footer{flex-direction:column;align-items:center;text-align:center;gap:6px}
 .top{padding-bottom:6px}
}
@media (prefers-reduced-motion:reduce){
 .joey,.hat,.ears,.pouch,.clip,.bubble,.ph,.track span,.st{animation:none!important}
 .joey{transform:none}.bubble{opacity:1}.clip{display:none}.st{fill:var(--zloto)}.track span{opacity:1}
}
'''

def page(L, V=None):
    V = V or {}
    L = {**L, **V.get('text', {})}
    pre = L['pre']
    logo = open(os.path.join(ROOT, 'brand', 'logo', 'svg', f"montaroo-poziome-{V.get('logo','kolor')}.svg"), encoding='utf-8').read()
    import re
    logo = re.sub(r'<title>.*?</title>', '', logo).replace('<svg ', '<svg class="logo" role="img" aria-label="montaroo" ', 1)
    back, front = joey_svg(V.get('joey', '#10251F'))
    clips = ''.join(f'<div class="clip" style="background-image:url({pre}assets/img/soon/c_{c}.jpg);animation:clip{i} var(--loop) infinite"></div>' for i, c in enumerate(CLIPS))
    track = ''.join(f'<span style="animation:tl{i} var(--loop) infinite"></span>' for i in range(N))
    css = CSS_BASE.replace('PRE/', pre).replace('LOOPs', f'{LOOP}s') + keyframes()
    css += '\n' + '\n'.join(f'.st{i}{{animation:st{i} var(--loop) infinite}}' for i in range(N)) + '\n' + V.get('css', '').replace('PRE/', pre)
    return f'''<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{L['title']}</title>
<meta name="description" content="{L['desc']}">
<link rel="alternate" hreflang="en" href="https://montaroo.com/">
<link rel="alternate" hreflang="pl" href="https://montaroo.com/pl/">
<meta property="og:title" content="{L['title']}">
<meta property="og:description" content="{L['desc']}">
<meta property="og:image" content="https://montaroo.com/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F4E9D6">
<link rel="icon" href="{pre}favicon.ico" sizes="any">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/gabarito-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{css}</style>
</head>
<body>
<header class="top"><a href="./" aria-label="montaroo">{logo}</a><a class="lang" href="{L['other']}" hreflang="{'pl' if L['lang']=='en' else 'en'}">{L['other_label']}</a></header>{V.get('after_header','')}
<main>
 <div class="stagewrap" aria-hidden="true">
  <div class="sizer"></div>
  <div class="stage">
   <div class="pile"><span></span><span></span><span></span><b>{L['pile']}</b></div>
   {V.get('decor_back','')}{back}{clips}{front}{V.get('decor','')}
   <div class="bubble">{L['bubble']}</div>
  </div>
  <div class="timeline"><div class="track">{track}</div><div class="ticks"></div><div class="ph"></div></div>
 </div>
 <div class="text">
  <p class="k">{L['k']}</p>
  <h1>{L['h']}</h1>
  <p class="lead">{L['p']}</p>
  <div class="status" role="status">
   <div class="status-row"><span>{L['status']}…</span><span><span class="tc" id="tc">00:00:00:00</span> · <b id="pc">0%</b></span></div>
   <div class="bar"><i id="bar"></i></div>
   <p class="note">{L['note']}</p>
  </div>
 </div>
</main>
<footer><b>{L['tagline']}</b><span>© 2026 Montaroo · {L.get('legal','')}</span></footer>
<script>
(()=>{{
 const w=document.querySelector('.stagewrap'),st=document.querySelector('.stage');
 const fit=()=>st.style.setProperty('--s',w.clientWidth/600);fit();addEventListener('resize',fit);
 const t0=performance.now(),tc=document.getElementById('tc'),pc=document.getElementById('pc'),bar=document.getElementById('bar');
 const p2=n=>String(n).padStart(2,'0');
 const tick=()=>{{const s=(performance.now()-t0)/1000,f=Math.floor(s*25)%25,sec=Math.floor(s);
  tc.textContent=p2(Math.floor(sec/3600))+':'+p2(Math.floor(sec/60)%60)+':'+p2(sec%60)+':'+p2(f);
  const p=Math.min(98,Math.round(98*(1-Math.exp(-s/6))));pc.textContent=p+'%';bar.style.width=p+'%';
  requestAnimationFrame(tick)}};
 if(!matchMedia('(prefers-reduced-motion: reduce)').matches)tick();else{{pc.textContent='98%';bar.style.width='98%'}}
}})();
</script>
</body>
</html>
'''

if __name__ == '__main__':
  for k in ('en', 'pl'):
    out = os.path.join(ROOT, 'index.html' if k == 'en' else 'pl/index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page(T[k]))
    print('ok', out)
