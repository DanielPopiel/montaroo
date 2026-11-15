"""Siatka IG „Trasa skoku”: panorama 3×2 kafelki 1080×1440 (3:4) + okładki Reeli 1080×1920.
Kafelki numerowane jak na profilu (T1 lewy górny … T6 prawy dolny).
Publikacja od końca: post 1 = T6, post 6 = T1 (Instagram wstawia najnowszy w lewy górny róg)."""
import io, os, sys, json
import cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trasa_lib import *

TW, TH = 1080, 1440
W, H = 3 * TW, 2 * TH
EXT = 240                         # okładka 1920 = kafelek 1440 + 240 u góry i u dołu
OUT = os.path.join(ROOT, 'kampania', 'trasa')
os.makedirs(OUT, exist_ok=True)

# --- teksty (EN, konta marki) ---
TILES = {
 1: dict(k='Sound familiar?', h=['1,434 clips.', 'Never watched.'], s='Every trip ends up in a folder.', size=124),
 2: dict(k='Roo fact #4', h=['A kangaroo can', 'clear 8 m in', 'one hop.'], s='Montaroo gets footage to film in one.', size=112),
 3: dict(k='Roo fact #3', h=['A joey stays', 'in the pouch', 'for 8 months.'], s='Your footage never leaves it. Offline.', size=112),
 4: dict(k='Roo fact #2', h=['Kangaroos', "don't hop", 'backwards.'], s='Neither do we. Folder in, film out.', size=124),
 5: dict(k='Family trips', h=['5 phones.', '1 film.'], s="Everyone's footage. One story.", size=150),
 6: dict(k='Roo fact #1', h=['A group of', 'kangaroos is', 'called a mob.'], s='Join ours. Link in bio.', size=112),
}
POST_OF_TILE = {t: 7 - t for t in TILES}   # T6 = post 1 … T1 = post 6

def tile_xy(t):
    c = (t - 1) % 3; r = (t - 1) // 3
    return c * TW, r * TH

def text_block(t):
    x0, y0 = tile_xy(t); d = TILES[t]; x = x0 + 84
    s, _ = text(d['k'].upper(), 'I6', 30, x, y0 + 236, track=0.14, fill=GOLD)
    y = y0 + 236 + 40 + d['size'] * 0.86
    for line in d['h']:
        p, w = text(line, 'G', d['size'], x, y, track=-0.035, fill=SAND)
        assert w < TW - 150, (t, line, w)
        s += p; y += d['size'] * 0.97
    p, _ = text(d['s'], 'I4', 36, x, y - d['size'] * 0.97 + 74, fill=SAND, opacity=.72)
    return s + p

# --- scena: wiersz 1 (y ziemi 1200) ---
G1, G2 = 1200, TH + 1200
HOPS1 = [((500, 1010), (880, G1), 170), ((880, G1), (2060, G1), 300),
         ((2060, G1), (3130, 1150), 330), ((3130, 1150), (3560, 1150), 130)]
HOPS2 = [((-330, G2 - 40), (250, G2), 150), ((250, G2), (560, G2), 140), ((560, G2), (870, G2), 140),
         ((870, G2), (1170, G2), 140), ((1170, G2), (2110, G2), 450), ((2110, G2), (2340, G2 - 70), 150)]

def path_of(hops):
    d = ''
    for (a, b, h) in hops:
        seg = hop(*a, *b, h)
        d += seg if not d else 'Q' + seg.split('Q')[1]
    return d

def scene():
    s = ''
    # T1 – stos klipów
    rnd = random.Random(7); cols = [OCH, GOLD, EUC, SAND, '#2C5A4B', OCH, GOLD, SAND, EUC]
    pile = [(150, 1240, -8), (300, 1250, 6), (450, 1245, -3), (220, 1160, 12), (380, 1170, -10), (300, 1088, 4),
            (470, 1150, 15), (140, 1310, 3), (420, 1325, -6), (260, 1330, 9)]
    for i, (x, y, r) in enumerate(sorted(pile, key=lambda p: -p[1])):
        s += clip_card(x, y, 190, 124, r, cols[i % len(cols)], INK)
    # wymiar „8 m” pod wielkim skokiem
    yd = 1290
    s += f'<path d="M880 {yd}H2060M880 {yd-22}V{yd+22}M2060 {yd-22}V{yd+22}" stroke="{SAND}" stroke-width="4" opacity=".55"/>'
    lab, lw = text('8 m', 'I6', 40, 1470, yd + 14, fill=SAND, anchor='middle')
    s += f'<rect x="{1470-lw/2-22:.0f}" y="{yd-34}" width="{lw+44:.0f}" height="64" fill="{INK}"/>' + lab
    # T3 – torba (znak) pod łukiem
    s += mark(2600, 1130, 540, joeycol=SAND, pouchcol=OCH, stitchcol=INK)
    # T5 – wachlarz telefonów
    for x, r, f, sc in [(1405, -10, EUC, INK), (1525, -4, OCH, INK), (1645, 1, GOLD, INK), (1765, 6, SAND, INK), (1885, 11, '#2C5A4B', INK)]:
        s += phone(x, G2 - 105, 108, 216, r, f, sc)
        s += f'<g transform="translate({x} {G2-110}) rotate({r})"><path d="M-14 -22L24 0L-14 22Z" fill="{f}" stroke="{f}" stroke-width="8" stroke-linejoin="round"/></g>'
    # T6 – stado (mob)
    for x, h, f in [(2420, 190, SAND), (2600, 300, GOLD), (2790, 230, SAND), (2960, 340, OCH), (3120, 170, SAND)]:
        s += joey(x, G2 - h / 2, h, fill=f)
    # trasa
    s += trail(path_of(HOPS1), w=11, dash='22 22') + trail(path_of(HOPS2), w=11, dash='22 22')
    # T4 – strzałki „tylko do przodu” na szczytach skoków
    for (a, b, h) in HOPS2[1:4]:
        x, y, _ = hop_point(*a, *b, h, 0.5)
        s += f'<path d="M{x-12} {y-58}l26 22l-26 22" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    # joeye w locie
    for hops, i, t, hh in [(HOPS1, 0, 0.42, 120), (HOPS1, 1, 0.5, 190), (HOPS2, 2, 0.45, 150), (HOPS2, 4, 0.76, 140), (HOPS2, 5, 0.62, 130)]:
        a, b, h = hops[i]; x, y, ang = hop_point(*a, *b, h, t)
        s += joey(x, y - hh * 0.55, hh, fill=SAND, rot=ang * 0.35)
    return s

def background():
    return (f'<rect x="-10" y="{-EXT-10}" width="{W+20}" height="{H+2*EXT+20}" fill="{INK}"/>'
            + contours(W, -EXT, H + EXT, [(600, 1500, 60, 0.3), (2650, 380, 40, 1.4), (2950, 2950, 50, 2.2)], step=72, n=24))

def render(inner, scale=1.0):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*scale:.0f}" height="{(H+2*EXT)*scale:.0f}" '
           f'viewBox="0 {-EXT} {W} {H+2*EXT}">{inner}</svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGB')

if __name__ == '__main__':
    bg = background()
    full = render(bg + scene() + ''.join(text_block(t) for t in TILES))
    bgonly = render(bg)
    full.crop((0, EXT, W, EXT + H)).save(f'{OUT}/panorama.png')
    for t in TILES:
        x0, y0 = tile_xy(t); p = POST_OF_TILE[t]
        tile = full.crop((x0, y0 + EXT, x0 + TW, y0 + EXT + TH))
        tile.save(f'{OUT}/kafel-T{t}_post-{p}.png')
        cover = bgonly.crop((x0, y0, x0 + TW, y0 + TH + 2 * EXT))
        cover.paste(tile, (0, EXT))
        cover.save(f'{OUT}/okladka-post-{p}_T{t}.png')
    json.dump({'tiles': TILES, 'post_of_tile': POST_OF_TILE}, open(f'{OUT}/teksty.json', 'w'), ensure_ascii=False, indent=1)
    print('ok')
