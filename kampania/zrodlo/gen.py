import subprocess, os
F='/home/claude/mt/brand/fonts/'
CSS=f"""@font-face{{font-family:G;font-weight:800;src:url({F}gabarito-latin-800-normal.woff2)}}@font-face{{font-family:G;font-weight:800;src:url({F}gabarito-latin-ext-800-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:I;font-weight:600;src:url({F}inter-latin-600-normal.woff2)}}@font-face{{font-family:I;font-weight:600;src:url({F}inter-latin-ext-600-normal.woff2);unicode-range:U+0100-024F}}
@font-face{{font-family:I;font-weight:400;src:url({F}inter-latin-400-normal.woff2)}}@font-face{{font-family:I;font-weight:400;src:url({F}inter-latin-ext-400-normal.woff2);unicode-range:U+0100-024F}}
*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1350px;overflow:hidden;font-family:I;color:#10251F;background:#F4E9D6}}
h1{{font:800 112px/.92 G;letter-spacing:-.045em}}.k{{font:600 24px/1 I;letter-spacing:.14em;text-transform:uppercase;color:#B4471A}}
.st{{height:10px;background:repeating-linear-gradient(90deg,#F4E9D6 0 52px,transparent 52px 84px);border-radius:5px}}
.logo{{position:absolute;left:72px;bottom:64px;height:52px}}
"""
P={
'en':[
 ('01-clips', 'st_489.jpg', '<div class="img"></div><div class="pouch"><div class="st"></div></div><div class="t"><p class="k" style="color:#F2B544">From the first film</p><h1 style="color:#F4E9D6">1,434 clips in.<br>One film out.</h1></div>','dark'),
 ('02-pilot', 'st_401.jpg', '<div class="img half"></div><div class="t2"><p class="k">Why Montaroo exists</p><h1 style="font-size:86px">I fly a 737. I came home with 1,434 clips.</h1><p class="b">So I built the editor I wanted. Point it at the folder, pick the songs, get the film.</p></div>','light'),
 ('03-pouch', None, '<div class="mk"></div><div class="t3"><p class="k" style="color:#F2B544">Offline · private</p><h1 style="color:#F4E9D6;font-size:104px">Your footage never leaves the pouch.</h1></div>','ink'),
 ('04-words', 'st_145.jpg', '<div class="img"></div><div class="chat"><div class="say">“More drone over Monument Valley.”</div><div class="said">✓ Done. +2 drone shots, chapter 11 s longer.</div></div><div class="t"><p class="k" style="color:#F2B544">Edit in words</p><h1 style="color:#F4E9D6;font-size:96px">No timeline.<br>Just say it.</h1></div>','dark'),
],
'pl':[
 ('01-clips', 'st_489.jpg', '<div class="img"></div><div class="pouch"><div class="st"></div></div><div class="t"><p class="k" style="color:#F2B544">Z pierwszego filmu</p><h1 style="color:#F4E9D6">1 434 nagrania.<br>Jeden film.</h1></div>','dark'),
 ('02-pilot', 'st_401.jpg', '<div class="img half"></div><div class="t2"><p class="k">Skąd Montaroo</p><h1 style="font-size:84px">Latam Boeingiem 737. Z podróży wróciłem z 1 434 nagraniami.</h1><p class="b">Zbudowałem montażystę, jakiego chciałem. Wskazujesz folder, wybierasz piosenki, dostajesz film.</p></div>','light'),
 ('03-pouch', None, '<div class="mk"></div><div class="t3"><p class="k" style="color:#F2B544">Offline · prywatnie</p><h1 style="color:#F4E9D6;font-size:100px">Twoje nagrania nie opuszczają torby.</h1></div>','ink'),
 ('04-words', 'st_145.jpg', '<div class="img"></div><div class="chat"><div class="say">„Więcej drona nad Monument Valley.”</div><div class="said">✓ Zrobione. +2 ujęcia z drona, rozdział dłuższy o 11 s.</div></div><div class="t"><p class="k" style="color:#F2B544">Poprawki słowami</p><h1 style="color:#F4E9D6;font-size:96px">Bez osi czasu.<br>Po prostu powiedz.</h1></div>','dark'),
]}
EXTRA="""
.img{position:absolute;inset:0;background-size:cover;background-position:center}
.img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#10251f00 30%,#10251fee 78%)}
.img.half{inset:0 0 auto 0;height:620px}.img.half::after{display:none}
.pouch{position:absolute;left:-40px;right:-40px;top:470px;height:300px;background:#E2642A;border-radius:0 0 50% 50%/0 0 100% 100%;display:none}
.t{position:absolute;left:72px;right:72px;bottom:170px;display:flex;flex-direction:column;gap:26px}
.t2{position:absolute;left:72px;right:72px;top:690px;display:flex;flex-direction:column;gap:24px}
.t2 .b{font:400 30px/1.45 I;color:#3E5A50;max-width:880px}
.t3{position:absolute;left:72px;right:72px;bottom:170px;display:flex;flex-direction:column;gap:26px}
.mk{position:absolute;left:50%;top:110px;width:560px;height:560px;margin-left:-280px;background:url(montaroo-znak-kolor-ciemne.svg) center/contain no-repeat}
.chat{position:absolute;left:72px;right:72px;top:150px;display:flex;flex-direction:column;gap:18px}
.say{align-self:flex-end;background:#E2642A;color:#10251F;font:600 36px/1.3 I;padding:22px 28px;border-radius:28px 28px 8px 28px;max-width:86%}
.said{background:#10251Fe6;color:#F4E9D6;font:400 30px/1.35 I;padding:20px 26px;border-radius:28px 28px 28px 8px;max-width:86%}
"""
for lang,items in P.items():
    for name,img,body,theme in items:
        bg={'dark':'#10251F','light':'#F4E9D6','ink':'#10251F'}[theme]
        logo='montaroo-poziome-kolor.svg' if theme=='light' else 'montaroo-poziome-kolor-ciemne.svg'
        style=f'background-image:url({img})' if img else ''
        body=body.replace('<div class="img','<div style="'+style+'" class="img')
        html=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{EXTRA}body{{background:{bg}}}</style></head><body>{body}<img class="logo" src="{logo}"></body></html>'
        fn=f'{lang}-{name}.html'; open(fn,'w').write(html)
        subprocess.run(['google-chrome','--headless=new','--no-sandbox','--hide-scrollbars','--allow-file-access-from-files','--window-size=1080,1350','--virtual-time-budget=2000',f'--screenshot=montaroo-post-{lang}-{name}.png','file://'+os.path.abspath(fn)],stderr=subprocess.DEVNULL)
print('ok')
