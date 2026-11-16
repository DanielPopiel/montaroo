"""Rząd 4 siatki „Trasa skoku” (posty 10–12) – spoty z klipami AI, dokleja się NAD panoramą 9 postów.
Kafle od lewej: T10 Telefon (post 12), T11 Laptop (post 11), T12 The Hop (post 10).
Publikacja: najpierw post 10 (prawy kafel), na końcu post 12 (lewy) – jak w rzędach 1–3.
python rzad4.py [en|pl]"""
import io, os, sys, base64, subprocess
import cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trasa_lib import *

LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
TW, TH, EXT = 1080, 1440, 240
OUT = os.path.join(ROOT, 'kampania', 'trasa')
SRC = os.path.join(ROOT, 'kampania', 'higgsfield')
# post -> (kolumna, T, plik klipu, sekunda klatki, obrót karty, tekst)
TILES = {
 12: (0, 10, 'gemini_telefon.mp4', 4.2, -3.5,
      {'en': dict(k='STORAGE FULL', h=['47 GB from', 'one trip.'], s='Watched: 0.'),
       'pl': dict(k='PAMIĘĆ PEŁNA', h=['47 GB z jed-', 'nego wyjazdu.'], s='Obejrzane: 0.')}),
 11: (1, 11, 'gemini_laptop.mp4', 8.2, 3.0,
      {'en': dict(k='EVERY. SINGLE. TRIP.', h=['900 clips.', 'Editing? Days.'], s='With Montaroo: one hop.'),
       'pl': dict(k='PO KAŻDYM WYJEŹDZIE', h=['900 klipów.', 'Montaż? Dni.'], s='Z Montaroo: jeden skok.')}),
 10: (2, 12, 'canyon.mp4', 2.0, -2.5,
      {'en': dict(k='MEET MONTAROO', h=['From footage', 'to film.'], s='In one hop.'),
       'pl': dict(k='POZNAJ MONTAROO', h=['Od nagrań', 'do filmu.'], s='Jednym skokiem.')}),
}
if LANG == 'pl':   # krótsze łamanie dla PL
    TILES[12][5]['pl']['h'] = ['47 GB z jednego', 'wyjazdu.']

def frame_b64(fn, t):
    png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', os.path.join(SRC, fn), '-frames:v', '1',
                          '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    return base64.b64encode(png).decode()

def card(X, fn, t, rot, i):
    # karta-pocztówka 9:16 ze stopklatką, piaskowa ramka, cień
    w, h = 560, 820; cx, cy = X + TW / 2, 905
    img = frame_b64(fn, t)
    return (f'<defs><clipPath id="cc{i}"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="34"/></clipPath></defs>'
            f'<g transform="translate({cx} {cy}) rotate({rot})">'
            f'<rect x="{-w/2 - 18 + 14}" y="{-h/2 - 18 + 22}" width="{w + 36}" height="{h + 36}" rx="46" fill="#000" opacity=".35"/>'
            f'<rect x="{-w/2 - 18}" y="{-h/2 - 18}" width="{w + 36}" height="{h + 36}" rx="46" fill="{SAND}"/>'
            f'<image href="data:image/png;base64,{img}" x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#cc{i})"/>'
            f'<circle cx="0" cy="0" r="62" fill="{INK}" opacity=".55"/>'
            f'<path d="M-18 -30L32 0L-18 30Z" fill="{SAND}"/></g>')

def tile_text(d, X):
    x = X + 84; s, _ = text(d['k'], 'I6', 30, x, 150, track=0.14, fill=GOLD)
    y = 150 + 40 + 96 * 0.86
    for line in d['h']:
        p, w = text(line, 'G', 96, x, y, track=-0.035, fill=SAND); assert w < TW - 150, (line, w); s += p; y += 96 * 0.97
    p, _ = text(d['s'], 'I5', 36, x, y - 96 * 0.97 + 66, fill=GOLD, opacity=.9)
    return s + p

if __name__ == '__main__':
    W, H, G = 3 * TW, TH, 1385
    bg = (f'<rect x="-10" y="{-EXT - 10}" width="{W + 20}" height="{H + 2 * EXT + 20}" fill="{INK}"/>'
          f'<g transform="translate(0 1440)">' + contours(W, 0, 0, [(500, 2600, 55, 0.9), (1700, 300, 45, 1.9), (2900, 1900, 60, 2.6)], seed=7, step=72, n=24) + '</g>')
    # szlak u dołu rzędu, łączy karty; joey w locie między kartą 2 i 3
    hops = [((-20, G), (380, G), 100), ((380, G), (820, G), 120), ((820, G), (1360, G), 230),
            ((1360, G), (1900, G), 110), ((1900, G), (2450, G), 330), ((2450, G), (3100, G), 120)]
    d = hop(*hops[0][0], *hops[0][1], hops[0][2])
    for a, b, h in hops[1:]: d += 'Q' + hop(*a, *b, h).split('Q')[1]
    scene = trail(d, w=11, dash='22 22')
    for i, (post, (c, T, fn, t, rot, tx)) in enumerate(TILES.items()):
        scene += card(c * TW, fn, t, rot, i)
    x, y, ang = hop_point(*hops[4][0], *hops[4][1], hops[4][2], 0.5)
    scene += joey(x, y - 60, 130, rot=ang * 0.35)
    texts = ''.join(tile_text(tx[LANG], c * TW) for post, (c, T, fn, t, rot, tx) in TILES.items())
    def render(body):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H + 2 * EXT}" '
               f'viewBox="0 {-EXT} {W} {H + 2 * EXT}">{body}</svg>')
        return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGB')
    full = render(bg + scene + texts); bgo = render(bg)
    sfx = '' if LANG == 'en' else '_pl'
    row = full.crop((0, EXT, W, EXT + H)); row.save(f'{OUT}/panorama_rzad4{sfx}.png')
    for post, (c, T, *_r) in TILES.items():
        tile = full.crop((c * TW, EXT, (c + 1) * TW, EXT + TH)); tile.save(f'{OUT}/kafel-T{T}_post-{post}{sfx}.png')
        cov = bgo.crop((c * TW, 0, (c + 1) * TW, H + 2 * EXT)); cov.paste(tile, (0, EXT)); cov.save(f'{OUT}/okladka-post-{post}_T{T}{sfx}.png')
    if LANG == 'en':
        old = Image.open(f'{OUT}/panorama_9.png')
        allp = Image.new('RGB', (W, 4 * H)); allp.paste(row, (0, 0)); allp.paste(old, (0, H)); allp.save(f'{OUT}/panorama_12.png')
    print('ok')
