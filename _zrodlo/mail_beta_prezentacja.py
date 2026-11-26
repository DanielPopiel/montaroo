"""PREZENTACJA_mail_beta.html – wszystkie warianty w zakładkach, obrazy wbudowane. Uruchom po mail_beta.py."""
import json, base64, html as H, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
prev = json.load(open('/tmp/mail_prev.json'))
b64 = lambda f, mt: f'data:{mt};base64,' + base64.b64encode(open(f, 'rb').read()).decode()
img = {f: b64(f'assets/mail/{f}', 'image/gif' if f.endswith('gif') else 'image/jpeg') for f in os.listdir('assets/mail')}
logo = b64('brand/logo/png/montaroo-poziome-kolor-ciemne.png', 'image/png')
docs = []
for n, p, h in prev:
    for k, v in img.items(): h = h.replace('__IMG__' + k, v)
    docs.append((n, p, h.replace('https://montaroo.com/brand/logo/png/montaroo-poziome-kolor-ciemne.png', logo)))
gab = base64.b64encode(open('assets/fonts/gabarito-latin-ext-800-normal.woff2', 'rb').read()).decode()
tabs = ''.join(f'<button class="t{" on" if i==0 else ""}" data-i="{i}"><b>{i+1}</b>{H.escape(n)}</button>' for i, (n, _, _) in enumerate(docs))
page = f'''<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Montaroo – mail powitalny, {len(docs)} wersji</title>
<style>@font-face{{font-family:G;src:url(data:font/woff2;base64,{gab})}}
*{{box-sizing:border-box}}body{{margin:0;background:#10251F;color:#F4E9D6;font:15px/1.5 Inter,Segoe UI,system-ui,sans-serif}}
header{{padding:28px 24px 10px;max-width:1100px;margin:auto}}h1{{font:800 32px/1.1 G,sans-serif;margin:0 0 6px}}header p{{margin:0;color:#F4E9D6b0}}
nav{{display:flex;gap:8px;flex-wrap:wrap;padding:16px 24px;max-width:1100px;margin:auto}}
.t{{font:inherit;color:#F4E9D6;background:#ffffff10;border:1px solid #ffffff22;border-radius:999px;padding:9px 16px;cursor:pointer}}.t b{{color:#F2B544;margin-right:8px}}.t.on{{background:#E2642A;border-color:#E2642A;color:#10251F}}.t.on b{{color:#10251F}}
.meta{{max-width:1100px;margin:4px auto 0;padding:0 24px}}.inbox{{background:#FFFBF4;color:#10251F;border-radius:12px;padding:12px 16px;max-width:600px}}.inbox small{{color:#6a7a75}}
.view{{display:flex;gap:28px;justify-content:center;flex-wrap:wrap;padding:20px 24px 50px}}.view figure{{margin:0}}.view figcaption{{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#F2B544;margin-bottom:8px}}
iframe{{border:0;border-radius:18px;background:#F4E9D6;display:block}}.ph{{width:390px;height:820px;border:10px solid #000;border-radius:38px}}.dk{{width:660px;height:820px}}
@media(max-width:1120px){{.view figure:last-child{{display:none}}}}@media(max-width:440px){{.ph{{width:100%;border-width:6px}}.view{{padding:16px 8px}}}}</style></head><body>
<header><h1>Mail powitalny – {len(docs)} wersji</h1><p>Grafiki z prawdziwych kadrów filmu z USA, zrobione w kodzie (0 kredytów). Każda wersja prosi o odpowiedź – zgłoszenie testera trafia prosto do skrzynki.</p></header>
<nav>{tabs}</nav><div class="meta"><div class="inbox"><b>Montaroo</b> <small>· hello@montaroo.com</small><br><span id="sub"></span></div></div>
<div class="view"><figure><figcaption>Telefon</figcaption><iframe class="ph" id="a"></iframe></figure><figure><figcaption>Komputer</figcaption><iframe class="dk" id="b"></iframe></figure></div>
<script>const D={json.dumps([[n,p,h] for n,p,h in docs], ensure_ascii=False)};
function show(i){{document.querySelectorAll('.t').forEach((b,j)=>b.classList.toggle('on',i==j));a.srcdoc=b.srcdoc=D[i][2];sub.textContent=D[i][1];}}
document.querySelectorAll('.t').forEach(b=>b.onclick=()=>show(+b.dataset.i));show({len(docs)-5});</script></body></html>'''
open('kampania/mail-beta/PREZENTACJA_mail_beta.html', 'w', encoding='utf-8').write(page)
print(os.path.getsize('kampania/mail-beta/PREZENTACJA_mail_beta.html')//1024, 'KB')
