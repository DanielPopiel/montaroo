# montaroo.com

Strona produktu Montaroo (automatyczny montaż filmów z podróży, Windows, offline) + pliki marki i kampanii.

- `index.html` – strona EN, `pl/index.html` – PL. **Nie edytuj ich ręcznie** – generuje je `_zrodlo/build_site.py` (teksty obu języków są w słowniku `T` na górze pliku). Po zmianie: `python _zrodlo/build_site.py`.
- `DOWNLOAD_URL` w `build_site.py`: gdy instalator będzie gotowy, wpisz adres pliku – przyciski zmienią się z „Get the Windows beta” na „Download for Windows”.
- `assets/` – CSS, JS, fonty (Gabarito 800, Inter), wideo (hero, próbka bez dźwięku), obrazy, favicon.
- `brand/` – logo (SVG/PNG/ICO, generator w `brand/logo/zrodlo/`), fonty, kopia księgi marki.
- `kampania/` – spot (16:9 i 9:16, EN/PL), posty 1080×1350, źródła generatorów.
- `CNAME` – domena dla GitHub Pages (montaroo.com).

Księga marki: https://claude.ai/artifact/G97krjLu43aei4xafaxjef
