"""Mail powitalny EN = wariant 11 po angielsku (play + 3 punkty + rozdziały + prośba o testerów).
Grafiki: assets/mail/m9-play-en.jpg, m7-rozdzialy-en.jpg (z klatek filmu w <katalog_z_klatkami>, domyślnie /tmp).
Wyjście: kampania/mail-beta/mail_beta_en_11.html.   python _zrodlo/mail_beta_en.py [katalog_z_klatkami] [--bez-grafik]"""
import os, sys, html as H
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_IMG = f'{R}/assets/mail'; OUT = f'{R}/kampania/mail-beta'
K = next((a for a in sys.argv[1:] if not a.startswith('--')), '/tmp')
F = 'font-family:Inter,Segoe UI,Helvetica,Arial,sans-serif;'
URL = 'https://montaroo.com/'
MAILTO = 'mailto:hello@montaroo.com?subject=Montaroo%20beta%20%E2%80%93%20I%20want%20to%20test%20it'
P = lambda t, mb=14: f'<p style="margin:0 0 {mb}px;font-size:16px;line-height:26px;">{t}</p>'


def grafiki():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    FONTS = f'file://{R}/assets/fonts'
    BASE = f"""<meta charset="utf-8"><style>
@font-face{{font-family:G;src:url({FONTS}/gabarito-latin-800-normal.woff2)}}
@font-face{{font-family:I;font-weight:600;src:url({FONTS}/inter-latin-600-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;font-family:I,sans-serif;background:#10251F}}</style>"""
    def frame(f, lab, n):
        return f'<div style="flex:1;position:relative"><img src="file://{K}/{f}" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:6px"><div style="font:600 17px I;letter-spacing:.16em;color:#F2B544;margin-top:14px">CHAPTER {n}</div><div style="font:800 30px G;color:#F4E9D6">{lab}</div></div>'
    holes = '<div style="height:26px;background:repeating-linear-gradient(90deg,transparent 0 18px,#F4E9D6 18px 36px,transparent 36px 54px);opacity:.25;border-radius:4px"></div>'
    M7 = f"""<div style="height:500px;padding:40px 50px"><div style="background:#0a1814;border-radius:18px;padding:22px 28px">{holes}
<div style="display:flex;gap:24px;margin:22px 0">{frame('g3.8.jpg','On the road',1)}{frame('g7.2.jpg','Grand Canyon',2)}{frame('f16.jpg','Monument Valley',3)}</div>{holes}</div>
<div style="font:600 21px I;color:#F4E9D6b0;margin-top:22px">Chapters from a real film Montaroo put together. It added the title cards itself.</div></div>"""
    M9 = f"""<div style="position:relative;height:675px;overflow:hidden"><img src="file://{K}/f16.jpg" style="width:1200px;display:block;filter:brightness(.82)">
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><div style="width:170px;height:170px;border-radius:50%;background:#E2642A;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 50px #0008"><svg width="70" height="70" viewBox="0 0 24 24"><path d="M7 4v16l14-8z" fill="#10251F"/></svg></div></div>
<div style="position:absolute;right:34px;bottom:34px;background:#10251FE6;color:#F4E9D6;font:600 24px I;padding:10px 18px;border-radius:10px">▶ 0:20 · edited by Montaroo</div></div>"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for html, h, name in ((M7, 500, 'm7-rozdzialy-en'), (M9, 675, 'm9-play-en')):
            pg.set_viewport_size({'width': 1200, 'height': h}); tmp = f'{OUT_IMG}/_tmp.html'
            open(tmp, 'w', encoding='utf-8').write(BASE + html); pg.goto('file://' + tmp); pg.wait_for_timeout(700); os.remove(tmp)
            pg.screenshot(path=f'{OUT_IMG}/{name}.png')
            Image.open(f'{OUT_IMG}/{name}.png').convert('RGB').save(f'{OUT_IMG}/{name}.jpg', quality=84, optimize=True); os.remove(f'{OUT_IMG}/{name}.png')
        b.close()


def mail(base):
    kroki = [(1, 'picked the best shots from the whole folder,'), (2, 'cut them to the beat of the music,'),
             (3, 'split the trip into chapters and added title cards with place names.')]
    body = (f'<p style="margin:0 0 14px;font-size:16px;line-height:26px;"><a href="{URL}" style="color:#E2642A;font-weight:700;">▶ Watch the 20 seconds on montaroo.com</a></p>'
        + P('It’s a clip from our USA road trip film. Montaroo did it all by itself:')
        + '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 14px;">'
        + ''.join(f'<tr><td valign="top" style="padding:0 12px 10px 0;"><span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:#E2642A;color:#10251F;font:700 14px/26px Inter,Arial,sans-serif;text-align:center;">{n}</span></td><td style="padding:2px 0 10px;{F}font-size:16px;line-height:24px;color:#10251F;">{t}</td></tr>' for n, t in kroki)
        + '</table>'
        + f'<img src="{base}m7-rozdzialy-en.jpg" width="520" alt="Film chapters: On the road, Grand Canyon, Monument Valley" style="display:block;width:100%;max-width:520px;height:auto;border:0;border-radius:10px;margin:0 0 18px;">'
        + P('Now I want to see how it tells the story of <strong>your</strong> trip. I’m looking for the first testers.', 18))
    ask = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4E9D6;border-radius:12px;margin:8px 0 22px;"><tr><td style="padding:18px 20px;{F}font-size:15px;line-height:23px;color:#10251F;">
<strong>What I need from a tester:</strong><br>• a Windows PC<br>• a folder of clips from a trip (phone, GoPro, DJI, whatever you have)<br>• about 15 minutes for a short survey after your first film
</td></tr></table>
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:#E2642A;border-radius:999px;">
<a href="{MAILTO}" style="display:inline-block;padding:14px 28px;{F}font-size:16px;font-weight:700;color:#FFFBF4;text-decoration:none;">I want a film like this from my trip</a></td></tr></table>
<p style="margin:12px 0 0;font-size:13px;line-height:20px;color:#5b6b66;">Or just reply to this email. It comes straight to me.</p>'''
    sig = '<p style="margin:28px 0 0;font-size:15px;line-height:24px;">Daniel<br><span style="color:#3E7C68;">maker of Montaroo, airline pilot</span></p>'
    h1 = 'An app edited this film. I just dropped in the folder.'
    pre = '20 seconds edited by an app. I’m looking for the first testers.'
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only">
<title>{H.escape(h1)}</title><style>body{{margin:0;padding:0;background:#F4E9D6}}a{{color:#E2642A}}@media (max-width:620px){{.wrap{{width:100%!important}}.pad{{padding-left:22px!important;padding-right:22px!important}}h1{{font-size:26px!important;line-height:32px!important}}}}</style></head>
<body style="margin:0;padding:0;background:#F4E9D6;"><div style="display:none;max-height:0;overflow:hidden;opacity:0;">{H.escape(pre)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4E9D6;"><tr><td align="center" style="padding:28px 10px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFBF4;border-radius:14px;overflow:hidden;">
<tr><td style="background:#10251F;padding:24px 40px 20px;" class="pad"><a href="{URL}" style="text-decoration:none;"><img src="https://montaroo.com/brand/logo/png/montaroo-poziome-kolor-ciemne.png" width="170" alt="montaroo" style="display:block;width:170px;height:auto;border:0;"></a></td></tr>
<tr><td style="background:#10251F;padding:0;"><a href="{URL}"><img src="{base}m9-play-en.jpg" width="600" alt="A frame from a Montaroo film with a play button" style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a></td></tr>
<tr><td style="height:6px;background:#E2642A;line-height:6px;font-size:6px;">&nbsp;</td></tr>
<tr><td class="pad" style="padding:34px 40px 36px;{F}color:#10251F;">
<p style="margin:0 0 10px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#3E7C68;font-weight:700;">See the result</p>
<h1 style="margin:0 0 16px;font-size:30px;line-height:36px;font-weight:800;color:#10251F;">{h1}</h1>
{body}{ask}{sig}</td></tr>
<tr><td class="pad" style="background:#10251F;padding:22px 40px;{F}font-size:12px;line-height:19px;color:#F4E9D6;"><strong style="color:#F2B544;">Hop from footage to film.</strong><br>You are getting this email because you joined the waitlist on montaroo.com.<br><a href="{{$unsubscribe}}" style="color:#F2B544;">Unsubscribe</a></td></tr>
</table></td></tr></table></body></html>'''


if __name__ == '__main__':
    if '--bez-grafik' not in sys.argv: grafiki()
    os.makedirs(OUT, exist_ok=True)
    open(f'{OUT}/mail_beta_en_11.html', 'w', encoding='utf-8').write(mail('https://montaroo.com/assets/mail/'))
    open('/tmp/mail_en_local.html', 'w', encoding='utf-8').write(mail(f'file://{OUT_IMG}/'))
    print('ok')
