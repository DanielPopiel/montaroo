# -*- coding: utf-8 -*-
"""Trzy odmiany strony W1 („Torba”) + PREZENTACJA do obejrzenia lokalnie.
  warianty/w1a/  Taśma   – klipy jadą taśmą filmową i wpadają do torby, układ wyśrodkowany
  warianty/w1b/  Noc     – ciemna wersja, joey w piasku, przy każdym lądowaniu fala w rytm
  warianty/w1c/  Budowa  – żuraw wieżowy przenosi klipy do torby, taśma ostrzegawcza
Plus PREZENTACJA_w_budowie.html – jeden plik ze wszystkimi wersjami (fonty i obrazki w środku),
który otwiera się bez internetu.
Uruchom:  python _zrodlo/build_w1_warianty.py
"""
import os, re, base64, html as H
import build_soon as B

ROOT = B.ROOT
L_EN = dict(B.T['en'], pre='../../', other='../../pl/')

def rings_css(color):
    out = []
    for i, t in enumerate(B.LAND):
        out.append(f'@keyframes rg{i}{{0%,{B.pct(t-0.01)}{{opacity:0;transform:scale(.2)}}{B.pct(t)}{{opacity:.9;transform:scale(.3)}}{B.pct(t+0.55)},100%{{opacity:0;transform:scale(1.6)}}}}')
        out.append(f'.ring:nth-child({i+1}){{animation:rg{i} var(--loop) infinite}}')
    return '\n'.join(out) + f'\n.rings{{position:absolute;left:150px;top:180px;width:300px;height:300px;z-index:0}}.ring{{position:absolute;inset:0;border-radius:50%;border:3px solid {color};opacity:0}}'

V = {
 'w1a': dict(
   name='W1a · Taśma',
   decor_back='<div class="belt"><i></i></div><div class="roller"></div>',
   css='''
main{grid-template-columns:1fr;max-width:860px;text-align:center;justify-items:center;padding-top:0}
.stagewrap{order:-1;max-width:600px}
.lead{margin-left:auto;margin-right:auto}
.status{width:100%;max-width:460px;margin:0 auto;text-align:left}
.pile{display:none}
.clip{offset-path:path("M-170 188 L190 188 Q 282 188 300 300")}
.belt{position:absolute;left:-210px;top:226px;width:440px;height:34px;border-radius:6px;background:var(--noc);overflow:hidden;z-index:1}
.belt i{position:absolute;inset:7px 0;background:repeating-linear-gradient(90deg,var(--piasek) 0 10px,transparent 10px 26px);-webkit-mask:linear-gradient(#000 0 6px,transparent 6px 14px,#000 14px);mask:linear-gradient(#000 0 6px,transparent 6px 14px,#000 14px);animation:belt .58s linear infinite}
@keyframes belt{to{transform:translateX(26px)}}
.roller{position:absolute;left:214px;top:222px;width:42px;height:42px;border-radius:50%;background:var(--euk);box-shadow:inset 0 0 0 10px var(--noc);z-index:1;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@media (max-width:860px){.stagewrap{max-width:520px}}
'''),
 'w1b': dict(
   name='W1b · Noc', logo='kolor-ciemne', joey='#F4E9D6',
   decor_back='<div class="rings">' + '<i class="ring"></i>' * len(B.CLIPS) + '</div>',
   text=dict(h='Joey’s still<br>in the edit.'),
   css='''
:root{--szew:#10251F}
body{background:var(--noc);color:var(--piasek)}
a{color:var(--piasek)}
.k{color:var(--zloto)}
.lead,.note,.status-row .tc,footer{color:#CFC4AE}
footer b{color:var(--piasek)}
.lang{box-shadow:inset 0 0 0 1px #f4e9d62e}.lang:hover{background:#183730}
.bar{background:#f4e9d61a}
.pile span{background:#183730;box-shadow:0 0 0 3px var(--noc)}
.pile span:nth-child(3){background:#183730 url(PRE/assets/img/soon/c_mv.jpg) center/cover}
.pile b{color:#CFC4AE}
.clip{box-shadow:0 0 0 3px var(--noc),0 10px 26px -10px #000}
.bubble{background:var(--zloto);color:var(--noc)}
.ticks{background:repeating-linear-gradient(90deg,#f4e9d655 0 2px,transparent 2px 25%)}
.ph::before{background:var(--zloto)}.ph::after{background:var(--zloto)}
''' + rings_css('#F2B544')),
 'w1c': dict(
   name='W1c · Budowa',
   after_header='<div class="tape" aria-hidden="true"><span>UNDER CONSTRUCTION · CUTTING IN PROGRESS · UNDER CONSTRUCTION · CUTTING IN PROGRESS · UNDER CONSTRUCTION · CUTTING IN PROGRESS · </span></div>',
   decor_back=('<div class="crane" aria-hidden="true"><div class="mast"></div><div class="jib"></div><div class="cjib"></div>'
               '<div class="weight"></div><div class="cab"></div><div class="peak"></div></div>'),
   decor='<div class="sky"></div>',
   text=dict(k='Under construction', h='Joey’s building<br>your next film.'),
   css='''
.tape{overflow:hidden;background:repeating-linear-gradient(-45deg,var(--zloto) 0 22px,var(--noc) 22px 44px);height:34px;display:flex;align-items:center}
.tape span{white-space:nowrap;font:800 14px/1 Gabarito,sans-serif;letter-spacing:.12em;color:var(--noc);background:var(--zloto);padding:5px 12px;margin-left:24px;animation:tape 18s linear infinite}
@keyframes tape{to{transform:translateX(-50%)}}
.pile{left:16px;top:318px;width:110px;height:62px}
.clip{offset-path:path("M70 349 L70 92 L300 92 L300 300")}
.clip::before{content:"";position:absolute;left:50%;bottom:100%;width:2px;height:460px;margin-left:-1px;background:var(--noc)}
.clip::after{content:"";position:absolute;left:50%;top:-12px;width:14px;height:12px;margin-left:-7px;border:3px solid var(--zloto);border-top:0;border-radius:0 0 8px 8px}
.stage{overflow:hidden}
.sky{position:absolute;left:0;right:0;top:0;height:52px;background:var(--piasek);z-index:2;pointer-events:none}
.crane{position:absolute;inset:0;z-index:3;pointer-events:none}
.mast{position:absolute;left:520px;top:40px;width:22px;height:380px;background:repeating-linear-gradient(45deg,transparent 0 9px,var(--noc) 9px 12px),repeating-linear-gradient(-45deg,transparent 0 9px,var(--noc) 9px 12px);box-shadow:inset 3px 0 var(--noc),inset -3px 0 var(--noc)}
.jib{position:absolute;left:30px;top:40px;width:512px;height:14px;background:repeating-linear-gradient(45deg,transparent 0 8px,var(--noc) 8px 11px);box-shadow:inset 0 3px var(--noc),inset 0 -3px var(--noc)}
.cjib{position:absolute;left:542px;top:40px;width:54px;height:14px;background:var(--noc)}
.weight{position:absolute;left:566px;top:54px;width:30px;height:30px;background:var(--euk)}
.cab{position:absolute;left:498px;top:54px;width:26px;height:24px;background:var(--zloto);border-radius:3px;box-shadow:inset 0 0 0 3px var(--noc)}
.peak{position:absolute;left:520px;top:6px;width:22px;height:34px;background:var(--noc);clip-path:polygon(50% 0,100% 100%,0 100%)}
.stagewrap{margin-top:30px}
.track span{background:repeating-linear-gradient(-45deg,var(--zloto) 0 8px,var(--noc) 8px 16px);opacity:.25}
.track span:nth-child(odd){background:repeating-linear-gradient(-45deg,var(--zloto) 0 8px,var(--noc) 8px 16px)}
'''),
}

def inline(html, base_dir):
    """Wstawia fonty, obrazki i favicon do HTML jako data: – plik działa sam, bez internetu."""
    def rep(m):
        rel = m.group(2)
        path = os.path.normpath(os.path.join(base_dir, rel))
        if not os.path.exists(path):
            return m.group(0)
        ext = rel.rsplit('.', 1)[-1].lower()
        mime = {'woff2': 'font/woff2', 'jpg': 'image/jpeg', 'png': 'image/png', 'svg': 'image/svg+xml', 'ico': 'image/x-icon'}.get(ext, 'application/octet-stream')
        data = base64.b64encode(open(path, 'rb').read()).decode()
        return f'{m.group(1)}data:{mime};base64,{data}{m.group(3)}'
    html = re.sub(r'(url\()([^)]+?\.(?:woff2|jpg|png|svg))(\))', rep, html)
    html = re.sub(r'(href=")([^"]+?\.(?:ico|svg|png))(")', rep, html)
    html = re.sub(r'<link rel="preload"[^>]*>', '', html)
    return html

if __name__ == '__main__':
    pages = []
    # W1 – obecna wersja (z katalogu głównego)
    w1 = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    pages.append(('W1 · Torba (obecna)', inline(w1, ROOT)))
    for key, v in V.items():
        out = os.path.join(ROOT, 'warianty', key, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        page = B.page(L_EN, v).replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
        open(out, 'w', encoding='utf-8').write(page)
        pages.append((v['name'], inline(page, os.path.dirname(out))))
        print('ok', out)
    tabs = ''.join(f'<button data-i="{i}"{" class=on" if i == 0 else ""}>{H.escape(n)}</button>' for i, (n, _) in enumerate(pages))
    frames = ''.join(f'<iframe data-i="{i}" title="{H.escape(n)}"{"" if i == 0 else " hidden"} srcdoc="{H.escape(p, quote=True)}"></iframe>' for i, (n, p) in enumerate(pages))
    pres = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Montaroo – PREZENTACJA strony „w budowie”</title>
<style>html,body{{margin:0;height:100%;background:#10251F;font:600 14px/1 system-ui,sans-serif}}
nav{{display:flex;gap:6px;padding:10px;align-items:center;flex-wrap:wrap}}nav b{{color:#F4E9D6;margin-right:10px;font-size:15px}}
nav button{{font:inherit;border:0;border-radius:99px;padding:10px 14px;background:#183730;color:#F4E9D6;cursor:pointer}}
nav button.on{{background:#E2642A;color:#10251F}}
nav label{{margin-left:auto;color:#CFC4AE;display:flex;gap:6px;align-items:center}}
.wrap{{height:calc(100% - 58px);display:flex;justify-content:center;background:#0b1a16}}
iframe{{border:0;width:100%;height:100%;background:#fff;transition:width .3s}}
.mob iframe{{width:390px;border-left:1px solid #333;border-right:1px solid #333}}</style></head>
<body><nav><b>montaroo · w budowie</b>{tabs}<label><input type="checkbox" id="m"> widok telefonu</label></nav><div class="wrap" id="w">{frames}</div>
<script>
const bs=[...document.querySelectorAll('nav button')],fs=[...document.querySelectorAll('iframe')];
bs.forEach(b=>b.onclick=()=>{{bs.forEach(x=>x.classList.toggle('on',x===b));fs.forEach(f=>f.hidden=f.dataset.i!==b.dataset.i)}});
document.getElementById('m').onchange=e=>document.getElementById('w').classList.toggle('mob',e.target.checked);
</script></body></html>'''
    out = os.path.join(ROOT, 'warianty', 'PREZENTACJA_w_budowie.html')
    open(out, 'w', encoding='utf-8').write(pres)
    print('ok', out, os.path.getsize(out) // 1024, 'KB')
