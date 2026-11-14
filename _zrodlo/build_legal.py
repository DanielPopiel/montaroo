# -*- coding: utf-8 -*-
"""Strony prawne montaroo.com: polityka prywatności i licencja (EULA), EN + PL,
oraz robots.txt i sitemap.xml.
  EN: /privacy/  /eula/        PL: /pl/prywatnosc/  /pl/licencja/
Uruchom z katalogu repozytorium:  python _zrodlo/build_legal.py
Treść jest w słowniku DOCS (zwykły HTML w akapitach). Przy zmianie treści podbij UPDATED.
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = {'en': '14 November 2026', 'pl': '14 listopada 2026'}
ISO = '2026-11-14'
EMAIL = 'hello@montaroo.com'
OWNER_EN = 'Daniel Popiel, running the business <i>Daniel Popiel Airline Partner</i> in Poland'
OWNER_PL = 'Daniel Popiel, prowadzący działalność gospodarczą <i>Daniel Popiel Airline Partner</i>'

M = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

DOCS = {
# ------------------------------------------------------------------ PRIVACY EN
('privacy', 'en'): dict(
 path='privacy/', title='Privacy policy', desc='How Montaroo handles your data: the app edits on your PC and uploads nothing.',
 short='Montaroo edits your films on your own computer. Your clips, photos and music are not uploaded anywhere, there is no account to create, and the app does not send usage data. The website has no cookies and no trackers.',
 body=f'''
<h2>1. Who is responsible</h2>
<p>The controller of your personal data is {OWNER_EN} (“we”). Contact: {M}.</p>

<h2>2. The Montaroo app</h2>
<p><b>Your footage stays on your PC.</b> Montaroo reads the videos, photos and music you point it to and makes the film on your own computer. We never receive these files, their contents or their metadata (dates, GPS positions, faces, voices), and we do not use them to train any model.</p>
<p><b>No account, no telemetry.</b> The app does not ask you to sign in and does not send usage statistics, crash reports or identifiers to us.</p>
<p><b>Optional place names from OpenStreetMap.</b> Place names work offline by default. If you switch on precise names from OpenStreetMap, the app sends the GPS coordinates of your clips (without the clips themselves) to the OpenStreetMap Nominatim service to look up the names. That service is run by the OpenStreetMap Foundation under its own <a href="https://osmfoundation.org/wiki/Privacy_Policy">privacy policy</a>. You can turn this off at any time.</p>
<p><b>Installation and updates through Microsoft Store.</b> If you get Montaroo from Microsoft Store, Microsoft handles the download, licence, payment and updates as a separate controller under the <a href="https://privacy.microsoft.com/privacystatement">Microsoft Privacy Statement</a>. Microsoft shares with us only aggregated reports (for example the number of installs per country) and, if you choose to write one, your public review.</p>

<h2>3. This website</h2>
<p>montaroo.com has no cookies, no analytics and no advertising trackers. Fonts and videos are served from our own site.</p>
<p>The site is hosted by GitHub Pages (GitHub, Inc.). Like any web server, GitHub records technical data such as your IP address and browser type when you open a page, to deliver the page and protect the service. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy Statement</a>.</p>

<h2>4. When you write to us</h2>
<p>If you email us, for example to join the beta or ask a question, we use your email address and what you write to reply and, for beta testers, to send the download link and beta updates. Legal basis: our legitimate interest in answering you and running the beta (Art. 6(1)(f) GDPR), or steps you ask for before a purchase (Art. 6(1)(b)). We keep these emails for up to 2 years after our last contact, unless you ask us to delete them sooner.</p>
<p><b>Beta list.</b> If you sign up on montaroo.com, we store your email address and the date you joined, to tell you when the Windows beta opens and send occasional launch news. Legal basis: your consent (Art. 6(1)(a) GDPR), which you can withdraw at any time with the unsubscribe link in every email or by writing to us. The list is run by MailerLite (MailerLite Limited, Ireland), which processes the data on our behalf as our processor. We keep your address until you unsubscribe, or for up to 12 months after Montaroo launches if you never open our emails.</p>

<h2>5. Who else sees your data</h2>
<p>Only the providers named above (GitHub for the website, our email provider for messages, MailerLite for the beta list, Microsoft for Store purchases, OpenStreetMap if you switch it on). We do not sell or share your data with advertisers. Some of these providers are based in the USA; transfers rely on the EU–US Data Privacy Framework or the EU standard contractual clauses.</p>

<h2>6. Your rights</h2>
<p>You can ask us for access to your data, correction, deletion, restriction, a copy in a portable format, and you can object to processing based on legitimate interest. Write to {M}. You can also complain to the Polish data protection authority, the President of the Personal Data Protection Office (UODO, <a href="https://uodo.gov.pl/en">uodo.gov.pl</a>), or to the authority in your own EU country.</p>

<h2>7. Children</h2>
<p>Montaroo is not directed at children under 16, and we do not knowingly collect their data.</p>

<h2>8. Changes</h2>
<p>If the app or this website starts handling data in a new way, we will update this page before that happens and change the date at the top.</p>
'''),
# ------------------------------------------------------------------ PRIVACY PL
('privacy', 'pl'): dict(
 path='pl/prywatnosc/', title='Polityka prywatności', desc='Jak Montaroo traktuje twoje dane: aplikacja montuje na twoim komputerze i niczego nie wysyła.',
 short='Montaroo montuje filmy na twoim komputerze. Twoje nagrania, zdjęcia i muzyka nigdzie nie są wysyłane, nie trzeba zakładać konta, a aplikacja nie wysyła danych o użytkowaniu. Strona nie używa cookies ani narzędzi śledzących.',
 body=f'''
<h2>1. Kto odpowiada za dane</h2>
<p>Administratorem twoich danych osobowych jest {OWNER_PL} („my”). Kontakt: {M}.</p>

<h2>2. Aplikacja Montaroo</h2>
<p><b>Nagrania zostają na twoim komputerze.</b> Montaroo czyta filmy, zdjęcia i muzykę, które wskażesz, i montuje film na twoim komputerze. Nie dostajemy tych plików, ich treści ani metadanych (dat, pozycji GPS, twarzy, głosów) i nie używamy ich do trenowania żadnych modeli.</p>
<p><b>Bez konta i bez telemetrii.</b> Aplikacja nie wymaga logowania i nie wysyła nam statystyk użycia, raportów o błędach ani identyfikatorów.</p>
<p><b>Opcjonalne nazwy miejsc z OpenStreetMap.</b> Domyślnie nazwy miejsc działają offline. Jeśli włączysz dokładniejsze nazwy z OpenStreetMap, aplikacja wyśle współrzędne GPS nagrań (bez samych nagrań) do usługi OpenStreetMap Nominatim, żeby odczytać nazwy miejsc. Usługę prowadzi OpenStreetMap Foundation na zasadach swojej <a href="https://osmfoundation.org/wiki/Privacy_Policy">polityki prywatności</a>. Możesz to w każdej chwili wyłączyć.</p>
<p><b>Instalacja i aktualizacje przez Microsoft Store.</b> Jeśli pobierasz Montaroo z Microsoft Store, pobieranie, licencję, płatność i aktualizacje obsługuje Microsoft jako osobny administrator, według <a href="https://privacy.microsoft.com/pl-pl/privacystatement">Oświadczenia o ochronie prywatności firmy Microsoft</a>. Microsoft przekazuje nam tylko zbiorcze raporty (np. liczbę instalacji w danym kraju) i, jeśli ją napiszesz, twoją publiczną opinię.</p>

<h2>3. Ta strona</h2>
<p>montaroo.com nie używa plików cookies, narzędzi analitycznych ani reklamowych. Fonty i filmy ładują się z naszej strony.</p>
<p>Stronę hostuje GitHub Pages (GitHub, Inc.). Jak każdy serwer, GitHub zapisuje przy otwarciu strony dane techniczne, np. adres IP i typ przeglądarki, żeby ją wyświetlić i chronić usługę. Szczegóły: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy Statement</a>.</p>

<h2>4. Gdy do nas piszesz</h2>
<p>Jeśli napiszesz do nas maila, np. żeby dołączyć do bety albo zadać pytanie, używamy twojego adresu i treści wiadomości, żeby odpowiedzieć, a testerom bety także żeby wysłać link do pobrania i informacje o becie. Podstawa prawna: nasz prawnie uzasadniony interes w odpowiedzi i prowadzeniu bety (art. 6 ust. 1 lit. f RODO) albo działania na twoje żądanie przed zakupem (art. 6 ust. 1 lit. b). Maile przechowujemy do 2 lat od ostatniego kontaktu, chyba że wcześniej poprosisz o usunięcie.</p>
<p><b>Lista oczekujących na betę.</b> Jeśli zapiszesz się na montaroo.com, przechowujemy twój adres e-mail i datę zapisu, żeby dać ci znać o starcie bety na Windows i czasem wysłać informacje o premierze. Podstawa prawna: twoja zgoda (art. 6 ust. 1 lit. a RODO), którą możesz w każdej chwili wycofać linkiem do wypisania w każdym mailu albo pisząc do nas. Listę obsługuje MailerLite (MailerLite Limited, Irlandia), który przetwarza dane w naszym imieniu jako podmiot przetwarzający. Adres trzymamy do czasu wypisania się, a jeśli nie otwierasz naszych maili – najdłużej 12 miesięcy po premierze Montaroo.</p>

<h2>5. Kto jeszcze widzi dane</h2>
<p>Tylko wymienieni wyżej dostawcy (GitHub dla strony, nasz dostawca poczty dla maili, MailerLite dla listy oczekujących, Microsoft przy zakupie w Sklepie, OpenStreetMap jeśli go włączysz). Nie sprzedajemy danych i nie przekazujemy ich reklamodawcom. Część dostawców ma siedzibę w USA; przekazanie opiera się na programie EU–US Data Privacy Framework albo standardowych klauzulach umownych UE.</p>

<h2>6. Twoje prawa</h2>
<p>Możesz żądać dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania i przeniesienia, a także wnieść sprzeciw wobec przetwarzania opartego na prawnie uzasadnionym interesie. Napisz na {M}. Możesz też złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych (<a href="https://uodo.gov.pl">uodo.gov.pl</a>).</p>

<h2>7. Dzieci</h2>
<p>Montaroo nie jest kierowane do dzieci poniżej 16 lat i świadomie nie zbieramy ich danych.</p>

<h2>8. Zmiany</h2>
<p>Jeśli aplikacja albo strona zacznie przetwarzać dane w nowy sposób, zaktualizujemy tę stronę, zanim to nastąpi, i zmienimy datę na górze.</p>
'''),
# ------------------------------------------------------------------ EULA EN
('eula', 'en'): dict(
 path='eula/', title='Licence agreement (EULA)', desc='End user licence agreement for the Montaroo app for Windows.',
 short='You may install Montaroo and use it to make films, for free or with the paid upgrade. The films you make are yours. The app itself stays ours, so please don’t copy, resell or crack it.',
 body=f'''
<p>This agreement is between you and {OWNER_EN} (“we”), the maker of Montaroo. By installing or using Montaroo you accept it. If you get Montaroo from Microsoft Store, the Microsoft Store terms of sale also apply to the purchase itself.</p>

<h2>1. What you may do</h2>
<p>We give you a personal, non-exclusive, non-transferable licence to install and use Montaroo on Windows devices you own or control, for personal and commercial projects. The free version and the paid version (“Montaroo” upgrade) differ only in the features described on montaroo.com and in Microsoft Store.</p>

<h2>2. Your films and files are yours</h2>
<p>Everything you put into Montaroo (videos, photos, music, text) and every film you make with it belongs to you or to whoever owns those materials. We claim no rights to it. The free version may add a short “Edited in Montaroo” end card; you may keep or cut it in your own edit.</p>

<h2>3. Music and other materials</h2>
<p>You are responsible for having the rights to the music, footage and other materials you use, especially if you publish the film. Music included with Montaroo comes from authors who released it under Creative Commons or public domain licences; when a track requires credit, Montaroo shows the credit text to add to your video description. Some platforms (for example YouTube Content ID) may still flag licensed tracks; this is not something we control.</p>

<h2>4. What you may not do</h2>
<p>You may not sell, rent, sublicense or share copies of Montaroo or your licence key; remove or bypass the licence check or paid features; or decompile or modify the app, except where the law expressly allows it (for example for interoperability under EU law).</p>

<h2>5. Updates and beta versions</h2>
<p>We may release updates that fix bugs or change features. Beta versions are for testing, may contain errors and may stop working when the final version is released. Please keep copies of your original files; Montaroo never moves or changes them, but no software is perfect.</p>

<h2>6. Warranty and liability</h2>
<p>We work hard to make Montaroo reliable, but it is provided “as is” to the extent the law allows. We are not liable for indirect damage, lost profits or lost data caused by using the app, except where liability cannot be limited by law (for example for intentional harm or gross negligence). <b>If you are a consumer, nothing in this agreement limits your statutory rights</b>, including those under the consumer law of your country of residence.</p>

<h2>7. Ending the licence</h2>
<p>You can stop using Montaroo and uninstall it at any time. If you seriously break this agreement (for example by distributing cracked copies), your licence ends.</p>

<h2>8. Law and disputes</h2>
<p>This agreement is governed by Polish law. If you are a consumer, you also keep the protection of the mandatory laws of your country, and you may bring a claim in the courts of your country. Questions or complaints: {M}; we reply within 14 days.</p>
'''),
# ------------------------------------------------------------------ EULA PL
('eula', 'pl'): dict(
 path='pl/licencja/', title='Umowa licencyjna (EULA)', desc='Umowa licencyjna użytkownika końcowego aplikacji Montaroo dla Windows.',
 short='Możesz zainstalować Montaroo i robić nim filmy, za darmo albo w płatnej wersji. Filmy, które zrobisz, są twoje. Sama aplikacja pozostaje nasza, więc prosimy jej nie kopiować, nie odsprzedawać i nie łamać.',
 body=f'''
<p>Ta umowa zawierana jest między tobą a {OWNER_PL.replace('Daniel Popiel, prowadzący', 'Danielem Popielem, prowadzącym')} („my”), twórcą Montaroo. Instalując lub używając Montaroo, akceptujesz ją. Jeśli pobierasz Montaroo z Microsoft Store, do samego zakupu stosuje się też warunki sprzedaży Microsoft Store.</p>

<h2>1. Co możesz</h2>
<p>Udzielamy ci osobistej, niewyłącznej i niezbywalnej licencji na instalację i używanie Montaroo na urządzeniach z Windows, które posiadasz lub którymi zarządzasz, do projektów prywatnych i komercyjnych. Wersja darmowa i płatna (rozszerzenie „Montaroo”) różnią się tylko funkcjami opisanymi na montaroo.com i w Microsoft Store.</p>

<h2>2. Twoje filmy i pliki są twoje</h2>
<p>Wszystko, co dodajesz do Montaroo (filmy, zdjęcia, muzyka, tekst), i każdy film, który nim zrobisz, należy do ciebie albo do właściciela tych materiałów. Nie rościmy sobie do nich żadnych praw. Wersja darmowa może dodać krótką planszę „Edited in Montaroo”; możesz ją zostawić albo wyciąć we własnym montażu.</p>

<h2>3. Muzyka i inne materiały</h2>
<p>Odpowiadasz za to, żeby mieć prawa do muzyki, nagrań i innych materiałów, których używasz, zwłaszcza gdy publikujesz film. Muzyka dołączona do Montaroo pochodzi od autorów, którzy udostępnili ją na licencjach Creative Commons lub w domenie publicznej; gdy utwór wymaga podania autora, Montaroo pokazuje gotowy tekst do opisu filmu. Niektóre serwisy (np. YouTube Content ID) mogą mimo to oznaczyć licencjonowany utwór; nie mamy na to wpływu.</p>

<h2>4. Czego nie możesz</h2>
<p>Nie możesz sprzedawać, wynajmować, sublicencjonować ani udostępniać kopii Montaroo lub klucza licencji; usuwać ani obchodzić sprawdzania licencji lub płatnych funkcji; dekompilować ani modyfikować aplikacji, chyba że prawo wyraźnie na to pozwala (np. w celu zapewnienia interoperacyjności).</p>

<h2>5. Aktualizacje i wersje beta</h2>
<p>Możemy wydawać aktualizacje, które poprawiają błędy lub zmieniają funkcje. Wersje beta służą do testów, mogą zawierać błędy i przestać działać po wydaniu wersji końcowej. Zachowuj kopie oryginalnych plików; Montaroo nigdy ich nie przenosi ani nie zmienia, ale żaden program nie jest idealny.</p>

<h2>6. Gwarancja i odpowiedzialność</h2>
<p>Staramy się, żeby Montaroo działało niezawodnie, ale w zakresie dozwolonym przez prawo udostępniamy je „w stanie, w jakim jest”. Nie odpowiadamy za szkody pośrednie, utracone korzyści ani utratę danych wynikające z używania aplikacji, z wyjątkiem przypadków, w których prawo nie pozwala ograniczyć odpowiedzialności (np. szkody wyrządzone umyślnie lub przez rażące niedbalstwo). <b>Jeśli jesteś konsumentem, nic w tej umowie nie ogranicza twoich praw ustawowych</b>, w tym praw z ustawy o prawach konsumenta.</p>

<h2>7. Koniec licencji</h2>
<p>Możesz w każdej chwili przestać używać Montaroo i je odinstalować. Jeśli poważnie naruszysz tę umowę (np. rozpowszechniając złamane kopie), licencja wygasa.</p>

<h2>8. Prawo i spory</h2>
<p>Umowa podlega prawu polskiemu. Konsument zachowuje ochronę bezwzględnie obowiązujących przepisów swojego kraju i może dochodzić roszczeń przed sądem właściwym dla swojego miejsca zamieszkania. Pytania i reklamacje: {M}; odpowiadamy w ciągu 14 dni.</p>
'''),
}

UI = {
 'en': dict(updated='Last updated', back='Back to montaroo.com', home='', short='In short', privacy='Privacy', eula='EULA'),
 'pl': dict(updated='Ostatnia aktualizacja', back='Wróć na montaroo.com', home='pl/', short='W skrócie', privacy='Prywatność', eula='Licencja'),
}

CSS = r'''
@font-face{font-family:Gabarito;font-weight:800;font-display:swap;src:url(/assets/fonts/gabarito-latin-800-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F,U+2212}
@font-face{font-family:Gabarito;font-weight:800;font-display:swap;src:url(/assets/fonts/gabarito-latin-ext-800-normal.woff2) format("woff2");unicode-range:U+0100-024F}
@font-face{font-family:Inter;font-weight:400;font-display:swap;src:url(/assets/fonts/inter-latin-400-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F,U+2212}
@font-face{font-family:Inter;font-weight:400;font-display:swap;src:url(/assets/fonts/inter-latin-ext-400-normal.woff2) format("woff2");unicode-range:U+0100-024F}
@font-face{font-family:Inter;font-weight:600;font-display:swap;src:url(/assets/fonts/inter-latin-600-normal.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F,U+2212}
@font-face{font-family:Inter;font-weight:600;font-display:swap;src:url(/assets/fonts/inter-latin-ext-600-normal.woff2) format("woff2");unicode-range:U+0100-024F}
:root{--noc:#10251F;--ochra:#E2642A;--zloto:#F2B544;--piasek:#F4E9D6;--karta:#FBF6EC;--cichy:#3E5A50;--akcent:#B4471A;--link:#2F6553;--linia:#10251f24}
*{box-sizing:border-box}
body{margin:0;background:var(--piasek);color:var(--noc);font:400 17px/1.7 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--link);text-underline-offset:3px}a:hover{color:var(--noc)}
:focus-visible{outline:3px solid var(--zloto);outline-offset:3px;border-radius:4px}
.top{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px clamp(20px,5vw,56px)}
.top .logo{height:30px;width:auto;display:block}
.lang{font:600 14px/1 Inter,sans-serif;color:var(--noc);text-decoration:none;padding:12px 14px;border-radius:8px;box-shadow:inset 0 0 0 1px var(--linia)}
.lang:hover{background:var(--karta)}
main{max-width:46rem;margin:0 auto;padding:clamp(16px,4vw,48px) clamp(20px,5vw,32px) 72px}
.k{font:600 13px/16px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--akcent);margin:0 0 14px}
h1{font:800 clamp(38px,6vw,60px)/1 Gabarito,"Arial Rounded MT Bold",sans-serif;letter-spacing:-.035em;margin:0 0 14px;text-wrap:balance}
.date{color:var(--cichy);font-size:15px;margin:0 0 32px}
.tldr{background:var(--noc);color:var(--piasek);border-radius:18px 18px 18px 6px;padding:22px 26px;margin:0 0 44px}
.tldr b{display:block;font:800 19px/1.2 Gabarito,sans-serif;color:var(--zloto);margin-bottom:6px}
.tldr p{margin:0}
h2{font:800 23px/1.2 Gabarito,sans-serif;letter-spacing:-.01em;margin:40px 0 10px}
p{margin:0 0 14px}
footer{border-top:1px solid var(--linia);padding:24px clamp(20px,5vw,56px) 32px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:14px;color:var(--cichy)}
footer nav{display:flex;gap:18px;flex-wrap:wrap}
@media (max-width:600px){body{font-size:16px}.tldr{padding:18px 20px}footer{flex-direction:column}}
'''

def logo():
    s = open(os.path.join(ROOT, 'brand', 'logo', 'svg', 'montaroo-poziome-kolor.svg'), encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', '', s)
    return s.replace('<svg ', '<svg class="logo" role="img" aria-label="montaroo" ', 1)

def url(doc, lang): return 'https://montaroo.com/' + DOCS[(doc, lang)]['path']

def page(doc, lang):
    D, U = DOCS[(doc, lang)], UI[lang]
    other = 'pl' if lang == 'en' else 'en'
    O = DOCS[(doc, other)]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{D['title']} · Montaroo</title>
<meta name="description" content="{D['desc']}">
<link rel="canonical" href="{url(doc, lang)}">
<link rel="alternate" hreflang="{lang}" href="{url(doc, lang)}">
<link rel="alternate" hreflang="{other}" href="{url(doc, other)}">
<meta name="theme-color" content="#F4E9D6">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<style>{CSS}</style>
</head>
<body>
<header class="top"><a href="/{U['home']}" aria-label="montaroo">{logo()}</a><a class="lang" href="/{O['path']}" hreflang="{other}">{other.upper()}</a></header>
<main>
<p class="k">Montaroo</p>
<h1>{D['title']}</h1>
<p class="date">{U['updated']}: <time datetime="{ISO}">{UPDATED[lang]}</time></p>
<div class="tldr"><b>{U['short']}</b><p>{D['short']}</p></div>
{D['body'].strip()}
</main>
<footer><span>© 2026 Montaroo · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
<nav><a href="/{DOCS[('privacy', lang)]['path']}">{U['privacy']}</a><a href="/{DOCS[('eula', lang)]['path']}">{U['eula']}</a><a href="/{U['home']}">{U['back']}</a></nav></footer>
</body>
</html>
'''

if __name__ == '__main__':
    for (doc, lang) in DOCS:
        out = os.path.join(ROOT, DOCS[(doc, lang)]['path'], 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(page(doc, lang))
        print('ok', out)
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(
        'User-agent: *\nDisallow: /_zrodlo/\nDisallow: /warianty/\nDisallow: /kampania/zrodlo/\n\nSitemap: https://montaroo.com/sitemap.xml\n')
    pages = [('https://montaroo.com/', 'https://montaroo.com/pl/')] + \
            [(url(d, 'en'), url(d, 'pl')) for d in ('privacy', 'eula')]
    items = []
    for en, pl in pages:
        for loc in (en, pl):
            items.append(f'''<url><loc>{loc}</loc><lastmod>{ISO}</lastmod>
 <xhtml:link rel="alternate" hreflang="en" href="{en}"/><xhtml:link rel="alternate" hreflang="pl" href="{pl}"/></url>''')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(items) + '\n</urlset>\n')
    print('ok robots.txt, sitemap.xml')
