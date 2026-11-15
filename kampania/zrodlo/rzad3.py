"""Rząd 3 siatki „Trasa skoku” (posty 7–9) – dokleja się NAD panoramą T1–T6.
Kafle: T7 (lewy, post 9), T8 (środek, post 8), T9 (prawy, post 7). Trasa płynie od lewej do prawej.
Sceny są funkcjami czasu t (kafel = stan końcowy, t=99) – te same funkcje używa reels.py."""
import io, os, sys, math, random
import cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trasa_lib import *

def _c(x): return max(0.0, min(1.0, x))
def _eback(x, s=2.0): x = _c(x) - 1; return x * x * ((s + 1) * x + s) + 1
def _eo(x): x = _c(x); return 1 - (1 - x) ** 3

TXT = {
 7: {'en': dict(k='BE HONEST', h=['Your camera roll', 'after holidays:'], s='4,812 photos. 391 videos. 0 films.', size=112),
     'pl': dict(k='BĄDŹMY SZCZERZY', h=['Twoja galeria', 'po wakacjach:'], s='4 812 zdjęć. 391 nagrań. 0 filmów.', size=112)},
 8: {'en': dict(k='ROO FACT #5', h=['Kangaroos can', 'hop at 60 km/h.'], s='Montaroo is quick too. Folder in, film out.', size=112),
     'pl': dict(k='KANGURZY FAKT #5', h=['Kangur skacze', 'nawet 60 km/h.'], s='Montaroo też się nie ślimaczy.', size=112)},
 9: {'en': dict(k='EVERY GROUP CHAT', h=['“Who’s editing', 'the trip video?”'], s='Silence. Then: Montaroo.', size=112),
     'pl': dict(k='KAŻDY CZAT RODZINNY', h=['„Kto zmontuje', 'film z wyjazdu?”'], s='Cisza. Aż do Montaroo.', size=112)},
}
BUB = {'en': ['not me', 'busy this week', '...', 'Montaroo: on it.'],
       'pl': ['nie ja', 'mam ciężki tydzień', '...', 'Montaroo: biorę to.']}

def bubble(x, y, txt, fill, col, right=False, k=1.0):
    p, w = text(txt, 'I6', 40, 0, 0, fill=col)
    W, H = w + 64, 84; bx = x - W if right else x
    r = (f'<g transform="translate({bx + W / 2:.1f} {y:.1f}) scale({k:.3f}) translate({-W / 2:.1f} {-H / 2:.1f})">'
         f'<rect width="{W:.1f}" height="{H}" rx="34" fill="{fill}"/>'
         f'<path d="M{W - 30 if right else 30} {H - 2}l{14 if right else -14} 18l{-2 if right else 2} -22z" fill="{fill}"/>'
         f'<g transform="translate(32 57)">{p}</g></g>')
    return r, bx, W

# ---- sceny (współrzędne: X = lewa krawędź kafla, G = poziom „ziemi”) ----
def scene_chat(t, X, G, lang='en', show_joey=True):
    s = ''; b = BUB[lang]
    rows = [(X + 84, G - 520, b[0], '#2C5A4B', SAND, False, 1.5), (X + 84, G - 410, b[1], '#2C5A4B', SAND, False, 2.0),
            (X + 84, G - 300, b[2], '#2C5A4B', SAND, False, 2.5), (X + 996, G - 150, b[3], GOLD, INK, True, 3.5)]
    end = None
    for x, y, tx, f, c, right, t0 in rows:
        k = _eback((t - t0) / 0.3, 2.2)
        if k > 0.01:
            r, bx, W = bubble(x, y, tx, f, c, right, k); s += r
            if right: end = (bx, W)
    if end and t >= 3.5 and show_joey:
        s += joey(end[0] - 70, G - 150, 96, fill=SAND)
    return s

def scene_gauge(t, X, G, lang='en'):
    cx, cy, R = X + 540, G - 40, 230; s = ''
    val = 60 * _eo((t - 1.5) / 2.0) if t < 99 else 60
    def pt(v, r): a = math.pi * (1 - v / 80); return cx + r * math.cos(a), cy - r * math.sin(a)
    x0, y0 = pt(0, R); x1, y1 = pt(80, R); xv, yv = pt(val, R)
    s += f'<path d="M{x0:.1f} {y0:.1f}A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{SAND}" stroke-opacity=".18" stroke-width="30" stroke-linecap="round"/>'
    if val > 0.5:
        s += f'<path d="M{x0:.1f} {y0:.1f}A{R} {R} 0 0 1 {xv:.1f} {yv:.1f}" fill="none" stroke="{GOLD}" stroke-width="30" stroke-linecap="round"/>'
    for v in range(0, 81, 10):
        a, b2 = pt(v, R - 38), pt(v, R - 62)
        s += f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b2[0]:.1f} {b2[1]:.1f}" stroke="{SAND}" stroke-opacity=".5" stroke-width="5" stroke-linecap="round"/>'
    nx, ny = pt(val, R - 70)
    s += f'<path d="M{cx} {cy}L{nx:.1f} {ny:.1f}" stroke="{OCH}" stroke-width="14" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="22" fill="{OCH}"/>'
    p, _ = text(f'{int(round(val))}', 'G', 96, cx, cy + 105, track=-0.03, fill=SAND, anchor='middle')
    q, _ = text('km/h', 'I6', 30, cx, cy + 145, fill=SAND, opacity=.65, anchor='middle')
    return s + p + q

def scene_roll(t, X, G, lang='en'):
    cx, cy, W, H = X + 600, G - 250, 300, 520; s = phone(cx, cy, W, H, 4, SAND, INK)
    rnd = random.Random(5); cols = [OCH, GOLD, EUC, '#2C5A4B', SAND]
    n_on = 28 if t >= 99 else int(28 * _c((t - 1.5) / 1.8))
    cells = ''
    for i in range(28):
        r, c = divmod(i, 4)
        if i >= n_on: break
        cells += (f'<rect x="{-W / 2 + 34 + c * 60:.1f}" y="{-H / 2 + 60 + r * 60:.1f}" width="52" height="52" rx="8" '
                  f'fill="{rnd.choice(cols)}" opacity="{0.55 + 0.45 * rnd.random():.2f}"/>')
    s += f'<g transform="translate({cx} {cy}) rotate(4)">{cells}</g>'
    k = _eback((t - 3.5) / 0.35, 2.2) if t < 99 else 1
    num = int(round(4812 * (_c((t - 1.5) / 2.0) if t < 99 else 1)))
    lab = ('+' + f'{num:,}') if lang == 'en' else ('+' + f'{num:,}'.replace(',', ' '))
    p, w = text(lab, 'G', 64, 0, 0, fill=INK)
    if t >= 1.5:
        s += (f'<g transform="translate({cx + 150} {cy - H / 2 + 10}) scale({max(k, 0.7) if t < 3.5 else k:.3f})">'
              f'<rect x="{-w / 2 - 28:.1f}" y="-52" width="{w + 56:.1f}" height="84" rx="42" fill="{OCH}"/>'
              f'<g transform="translate({-w / 2:.1f} 12)">{p}</g></g>')
    return s

# ---- trasa przez cały rząd (współrzędne rzędu: X kafla T7 = 0) ----
def row_hops(G):
    return [((1000, G - 110), (1290, G), 170), ((1290, G), (1950, G), 430), ((1950, G), (2260, G), 120),
            ((2260, G), (2560, G), 90), ((2560, G), (2860, G), 90), ((2860, G), (3160, G), 90), ((3160, G), (3460, G - 40), 110)]

TW, TH, EXT = 1080, 1440, 240
OUT = os.path.join(ROOT, 'kampania', 'trasa')
TILES = {7: (2, 9), 8: (1, 8), 9: (0, 7)}   # post -> (kolumna, T)

def tile_text(post, X, Y, lang='en'):
    d = TXT[post][lang]; x = X + 84
    s, _ = text(d['k'], 'I6', 30, x, Y + 236, track=0.14, fill=GOLD)
    y = Y + 236 + 40 + d['size'] * 0.86
    for line in d['h']:
        p, w = text(line, 'G', d['size'], x, y, track=-0.035, fill=SAND); assert w < TW - 150, (line, w); s += p; y += d['size'] * 0.97
    p, _ = text(d['s'], 'I4', 36, x, y - d['size'] * 0.97 + 74, fill=SAND, opacity=.72)
    return s + p

if __name__ == '__main__':
    W, H = 3 * TW, TH
    G = 1200
    inner = (f'<rect x="-10" y="{-EXT - 10}" width="{W + 20}" height="{H + 2 * EXT + 20}" fill="{INK}"/>'
             f'<g transform="translate(0 1440)">' + contours(W, 0, 0, [(600, 1500, 60, 0.3), (2650, 380, 40, 1.4), (2950, 2950, 50, 2.2)], step=72, n=24) + '</g>')
    bg = inner
    hops = row_hops(G); d = hop(*hops[0][0], *hops[0][1], hops[0][2])
    for a, b, h in hops[1:]: d += 'Q' + hop(*a, *b, h).split('Q')[1]
    scene = (scene_chat(99, 0, G) + scene_gauge(99, TW, G) + scene_roll(99, 2 * TW, G) + trail(d, w=11, dash='22 22'))
    x, y, ang = hop_point(*hops[1][0], *hops[1][1], hops[1][2], 0.5)
    scene += joey(x, y - 110, 200, rot=ang * 0.35)
    for i, sp in enumerate((0, 1, 2)):
        scene += f'<path d="M{x - 130 - sp * 18} {y - 150 + i * 40}h-{70 - i * 15}" stroke="{SAND}" stroke-opacity=".5" stroke-width="8" stroke-linecap="round"/>'
    texts = ''.join(tile_text(p, c * TW, 0) for p, (c, _) in TILES.items())
    def render(body):
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H + 2 * EXT}" viewBox="0 {-EXT} {W} {H + 2 * EXT}">{body}</svg>'
        return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGB')
    full = render(bg + scene + texts); bgo = render(bg)
    row = full.crop((0, EXT, W, EXT + H)); row.save(f'{OUT}/panorama_rzad3.png')
    for post, (c, T) in TILES.items():
        tile = full.crop((c * TW, EXT, (c + 1) * TW, EXT + TH)); tile.save(f'{OUT}/kafel-T{T}_post-{post}.png')
        cov = bgo.crop((c * TW, 0, (c + 1) * TW, H + 2 * EXT)); cov.paste(tile, (0, EXT)); cov.save(f'{OUT}/okladka-post-{post}_T{T}.png')
    old = Image.open(f'{OUT}/panorama.png')
    allp = Image.new('RGB', (W, 3 * H)); allp.paste(row, (0, 0)); allp.paste(old, (0, H)); allp.save(f'{OUT}/panorama_9.png')
    print('ok')
