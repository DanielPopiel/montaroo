"""Trailer w pionie (9:16, 1080×1920) – Reels / TikTok / Shorts. Wersja pionowa trailer_yt.py.
Klip A (wyjazd) → klip B (noc przy laptopie, joey wciska klawisz) → animacja „folder → film” → plansza z joeyem.
python trailer_yt.py <en|pl> klipA.mp4 klipB.mp4 [wyjscie.mp4]"""
import io, os, sys, math, base64, subprocess
import numpy as np, cairosvg
from PIL import Image
LANG = sys.argv[1]
ARGS = sys.argv[2:]
sys.argv = [sys.argv[0], LANG]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_t2 as R
from trasa_lib import *

W, H, FPS = 1080, 1920, 24
CH = 1180                       # wysokość pasa z klipem
FOCUS = (0.5, 0.40)             # środek kadru (ułamek szerokości) klipu A, B
FY = 1330                       # środek gotowego filmu w animacji
MUS = os.path.join(R.OUT, 'montaroo-hop_podklad_26s.wav')
DUR = 25.96
POP = 22.46                     # joey wyskakuje (przesunięty „pop” z podkładu)
A_END, B_END, ANIM_END = 7.0, 14.5, 21.8
SRC = os.path.join(ROOT, 'kampania', 'higgsfield')
CLIP_A, CLIP_B = ARGS[0], ARGS[1]
OUTF = ARGS[2] if len(ARGS) > 2 else os.path.join(R.OUT, f'trailer-pion_{LANG}.mp4')
eo, eio, eback, clamp = R.eo, R.eio, R.eback, R.clamp

TX = {'en': dict(a1='You filmed everything.', a2='Every hop.|Every view.', b1='1,434 clips later…', b2='Editing it?|Days.', b3='Or… one hop.',
                 m1='Montaroo cuts it|for you.', m2='Folder in. Film out.', cnt='clips',
                 slogan='Hundreds of clips in. One film out.', cta='Join the waitlist · montaroo.com'),
      'pl': dict(a1='Nagrałeś wszystko.', a2='Każdy skok.|Każdy widok.', b1='1434 klipy później…', b2='Montaż?|Kilka dni.', b3='Albo… jeden skok.',
                 m1='Montaroo zmontuje|to za Ciebie.', m2='Folder na wejściu.|Film na wyjściu.', cnt='klipów',
                 slogan='Setki klipów na wejściu. Jeden film.', cta='Zapisz się · montaroo.com')}[LANG]

def read_clip(path, start, dur, fx=0.5):
    """natywny pion: pełny kadr 1080×1920 (bez pasów i rozmycia)"""
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', path, '-vf',
                        f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3)

def read_film(path, start, dur):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', path, '-vf', f'fps={FPS},scale=960:540',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, 540, 960, 3)

def probe(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True).stdout)

def thumb_b64(path, t, w=240, h=426):
    png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', path, '-frames:v', '1', '-vf',
                          f'scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}', '-f', 'image2pipe',
                          '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
    return base64.b64encode(png).decode()

# miniatury lecące z folderu do filmu
THUMBS = []
for fn, t in [('road.mp4', 1.5), ('canyon.mp4', 2.2), ('sunset.mp4', 2.0), ('gemini_telefon.mp4', 2.0),
              ('gemini_laptop.mp4', 2.0), ('canyon.mp4', 3.2), ('road.mp4', 3.0), ('sunset.mp4', 3.5)]:
    p = os.path.join(SRC, fn)
    if os.path.exists(p): THUMBS.append(thumb_b64(p, t))
for path, t in [(CLIP_A, 2.0), (CLIP_A, 5.0)]:
    THUMBS.append(thumb_b64(path, t))

def wrap(txt, size, maxw=W - 160):
    if '|' in txt: return txt.split('|')
    words, lines, cur = txt.split(), [], ''
    for w_ in words:
        cand = (cur + ' ' + w_).strip()
        if width(cand, 'G', size, -0.03) > maxw and cur: lines.append(cur); cur = w_
        else: cur = cand
    return lines + [cur]

def lower_third(lines_t):
    s = (f'<defs><linearGradient id="tg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/>'
         f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient></defs><rect width="{W}" height="620" fill="url(#tg)"/>')
    for (txt, a, b, t) in lines_t:
        if a <= t < b:
            o = eo((t - a) / 0.2) * (1 - eo((t - (b - 0.18)) / 0.18))
            dy = (1 - eo((t - a) / 0.3)) * 30
            for i, ln in enumerate(wrap(txt, 104)):
                p, _ = text(ln, 'G', 104, 80, 250 + i * 112 + dy, track=-0.03, fill=SAND, opacity=round(o, 3)); s += p
    return s

def folder(cx, cy, k, count):
    w, h = 300 * k, 220 * k
    s = (f'<g transform="translate({cx-w/2:.1f} {cy-h/2:.1f})">'
         f'<path d="M0 {28*k:.1f}Q0 0 {28*k:.1f} 0H{110*k:.1f}L{140*k:.1f} {30*k:.1f}H{w-24*k:.1f}Q{w:.1f} {30*k:.1f} {w:.1f} {54*k:.1f}V{h-24*k:.1f}Q{w:.1f} {h:.1f} {w-24*k:.1f} {h:.1f}H{24*k:.1f}Q0 {h:.1f} 0 {h-24*k:.1f}Z" fill="{OCH}"/>'
         f'<rect x="0" y="{60*k:.1f}" width="{w:.1f}" height="{h-60*k:.1f}" rx="{24*k:.1f}" fill="#F07A3E"/></g>')
    p, _ = text(f'{count:,}'.replace(',', ',' if LANG == 'en' else ' ') + ' ' + TX['cnt'], 'I6', 40 * k, cx, cy + h / 2 + 64 * k,
                fill=SAND, anchor='middle'); return s + p

def card_img(b64, cx, cy, w, h, rot, op=1, i=0):
    return (f'<defs><clipPath id="c{i}"><rect x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w*0.1:.1f}"/></clipPath></defs>'
            f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})" opacity="{op:.3f}">'
            f'<rect x="{-w/2-6:.1f}" y="{-h/2-6:.1f}" width="{w+12:.1f}" height="{h+12:.1f}" rx="{w*0.12:.1f}" fill="{SAND}"/>'
            f'<image href="data:image/png;base64,{b64}" x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#c{i})"/></g>')

def anim_layer(t, film_frame_b64):
    """t lokalne 0..7.3"""
    s = f'<rect width="{W}" height="{H}" fill="{INK}"/>' + contours(W, 0, H, [(200, 1700, 60, 0.4), (900, 300, 55, 1.3)], seed=11, step=64, n=20)
    n = len(THUMBS)
    fx, fy = 540, 760
    slot_x0, slot_x1, slot_y = 60, 1020, 1300
    sw = (slot_x1 - slot_x0) / n
    landed = 0
    merge = eio((t - 4.9) / 0.7)            # karty → jeden film
    for i, b64 in enumerate(THUMBS):
        t0 = 0.35 + 0.45 * i; u = (t - t0) / 0.5
        tx, ty = slot_x0 + sw * (i + 0.5), slot_y
        if u < 0: continue
        if u < 1:
            x, y, ang = hop_point(fx, fy - 40, tx, ty, 220, eio(u))
            s += card_img(b64, x, y, 96, 170, ang * 0.3, 1, i)
        else:
            landed += 1
            if merge < 1:
                bounce = 10 * math.sin(clamp((t - t0 - 0.5) / 0.25) * math.pi)
                x = tx + (540 - tx) * merge; y = ty - bounce + (FY - ty) * merge
                s += card_img(b64, x, y, sw - 14, (sw - 14) * 1.77, 0, 1 - merge, i)
    # tor skoku pod kartami
    d = hop(fx, fy - 40, slot_x0 + sw * 0.5, slot_y, 220)
    s += trail(d, w=7, dash='16 18', op=0.55 * (1 - merge))
    cnt = int(1434 * (1 - clamp((t - 0.35) / (0.45 * n + 0.5))))
    s += folder(fx, fy, 1.0, max(cnt, 0))
    if merge > 0:          # gotowy film 16:9
        fw, fh = 960 * (0.6 + 0.4 * merge), 540 * (0.6 + 0.4 * merge)
        s += (f'<defs><clipPath id="ff"><rect x="{540-fw/2:.1f}" y="{FY-fh/2:.1f}" width="{fw:.1f}" height="{fh:.1f}" rx="26"/></clipPath></defs>'
              f'<g opacity="{merge:.3f}"><rect x="{540-fw/2-10:.1f}" y="{FY-fh/2-10:.1f}" width="{fw+20:.1f}" height="{fh+20:.1f}" rx="34" fill="{SAND}"/>'
              f'<image href="data:image/jpeg;base64,{film_frame_b64}" x="{540-fw/2:.1f}" y="{FY-fh/2:.1f}" width="{fw:.1f}" height="{fh:.1f}" '
              f'preserveAspectRatio="xMidYMid slice" clip-path="url(#ff)"/>'
              f'<rect x="{540-fw/2+40:.1f}" y="{FY+fh/2-44:.1f}" width="{fw-80:.1f}" height="10" rx="5" fill="{SAND}" opacity=".35"/>'
              f'<rect x="{540-fw/2+40:.1f}" y="{FY+fh/2-44:.1f}" width="{(fw-80)*clamp((t-5.2)/2.1):.1f}" height="10" rx="5" fill="{GOLD}"/></g>')
    for (txt, a, b) in [(TX['m1'], 0.2, 4.7), (TX['m2'], 5.0, 7.3)]:
        if a <= t < b:
            o = eo((t - a) / 0.25) * (1 - eo((t - (b - 0.2)) / 0.2))
            for i, ln in enumerate(wrap(txt, 92)):
                p, _ = text(ln, 'G', 92, 80, 250 + i * 100 + (1 - eo((t - a) / 0.3)) * 24, track=-0.03, fill=SAND, opacity=round(o, 3)); s += p
    return s

def endcard(t):
    s = f'<rect width="{W}" height="{H}" fill="{INK}"/>' + contours(W, 0, H, [(540, 2150, 70, 0.8)], seed=5, step=64, n=22)
    cy = 780
    v = (t - POP) / 0.42
    jdy = 46 if v < 0 else (46 * (1 - eback(v, 2.6)) if v < 1 else 0)
    size = 360 * eback((t - (POP - 0.3)) / 0.35, 1.6)
    if size > 1: s += mark(540, cy, size, joey_dy=jdy)
    o = eo((t - (POP + 0.3)) / 0.45)
    p, _ = text('montaroo', 'G', 160, 540, cy + 330 + (1 - o) * 26, track=-0.04, fill=SAND, anchor='middle', opacity=round(o, 3)); s += p
    o = eo((t - (POP + 0.7)) / 0.45)
    p, _ = text(TX['slogan'], 'I6', 46, 540, cy + 420 + (1 - o) * 20, fill=GOLD, anchor='middle', opacity=round(o, 3)); s += p
    o = eo((t - (POP + 1.1)) / 0.45)
    p, lw = text(TX['cta'], 'I5', 36, 540, cy + 552, fill=SAND, anchor='middle', opacity=round(o, 3))
    s += (f'<rect x="{540-lw/2-40:.0f}" y="{cy+496}" width="{lw+80:.0f}" height="84" rx="42" fill="none" stroke="{SAND}" '
          f'stroke-width="3" opacity="{.6*o:.3f}"/>') + p
    return s

def svg_png(body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA')

def main(only=None):
    la, lb = probe(CLIP_A), probe(CLIP_B)
    A1 = os.path.join(SRC, 'road.mp4'); A2 = os.path.join(SRC, 'canyon.mp4')
    va = np.concatenate([read_clip(A1, 0.3, 3.5), read_clip(A2, 0.4, A_END - 3.5)])
    vb = read_clip(CLIP_B, max(0.0, lb - (B_END - A_END) - 0.05), B_END - A_END)
    vfilm = read_film(CLIP_A, max(0.0, min(1.0, la - A_END)), A_END)
    film_b64 = thumb_b64(CLIP_A, 3.0, 980, 551)
    times = [i / FPS for i in range(int(DUR * FPS))] if only is None else only
    ff = None
    if only is None:
        ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                               '-i', '-', '-i', MUS, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                               '-c:a', 'aac', '-b:a', '256k', '-af', 'loudnorm=I=-14:TP=-1,aresample=48000', '-ar', '48000', '-shortest', '-movflags', '+faststart', OUTF],
                              stdin=subprocess.PIPE)
    for t in times:
        if t < A_END:
            img = Image.fromarray(va[min(len(va) - 1, int(t * FPS))]).convert('RGBA')
            img.alpha_composite(svg_png(lower_third([(TX['a1'], 0.4, 3.4, t), (TX['a2'], 3.6, 6.85, t)])))
        elif t < B_END:
            img = Image.fromarray(vb[min(len(vb) - 1, int((t - A_END) * FPS))]).convert('RGBA')
            img.alpha_composite(svg_png(lower_third([(TX['b1'], 7.3, 9.3, t), (TX['b2'], 9.5, 11.4, t), (TX['b3'], 11.7, 14.35, t)])))
        else:
            k = min(len(vfilm) - 1, int((t - B_END - 5.0) * FPS) % len(vfilm)) if t - B_END > 4.9 else 0
            buf = io.BytesIO(); Image.fromarray(vfilm[k]).save(buf, 'JPEG', quality=85)
            img = svg_png(anim_layer(t - B_END, base64.b64encode(buf.getvalue()).decode()).replace('image/png;base64,' + '__F__', ''))
            if t > ANIM_END - 0.3:
                e = svg_png(endcard(t)); a = eio((t - (ANIM_END - 0.3)) / 0.3)
                img = Image.blend(img, e, a)
        if ff: ff.stdin.write(img.convert('RGB').tobytes())
        else: img.convert('RGB').save(f'/tmp/tp_{t:.2f}.png')
    if ff: ff.stdin.close(); ff.wait(); print(OUTF)

if __name__ == '__main__':
    pv = os.environ.get('PODGLAD')
    main([float(x) for x in pv.split(',')] if pv else None)
