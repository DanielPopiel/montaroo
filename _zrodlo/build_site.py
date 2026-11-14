# -*- coding: utf-8 -*-
"""Buduje montaroo.com: index.html (EN) i pl/index.html (PL) z jednego szablonu.
Uruchom z katalogu repozytorium:  python _zrodlo/build_site.py
"""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, 'brand', 'logo', 'svg')

def svg_inline(name, cls='', label='montaroo'):
    s = open(os.path.join(LOGO, name + '.svg'), encoding='utf-8').read().strip()
    s = re.sub(r'<title>.*?</title>', '', s)
    s = s.replace('<svg ', f'<svg class="{cls}" role="img" aria-label="{label}" ', 1)
    return s

# Gdy instalator będzie gotowy: wpisz adres pliku (np. 'https://github.com/.../Montaroo-Setup.exe'). Puste = przyciski zapisują do bety mailem.
DOWNLOAD_URL = ''
BETA_MAIL = 'mailto:hello@montaroo.com?subject=Montaroo%20beta%20for%20Windows'

T = {
 'en': dict(
  lang='en', path='../', other='pl/', other_label='PL', other_name='Polski',
  title='Montaroo · Hop from footage to film',
  desc='Montaroo turns the hours of clips from your trip into a film with chapters, music and a story. It edits on your Windows PC, offline. Nothing is uploaded.',
  nav_how='How it works', nav_private='Offline', nav_films='Films', nav_price='Pricing', nav_cta='Download',
  hero_k='Automatic travel film editor for Windows',
  hero_h='Hop from footage<br>to film.',
  hero_p='Point Montaroo at the folder from your trip. It sorts the clips by day and place, cuts them to your music and hands back a film with a story. On your PC. Nothing gets uploaded.',
  cta1='Download for Windows' , cta1_beta='Get the Windows beta', cta1_s='Free · Windows 10 and 11',
  cta2='Watch a sample film',
  hero_cap='Excerpt from the first film made with Montaroo: 10 days on the Grand Circle, USA.',
  proof=[('1,434','clips in'),('10','days'),('6','chapters'),('12:02','film out'),('0','uploads')],
  proof_note='Numbers from the first film. One trip, one folder, one evening.',
  how_k='How it works', how_h='Three steps. No timeline.',
  steps=[
   ('Point to the trip', 'Phones, drone, GoPro, camera. Montaroo reads the dates and GPS, fixes time zones and splits the trip into days and places.', 'folder'),
   ('Pick the music', 'Choose a few songs. Cuts land on beats and phrases, transitions follow the energy of each chorus.', 'music'),
   ('Get the film', 'Chapters, place names, a route map, a title over your best drone shot. Want a change? Say it in words.', 'film'),
  ],
  say='“More drone over Monument Valley.”', said='Done. +2 drone shots, chapter 11 s longer.',
  story_k='Not just cuts to the beat', story_h='Edited like a story.',
  story_p='A teaser up front, a chapter for every day, the big moment where the music peaks, and an ending that brings you home. The same structure a film editor would use, built from your own clips.',
  chapters=[('LA & Vegas','26–27 Oct'),('Hoover & Route 66','28 Oct'),('Grand Canyon','29 Oct'),('Monument Valley','30–31 Oct'),('Page · Antelope · Zion','1–2 Nov'),('Home','3–4 Nov')],
  feat=[('Picks the good bits','Sharp, steady, well lit. Skips the shots of your shoes and the twelve near-identical sunsets.'),
        ('Knows the places','Names every stop from GPS, offline. “Horseshoe Bend”, not “36.88, −111.51”.'),
        ('Renders to 4K','Preview in minutes, final film in 4K. Export to Resolve, Premiere or Final Cut if you want to keep going.')],
  priv_k='Offline and private', priv_h='Your footage never leaves the pouch.',
  priv_p='Montaroo edits on your own computer. Your family videos are not uploaded, not used to train anything, and not stuck behind a subscription to see them again.',
  priv=[('Runs on your PC','Windows 10 or 11. A gaming laptop is plenty.'),('No upload, no account','Edit on a plane, in a cabin, with Wi-Fi off.'),('Originals untouched','Montaroo never moves or changes your files.')],
  films_k='Sample films', films_h='Made with Montaroo.',
  film1_t='USA 2026 · Grand Circle road trip', film1_m='12:02 · 4K · 6 chapters · 1,434 clips from 3 phones and a drone',
  film1_play='Play excerpt', film_note='Sample shown without the original soundtrack.',
  film2_t='Your trip next', film2_p='Back from a trip with a phone full of clips? That folder is a film already. It just needs editing.',
  film2_cta='Download Montaroo',
  pilot_k='Why Montaroo exists', pilot_h='Built by an airline pilot who came home with 1,434 clips.',
  pilot_p1='I fly the Boeing 737 for a living. After ten days driving the Grand Circle with my family, I had footage from three phones and my dad’s drone, and no time to sit at a timeline for a week.',
  pilot_p2='So I built the editor I wanted: point it at the folder, choose the songs, get the film. The first one runs twelve minutes and my family has watched it more times than I can count. Montaroo is that tool, made for everyone else’s trips.',
  pilot_sig='Daniel Popiel, founder · First Officer, Boeing 737',
  price_k='Pricing', price_h='Edit for free. Upgrade when you love it.',
  plans=[
   dict(n='Free', p='$0', s='forever', items=['Every feature, unlimited films','Export up to 1080p','Short “Edited in Montaroo” end card'], cta='Download free', hl=False),
   dict(n='Montaroo', p='$59', s='one-time · launch price', items=['Export in 4K','No end card, or your own','Export to Resolve, Premiere, Final Cut','A year of updates included'], cta='Get Montaroo', hl=True),
  ],
  price_note='Prices in USD, VAT may apply. The free version is not a trial: keep it as long as you like.',
  dl_h='Your trip, already edited.', dl_p='Free download for Windows 10 and 11 (64-bit). Mac version later.',
  dl_cta='Download for Windows', dl_beta='Join the beta for Windows', dl_beta_note='The beta opens soon. Send us a line and you get the download link first.', dl_req='8 GB RAM · 2 GB disk · any recent Intel, AMD or NVIDIA graphics',
  faq_h='Questions', faq=[
   ('Does it need the internet?','No. Editing, music analysis and place names all work offline. You can switch on more precise place names from OpenStreetMap if you want.'),
   ('Which cameras work?','Phones (iPhone and Android), DJI drones, GoPro and most cameras that save MP4 or MOV, plus photos. Montaroo mixes them on one timeline by real local time.'),
   ('How long does it take?','The first draft takes about two minutes, a preview a few more. The final 4K film renders in the background while you do something else.'),
   ('Can I use my own music?','Yes, any song file on your PC. Make sure you have the rights if you post the film publicly.'),
  ],
  foot='Montaroo · automatic travel film editor for Windows', foot_c='© 2026 Montaroo. Made in Warsaw.',
  skip='Skip to content', menu='Menu', mute='Video without sound', pause='Pause video', play='Play video', film_lang='Film narrated with Polish captions.',
 ),
 'pl': dict(
  lang='pl', path='../../', other='../', other_label='EN', other_name='English',
  title='Montaroo · Od nagrań do filmu jednym skokiem',
  desc='Montaroo zamienia godziny nagrań z wyjazdu w film z rozdziałami, muzyką i historią. Montuje na twoim komputerze z Windows, offline. Nic nie jest wysyłane.',
  nav_how='Jak to działa', nav_private='Offline', nav_films='Filmy', nav_price='Cennik', nav_cta='Pobierz',
  hero_k='Automatyczny montaż filmów z podróży na Windows',
  hero_h='Od nagrań do filmu<br>jednym skokiem.',
  hero_p='Wskaż Montaroo folder z wyjazdu. Program ułoży nagrania po dniach i miejscach, potnie je do twojej muzyki i odda film z historią. Na twoim komputerze. Nic nie trafia do chmury.',
  cta1='Pobierz na Windows', cta1_beta='Zapisz się do bety', cta1_s='Za darmo · Windows 10 i 11',
  cta2='Zobacz przykładowy film',
  hero_cap='Fragment pierwszego filmu zmontowanego w Montaroo: 10 dni na Grand Circle w USA.',
  proof=[('1 434','nagrań na wejściu'),('10','dni'),('6','rozdziałów'),('12:02','filmu'),('0','wysłanych plików')],
  proof_note='Liczby z pierwszego filmu. Jeden wyjazd, jeden folder, jeden wieczór.',
  how_k='Jak to działa', how_h='Trzy kroki. Bez osi czasu.',
  steps=[
   ('Wskaż wyjazd', 'Telefony, dron, GoPro, aparat. Montaroo czyta daty i GPS, poprawia strefy czasowe i dzieli wyjazd na dni i miejsca.', 'folder'),
   ('Wybierz muzykę', 'Kilka piosenek. Cięcia padają na takty i frazy, przejścia podążają za energią refrenu.', 'music'),
   ('Odbierz film', 'Rozdziały, nazwy miejsc, mapa trasy, tytuł na najlepszym ujęciu z drona. Coś zmienić? Powiedz to słowami.', 'film'),
  ],
  say='„Więcej drona nad Monument Valley.”', said='Zrobione. +2 ujęcia z drona, rozdział dłuższy o 11 s.',
  story_k='Nie tylko cięcia do beatu', story_h='Zmontowane jak opowieść.',
  story_p='Zapowiedź na początek, rozdział na każdy dzień, kulminacja tam, gdzie muzyka wchodzi najwyżej, i zakończenie, które wraca do domu. Taka sama budowa, jakiej użyłby montażysta, z twoich własnych nagrań.',
  chapters=[('LA i Vegas','26–27.10'),('Hoover i Route 66','28.10'),('Wielki Kanion','29.10'),('Monument Valley','30–31.10'),('Page · Antelope · Zion','1–2.11'),('Powrót','3–4.11')],
  feat=[('Wybiera dobre fragmenty','Ostre, stabilne, dobrze naświetlone. Pomija ujęcia butów i dwanaście prawie takich samych zachodów słońca.'),
        ('Zna miejsca','Podpisuje każdy przystanek z GPS, offline. „Horseshoe Bend”, a nie „36,88, −111,51”.'),
        ('Renderuje w 4K','Podgląd w kilka minut, finał w 4K. Eksport do Resolve, Premiere lub Final Cut, jeśli chcesz pracować dalej.')],
  priv_k='Offline i prywatnie', priv_h='Twoje nagrania nie opuszczają torby.',
  priv_p='Montaroo montuje na twoim komputerze. Rodzinne nagrania nie są wysyłane, nie trenują żadnych modeli i nie są zamknięte za abonamentem.',
  priv=[('Działa na twoim PC','Windows 10 lub 11. Wystarczy laptop do gier.'),('Bez wysyłania i konta','Montuj w samolocie, w domku w górach, z wyłączonym Wi-Fi.'),('Oryginały nietknięte','Montaroo nigdy nie przenosi ani nie zmienia twoich plików.')],
  films_k='Przykładowe filmy', films_h='Zmontowane w Montaroo.',
  film1_t='USA 2026 · road trip po Grand Circle', film1_m='12:02 · 4K · 6 rozdziałów · 1 434 nagrania z 3 telefonów i drona',
  film1_play='Odtwórz fragment', film_note='Fragment pokazany bez oryginalnej ścieżki muzycznej.',
  film2_t='Teraz twój wyjazd', film2_p='Wróciłeś z wyjazdu z telefonem pełnym nagrań? Ten folder to już film. Trzeba go tylko zmontować.',
  film2_cta='Pobierz Montaroo',
  pilot_k='Skąd Montaroo', pilot_h='Zbudował je pilot, który wrócił z podróży z 1 434 nagraniami.',
  pilot_p1='Zawodowo latam Boeingiem 737. Po dziesięciu dniach jazdy po Grand Circle z rodziną miałem nagrania z trzech telefonów i drona taty, a nie miałem tygodnia na siedzenie nad osią czasu.',
  pilot_p2='Zbudowałem więc montażystę, jakiego potrzebowałem: wskazujesz folder, wybierasz piosenki, dostajesz film. Pierwszy trwa dwanaście minut i rodzina obejrzała go więcej razy, niż potrafię policzyć. Montaroo to to samo narzędzie, dla wszystkich innych wyjazdów.',
  pilot_sig='Daniel Popiel, założyciel · pierwszy oficer, Boeing 737',
  price_k='Cennik', price_h='Montuj za darmo. Kup, gdy pokochasz.',
  plans=[
   dict(n='Free', p='0 zł', s='na zawsze', items=['Wszystkie funkcje, filmy bez limitu','Eksport do 1080p','Krótka plansza „Zmontowane w Montaroo”'], cta='Pobierz za darmo', hl=False),
   dict(n='Montaroo', p='249 zł', s='jednorazowo · cena na start', items=['Eksport w 4K','Bez planszy albo z własną','Eksport do Resolve, Premiere, Final Cut','Rok aktualizacji w cenie'], cta='Kup Montaroo', hl=True),
  ],
  price_note='Ceny brutto. Wersja darmowa to nie okres próbny: korzystaj, jak długo chcesz.',
  dl_h='Twój wyjazd, już zmontowany.', dl_p='Darmowe pobranie na Windows 10 i 11 (64-bit). Wersja na Maca później.',
  dl_cta='Pobierz na Windows', dl_beta='Zapisz się do bety na Windows', dl_beta_note='Beta rusza wkrótce. Napisz do nas, a link do pobrania dostaniesz jako pierwszy.', dl_req='8 GB RAM · 2 GB miejsca · dowolna nowa karta Intel, AMD lub NVIDIA',
  faq_h='Pytania', faq=[
   ('Czy potrzebny jest internet?','Nie. Montaż, analiza muzyki i nazwy miejsc działają offline. Jeśli chcesz, możesz włączyć dokładniejsze nazwy z OpenStreetMap.'),
   ('Jakie aparaty działają?','Telefony (iPhone i Android), drony DJI, GoPro i większość aparatów zapisujących MP4 lub MOV, a także zdjęcia. Montaroo układa je razem według prawdziwego czasu lokalnego.'),
   ('Ile to trwa?','Pierwsza wersja około dwóch minut, podgląd kilka kolejnych. Finał w 4K renderuje się w tle, kiedy robisz coś innego.'),
   ('Czy mogę użyć własnej muzyki?','Tak, dowolnego pliku z komputera. Jeśli publikujesz film, upewnij się, że masz prawa do muzyki.'),
  ],
  foot='Montaroo · automatyczny montaż filmów z podróży na Windows', foot_c='© 2026 Montaroo. Zrobione w Warszawie.',
  skip='Przejdź do treści', menu='Menu', mute='Wideo bez dźwięku', pause='Zatrzymaj wideo', play='Odtwórz wideo', film_lang='',
 ),
}

ICONS = {
 'folder': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5A2.5 2.5 0 0 1 5.5 4h3.6c.7 0 1.3.3 1.8.8L12.2 6H18.5A2.5 2.5 0 0 1 21 8.5v9a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5z"/></svg>',
 'music': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 17.5V6.2c0-.6.4-1.1 1-1.2l9-1.8c.6-.1 1.2.4 1.2 1v10.8a3 3 0 1 1-2-2.8V7.4l-7.2 1.5v8.6a3 3 0 1 1-2-2.8z"/></svg>',
 'film': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.6c0-1 1.1-1.6 2-1.1l9.6 6.4c.8.5.8 1.7 0 2.2L10 19.5c-.9.5-2-.1-2-1.1z"/></svg>',
}

def vignette(kind, L):
    if kind == 'folder':
        days = ['26','27','28','29','30','31','1','2','3','4']; hs=[30,82,46,60,52,96,64,44,28,40]
        bars=''.join(f'<span style="--h:{h}%"><i>{d}</i></span>' for d,h in zip(days,hs))
        rows=''.join(f'<div class="vr"><b>{a}</b><em>{b}</em></div>' for a,b in [('Daniel','1 365'),('Tata · dron' if L['lang']=='pl' else 'Dad · drone','63'),('Natalka','6')])
        return f'<div class="vig vig-folder">{rows}<div class="bars">{bars}</div></div>'
    if kind == 'music':
        import math
        w=''.join(f'<span style="--h:{int(18+70*abs(math.sin(i*0.55)*math.sin(i*0.13+1)))}%" class="{ "cut" if i%8==0 else ""}"></span>' for i in range(48))
        songs=''.join(f'<div class="song"><b>▶</b>{n}<em>{t}</em></div>' for n,t in [('road-trip.mp3','4:12'),('golden-hour.mp3','3:16')])
        return f'<div class="vig vig-music">{songs}<div class="wave">{w}</div><p class="vnote">♪ {"cięcia na taktach" if L["lang"]=="pl" else "cuts on the beat"}</p></div>'
    return (f'<div class="vig vig-film"><div class="say">{L["say"]}</div><div class="said">{L["said"]}</div>'
            f'<div class="chips"><span>{"Rytm" if L["lang"]=="pl" else "Rhythm"} 94%</span><span>4K</span><span>12:02</span></div></div>')

def page(L):
    p=L['path']; pre = p if p else ''
    logo = svg_inline('montaroo-poziome-kolor','logo')
    logo_d = svg_inline('montaroo-poziome-kolor-ciemne','logo')
    mark_d = svg_inline('montaroo-znak-kolor-ciemne','mark-big','')
    proof=''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a,b in L['proof'])
    steps=''.join(f'''<li class="step rv"><div class="step-n"><span>{i+1}</span>{ICONS[k]}</div><h3>{t}</h3><p>{d}</p>{vignette(k,L)}</li>''' for i,(t,d,k) in enumerate(L['steps']))
    chap=''.join(f'<li style="--i:{i}"><b>{a}</b><span>{b}</span></li>' for i,(a,b) in enumerate(L['chapters']))
    feat=''.join(f'<div class="feat rv"><h3>{a}</h3><p>{b}</p></div>' for a,b in L['feat'])
    priv=''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a,b in L['priv'])
    plans=''
    for pl in L['plans']:
        items=''.join(f'<li>{x}</li>' for x in pl['items'])
        plans+=f'''<div class="plan{' plan-hl' if pl['hl'] else ''} rv"><h3>{pl['n']}</h3><p class="price"><b>{pl['p']}</b><span>{pl['s']}</span></p><ul>{items}</ul><a class="btn {'btn-p' if pl['hl'] else 'btn-s'}" href="#download">{pl['cta']}</a></div>'''
    faq=''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(L['faq']))
    stitch='<div class="stitch" aria-hidden="true"></div>'
    dl = DOWNLOAD_URL or BETA_MAIL
    cta1 = L['cta1'] if DOWNLOAD_URL else L['cta1_beta']
    dl_cta = L['dl_cta'] if DOWNLOAD_URL else L['dl_beta']
    dl_note = '' if DOWNLOAD_URL else f'<p class="small">{L["dl_beta_note"]}</p>'
    mark_s = svg_inline('montaroo-znak-mono-jasny','next-mark','')
    ears = '<svg class="ears" viewBox="38 6 34 30" aria-hidden="true"><ellipse cx="49.6" cy="22.6" rx="5.2" ry="11" transform="rotate(-14 49.6 22.6)"/><ellipse cx="63" cy="26" rx="5.2" ry="11" transform="rotate(24 63 26)"/></svg>'
    alt_href = 'https://montaroo.com/preview/' + ('pl/' if L['lang']=='en' else '')
    self_href = 'https://montaroo.com/preview/' + ('pl/' if L['lang']=='pl' else '')
    return f'''<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{L['title']}</title>
<meta name="description" content="{L['desc']}">
<link rel="canonical" href="{self_href}">
<link rel="alternate" hreflang="en" href="https://montaroo.com/">
<link rel="alternate" hreflang="pl" href="https://montaroo.com/pl/">
<meta property="og:title" content="{L['title']}">
<meta property="og:description" content="{L['desc']}">
<meta property="og:image" content="https://montaroo.com/assets/og.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#10251F">
<link rel="icon" href="{pre}favicon.ico" sizes="any">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/gabarito-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/site.css">
<script>document.documentElement.classList.add("js")</script>
</head>
<body>
<a class="skip" href="#main">{L['skip']}</a>
<header class="nav" id="top">
 <div class="wrap nav-in">
  <a class="brand" href="{'./' if L['lang']=='en' else './'}" aria-label="montaroo">{logo}</a>
  <nav aria-label="main"><ul>
   <li><a href="#how">{L['nav_how']}</a></li><li><a href="#offline">{L['nav_private']}</a></li><li><a href="#films">{L['nav_films']}</a></li><li><a href="#pricing">{L['nav_price']}</a></li>
  </ul></nav>
  <div class="nav-r"><a class="lang" href="{L['other']}" hreflang="{'pl' if L['lang']=='en' else 'en'}" title="{L['other_name']}">{L['other_label']}</a><a class="btn btn-p btn-sm" href="#download">{L['nav_cta']}</a></div>
 </div>
</header>
<main id="main">
<section class="hero">
 <div class="wrap hero-in">
  <div class="hero-t">
   <p class="label">{L['hero_k']}</p>
   <h1>{L['hero_h']}</h1>
  </div>
  <figure class="hero-v">
   <div class="screen">
    {ears}
    <div class="screen-in">
     <video autoplay muted loop playsinline preload="auto" poster="{pre}assets/video/hero-poster.jpg" aria-label="{L['hero_cap']}">
      <source src="{pre}assets/video/hero.mp4" type="video/mp4">
     </video>
     <button class="vbtn" type="button" data-pause="{L['pause']}" data-play="{L['play']}" aria-label="{L['pause']}"><span></span></button>
    </div>
   </div>
   <div class="pouch-bg" aria-hidden="true"></div>
   <figcaption class="small muted">{L['hero_cap']}</figcaption>
  </figure>
  <div class="hero-b">
   <p class="lead">{L['hero_p']}</p>
   <div class="ctas"><a class="btn btn-p" href="{dl}">{ICONS['film'].replace('<svg','<svg class="i"')}{cta1}</a><a class="btn btn-s" href="#films">{L['cta2']}</a></div>
   <p class="small muted">{L['cta1_s']}</p>
  </div>
 </div>
 <div class="wrap"><ul class="proof">{proof}</ul><p class="small muted proof-note">{L['proof_note']}</p></div>
</section>

<section class="how" id="how">
 <div class="wrap">
  <p class="label">{L['how_k']}</p><h2>{L['how_h']}</h2>
  <ol class="steps">{steps}</ol>
 </div>
</section>

<section class="story">
 <div class="wrap">
  <div class="story-t rv"><p class="label">{L['story_k']}</p><h2>{L['story_h']}</h2><p class="lead">{L['story_p']}</p></div>
  <ol class="chapters rv" aria-label="USA 2026">{chap}</ol>
  <div class="feats">{feat}</div>
 </div>
</section>

<section class="offline" id="offline">
 <div class="wrap off-in">
  <div class="off-t rv"><p class="label">{L['priv_k']}</p><h2>{L['priv_h']}</h2><p class="lead">{L['priv_p']}</p><ul class="priv">{priv}</ul></div>
  <div class="off-mark rv" aria-hidden="true">{mark_d}</div>
 </div>
</section>

<section class="films" id="films">
 <div class="wrap">
  <p class="label">{L['films_k']}</p><h2>{L['films_h']}</h2>
  <div class="film-grid">
   <article class="film rv">
    <div class="film-v">
     <video controls muted playsinline preload="none" poster="{pre}assets/video/probka-poster.jpg" aria-label="{L['film1_t']}"><source src="{pre}assets/video/probka-usa.mp4" type="video/mp4"></video>
    </div>
    <h3>{L['film1_t']}</h3><p class="small muted">{L['film1_m']}</p><p class="small muted">{L['film_note']} {L['film_lang']}</p>
   </article>
   <article class="film film-next rv">
    {mark_s}<div class="next-in"><h3>{L['film2_t']}</h3><p>{L['film2_p']}</p><a class="btn btn-p" href="#download">{L['film2_cta']}</a></div>
   </article>
  </div>
 </div>
</section>

<section class="pilot">
 <div class="wrap pilot-in">
  <figure class="pilot-img rv"><img src="{pre}assets/img/pilot-road.jpg" alt="" loading="lazy" width="1280" height="720"></figure>
  <div class="pilot-t rv"><p class="label">{L['pilot_k']}</p><h2>{L['pilot_h']}</h2><p>{L['pilot_p1']}</p><p>{L['pilot_p2']}</p><p class="sig">{L['pilot_sig']}</p></div>
 </div>
</section>

<section class="pricing" id="pricing">
 <div class="wrap">
  <p class="label">{L['price_k']}</p><h2>{L['price_h']}</h2>
  <div class="plans">{plans}</div>
  <p class="small muted">{L['price_note']}</p>
 </div>
</section>

<section class="faq">
 <div class="wrap faq-in"><h2>{L['faq_h']}</h2><div class="faq-l">{faq}</div></div>
</section>
<section class="download" id="download">
 <div class="wrap dl-in">
  {stitch}
  <h2>{L['dl_h']}</h2><p class="lead">{L['dl_p']}</p>
  <a class="btn btn-p btn-lg" href="{dl}">{ICONS['film'].replace('<svg','<svg class="i"')}{dl_cta}</a>
  {dl_note}<p class="small">{L['dl_req']}</p>
 </div>
</section>

</main>
<footer class="foot">
 <div class="wrap foot-in">
  <a class="brand" href="#top" aria-label="montaroo">{logo_d}</a>
  <p>{L['foot']}<br><span class="muted">{L['foot_c']}</span></p>
  <p class="foot-r"><a href="{L['other']}" hreflang="{'pl' if L['lang']=='en' else 'en'}">{L['other_name']}</a> · <a href="mailto:hello@montaroo.com">hello@montaroo.com</a><br>{'<a href="/privacy/">Privacy</a> · <a href="/eula/">EULA</a>' if L['lang']=='en' else '<a href="/pl/prywatnosc/">Prywatność</a> · <a href="/pl/licencja/">Licencja</a>'}</p>
 </div>
</footer>
<script src="{pre}assets/site.js" defer></script>
</body>
</html>
'''

for k in ('en','pl'):
    # pełna strona produktu leży w /preview/ (niewidoczna dla wyszukiwarek) do czasu premiery
    out = os.path.join(ROOT, 'preview', 'index.html' if k=='en' else 'pl/index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out,'w',encoding='utf-8').write(page(T[k]))
    print('ok', out)
