# Montaroo – spot 20 s (16:9 i 9:16). Animacja znaku: joey wyskakuje z torby na pierwszym uderzeniu.
import sys, math, os, io, subprocess
sys.path.insert(0, '/home/claude/mt')
import numpy as np, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import mark
from mark import INK, OCH, GOLD, SAND, EUC
from word import word, UPM

FPS = 25; BPM = 120; BEAT = 60 / BPM; T0 = 1.0   # pierwsze uderzenie
DUR = 20.0
LANG = sys.argv[2] if len(sys.argv) > 2 else 'en'
FMT = sys.argv[1] if len(sys.argv) > 1 else 'h'   # h = 1920x1080, v = 1080x1920
W, H = (1920, 1080) if FMT == 'h' else (1080, 1920)
OUT = f'out_{FMT}_{LANG}'; os.makedirs(OUT, exist_ok=True)
GAB = '/home/claude/spot/gab800.ttf'; INT6 = '/home/claude/spot/inter600.ttf'
TX = {
 'en': dict(c=['1,434 clips.', '10 days.', '3 phones and a drone.', 'One folder in.', 'One film out.', 'Cut to the beat.', 'Told like a story.'],
            end='Hop from footage to film.', sub='Free for Windows · montaroo.com', said='“More drone over Monument Valley.”'),
 'pl': dict(c=['1 434 nagrania.', '10 dni.', '3 telefony i dron.', 'Jeden folder.', 'Jeden film.', 'Cięte do rytmu.', 'Opowiedziane jak historia.'],
            end='Od nagrań do filmu jednym skokiem.', sub='Za darmo na Windows · montaroo.com', said='„Więcej drona nad Monument Valley.”'),
}[LANG]

def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def ease_out(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def ease_back(x, s=1.9):
    x = max(0, min(1, x)); x -= 1; return x * x * ((s + 1) * x + s) + 1

def joey_anim(t):
    """przesunięcie joeya (jednostki siatki 128) i skala pionowa (squash/stretch)."""
    if t < 0: return 46, 1.0          # schowany w torbie
    # skok: 0..0.36 s w górę z przesadą, potem lądowanie
    u = t / 0.36
    if u < 1:
        y = 46 * (1 - ease_back(u, 2.6)); sy = 1 + 0.18 * math.sin(min(1, u) * math.pi)
        return y, sy
    v = (t - 0.36) / 0.22
    if v < 1:  # małe przysiadnięcie
        return 2.5 * math.sin(v * math.pi), 1 - 0.07 * math.sin(v * math.pi)
    return 0, 1.0

def mark_svg(t, joeycol=SAND, stitchcol=INK, show_stitch=1.0):
    y, sy = joey_anim(t)
    # maska: joey widoczny tylko nad dnem torby (torba go zasłania)
    j = mark.joey()
    n = int(round(7 * show_stitch))
    dashes = ''.join(f'<rect x="{27 + i*10.8:.2f}" y="73.3" width="6.4" height="3.4" rx="1.7" fill="{stitchcol}"/>' for i in range(n))
    body = (f'<defs><clipPath id="cj"><rect x="0" y="-40" width="128" height="110"/></clipPath></defs><g clip-path="url(#cj)"><g transform="translate(0 {y:.2f}) translate(64 64) scale({1/sy**0.5:.3f} {sy:.3f}) translate(-64 -64)">'
            f'<path d="{j}" fill="{joeycol}"/></g></g>'
            f'<path d="{mark.pouch()}" fill="{OCH}"/>{dashes}')
    return body

def word_svg(col, x0, base, size):
    d, w = word(size=size, x0=x0, baseline=base); return f'<path d="{d}" fill="{col}"/>', w

def render_svg(inner, w, h, vb):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}">{inner}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert('RGBA')

def logo_frame(t, bg=INK, word_t=None, scale=1.0, dy=0):
    """znak + napis na tle; t = czas od uderzenia."""
    im = Image.new('RGB', (W, H), hx(bg))
    FS = 114; LSB = 48 * FS / UPM
    d, wd = word(size=FS, x0=0, baseline=0)
    total = 96 + 24 + (wd - LSB)
    # skala tak, by logo zajęło ok. 56% szerokości (h) / 78% (v)
    k = (W * (0.52 if FMT == 'h' else 0.8)) / total * scale
    ox = (W - total * k) / 2 - 16 * k; oy = H / 2 - 64 * k + dy
    wt = 0 if word_t is None else word_t
    wo = ease_out(wt / 0.45); wx = (1 - wo) * -30
    ox += (1 - wo) * ((total - 96) / 2) * k
    inner = (f'<g transform="translate({ox:.1f} {oy:.1f}) scale({k:.4f})">' + mark_svg(t, show_stitch=ease_out((t - 0.15) / 0.5) if t > 0 else 0) +
             f'<g opacity="{wo:.3f}" transform="translate({112+24-LSB+wx:.2f} 120)"><path d="{d}" fill="{SAND}"/></g></g>')
    lg = render_svg(inner, W, H, f'0 0 {W} {H}')
    im.paste(lg, (0, 0), lg); return im

FR = sorted(os.listdir('/home/claude/spot/fr'))
def foot(seg, off):
    """klatka z hero.mp4: segment 0..9 (po 60 klatek), przesunięcie w klatkach."""
    i = min(len(FR) - 1, seg * 60 + 10 + int(off))
    im = Image.open('/home/claude/spot/fr/' + FR[i]).convert('RGB')
    # kadrowanie do formatu
    sw, sh = im.size; tr = W / H
    if sw / sh > tr: nw = int(sh * tr); im = im.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else: nh = int(sw / tr); im = im.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    im = im.resize((W, H), Image.LANCZOS)
    # lekkie przybliżenie (Ken Burns)
    z = 1.0 + off * 0.0025; cw, ch = W / z, H / z
    return im.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.LANCZOS)

def font(p, s): return ImageFont.truetype(p, s)
def caption(im, text, size, pos='bl', col=SAND, shadow=True, t=1.0, maxw=None):
    d = ImageDraw.Draw(im); f = font(GAB, size)
    lines = wrap(text, f, maxw or W * 0.8)
    lh = int(size * 1.0); hgt = lh * len(lines)
    x = int(W * 0.07); y = int(H * (0.09 if FMT == 'h' else 0.12))
    if pos == 'c': y = (H - hgt) // 2
    rise = int((1 - ease_out(t / 0.25)) * size * 0.35)
    if shadow:
        sh = Image.new('L', im.size, 0); sd = ImageDraw.Draw(sh)
        for k, ln in enumerate(lines): sd.text((x, y + k * lh + rise), ln, font=f, fill=150)
        sh = sh.filter(ImageFilter.GaussianBlur(size * 0.18))
        im.paste(Image.new('RGB', im.size, hx(INK)), (0, 0), sh)
    for k, ln in enumerate(lines):
        if pos == 'c':
            x = (W - d.textlength(ln, font=f)) // 2
        d.text((x, y + k * lh + rise), ln, font=f, fill=hx(col))
    return im

def wrap(text, f, maxw):
    words = text.split(' '); lines = []; cur = ''
    for w_ in words:
        t2 = (cur + ' ' + w_).strip()
        if f.getlength(t2) <= maxw or not cur: cur = t2
        else: lines.append(cur); cur = w_
    lines.append(cur); return lines

def stitch_bar(im, y, col=OCH, n=None, prog=1.0):
    d = ImageDraw.Draw(im); dw, gap, hh = (W * 0.035, W * 0.02, max(8, W // 160))
    cnt = int((W * 0.6) // (dw + gap)); x0 = (W - cnt * (dw + gap) + gap) / 2
    for i in range(int(cnt * prog)):
        x = x0 + i * (dw + gap); d.rounded_rectangle((x, y, x + dw, y + hh), radius=hh // 2, fill=hx(col))

def frame(t):
    b = (t - T0) / BEAT   # numer uderzenia od pierwszego
    # S1: logo intro 0 .. 3.0 s
    if t < 3.0:
        im = logo_frame(t - T0, word_t=t - (T0 + 0.5))
        if t > 2.6:  # przejście: torba "rośnie" w czerń
            a = ease_out((t - 2.6) / 0.4); im = Image.blend(im, Image.new('RGB', (W, H), hx(INK)), a)
        return im
    # S2: montaż na beat 3.0 .. 9.0 (12 cięć po 0.5 s), napisy co 2 s
    if t < 9.0:
        k = int((t - 3.0) / BEAT); off = ((t - 3.0) % BEAT) * FPS
        seq = [2, 4, 1, 6, 3, 7, 5, 8, 2, 6, 4, 9]
        im = foot(seq[k], off + (k % 3) * 8)
        ci = int((t - 3.0) / 2.0); ct = (t - 3.0) % 2.0
        caption(im, TX['c'][ci], int(H * (0.11 if FMT == 'h' else 0.075)), t=ct)
        return im
    # S3: karta na piasku 9.0 .. 13.0: "One folder in." / "One film out." + polecenie słowami
    if t < 13.0:
        im = Image.new('RGB', (W, H), hx(SAND)); lt = t - 9.0
        txt = TX['c'][3] if lt < 2.0 else TX['c'][4]
        caption(im, txt, int(H * (0.13 if FMT == 'h' else 0.08)), pos='c', col=INK, shadow=False, t=lt % 2.0)
        stitch_bar(im, int(H * (0.66 if FMT == 'h' else 0.6)), prog=ease_out(lt / 3.5))
        d = ImageDraw.Draw(im); f = font(INT6, int(H * (0.032 if FMT == 'h' else 0.022)))
        if lt > 2.0:
            s = TX['said']; tw = d.textlength(s, font=f); pad = int(H * 0.02)
            bx = (W - tw) / 2 - pad; by = int(H * (0.74 if FMT == 'h' else 0.67))
            a = ease_out((lt - 2.0) / 0.3)
            d.rounded_rectangle((bx, by + (1 - a) * 20, bx + tw + 2 * pad, by + f.size + 2 * pad + (1 - a) * 20), radius=18, fill=hx(OCH))
            d.text((bx + pad, by + pad + (1 - a) * 20), s, font=f, fill=hx(INK))
        return im
    # S4: montaż 13.0 .. 17.0 cięcia co pół beatu przy refrenie
    if t < 17.0:
        step = BEAT if t < 15.0 else BEAT / 2
        k = int((t - 13.0) / step); off = ((t - 13.0) % step) * FPS
        seq = [3, 6, 8, 4, 7, 5, 9, 2, 6, 3, 8, 4, 7, 5]
        im = foot(seq[k % len(seq)], off + 14)
        ci = 5 if t < 15.0 else 6; ct = (t - 13.0) % 2.0
        caption(im, TX['c'][ci], int(H * (0.11 if FMT == 'h' else 0.075)), t=ct)
        if t > 16.75: im = Image.blend(im, Image.new('RGB', (W, H), hx(INK)), ease_out((t - 16.75) / 0.25))
        return im
    # S5: plansza końcowa 17 .. 20, joey skacze na uderzeniu 17.0
    lt = t - 17.0
    im = logo_frame(lt, word_t=10, scale=0.82, dy=-H * (0.07 if FMT == 'h' else 0.06))
    d = ImageDraw.Draw(im)
    f1 = font(GAB, int(H * (0.07 if FMT == 'h' else 0.042))); f2 = font(INT6, int(H * (0.03 if FMT == 'h' else 0.02)))
    a = ease_out((lt - 0.35) / 0.4)
    col = tuple(int(hx(INK)[i] + (hx(SAND)[i] - hx(INK)[i]) * a) for i in range(3))
    col2 = tuple(int(hx(INK)[i] + (hx(GOLD)[i] - hx(INK)[i]) * a) for i in range(3))
    for k_, (txt, f, c, yy) in enumerate([(TX['end'], f1, col, 0.66), (TX['sub'], f2, col2, 0.77 if FMT == 'h' else 0.72)]):
        for j, ln in enumerate(wrap(txt, f, W * 0.86)):
            tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, int(H * yy) + j * int(f.size * 1.05)), ln, font=f, fill=c)
    return im

if __name__ == '__main__':
    only = os.environ.get('ONLY')
    N = int(DUR * FPS)
    rng = range(N) if not only else [int(float(x) * FPS) for x in only.split(',')]
    for i in rng:
        frame(i / FPS).save(f'{OUT}/{i:04d}.jpg', quality=92)
    print('frames', OUT)
