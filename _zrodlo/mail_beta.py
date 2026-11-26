"""5 wariantów maila powitalnego PL – rekrutacja testerów bety. Wyjście: kampania/mail-beta/mail_beta_N.html (do MailerLite, obrazy z montaroo.com)
oraz PREZENTACJA_mail_beta.html (podgląd, obrazy lokalne).  python _zrodlo/mail_beta.py"""
import os, json, html as H
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f'{R}/kampania/mail-beta'; os.makedirs(OUT, exist_ok=True)
F = 'font-family:Inter,Segoe UI,Helvetica,Arial,sans-serif;'
MAILTO = 'mailto:hello@montaroo.com?subject=Beta%20Montaroo%20%E2%80%93%20chc%C4%99%20testowa%C4%87'
P = lambda t, mb=14: f'<p style="margin:0 0 {mb}px;font-size:16px;line-height:26px;">{t}</p>'

def ask(btn):
    return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4E9D6;border-radius:12px;margin:8px 0 22px;"><tr><td style="padding:18px 20px;{F}font-size:15px;line-height:23px;color:#10251F;">
<strong>Czego potrzebuję od testera:</strong><br>• komputer z Windows<br>• folder z nagraniami z jakiegoś wyjazdu (telefon, GoPro, DJI – co masz)<br>• ok. 15 minut na krótką ankietę po pierwszym filmie
</td></tr></table>
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:#E2642A;border-radius:999px;">
<a href="{MAILTO}" style="display:inline-block;padding:14px 28px;{F}font-size:16px;font-weight:700;color:#FFFBF4;text-decoration:none;">{btn}</a></td></tr></table>
<p style="margin:12px 0 0;font-size:13px;line-height:20px;color:#5b6b66;">Albo po prostu odpisz na tego maila – trafia prosto do mnie.</p>'''

SIG = '<p style="margin:28px 0 0;font-size:15px;line-height:24px;">Daniel<br><span style="color:#3E7C68;">twórca Montaroo, pilot liniowy</span></p>'

MAILS = [
 dict(nazwa='Karta pokładowa', img='m1-karta.jpg', alt='Karta pokładowa Montaroo: z FOLDER do FILM, miejsce: Tester',
  pre='Masz miejsce na pokładzie. Szukam pierwszych testerów Montaroo.', eyebrow='Beta · nabór testerów',
  h1='Masz miejsce na pokładzie. Szukam pierwszych testerów.',
  body=P('Dzięki za zapis! Montaroo to program na Windows, który z nagrań z wyjazdu sam układa film: rozdziały po dniach, cięcia do rytmu muzyki, podpisy miejsc i mapę trasy. Działa offline – nagrania nie opuszczają twojego komputera.')
      +P('Zanim program trafi do sklepu, chcę, żeby <strong>20 osób</strong> zmontowało nim prawdziwy film z własnego wyjazdu. Każdy błąd, który znajdziesz, to jeden mniej u kolejnych osób.', 18),
  btn='Odpisz „TAK” – biorę miejsce'),
 dict(nazwa='1 434 nagrania → 1 film (GIF)', img='m2-folder-film.gif', alt='Siatka 1 434 nagrań zamienia się w jeden kadr filmu',
  pre='10 dni, 1 434 nagrania, jeden film. Szukam testerów.', eyebrow='Lista oczekujących',
  h1='10 dni w USA. 1 434 nagrania. Jeden film.',
  body=P('Tyle nagrań przywiozłem z road tripu po parkach narodowych. Znasz to: wszystko leży w folderze i nikt tego nigdy nie obejrzy.')
      +P('Montaroo przegląda cały folder, wybiera najlepsze momenty, tnie je do rytmu muzyki i dokłada plansze z nazwami miejsc. Offline, na Windowsie.')
      +P('<strong>Masz podobny folder?</strong> Szukam osób, które sprawdzą program na swoich nagraniach, zanim ruszy dla wszystkich.', 18),
  btn='Chcę przetestować na swoich nagraniach'),
 dict(nazwa='List od pilota', img='m3-list.jpg', alt='Zdjęcia z filmu z road tripu po USA',
  pre='Latam Boeingiem 737. Napisałem program, który robi filmy z wyjazdów.', eyebrow='Od twórcy',
  h1='Cześć, tu Daniel. Latam 737 i mam do ciebie prośbę.',
  body=P('Na co dzień siedzę w kokpicie, a po pracy podróżuję. Przez lata zbierałem setki nagrań z każdego wyjazdu i ani jednego filmu – bo kto ma na to wieczór przy osi czasu?')
      +P('Więc napisałem program, który robi to za mnie. Zdjęcia wyżej są z filmu, który Montaroo złożył z naszego road tripu po USA.')
      +P('Teraz potrzebuję ludzi, którzy wrzucą do niego <strong>swoje</strong> nagrania i powiedzą mi szczerze, co działa, a co nie. Czytam każdą odpowiedź sam.', 18),
  btn='Pomogę – odpisz „beta”'),
 dict(nazwa='Kadr z gotowego filmu', img='m4-kadr.jpg', alt='Kadr z filmu: plansza Monument Valley, opisy funkcji Montaroo',
  pre='Te napisy, cięcia i wybór ujęć zrobił program. Szukam testerów.', eyebrow='Tak wygląda efekt',
  h1='Ten kadr złożył program. Ja tylko wrzuciłem folder.',
  body=P('To klatka z filmu z naszego wyjazdu do USA. Montaroo sam:')
      +'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 18px;">'
      +''.join(f'<tr><td valign="top" style="padding:0 12px 10px 0;"><span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:#E2642A;color:#10251F;font:700 14px/26px Inter,Arial,sans-serif;text-align:center;">{n}</span></td><td style="padding:2px 0 10px;{F}font-size:16px;line-height:24px;color:#10251F;">{t}</td></tr>'
               for n, t in [(1,'podpisał miejsce na podstawie GPS z nagrania,'),(2,'wybrał najlepsze ujęcia z całego dnia,'),(3,'pociął je w rytm muzyki i ułożył w rozdziały.')])
      +'</table>'+P('Chcę zobaczyć, jak poradzi sobie z <strong>twoimi</strong> nagraniami. Szukam pierwszych testerów.', 18),
  btn='Chcę taki film ze swojego wyjazdu'),
 dict(nazwa='Przed i po', img='m5-przed-po.jpg', alt='Przed: folder z plikami VID. Po: kadr gotowego filmu',
  pre='Od folderu do filmu, bez osi czasu. Szukam testerów – w zamian pełna wersja.', eyebrow='Beta · nabór testerów',
  h1='Od folderu do filmu. Bez osi czasu.',
  body=P('Po lewej: tak wygląda folder po wyjeździe. Po prawej: kadr z filmu, który Montaroo z niego złożył – z rozdziałami, muzyką i podpisami miejsc.')
      +P('Szukam osób, które przetestują to na swoich nagraniach, zanim program ruszy dla wszystkich.')
      +'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:2px solid #E2642A;border-radius:12px;margin:4px 0 18px;"><tr><td style="padding:16px 20px;'+F+'font-size:16px;line-height:24px;color:#10251F;"><strong style="color:#E2642A;">Uczciwa wymiana:</strong> ty dajesz 15 minut opinii, ja daję ci <strong>pełną wersję Montaroo za darmo</strong> na start.</td></tr></table>',
  btn='Wchodzę – odpisz „TAK”'),
]

def btn3():
    out = '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 4px;"><tr>'
    for t in ['Telefon', 'GoPro', 'Dron DJI']:
        subj = ('Beta Montaroo – nagrywam: ' + t).replace(' ', '%20').replace('–', '%E2%80%93')
        out += f'<td style="padding:0 4px 8px;" width="33%"><a href="mailto:hello@montaroo.com?subject={subj}" style="display:block;text-align:center;border:2px solid #E2642A;border-radius:12px;padding:14px 6px;{F}font-size:16px;font-weight:700;color:#10251F;text-decoration:none;">{t}</a></td>'
    return out + '</tr></table><p style="margin:6px 0 0;font-size:13px;line-height:20px;color:#5b6b66;">Kliknij jedno – otworzy się gotowa odpowiedź. Możesz dopisać zdanie od siebie.</p>'

MAILS += [
 dict(nazwa='Jedno pytanie: czym nagrywasz?', img='m6-pytanie.jpg', alt='Czym nagrywasz? Telefon, GoPro, dron',
  pre='Jedno pytanie, jedno kliknięcie. Szukam testerów Montaroo.', eyebrow='Nabór do bety',
  h1='Jedno kliknięcie i jesteś w kolejce do bety.',
  body=P('Dzięki za zapis! Montaroo to program na Windows, który z nagrań z wyjazdu sam układa film – z rozdziałami, muzyką i podpisami miejsc. Offline, nagrania zostają u ciebie.')
      +P('Szukam pierwszych testerów i chcę dobrać ich tak, żeby sprawdzić każdy sprzęt. <strong>Kliknij, czym nagrywasz najczęściej</strong> – to zgłoszenie do bety:', 16),
  ask_html=btn3()),
 dict(nazwa='Rozdziały na taśmie filmowej', img='m7-rozdzialy.jpg', alt='Trzy rozdziały filmu: W drodze, Grand Canyon, Monument Valley',
  pre='Twój wyjazd w rozdziałach, które program ułoży sam. Szukam testerów.', eyebrow='Lista oczekujących',
  h1='Twój wyjazd, opowiedziany w rozdziałach.',
  body=P('Tak wygląda film z naszego road tripu po USA. Nie układałem go ręcznie: Montaroo rozpoznał dni i miejsca, podzielił nagrania na rozdziały i dodał do nich plansze.')
      +P('Droga, helikopter nad Grand Canyon, wschód słońca w Monument Valley – każdy rozdział ma swój rytm i swoją muzykę.')
      +P('Teraz chcę sprawdzić, jak program opowie <strong>twój</strong> wyjazd. Szukam pierwszych testerów.', 18),
  btn='Chcę zobaczyć swój wyjazd w rozdziałach'),
 dict(nazwa='Zwykły list (bez grafiki)', img='', alt='',
  pre='Krótko: szukam kilku osób do testów. Pomożesz?', eyebrow='Od Daniela',
  h1='Krótko i po ludzku.',
  body=P('Cześć,')
      +P('dzięki za zapis na listę Montaroo. Piszę sam, bez działu marketingu, bo go nie ma.')
      +P('Na co dzień jestem pilotem. Po godzinach napisałem program na Windows, który z folderu nagrań z wyjazdu robi gotowy film. Działa offline. Zmontowałem nim film z naszego wyjazdu do USA:')
      +'<a href="https://montaroo.com/pl/" style="display:block;margin:4px 0 18px;"><img src="__BASE__m8-miniatura.jpg" width="280" alt="Zobacz 20 sekund filmu" style="display:block;width:280px;max-width:100%;height:auto;border:0;border-radius:10px;"></a>'
      +P('Zanim pokażę go szerzej, potrzebuję kilku osób, które sprawdzą go na swoich nagraniach i powiedzą mi wprost, co jest nie tak. Jeśli masz chwilę – odpisz jednym słowem: <strong>„beta”</strong>.', 18),
  btn='Odpisuję „beta”'),
 dict(nazwa='Miniatura z przyciskiem play', img='m9-play.jpg', alt='Kadr z filmu Montaroo z przyciskiem odtwarzania',
  pre='20 sekund, które zmontował program. Zobacz i zgłoś się do testów.', eyebrow='Zobacz efekt',
  h1='20 sekund, które zmontował program – nie człowiek.',
  body='<p style="margin:0 0 14px;font-size:16px;line-height:26px;"><a href="https://montaroo.com/pl/" style="color:#E2642A;font-weight:700;">▶ Obejrzyj na montaroo.com</a></p>'
      +P('Wybór ujęć, cięcia w rytm muzyki, plansze z nazwami miejsc – wszystko to Montaroo zrobił sam z folderu nagrań z naszego wyjazdu.')
      +P('Jeśli chcesz zobaczyć taki film ze <strong>swoich</strong> nagrań, zanim program trafi do wszystkich – szukam pierwszych testerów.', 18),
  btn='Chcę taki film – zgłaszam się'),
 dict(nazwa='20 miejsc w pierwszej rundzie', img='m10-miejsca.jpg', alt='20 miejsc w pierwszej rundzie testów',
  pre='Pierwsza runda testów: 20 miejsc dla osób z listy.', eyebrow='Pierwsza runda testów',
  h1='20 miejsc. Osoby z listy mają pierwszeństwo.',
  body=P('Dzięki za zapis! Montaroo – program na Windows, który z nagrań z wyjazdu sam robi film – jest gotowy na pierwsze testy poza moim komputerem.')
      +P('W pierwszej rundzie zapraszam <strong>20 osób</strong>. Najpierw z tej listy, potem z zewnątrz. Każdy tester dostaje wersję testową, krótką instrukcję i bezpośredni kontakt ze mną.')
      +P('Jeśli chcesz jedno z miejsc, daj znać teraz – zapisuję w kolejności zgłoszeń.', 18),
  btn='Rezerwuję miejsce'),
]

def mail(m, base):
    return f'''<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only">
<title>{H.escape(m["h1"])}</title><style>body{{margin:0;padding:0;background:#F4E9D6}}a{{color:#E2642A}}@media (max-width:620px){{.wrap{{width:100%!important}}.pad{{padding-left:22px!important;padding-right:22px!important}}h1{{font-size:26px!important;line-height:32px!important}}}}</style></head>
<body style="margin:0;padding:0;background:#F4E9D6;"><div style="display:none;max-height:0;overflow:hidden;opacity:0;">{H.escape(m["pre"])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4E9D6;"><tr><td align="center" style="padding:28px 10px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFBF4;border-radius:14px;overflow:hidden;">
<tr><td style="background:#10251F;padding:24px 40px 20px;" class="pad"><a href="https://montaroo.com/pl/" style="text-decoration:none;"><img src="https://montaroo.com/brand/logo/png/montaroo-poziome-kolor-ciemne.png" width="170" alt="montaroo" style="display:block;width:170px;height:auto;border:0;"></a></td></tr>
{'' if not m.get("img") else f'<tr><td style="background:#10251F;padding:0;"><img src="{base}{m["img"]}" width="600" alt="{H.escape(m["alt"])}" style="display:block;width:100%;max-width:600px;height:auto;border:0;"></td></tr>'}
<tr><td style="height:6px;background:#E2642A;line-height:6px;font-size:6px;">&nbsp;</td></tr>
<tr><td class="pad" style="padding:34px 40px 36px;{F}color:#10251F;">
<p style="margin:0 0 10px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#3E7C68;font-weight:700;">{m["eyebrow"]}</p>
<h1 style="margin:0 0 16px;font-size:30px;line-height:36px;font-weight:800;color:#10251F;">{m["h1"]}</h1>
{m["body"].replace("__BASE__", base)}{m.get("ask_html") or ask(m["btn"])}{SIG}</td></tr>
<tr><td class="pad" style="background:#10251F;padding:22px 40px;{F}font-size:12px;line-height:19px;color:#F4E9D6;"><strong style="color:#F2B544;">Hop from footage to film.</strong><br>Dostajesz tego maila, bo zapisałeś(-aś) się na listę oczekujących na montaroo.com.<br><a href="{{$unsubscribe}}" style="color:#F2B544;">Wypisz się</a></td></tr>
</table></td></tr></table></body></html>'''

prev = []
for i, m in enumerate(MAILS, 1):
    open(f'{OUT}/mail_beta_{i}.html', 'w', encoding='utf-8').write(mail(m, 'https://montaroo.com/assets/mail/'))
    prev.append((m['nazwa'], m['pre'], mail(m, '__IMG__')))
json.dump([[n, p, h] for n, p, h in prev], open('/tmp/mail_prev.json', 'w'), ensure_ascii=False)
print('ok', len(MAILS))
