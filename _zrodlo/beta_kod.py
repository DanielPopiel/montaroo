"""Kod testera na stronie: wpisany w pole e-mail otwiera pobieranie wersji beta.

Użycie:  python _zrodlo/beta_kod.py <KOD> <ADRES_PACZKI>
         python _zrodlo/beta_kod.py --usun        (wyłącza trik)
Potem:   python _zrodlo/build_historia.py --bez-sync   (przebuduje index.html i pl/index.html)

Strona NIE zawiera ani kodu, ani adresu: adres jest zaszyfrowany (AES-GCM, klucz z kodu przez PBKDF2).
Kto nie zna kodu, nie wyciągnie adresu z kodu strony. Zapis: _zrodlo/beta_dostep.json.
"""
import base64, hashlib, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PLIK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beta_dostep.json')
ITER = 150000


def norm(k):
    return ''.join(k.lower().split())


def klucz(kod, sol):
    return hashlib.pbkdf2_hmac('sha256', norm(kod).encode('utf-8'), sol, ITER, 32)


def b(x):
    return base64.b64encode(x).decode()


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--usun':
        if os.path.exists(PLIK): os.remove(PLIK)
        print('trik wylaczony'); sys.exit()
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    kod, url = sys.argv[1], sys.argv[2]
    if len(norm(kod)) < 6: sys.exit('Kod za krótki (min. 6 znaków).')
    sol, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(klucz(kod, sol)).encrypt(iv, url.encode('utf-8'), None)
    json.dump({'s': b(sol), 'i': b(iv), 'c': b(ct), 'n': ITER}, open(PLIK, 'w'))
    print('zapisano', PLIK)
