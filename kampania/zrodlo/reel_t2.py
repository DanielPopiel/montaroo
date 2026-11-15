"""Reel do kafelka T2 (post 5): „A kangaroo can clear 8 m in one hop.” 1080×1920, 30 kl./s, 10 s."""
import io, os, sys, math, subprocess
import cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trasa_lib import *
import trasa

W, H, FPS, DUR = 1080, 1920, 30, 10.0
OFF = 140                      # kafelek w kadrze nieco wyżej niż w okładce (miejsce na podpis Reela)
G = OFF + 1290
DX = -1080                     # przesunięcie z panoramy (kafelek T2)
OUT = os.path.join(ROOT, 'kampania', 'trasa')
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
TX = {'en': dict(k='ROO FACT #4', h=['A kangaroo can', 'clear 8 m in', 'one hop.'], s='Montaroo gets footage to film in one.',
                 slogan='Hop from footage to film.', cta='Join the waitlist  ·  montaroo.com'),
      'pl': dict(k='KANGURZY FAKT #4', h=['Kangur potrafi', 'przeskoczyć 8 m', 'jednym susem.'], s='Montaroo robi z nagrań film jednym skokiem.',
                 slogan='Od nagrań do filmu jednym skokiem.', cta='Zapisz się na listę  ·  montaroo.com')}[LANG]

def clamp(x): return max(0.0, min(1.0, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def eback(x, s=2.2): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1

HOPS = [((250, G - 200), (990, G), 190), ((980, G), (2050, G - 50), 330)]
T_HOP = (1.49, 3.49)           # start skoku = wejście bitu w utworze, lądowanie na bicie
T_HOP2 = (3.74, 4.49)

def bez(a, b, h, u):
    return hop_point(*a, *b, h, u)

def partial(a, b, h, u, n=80):
    if u <= 0: return ''
    pts = [bez(a, b, h, u * i / n)[:2] for i in range(n + 1)]
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)

def bg_image():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{INK}"/><g transform="translate({DX} {OFF})">'
           + contours(0, 0, 0, [(600, 1500, 60, 0.3), (2650, 380, 40, 1.4), (2950, 2950, 50, 2.2)], step=72, n=24)
           + '</g></svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGB')

def text_layers(t, fade_all):
    s = ''; x = 84; size = TX.get('size', 112 if LANG == 'en' else 104)
    o = eo((t - 0.0) / 0.3) * fade_all
    p, _ = text(TX['k'], 'I6', 30, x, OFF + 236, track=0.14, fill=GOLD, opacity=round(o, 3)); s += p
    y = OFF + 236 + 40 + size * 0.86
    for i, line in enumerate(TX['h']):
        u = eo((t - 0.08 - i * 0.12) / 0.35)
        p, _ = text(line, 'G', size, x, y + (1 - u) * 46, track=-0.035, fill=SAND, opacity=round(u * fade_all, 3)); s += p
        y += size * 0.97
    u = eo((t - 3.9) / 0.5)
    p, _ = text(TX['s'], 'I4', 36, x, y - size * 0.97 + 74 + (1 - u) * 20, fill=SAND, opacity=round(.72 * u * fade_all, 3))
    return s + p

def scene_layer(t, fade_all):
    s = ''
    (a, b, h), (a2, b2, h2) = HOPS
    u = clamp((t - T_HOP[0]) / (T_HOP[1] - T_HOP[0]))
    u2 = clamp((t - T_HOP2[0]) / (T_HOP2[1] - T_HOP2[0]))
    # trasa (rysowana za joeyem)
    d = partial(a, b, h, u) + (partial(a2, b2, h2, u2) if u2 > 0 else '')
    if d: s += trail(d, w=11, dash='22 22', op=round(fade_all, 3))
    # wymiar 8 m rośnie razem ze skokiem
    yd = G + 190
    if u > 0:
        xe = a[0] + (b[0] - a[0]) * u
        s += (f'<g opacity="{.55*fade_all:.3f}"><path d="M{a[0]} {yd-22}V{yd+22}M{a[0]} {yd}H{xe:.1f}M{xe:.1f} {yd-22}V{yd+22}" stroke="{SAND}" stroke-width="4"/></g>')
        meters = 8 * u
        lab = f'{meters:.1f} m' if u < 1 else '8 m'
        cx = max(140, min(940, (0 + xe) / 2 if u < 1 else 390))
        cx = (a[0] + b[0]) / 2 if u >= 1 else max(a[0] + 70, xe - 90)
        p, lw = text(lab, 'I6', 40, cx, yd + 14, fill=SAND, anchor='middle', opacity=round(fade_all, 3))
        s += f'<rect x="{cx-lw/2-22:.0f}" y="{yd-34}" width="{lw+44:.0f}" height="64" fill="{INK}" opacity="{fade_all:.3f}"/>' + p
    # stos klipów, z którego startuje joey
    cols = [OCH, GOLD, EUC, SAND, '#2C5A4B', OCH, GOLD, SAND, EUC, EUC]
    pile = [(110, G+20, -8), (260, G+30, 6), (410, G+25, -3), (180, G-60, 12), (340, G-50, -10), (260, G-132, 4),
            (430, G-70, 15), (100, G+90, 3), (380, G+105, -6), (230, G+110, 9)]
    for i, (x, y, r) in enumerate(sorted(pile, key=lambda p: -p[1])):
        k = eback((t - 0.45 - i * 0.06) / 0.3, 1.8)
        if k > 0.01:
            s += f'<g opacity="{fade_all:.3f}" transform="translate({x} {y}) scale({k:.3f}) translate({-x} {-y})">' + clip_card(x, y, 190, 124, r, cols[i], INK) + '</g>'
    # joey
    hh = 215
    if t < T_HOP[0]:
        v = (t - 1.1) / 0.35
        if v > 0:
            x, y = a; s += joey(x, y - hh * 0.5 + 60 * (1 - eback(v, 2.4)), hh)
    elif u < 1:
        x, y, ang = bez(a, b, h, u)
        s += joey(x, y - hh * 0.55, hh, rot=ang * 0.35, sx=1 - 0.08 * math.sin(u * math.pi), sy=1 + 0.1 * math.sin(u * math.pi))
    elif t < T_HOP2[0]:
        v = (t - T_HOP[1]) / (T_HOP2[0] - T_HOP[1])
        sq = math.sin(clamp(v) * math.pi)
        x, y = b
        s += joey(x, y - hh * 0.5 * (1 - 0.18 * sq) - 4, hh, sx=1 + 0.15 * sq, sy=1 - 0.18 * sq)
    elif u2 < 1:
        x, y, ang = bez(a2, b2, h2, u2)
        s += joey(x, y - hh * 0.55, hh, rot=ang * 0.35)
    return s

def endcard(t):
    """plansza końcowa od 6.3 s."""
    if t < 6.3: return ''
    s = ''; cy = 760
    v = (t - 6.49) / 0.42
    if v < 0: jdy = 46
    elif v < 1: jdy = 46 * (1 - eback(v, 2.6))
    else: jdy = 2.5 * math.sin(clamp((t - 6.91) / 0.2) * math.pi)
    sc = eback((t - 6.3) / 0.35, 1.6)
    size = 380 * sc
    if size > 1:
        s += (f'<defs><clipPath id="cp"><rect x="0" y="0" width="{W}" height="{cy - size/2 + size*0.5:.1f}"/></clipPath></defs>')
        s += mark(540, cy, size, joeycol=SAND, pouchcol=OCH, stitchcol=INK, joey_dy=jdy)
    o = eo((t - 6.85) / 0.45)
    p, _ = text('montaroo', 'G', 168, 540, cy + 330 + (1 - o) * 30, track=-0.04, fill=SAND, anchor='middle', opacity=round(o, 3)); s += p
    o = eo((t - 7.25) / 0.45)
    p, _ = text(TX['slogan'], 'I6', 50, 540, cy + 440 + (1 - o) * 24, fill=GOLD, anchor='middle', opacity=round(o, 3)); s += p
    o = eo((t - 7.7) / 0.45)
    p, lw = text(TX['cta'], 'I5', 38, 540, cy + 590, fill=SAND, anchor='middle', opacity=round(o, 3))
    s += (f'<rect x="{540-lw/2-40:.0f}" y="{cy+530}" width="{lw+80:.0f}" height="88" rx="44" fill="none" '
          f'stroke="{SAND}" stroke-width="3" opacity="{.6*o:.3f}"/>') + p
    return s

def frame(t, bg):
    fade_all = 1 - eio((t - 5.9) / 0.45)
    inner = ''
    if fade_all > 0.001:
        lift = -40 * eio((t - 5.9) / 0.45)
        inner += f'<g transform="translate(0 {lift:.1f})">' + scene_layer(t, fade_all) + text_layers(t, fade_all) + '</g>'
    inner += endcard(t)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}</svg>'
    ov = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA')
    im = bg.copy(); im.paste(ov, (0, 0), ov); return im

if __name__ == '__main__':
    bg = bg_image()
    if len(sys.argv) > 2:          # podgląd pojedynczych klatek
        for ts in sys.argv[2:]:
            frame(float(ts), bg).save(f'/tmp/reel_{ts}.png')
        sys.exit()
    name = f'{OUT}/reel-post-5_T2_{LANG}.mp4'
    # muzyka: własny podkład „Montaroo Hop” (muzyka_hop.py) – drop 1.5 s = skok, 3.5 s lądowanie, 6.5 s logo
    mus = os.environ.get('MUZYKA', os.path.join(OUT, 'montaroo-hop_podklad.wav'))
    ss = float(os.environ.get('MUZYKA_OD', '0'))
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-ss', str(ss), '-i', mus, '-t', str(DUR),
                          '-af', f'afade=t=out:st={DUR-1.4}:d=1.4,loudnorm=I=-14:TP=-1:LRA=9,aresample=48000',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
                          '-movflags', '+faststart', '-shortest', name], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS, bg).tobytes())
    p.stdin.close(); p.wait(); print(name)
