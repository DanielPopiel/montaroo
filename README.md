# montaroo.com

Strona produktu Montaroo (automatyczny montaż filmów z podróży, Windows, offline) + pliki marki i kampanii.

- **Teraz (przed premierą):** `index.html` i `pl/index.html` to strona „w budowie” z animacją (joey w kasku, klipy wskakują do torby). Generuje ją `_zrodlo/build_soon.py`.
- Pełna strona produktu jest w `preview/` (EN) i `preview/pl/` (PL), ukryta przed wyszukiwarkami. Generuje ją `_zrodlo/build_site.py` (teksty w słowniku `T`). Na premierę: w `build_site.py` zmienić zapis z `preview/` z powrotem na katalog główny.
- Plików HTML nie edytuj ręcznie – po zmianie uruchom odpowiedni skrypt.
- `DOWNLOAD_URL` w `build_site.py`: gdy instalator będzie gotowy, wpisz adres pliku – przyciski zmienią się z „Get the Windows beta” na „Download for Windows”.
- `assets/` – CSS, JS, fonty (Gabarito 800, Inter), wideo (hero, próbka bez dźwięku), obrazy, favicon.
- `brand/` – logo (SVG/PNG/ICO, generator w `brand/logo/zrodlo/`), fonty, kopia księgi marki.
- `kampania/` – spot (16:9 i 9:16, EN/PL), posty 1080×1350, źródła generatorów.
- `CNAME` – domena dla GitHub Pages (montaroo.com).

Księga marki: https://claude.ai/artifact/G97krjLu43aei4xafaxjef
