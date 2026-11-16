"""Reklama „The Hop” – 3 klipy z Higgsfield + napisy + plansza końcowa z reel_t2. 1080×1920, 10 s.
python spot_hop.py <en|pl> droga.mp4 kanion.mp4 zachod.mp4 [wyjscie.mp4]"""
import io, os, sys, subprocess
import numpy as np, cairosvg
from PIL import Image
LANG = sys.argv[1]
sys.argv = [sys.argv[0], LANG] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_t2 as R
from trasa_lib import text, INK, SAND, GOLD, OCH

W, H, FPS, DUR = 1080, 1920, 30, 10.0
CLIPS = sys.argv[2:5]
OUTF = sys.argv[5] if len(sys.argv) > 5 else os.path.join(R.OUT, f'spot-hop_{LANG}.mp4')
# (klip, start w klipie, od, do) – cięcia na bitach: wejście bitu 1.5, lądowanie 3.5, plansza 6.3
SPD, SRC_FPS = 1.25, 24
CUTS = [(0, 0.4, 0.0, 1.5), (1, 0.9, 1.5, 3.5), (2, 0.3, 3.5, 6.3)]
WARIANT = os.environ.get('WARIANT', 'hop')
HOOK = {'en': [(0.1, 1.5, ['Hours of trip', 'footage?']), (1.55, 3.5, ['One hop.']),
               (3.6, 6.1, ['Montaroo cuts it', 'into a film.'])],
        'pl': [(0.1, 1.5, ['Godziny nagrań', 'z wyjazdu?']), (1.55, 3.5, ['Jeden skok.']),
               (3.6, 6.1, ['Montaroo zrobi', 'z nich film.'])]}[LANG]

if WARIANT == 'laptop':
    CUTS = [(0, 1.6, 0.0, 6.3)]   # jedno ciągłe ujęcie, bez skoków w czasie
    HOOK = {'en': [(0.1, 1.5, ['900 clips', 'from one trip.']), (1.55, 3.5, ['Editing them?', 'Days.']),
                   (3.6, 6.1, ['With Montaroo?', 'One hop.'])],
            'pl': [(0.1, 1.5, ['900 klipów', 'z jednego wyjazdu.']), (1.55, 3.5, ['Montaż?', 'Kilka dni.']),
                   (3.6, 6.1, ['Z Montaroo?', 'Jeden skok.'])]}[LANG]
    OUTF = sys.argv[5] if len(sys.argv) > 5 else os.path.join(R.OUT, f'spot-laptop_{LANG}.mp4')

if WARIANT == 'telefon':
    CUTS = [(0, 1.0, 0.0, 6.3)]
    HOOK = {'en': [(0.1, 1.5, ['47 GB', 'from one trip.']), (1.55, 3.5, ['Watched:', '0.']),
                   (3.6, 6.1, ['Montaroo turns it', 'into a film.'])],
            'pl': [(0.1, 1.5, ['47 GB', 'z jednego wyjazdu.']), (1.55, 3.5, ['Obejrzane:', '0.']),
                   (3.6, 6.1, ['Montaroo zrobi', 'z tego film.'])]}[LANG]
    OUTF = sys.argv[5] if len(sys.argv) > 5 else os.path.join(R.OUT, f'spot-telefon_{LANG}.mp4')

def read_clip(path):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf',
                        f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3)

def overlay(t):
    s = ''
    for a, b, lines in HOOK:
        if a <= t < b:
            o = R.eo((t - a) / 0.18) * (1 - R.eo((t - (b - 0.15)) / 0.15))
            y0 = 300 + (1 - R.eo((t - a) / 0.25)) * 40
            for i, ln in enumerate(lines):
                p, lw = text(ln, 'G', 104, 540, y0 + i * 118, track=-0.03, fill=SAND, anchor='middle', opacity=round(o, 3))
                s += p
    return s

def main():
    vids = [read_clip(c) for c in CLIPS if c]
    ff = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-i', os.environ.get('MUZYKA', os.path.join(R.OUT, 'montaroo-hop_podklad.wav')),
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-b:a', '256k', '-af', 'loudnorm=I=-14:TP=-1', '-shortest', '-movflags', '+faststart', OUTF],
                          stdin=subprocess.PIPE)
    ink = np.array([int(INK[i:i+2], 16) for i in (1, 3, 5)], np.uint8)
    for f in range(int(DUR * FPS)):
        t = f / FPS
        base = np.empty((H, W, 3), np.uint8); base[:] = ink
        for ci, st, a, b in CUTS:
            if a <= t < b:
                v = vids[ci]; idx = min(len(v) - 1, int(round((st + (t - a) * SPD) * SRC_FPS))); base = v[idx].copy()
                # lekki zoom-punch na cięciu
                if t - a < 0.12 and a > 0:
                    k = 1.06 - 0.5 * (t - a)
                    im = Image.fromarray(base).resize((int(W * k), int(H * k)), Image.BILINEAR)
                    x, y = (im.width - W) // 2, (im.height - H) // 2
                    base = np.asarray(im.crop((x, y, x + W, y + H)))
        img = Image.fromarray(base).convert('RGBA')
        if t >= 5.9:   # przejście w planszę: przyciemnienie do INK
            a = R.eio((t - 5.9) / 0.45)
            img = Image.blend(img, Image.new('RGBA', (W, H), tuple(ink) + (255,)), a)
        # gradient pod napisy
        svg_in = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/>'
                  '<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient></defs>'
                  f'<rect width="{W}" height="700" fill="url(#g)" opacity="{1 - R.eio((t - 5.9) / 0.45):.3f}"/>')
        svg_in += overlay(t) + R.endcard(t)
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{svg_in}</svg>'
        ov = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA')
        img.alpha_composite(ov)
        ff.stdin.write(img.convert('RGB').tobytes())
    ff.stdin.close(); ff.wait()
    print(OUTF)

if __name__ == '__main__':
    main()
