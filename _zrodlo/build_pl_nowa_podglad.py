"""PODGLĄD (noindex) strony PL – preview/pl-nowa/. Formularz i piksel wyłączone. python _zrodlo/build_nowa_wersja_podglad.py
Treść zmian jest w nowa_wersja.py (ta sama, co na żywo w /pl/)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_historia as bh, nowa_wersja
R = bh.ROOT
s = bh.strona('pl').replace('../assets/', '../../assets/').replace('<title>Montaroo · Zamień nagrania z podróży w film', '<title>PODGLĄD · Montaroo')
s = nowa_wersja.ulepsz(s, 'pl', '../../', bh.hashp(os.path.join(bh.AH, 'historia.pl.v2.js')), podglad=True)
os.makedirs(f'{R}/preview/pl-nowa', exist_ok=True)
open(f'{R}/preview/pl-nowa/index.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
