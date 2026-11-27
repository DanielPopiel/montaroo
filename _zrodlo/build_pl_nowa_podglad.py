"""PODGLĄD (noindex) proponowanej wersji montaroo.com/pl – preview/pl-nowa/. Formularz i piksel wyłączone. python _zrodlo/build_pl_nowa_podglad.py"""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/pl/index.html', encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, a[:80]
    s = s.replace(a, b) if n == 0 else s.replace(a, b, n)
rep('../assets/', '../../assets/', 0)
rep('<head>', '<head>\n<meta name="robots" content="noindex,nofollow">')
rep('<title>Montaroo · Zamień nagrania z podróży w film', '<title>PODGLĄD · Montaroo')
rep('<video id="vid" muted', '<video id="vid" poster="../../assets/video/film-20s-16x9.jpg" muted')
rep('window.mpx=()=>{', 'window.mpx=()=>{return;')               # bez piksela w podglądzie
rep('<p class="k">Darmowa beta · Windows</p>', '<p class="k">Nabór testerów · Windows</p>')
rep('<h1>Zamień nagrania z podróży w film. <em>Automatycznie.</em></h1>',
    '<h1 id="h1">Setki nagrań z wyjazdu. <em>Ani jednego filmu?</em></h1>')
rep('<p class="lead">Wrzuć folder', '<p class="lead"><b>Montaroo zmontuje go za ciebie.</b> Wrzuć folder')
rep('<li>Wersja darmowa</li>', '<li>Beta za darmo</li>')
rep('<button type="submit">Chcę wcześniejszy dostęp</button>', '<button type="submit">Zgłaszam się do testów</button>')
rep('<p class="wl-note">Mail powitalny teraz, potem jeden, gdy ruszy beta na Windows. Bez spamu, wypisujesz się jednym kliknięciem.',
    '<p class="wl-note"><b>Pierwsi testerzy dostaną program przed premierą.</b> Od razu przyjdzie mail powitalny. Bez spamu, wypisujesz się jednym kliknięciem.')
rep('</div>\n  <p class="cap">', '</div>\n  <button type="button" class="pf" id="pf">▶ Zobacz 20 s gotowego filmu z USA</button>\n  <p class="cap">')

EXTRA = '''
<section class="nx kto">
 <img src="../../assets/mail/m3-list.jpg" alt="Kadry z filmu z road tripu po USA, zmontowanego w Montaroo" loading="lazy">
 <div><p class="k">Kto za tym stoi</p>
 <h2>Cześć, tu Daniel. Jestem pilotem.</h2>
 <p>Z każdego wyjazdu wracałem z setkami nagrań i żadnym filmem – bo kto ma wieczór na oś czasu? Więc napisałem program, który robi to za mnie. Film z naszego road tripu po USA złożył Montaroo z 1&nbsp;434 nagrań.</p>
 <p>Teraz szukam pierwszych osób, które sprawdzą go na swoich nagraniach. Każde zgłoszenie czytam sam.</p></div>
</section>
<section class="nx faq">
 <p class="k">Zanim się zapiszesz</p>
 <h2>Krótko o tym, co ważne</h2>
 <details open><summary>Ile to kosztuje?</summary><p>Beta jest darmowa. <mark>[Do decyzji: cena po premierze, np. jednorazowo 249&nbsp;zł, i czy testerzy dostają zniżkę.]</mark></p></details>
 <details><summary>Kiedy ruszy beta?</summary><p><mark>[Do decyzji: przybliżony termin, np. „na początku 2027”.]</mark> Osoby z listy dostaną zaproszenie jako pierwsze.</p></details>
 <details><summary>Jaki komputer jest potrzebny?</summary><p>Komputer z Windows. <mark>[Do uzupełnienia: minimalne wymagania – wersja Windows, RAM, karta graficzna.]</mark></p></details>
 <details><summary>Czy moje nagrania gdzieś wysyłacie?</summary><p>Nie. Montaroo działa offline – nagrania nie opuszczają twojego komputera.</p></details>
 <a class="cta2" href="#wl-e">Zgłaszam się do testów</a>
</section>
<dialog id="fd"><button type="button" id="fdx" aria-label="Zamknij">×</button><video controls playsinline preload="none" poster="../../assets/video/probka-poster.jpg" src="../../assets/video/probka-usa.mp4"></video></dialog>
<div class="pod">PODGLĄD · nie wysyła zapisów</div>
<style>
.player{background:#10251F url(../../assets/video/film-20s-16x9.jpg) center/cover}
.pf{display:block;margin:12px auto 0;background:none;border:0;color:var(--akcent);font:600 15px Inter,sans-serif;text-decoration:underline;cursor:pointer}
.nx{max-width:980px;margin:0 auto;padding:44px clamp(18px,4.5vw,56px)}
.nx h2{font-family:Gabarito,sans-serif;font-weight:800;font-size:clamp(26px,4vw,38px);line-height:1.08;color:var(--noc);margin:.2em 0 .5em}
.nx p{color:var(--cichy);font:16px/1.6 Inter,sans-serif;margin:0 0 .8em}
.nx .k{font:600 12px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#3E7C68;margin:0}
.kto{display:grid;grid-template-columns:1fr 1.1fr;gap:36px;align-items:center;border-top:1px solid #10251F14}
.kto img{width:100%;border-radius:16px;display:block}
.faq details{background:var(--karta);border-radius:14px;padding:16px 20px;margin:0 0 10px;box-shadow:0 1px 0 #10251F10}
.faq summary{font:700 17px Inter,sans-serif;color:var(--noc);cursor:pointer}
.faq details p{margin:10px 0 0}
.faq mark{background:#F2B54455;color:var(--noc);padding:0 3px;border-radius:3px}
.cta2{display:block;text-align:center;margin-top:22px;background:var(--ochra);color:#FFFBF4;font:700 17px Inter,sans-serif;padding:16px;border-radius:14px;text-decoration:none}
#fd{border:0;padding:0;background:#000;border-radius:14px;max-width:min(92vw,1000px)}#fd::backdrop{background:#000c}#fd video{display:block;width:100%;max-height:85vh}
#fdx{position:absolute;right:8px;top:6px;z-index:2;background:#000a;color:#fff;border:0;font-size:26px;width:40px;height:40px;border-radius:50%}
.pod{position:fixed;right:8px;bottom:8px;opacity:.85;z-index:60;background:#E2642A;color:#10251F;font:700 11px Inter,sans-serif;letter-spacing:.08em;padding:6px 10px;border-radius:8px}
@media(max-width:900px){.kto{grid-template-columns:1fr;gap:20px}.nx{padding-top:30px;padding-bottom:30px}}
</style>
<script>
(()=>{const v=new URLSearchParams(location.search).get('v');const h=document.getElementById('h1');
if(v==='lot')h.innerHTML='Ten rok: setki nagrań. <em>Żadnego filmu.</em>';
const d=document.getElementById('fd');document.getElementById('pf').onclick=()=>{d.showModal();d.querySelector('video').play()};
document.getElementById('fdx').onclick=()=>{d.querySelector('video').pause();d.close()};
const f=document.getElementById('wl');f.addEventListener('submit',e=>{e.preventDefault();e.stopImmediatePropagation();document.getElementById('wl-m').textContent='To podgląd – zapis nie został wysłany.'},true);})();
</script>
'''
rep('</main>', '</main>' + EXTRA)
os.makedirs(f'{R}/preview/pl-nowa', exist_ok=True)
open(f'{R}/preview/pl-nowa/index.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
