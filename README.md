# montaroo.com

Strona produktu Montaroo (automatyczny montaż filmów z podróży, Windows, offline) + pliki marki i kampanii.

- **Teraz (przed premierą):** `index.html` i `pl/index.html` to strona główna z nagłówkiem, formularzem listy oczekujących i sceną „Historia” (animacja 14 s: intro → telefony przez QR → ściana z kangurkiem → muzyka → panel montażu → film 20 s; jedna muzyka, dźwięk po dotknięciu). Generuje ją `_zrodlo/build_historia.py`, który przy okazji **kopiuje najnowsze pliki sceny z makiet Daniela** (`Kampania reklamowa/5_Strona-3D/makiety`) do `assets/historia/` i `assets/video/`: odświeżenie = `python _zrodlo/build_historia.py` (bez kopiowania: `--bez-sync`). Piksel Meta: `MONTAROO_PIXEL=<ID> python _zrodlo/build_historia.py`. Test: `python -m http.server 8870 --bind 127.0.0.1` + `node _zrodlo/test_strona.mjs http://127.0.0.1:8870/pl/ 390 844 <folder> mobile`. Cennika na stronie jeszcze nie ma (po założeniu sklepu). Stara strona „w budowie” (joey w kasku) nadal da się zbudować przez `_zrodlo/build_soon.py`, ale to **nadpisze** index.html – nie uruchamiaj go po build_historia.
- Pełna strona produktu jest w `preview/` (EN) i `preview/pl/` (PL), ukryta przed wyszukiwarkami. Generuje ją `_zrodlo/build_site.py` (teksty w słowniku `T`). Na premierę: w `build_site.py` zmienić zapis z `preview/` z powrotem na katalog główny.
- Plików HTML nie edytuj ręcznie – po zmianie uruchom odpowiedni skrypt.
- `DOWNLOAD_URL` w `build_site.py`: gdy instalator będzie gotowy, wpisz adres pliku – przyciski zmienią się z „Get the Windows beta” na „Download for Windows”.
- `assets/` – CSS, JS, fonty (Gabarito 800, Inter), wideo (hero, próbka bez dźwięku), obrazy, favicon.
- `brand/` – logo (SVG/PNG/ICO, generator w `brand/logo/zrodlo/`), fonty, kopia księgi marki.
- `kampania/` – spot (16:9 i 9:16, EN/PL), posty 1080×1350, źródła generatorów.
- `CNAME` – domena dla GitHub Pages (montaroo.com).

Księga marki: https://claude.ai/artifact/G97krjLu43aei4xafaxjef
