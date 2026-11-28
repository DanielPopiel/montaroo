"""Nowa wersja strony PL (zatwierdzona 28.11.2026): hak-pytanie w kadrze zamiast bramki na cały ekran, film v2,
sekcje „Kto za tym stoi”, „Czym różni się Montaroo od…” i FAQ.
Używa: build_historia.py (strona na żywo, podglad=False) i build_pl_nowa_podglad.py (podglad=True)."""
import re


def ulepsz(s, pre='../', v2='1', podglad=False):
    def rep(a, b, n=1):
        nonlocal s
        assert a in s, 'pl_nowa: brak fragmentu ' + a[:80]
        s = s.replace(a, b) if n == 0 else s.replace(a, b, n)

    P = pre
    rep('<video id="vid" muted', f'<video id="vid" poster="{P}assets/video/film-20s-16x9-v2.jpg" muted')
    s = re.sub(r'historia\.pl\.js\?v=[0-9a-f]+', 'historia.pl.v2.js?v=' + v2, s)
    s = re.sub(r'<link[^>]*haczyk\.css[^>]*>', '', s)
    s = re.sub(r'<script[^>]*haczyk\.js[^>]*></script>\n?', '', s)
    rep('<p class="k">Darmowa beta · Windows</p>', '<p class="k">Nabór testerów · Windows</p>')
    rep('<h1>Zamień nagrania z podróży w film. <em>Automatycznie.</em></h1>',
        '<h1 id="h1">Setki nagrań z wyjazdu. <em>Ani jednego filmu?</em></h1>')
    rep('<p class="lead">Wrzuć folder', '<p class="lead"><b>Montaroo zmontuje go za ciebie.</b> Wrzuć folder')
    rep('<li>Wersja darmowa</li>', '<li>Beta za darmo</li>')
    rep('<button type="submit">Chcę wcześniejszy dostęp</button>', '<button type="submit">Zgłaszam się do testów</button>')
    rep('<p class="wl-note">Mail powitalny teraz, potem jeden, gdy ruszy beta na Windows. Bez spamu, wypisujesz się jednym kliknięciem.',
        '<p class="wl-note"><b>Pierwsi testerzy dostaną program przed premierą.</b> Od razu przyjdzie mail powitalny. Bez spamu, wypisujesz się jednym kliknięciem.')
    rep('</div>\n  <p class="cap">', '</div>\n  <button type="button" class="pf" id="pf">▶ Zobacz cały film z USA (20 s)</button>\n  <p class="cap">')

    T, N = '<span class="cmk">✓</span> ', '<span class="cmn">–</span> '
    wiersze = [
        ('Co dostajesz', 'Pełny film z całego wyjazdu', 'Skrót 15 s, 90 s albo dłuższy film', 'Film z wybranych ujęć'),
        ('Rozdziały po dniach i mapa trasy', T + 'Tak', N + 'Nie', N + 'Nie'),
        ('Kolejność wyjazdu', T + 'Zawsze chronologicznie', 'Program wybiera ujęcia', 'Może zmienić kolejność klipów'),
        ('Gdzie działa', 'Na twoim komputerze, bez internetu', 'Program na komputer', 'Aplikacja, wymaga konta Microsoft'),
        ('Cena', 'Jednorazowo, bez abonamentu (beta za darmo)', 'Za darmo ze znakiem wodnym, pełna wersja w abonamencie', 'Za darmo, eksport do 1080p'),
    ]
    marki = ('Montaroo', 'PowerDirector · Auto Edit', 'Clipchamp · auto compose')
    gl = '<div class="cr gl"><span></span>' + ''.join(f'<span>{m}</span>' for m in marki) + '</div>'
    rows = ''.join('<div class="cr"><span class="cl">' + w[0] + '</span>' +
                   ''.join(f'<span data-m="{m}">{c}</span>' for m, c in zip(marki, w[1:])) + '</div>' for w in wiersze)
    POR = f'''
<section class="nx por">
 <p class="k">Znasz inne programy?</p>
 <h2>Czym różni się Montaroo od PowerDirectora i Clipchampa</h2>
 <div class="ct" role="table" aria-label="Porównanie Montaroo z PowerDirector Auto Edit i Clipchamp auto compose">{gl}{rows}</div>
 <p class="pz"><b>Potrzebujesz 15-sekundowego klipu na Instagram?</b> Clipchamp wystarczy. <b>Chcesz film z całego wyjazdu, który obejrzysz za kilka lat?</b> Do tego jest Montaroo.</p>
 <p class="pzm">Według informacji producentów, stan na listopad 2026.</p>
</section>'''

    EXTRA = f'''
<section class="nx kto">
 <img src="{P}assets/mail/m3-list.jpg" alt="Kadry z filmu z road tripu po USA, zmontowanego w Montaroo" loading="lazy">
 <div><p class="k">Kto za tym stoi</p>
 <h2>Cześć, tu Daniel. Jestem pilotem.</h2>
 <p>Z każdego wyjazdu wracałem z setkami nagrań i żadnym filmem – bo kto ma wieczór na oś czasu? Więc napisałem program, który robi to za mnie. Film z naszego road tripu po USA złożył Montaroo z 1&nbsp;434 nagrań.</p>
 <p>Teraz szukam pierwszych osób, które sprawdzą go na swoich nagraniach. Każde zgłoszenie czytam sam.</p></div>
</section>{POR}
<section class="nx faq">
 <p class="k">Zanim się zapiszesz</p>
 <h2>Krótko o tym, co ważne</h2>
 <details open><summary>Ile to kosztuje?</summary><p>Beta jest darmowa. Po premierze Montaroo będzie płatne <b>jednorazowo, bez abonamentu</b>. Osoby z listy dostaną cenę na start, a testerzy, którzy wypełnią krótką ankietę, <b>50% zniżki</b> na pełną wersję.</p></details>
 <details><summary>Kiedy ruszy beta?</summary><p>Na początku 2027 roku. Osoby z listy dostaną zaproszenie jako pierwsze.</p></details>
 <details><summary>Jaki komputer jest potrzebny?</summary><p>Komputer z Windows. Dokładne wymagania podamy razem z zaproszeniem do bety.</p></details>
 <details><summary>Czy moje nagrania gdzieś wysyłacie?</summary><p>Nie. Montaroo działa offline – nagrania nie opuszczają twojego komputera.</p></details>
 <a class="cta2" href="#wl-e">Zgłaszam się do testów</a>
</section>
<dialog id="fd"><button type="button" id="fdx" aria-label="Zamknij">×</button><video controls playsinline preload="none" poster="{P}assets/video/film-20s-16x9-v2.jpg" src="{P}assets/video/film-20s-16x9-v2.mp4"></video></dialog>
<style>
.kh{{position:absolute;inset:0;z-index:8;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;background:radial-gradient(110% 120% at 50% 40%,#14302aee 0%,#0d1a16f2 60%,#070c0af7 100%);color:#F4E9D6;border-radius:inherit;transition:opacity .45s}}
.kh.out{{opacity:0;pointer-events:none}}
.kh .k1{{font:600 13px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#8FC3AE;margin:0 0 10px}}
.kh .k2{{font:800 clamp(28px,4.4vw,46px)/1.05 Gabarito,sans-serif;margin:0 0 22px;max-width:14ch}}
.kh .k2 em{{font-style:normal;color:#F2B544}}
.kh button{{font:700 16px Inter,sans-serif;border:0;border-radius:999px;padding:13px 24px;cursor:pointer;background:#E2642A;color:#10251F;box-shadow:0 0 0 4px #E2642A40}}
.kh .k3{{margin-top:12px;font:400 12px Inter,sans-serif;color:#F4E9D6aa;background:none;border:0;box-shadow:none;padding:4px;text-decoration:underline}}
.kh .kp{{position:absolute;left:24px;right:24px;bottom:18px;height:3px;background:#ffffff1f;border-radius:3px;overflow:hidden}}.kh .kp i{{display:block;height:100%;width:0;background:#F2B544;transition:width 5s linear}}
.player{{background:#10251F url({P}assets/video/film-20s-16x9-v2.jpg) center/cover}}
.pf{{display:block;margin:12px auto 0;background:none;border:0;color:var(--akcent);font:600 15px Inter,sans-serif;text-decoration:underline;cursor:pointer}}
.nx{{max-width:980px;margin:0 auto;padding:44px clamp(18px,4.5vw,56px)}}
.nx h2{{font-family:Gabarito,sans-serif;font-weight:800;font-size:clamp(26px,4vw,38px);line-height:1.08;color:var(--noc);margin:.2em 0 .5em}}
.nx p{{color:var(--cichy);font:16px/1.6 Inter,sans-serif;margin:0 0 .8em}}
.nx .k{{font:600 12px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#3E7C68;margin:0}}
.kto{{display:grid;grid-template-columns:1fr 1.1fr;gap:36px;align-items:center;border-top:1px solid #10251F14}}
.kto img{{width:100%;border-radius:16px;display:block}}
.ct{{border-radius:16px;overflow:hidden;background:var(--karta);box-shadow:0 1px 0 #10251F10;margin:6px 0 18px}}
.cr{{display:grid;grid-template-columns:1.05fr 1.15fr 1fr 1fr;border-top:1px solid #10251F12}}
.cr>span{{padding:13px 16px;font:15px/1.45 Inter,sans-serif;color:var(--cichy)}}
.cr>span:nth-child(2){{background:#10251F;color:#F4E9D6;font-weight:600}}
.cr .cl{{font-weight:700;color:var(--noc)}}
.cr.gl{{border-top:0}}.cr.gl>span{{font:700 13px Inter,sans-serif;letter-spacing:.04em;color:var(--noc)}}.cr.gl>span:nth-child(2){{color:#F2B544;font-size:15px}}
.ct .cmk{{color:#3E7C68;font-weight:800}}.cr>span:nth-child(2) .cmk{{color:#F2B544}}.ct .cmn{{color:#10251F55;font-weight:800}}
.pz{{font-size:17px!important}}.pz b{{color:var(--noc)}}.pzm{{font-size:12px!important;opacity:.75}}
.faq details{{background:var(--karta);border-radius:14px;padding:16px 20px;margin:0 0 10px;box-shadow:0 1px 0 #10251F10}}
.faq summary{{font:700 17px Inter,sans-serif;color:var(--noc);cursor:pointer}}
.faq details p{{margin:10px 0 0}}
.cta2{{display:block;text-align:center;margin-top:22px;background:var(--ochra);color:#FFFBF4;font:700 17px Inter,sans-serif;padding:16px;border-radius:14px;text-decoration:none}}
#fd{{border:0;padding:0;background:#000;border-radius:14px;max-width:min(92vw,1000px)}}#fd::backdrop{{background:#000c}}#fd video{{display:block;width:100%;max-height:85vh}}
#fdx{{position:absolute;right:8px;top:6px;z-index:2;background:#000a;color:#fff;border:0;font-size:26px;width:40px;height:40px;border-radius:50%}}
@media(max-width:900px){{.kto{{grid-template-columns:1fr;gap:20px}}.nx{{padding-top:30px;padding-bottom:30px}}}}
@media(max-width:700px){{.cr.gl{{display:none}}.cr{{grid-template-columns:1fr;padding:12px 0 6px}}.cr>span{{padding:3px 16px;font-size:14px}}
 .cr .cl{{font-size:15px;padding-bottom:6px}}.cr>span[data-m]::before{{content:attr(data-m);display:block;font:700 11px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;opacity:.65;margin-bottom:1px}}
 .cr>span:nth-child(2){{margin:0 10px 6px;border-radius:10px;padding:8px 12px}}.cr>span:nth-child(n+3){{padding-bottom:6px}}}}
</style>
<script>
(()=>{{const st=document.getElementById('stage');if(!st)return;document.body.setAttribute('data-hak','');
const k=document.createElement('div');k.className='kh';
k.innerHTML='<p class="k1">10 dni w USA · 1&nbsp;434 nagrania</p><p class="k2">Co z tego zrobi <em>Montaroo?</em></p><button type="button" data-d="1">▶ Pokaż z dźwiękiem</button><button type="button" class="k3" data-d="0">bez dźwięku</button><div class="kp"><i></i></div>';
const go=(d,a)=>{{if(k.dataset.x)return;k.dataset.x=1;k.classList.add('out');setTimeout(()=>k.remove(),500);const H=window.HIST;if(H){{H.skocz(0);H.dzwiek(!!d)}}
 try{{if(window.fbq)fbq('trackCustom','HaczykStart',{{wariant:'pytanie',dzwiek:d?1:0,auto:a?1:0}})}}catch(_){{}}}};
k.querySelectorAll('[data-d]').forEach(b=>b.onclick=()=>go(b.dataset.d==='1'));
const w=setInterval(()=>{{if(window.GOTOWE&&window.HIST){{clearInterval(w);window.HIST.zamroz(0.2);st.appendChild(k);
 const io=new IntersectionObserver(e=>{{if(e[0].isIntersecting){{io.disconnect();requestAnimationFrame(()=>k.querySelector('.kp i').style.width='100%');setTimeout(()=>go(false,1),5000)}}}},{{threshold:.5}});io.observe(st);}}}},60);}})();
(()=>{{const v=new URLSearchParams(location.search).get('v');const h=document.getElementById('h1');
if(v==='lot')h.innerHTML='Ten rok: setki nagrań. <em>Żadnego filmu.</em>';
const d=document.getElementById('fd');document.getElementById('pf').onclick=()=>{{d.showModal();d.querySelector('video').play()}};
document.getElementById('fdx').onclick=()=>{{d.querySelector('video').pause();d.close()}};}})();
</script>
'''
    if podglad:
        EXTRA += '''<div class="pod" style="position:fixed;right:8px;bottom:8px;opacity:.85;z-index:60;background:#E2642A;color:#10251F;font:700 11px Inter,sans-serif;letter-spacing:.08em;padding:6px 10px;border-radius:8px">PODGLĄD · nie wysyła zapisów</div>
<script>(()=>{const f=document.getElementById('wl');f.addEventListener('submit',e=>{e.preventDefault();e.stopImmediatePropagation();document.getElementById('wl-m').textContent='To podgląd – zapis nie został wysłany.'},true);})();</script>
'''
        rep('<head>', '<head>\n<meta name="robots" content="noindex,nofollow">')
        rep('window.mpx=()=>{', 'window.mpx=()=>{return;')
    rep('</main>', '</main>' + EXTRA)
    return s
