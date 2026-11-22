# -*- coding: utf-8 -*-
"""Strona główna montaroo.com (EN: index.html, PL: pl/index.html) = nagłówek z formularzem + scena „Historia”
(animacja 14 s: intro → telefony przez QR → ściana z kangurkiem → muzyka → panel montażu → film 20 s; jedna muzyka, dźwięk po dotknięciu).
Bez cennika (dojdzie po założeniu sklepu).

Źródło sceny: makiety Daniela – D:\\Claude AI Video\\Kampania reklamowa\\5_Strona-3D\\makiety (historia.js / historia.css / wspolne.css, kafle*, klatki.jpg,
historia-muzyka.mp3, film-20s-*). Daniel dopracowuje je dalej, więc ODŚWIEŻANIE = jedno polecenie z katalogu repozytorium:

    python _zrodlo/build_historia.py            kopiuje pliki z makiet do assets/historia i assets/video, buduje index.html i pl/index.html
    python _zrodlo/build_historia.py --bez-sync tylko przebudowuje HTML z plików, które już są w repozytorium

Co robi przy kopiowaniu: scala wspolne.css + historia.css (czcionki z strony, bez paska makiet), dopisuje do historia.js ścieżki (window.HB / HV),
usuwa makietowy „zapis wyłączony” formularza i dla wersji PL podmienia napisy sceny (tabela PL niżej; brak napisu w nowej wersji js = głośny błąd).
Formularz MailerLite, piksel Meta i baner zgody są wspólne z build_soon.py (pixel_parts). Piksel: MONTAROO_PIXEL=<ID> przed budowaniem.
Bramka na starcie (haczyk.js/.css): źródło _zrodlo/haczyk, kopiowana tu przy synchronizacji; ?hak=0 wyłącza, ?hak=1 wymusza, AB_PROC w haczyk.js = % widzących.
Plików HTML i assets/historia nie edytuj ręcznie."""
import os, re, sys, json, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_soon as bs
ROOT = bs.ROOT
MAKIETA = os.environ.get('MONTAROO_MAKIETA') or r'D:\Claude AI Video\Kampania reklamowa\5_Strona-3D\makiety'
AH = os.path.join(ROOT, 'assets', 'historia')
AV = os.path.join(ROOT, 'assets', 'video')

# ---------- napisy strony (EN / PL) ----------
PAGE = {
 'en': dict(
   title='Montaroo · Turn your trip clips into a film',
   desc='Montaroo turns your GoPro, DJI and phone clips into a finished travel film: best moments, cuts on the beat, chapters, a route map. Offline, on your Windows PC. Free beta.',
   k='Free beta · Windows', h='Turn your trip clips into a film. <em>Automatically.</em>',
   lead='Drop in the folder of GoPro, DJI and phone clips. Montaroo watches every one, picks the best moments and cuts them to the music, with chapters, a route map and titles. Offline, on your Windows PC.',
   chips=['No account', 'Runs offline', 'Free version'], f_btn='Get early access',
   replay='↺ Replay', sound='🔊 Sound on', rozd_l='Jump to a step',
   rozd=['Intro', 'Phones', 'Watching', 'Music', 'Editing', 'Film'],
   cap='<b>Our 10-day USA road trip</b> · 1,434 clips → one 20-second film',
   poster_alt='Frame from the film Montaroo made from 1,434 road-trip clips'),
 'pl': dict(
   title='Montaroo · Zamień nagrania z podróży w film',
   desc='Montaroo zamienia nagrania z GoPro, DJI i telefonu w gotowy film z podróży: najlepsze momenty, cięcia do rytmu, rozdziały, mapa trasy. Offline, na twoim komputerze z Windows. Darmowa beta.',
   k='Darmowa beta · Windows', h='Zamień nagrania z podróży w film. <em>Automatycznie.</em>',
   lead='Wrzuć folder z nagraniami z GoPro, DJI i telefonu. Montaroo ogląda każde, wybiera najlepsze momenty i tnie je do muzyki, z rozdziałami, mapą trasy i napisami. Offline, na twoim komputerze z Windows.',
   chips=['Bez konta', 'Działa offline', 'Wersja darmowa'], f_btn='Chcę wcześniejszy dostęp',
   replay='↺ Jeszcze raz', sound='🔊 Włącz dźwięk', rozd_l='Przejdź do kroku',
   rozd=['Intro', 'Telefony', 'Oglądanie', 'Muzyka', 'Montaż', 'Film'],
   cap='<b>Nasz 10-dniowy road trip po USA</b> · 1 434 nagrania → jeden film 20 s',
   poster_alt='Kadr z filmu, który Montaroo zmontowało z 1 434 nagrań z wyjazdu'),
}
RODZ = ['Intro', 'Phones', 'Watching', 'Music', 'Editing', 'Film']   # (kolejność przycisków; czasy w data-t poniżej)
CZASY = ['0', '2.531', '6.525', '10.519', '12.06', '14.512']

# ---------- napisy wewnątrz sceny: (szukane, podmiana) dokładnie jak w historia.js; brak trafienia = błąd ----------
PL_JS = [
 ("KTO = ['You', 'Anna', 'Dad']", "KTO = ['Ty', 'Anna', 'Tata']"),
 ('<b>DJI drone card detected</b><small>212 clips · adding…</small>', '<b>Wykryto kartę drona DJI</b><small>212 nagrań · dodaję…</small>'),
 ("'212 clips · added ✓'", "'212 nagrań · dodano ✓'"),
 ("'212 clips · adding…'", "'212 nagrań · dodaję…'"),
 ('Got clips on your phone?<small>Scan the code in my paws.</small>', 'Masz nagrania w telefonie?<small>Zeskanuj kod w moich łapkach.</small>'),
 ('Tap me 🎵<small>Watch it with music</small>', 'Dotknij mnie 🎵<small>Obejrzyj z muzyką</small>'),
 ("'Hop from footage to film.'", "'Od nagrań do filmu jednym skokiem.'"),
 ('class="soon">Coming soon<', 'class="soon">Wkrótce<'),
 ("'Calm'", "'Spokojny'"), ("'Cinematic'", "'Filmowy'"), ("'Upbeat · 119 BPM'", "'Pogodny · 119 BPM'"), ("'Upbeat'", "'Pogodny'"),
 ("'Energetic'", "'Energiczny'"), ("'Epic'", "'Epicki'"), ("'Happy'", "'Radosny'"),
 ("'DAY 3 · On the road'", "'DZIEŃ 3 · W drodze'"), ("'DAY 4 · Grand Canyon'", "'DZIEŃ 4 · Grand Canyon'"),
 ("['Video', 'Text', 'Sound', 'Music']", "['Wideo', 'Tekst', 'Dźwięk', 'Muzyka']"),
 ("['− Shorter', '+ Longer', '♪ Sound', 'T Text', '⇄ Swap']", "['− Krócej', '+ Dłużej', '♪ Dźwięk', 'T Tekst', '⇄ Zamień']"),
 ("'Every phone drops in'", "'Każdy telefon wskakuje do torby'"), ("'Watching every clip'", "'Oglądamy każde nagranie'"),
 ("'Picking the music'", "'Dobieramy muzykę'"), ("'Cutting to the beat'", "'Tniemy do rytmu'"), ("'Your film'", "'Twój film'"),
 ("'🔇 Mute' : '🔊 Sound on'", "'🔇 Wycisz' : '🔊 Włącz dźwięk'"),
 ('<small>IN THE BAG</small>', '<small>W TORBIE</small>'),
]


def czytaj(p): return open(p, encoding='utf-8').read()
def pisz(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
def kopiuj(a, b):
    """kopiuje plik binarny, gdy się różni (zwraca True, gdy skopiowano)"""
    os.makedirs(os.path.dirname(b), exist_ok=True)
    if os.path.exists(b) and os.path.getsize(a) == os.path.getsize(b) and open(a, 'rb').read() == open(b, 'rb').read(): return False
    shutil.copyfile(a, b); return True
def hashp(p): return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:8]


def js_dla(src, lang):
    """historia.js z makiety → wersja na stronę (ścieżki z window.HB/HV, bez makietowego formularza, napisy PL)"""
    s = src
    zam = [("fetch('kafle.json')", "fetch(HB + 'kafle.json')"),
           ("['kafle.jpg', 'kafle-szary.jpg', 'klatki.jpg'].map(s => new Promise(ok => { const i = new Image(); i.onload = i.onerror = ok; i.src = s }))",
            "['kafle.jpg', 'kafle-szary.jpg', 'klatki.jpg'].map(s => new Promise(ok => { const i = new Image(); i.onload = i.onerror = ok; i.src = HB + s }))"),
           ("'url(klatki.jpg)'", "('url(' + HB + 'klatki.jpg)')"),
           ("vid.poster = `film-20s-${f}.jpg`; vid.src = `film-20s-${f}.mp4`", "vid.poster = HV + `film-20s-${f}.jpg`; vid.src = HV + `film-20s-${f}.mp4`")]
    for a, b in zam:
        if a not in s: sys.exit(f'BŁĄD: w historia.js nie ma już fragmentu do przepisania ścieżek: {a[:70]}… – dopasuj build_historia.py (js_dla)')
        s = s.replace(a, b)
    s, n = re.subn(r"document\.getElementById\('wl'\)\.addEventListener\('submit'.*?\n", '', s)   # makietowy „zapis wyłączony”
    if n != 1: sys.exit('BŁĄD: nie znalazłem makietowej obsługi formularza (wl) w historia.js')
    if lang == 'pl':
        for a, b in PL_JS:
            if a not in s: sys.exit(f'BŁĄD: napisu sceny nie ma już w historia.js (zmieniony w makiecie?): {a[:70]}')
            s = s.replace(a, b)
    return s


def css_dla():
    """wspolne.css (układ strony i scena) + historia.css; czcionki idą z <style> strony, bez paska makiet (.mk)"""
    w = czytaj(os.path.join(MAKIETA, 'wspolne.css'))
    w = re.sub(r'@font-face\{[^}]*\}\n?', '', w)
    w = re.sub(r'\.mk[^{]*\{[^}]*\}\n?', '', w)
    w = re.sub(r'\n\s*\.mk span\{display:none\}', '', w)
    return '/* zbudowane przez _zrodlo/build_historia.py z makiet (wspolne.css + historia.css) – nie edytuj ręcznie */\n' + w.strip() + '\n' + czytaj(os.path.join(MAKIETA, 'historia.css'))


def sync():
    if not os.path.isdir(MAKIETA):
        print('(brak folderu makiet – pomijam kopiowanie, używam plików z repozytorium:', MAKIETA, ')'); return
    n = 0
    for f in ('kafle.jpg', 'kafle-szary.jpg', 'klatki.jpg', 'kafle.json', 'historia-muzyka.mp3'): n += kopiuj(os.path.join(MAKIETA, f), os.path.join(AH, f))
    for f in ('film-20s-16x9.mp4', 'film-20s-9x16.mp4', 'film-20s-16x9.jpg', 'film-20s-9x16.jpg'): n += kopiuj(os.path.join(MAKIETA, f), os.path.join(AV, f))
    src = czytaj(os.path.join(MAKIETA, 'historia.js'))
    pisz(os.path.join(AH, 'historia.js'), js_dla(src, 'en'))
    pisz(os.path.join(AH, 'historia.pl.js'), js_dla(src, 'pl'))
    pisz(os.path.join(AH, 'historia.css'), css_dla())
    for f in ('haczyk.js', 'haczyk.css'):                              # bramka na starcie (źródło w repozytorium: _zrodlo/haczyk)
        pisz(os.path.join(AH, f), czytaj(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haczyk', f)))
    print(f'skopiowano z makiet: {n} plików binarnych + historia.js/.pl.js/.css')


EXTRA_CSS = '''
.top .logo{height:30px;width:auto;display:block}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.wl button[disabled]{opacity:.6;cursor:wait;transform:none}
.wl-msg.err{color:var(--akcent)}
.wl-msg{color:var(--noc)}
.wl.done{margin-bottom:8px}
.wl.done .wl-row,.wl.done .wl-note{display:none}
.wl.done .wl-msg{background:var(--noc);color:var(--piasek);padding:14px 16px;border-radius:14px 14px 14px 4px;margin:0}
.wl-note a,footer a{color:var(--cichy);text-underline-offset:3px}footer a:hover{color:var(--noc)}
.stage .np{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
'''


def fonty(pre):
    m = re.findall(r'@font-face\{[^}]*\}', bs.CSS_BASE)
    return '\n'.join(x.replace('PRE/', pre) for x in m)


def strona(lang):
    L = bs.T[lang]; P = PAGE[lang]; pre = L['pre']
    px_css, cb_html, px_js = bs.pixel_parts(L)
    logo = open(os.path.join(ROOT, 'brand', 'logo', 'svg', 'montaroo-poziome-kolor.svg'), encoding='utf-8').read()
    logo = re.sub(r'<title>.*?</title>', '', logo).replace('<svg ', '<svg class="logo" role="img" aria-label="montaroo" ', 1)
    jsname = 'historia.js' if lang == 'en' else 'historia.pl.js'
    v = {f: hashp(os.path.join(AH, f)) for f in ('historia.css', jsname, 'haczyk.js', 'haczyk.css')}
    hb, hv = pre + 'assets/historia/', pre + 'assets/video/'
    ok, err, bad = (json.dumps(L[k], ensure_ascii=False) for k in ('f_ok', 'f_err', 'f_bad'))
    chips = ''.join(f'<li>{c}</li>' for c in P['chips'])
    rozd = ''.join(f'<button type="button" data-t="{t}">{n}</button>' for t, n in zip(CZASY, P['rozd']))
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{P['title']}</title>
<meta name="description" content="{P['desc']}">
<link rel="alternate" hreflang="en" href="https://montaroo.com/">
<link rel="alternate" hreflang="pl" href="https://montaroo.com/pl/">
<meta property="og:title" content="{P['title']}">
<meta property="og:description" content="{P['desc']}">
<meta property="og:image" content="https://montaroo.com/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F4E9D6">
<link rel="icon" href="{pre}favicon.ico" sizes="any">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/gabarito-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{hb}kafle.jpg" as="image"><link rel="preload" href="{hb}kafle-szary.jpg" as="image"><link rel="preload" href="{hb}klatki.jpg" as="image">
<style>{fonty(pre)}</style>
<link rel="stylesheet" href="{hb}historia.css?v={v['historia.css']}"><link rel="stylesheet" href="{hb}haczyk.css?v={v['haczyk.css']}">
<style>{EXTRA_CSS}{px_css}</style>
</head>
<body class="ef-historia">
<header class="top"><a href="./" aria-label="montaroo">{logo}</a><a class="lang" href="{L['other']}" hreflang="{'pl' if lang == 'en' else 'en'}">{L['other_label']}</a></header>
<main>
 <div class="txt">
  <p class="k">{P['k']}</p>
  <h1>{P['h']}</h1>
  <p class="lead">{P['lead']}</p>
  <ul class="chips">{chips}</ul>
  <form class="wl" id="wl" action="https://assets.mailerlite.com/jsonp/2795574/forms/204133928705984083/subscribe" method="post" novalidate>
   <div class="wl-row"><label class="hp" for="wl-e">{L['f_label']}</label><input id="wl-e" type="email" name="fields[email]" placeholder="{L['f_label']}" autocomplete="email" required><button type="submit">{P['f_btn']}</button></div>
   <div class="hp" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>
   <input type="hidden" name="ml-submit" value="1"><input type="hidden" name="anticsrf" value="true">
   <p class="wl-note">{L['f_note']}</p>
   <p class="wl-msg" id="wl-m" role="status" aria-live="polite"></p>
  </form>
 </div>
 <div class="scena">
  <div class="stage" id="stage">
   <div class="fx" id="fx" aria-hidden="true"></div>
   <div class="player"><video id="vid" muted playsinline preload="auto"></video></div>
   <div class="kont"><button id="again" type="button">{P['replay']}</button><button id="snd" type="button">{P['sound']}</button></div>
   <noscript><img class="np" src="{hv}film-20s-16x9.jpg" alt="{P['poster_alt']}"></noscript>
  </div>
  <div class="rozd" id="rozd" role="group" aria-label="{P['rozd_l']}">{rozd}</div>
  <p class="cap"><span>{P['cap']}</span></p>
 </div>
</main>
<footer><b>{L['tagline']}</b><span>© 2026 Montaroo · {L.get('legal', '')}</span></footer>{cb_html}
<audio id="aud" src="{hb}historia-muzyka.mp3" preload="auto"></audio>
<script>window.HB={json.dumps(hb)};window.HV={json.dumps(hv)};</script>
<script src="{hb}{jsname}?v={v[jsname]}" defer></script>
<script src="{hb}haczyk.js?v={v['haczyk.js']}" defer></script>
<script>
const MSG={{ok:{ok},err:{err},bad:{bad}}};
(()=>{{
 const f=document.getElementById('wl'),m=document.getElementById('wl-m'),e=document.getElementById('wl-e'),b=f.querySelector('button');
 f.addEventListener('submit',async ev=>{{ev.preventDefault();m.className='wl-msg';m.textContent='';
  if(f.website.value)return;
  if(!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(e.value.trim())){{m.className='wl-msg err';m.textContent=MSG.bad;e.focus();return}}
  b.disabled=true;
  try{{const r=await fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{Accept:'application/json'}}}});const j=await r.json().catch(()=>({{}}));
   if(r.ok&&j.success!==false){{f.classList.add('done');m.textContent=MSG.ok;if(window.mlead)mlead()}}else throw 0}}
  catch(_){{m.className='wl-msg err';m.textContent=MSG.err;b.disabled=false}}
 }});
}})();
{px_js}</script>
</body>
</html>
'''


if __name__ == '__main__':
    if '--bez-sync' not in sys.argv: sync()
    for k in ('en', 'pl'):
        out = os.path.join(ROOT, 'index.html' if k == 'en' else 'pl/index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8', newline='\n').write(strona(k))
        print('ok', out)
