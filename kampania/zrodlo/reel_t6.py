"""Reel do kafelka T6 (post 1): „A group of kangaroos is called a mob.” 1080×1920, 10 s.
Ta sama konstrukcja co reel_t2: drop 1.5 s, 3.5 s akcent, 6.5 s logo. Joeye stada wskakują na bity."""
import os, sys, math, subprocess
sys.argv_keep = list(sys.argv)
import reel_t2 as R
from trasa_lib import *

LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
R.LANG = LANG
R.TX = {'en': dict(k='ROO FACT #1', h=['A group of', 'kangaroos is', 'called a mob.'], s='Join ours. Link in bio.',
                   slogan='Hop from footage to film.', cta='Join the waitlist  ·  montaroo.com'),
        'pl': dict(k='KANGURZY FAKT #1', h=['Stado kangurów', 'po angielsku', 'to „mob”.'], s='Dołącz do naszego. Link w bio.',
                   slogan='Od nagrań do filmu jednym skokiem.', cta='Zapisz się na listę  ·  montaroo.com')}[LANG]
G = R.G
MOB = [(250, 190, SAND), (430, 300, GOLD), (620, 230, SAND), (800, 340, OCH), (965, 170, SAND)]
LAND_T = [1.5, 2.0, 2.5, 3.0, 3.5]            # każdy joey ląduje na bicie
TRAIL_IN = ((-300, G - 120), (150, G), 210)   # trasa z poprzedniego kafelka

def scene_layer(t, fade_all):
    s = ''
    a, b, h = TRAIL_IN
    u = R.clamp((t - 0.9) / 0.6)
    if u > 0: s += trail(R.partial(a, b, h, u), w=11, dash='22 22', op=round(fade_all, 3))
    for i, (x, hh, col) in enumerate(MOB):
        tl = LAND_T[i]
        if t < tl - 0.42: continue
        if t < tl:                              # w powietrzu: spada z góry po łuku
            v = (t - (tl - 0.42)) / 0.42
            y = G - hh / 2 - 520 * (1 - v) ** 2
            xx = x + 60 * (1 - v)
            s += joey(xx, y, hh, fill=col, rot=-8 * (1 - v), opacity=round(fade_all, 3))
            continue
        # po wylądowaniu: przysiad, potem wspólne podskoki stada na bitach 4.0–5.5
        v = (t - tl) / 0.2; sq = math.sin(R.clamp(v) * math.pi) * (1 if v < 1 else 0)
        jump = 0
        for tb in (4.0, 4.5, 5.0, 5.5):
            w = (t - tb) / 0.4
            if 0 <= w < 1: jump = max(jump, math.sin(w * math.pi) * (70 + 25 * (i % 2)))
        y = G - hh / 2 * (1 - 0.16 * sq) - jump
        s += joey(x, y, hh, fill=col, sx=1 + 0.14 * sq, sy=1 - 0.16 * sq, opacity=round(fade_all, 3))
    return s

R.scene_layer = scene_layer

if __name__ == '__main__':
    bg = R.bg_image()
    if len(sys.argv) > 2:
        for ts in sys.argv[2:]: R.frame(float(ts), bg).save(f'/tmp/r6_{ts}.png')
        sys.exit()
    name = f'{R.OUT}/reel-post-1_T6_{LANG}.mp4'
    mus = os.environ.get('MUZYKA', os.path.join(R.OUT, 'montaroo-hop_podklad.wav'))
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{R.W}x{R.H}', '-r', str(R.FPS), '-i', '-',
                          '-i', mus, '-t', str(R.DUR), '-af', f'afade=t=out:st={R.DUR-1.4}:d=1.4,loudnorm=I=-14:TP=-1:LRA=9,aresample=48000',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
                          '-movflags', '+faststart', '-shortest', name], stdin=subprocess.PIPE)
    for i in range(int(R.DUR * R.FPS)): p.stdin.write(R.frame(i / R.FPS, bg).tobytes())
    p.stdin.close(); p.wait(); print(name)
