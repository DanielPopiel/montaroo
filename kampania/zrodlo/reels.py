"""Reele postów 2, 3, 4 i 6 siatki „Trasa skoku” (posty 1 i 5: reel_t6.py, reel_t2.py).
Uruchom: python reels.py <en|pl> <nr_posta> [czasy klatek do podglądu...]
Konstrukcja jak w reszcie: drop 1.5 s, akcent 3.5 s, napis pomocniczy 3.9 s, przerwa 6.0, logo 6.5 s."""
import os, sys, math, subprocess
import reel_t2 as R
from trasa_lib import *

LANG = sys.argv[1]; POST = int(sys.argv[2])
R.LANG = LANG
G = R.G
clamp, eo, eback, eio = R.clamp, R.eo, R.eback, R.eio

TXT = {
 2: {'en': dict(k='FAMILY TRIPS', h=['5 phones.', '1 film.'], s="Everyone's footage. One story.", size=150),
     'pl': dict(k='RODZINNE WYJAZDY', h=['5 telefonów.', '1 film.'], s='Nagrania wszystkich. Jedna historia.', size=140)},
 3: {'en': dict(k='ROO FACT #2', h=['Kangaroos', "don't hop", 'backwards.'], s='Neither do we. Folder in, film out.', size=124),
     'pl': dict(k='KANGURZY FAKT #2', h=['Kangury nie', 'skaczą', 'do tyłu.'], s='My też nie. Folder na wejściu, film na wyjściu.', size=124)},
 4: {'en': dict(k='ROO FACT #3', h=['A joey stays', 'in the pouch', 'for 8 months.'], s='Your footage never leaves it. Offline.', size=112),
     'pl': dict(k='KANGURZY FAKT #3', h=['Młode kangura', 'siedzi w torbie', 'ok. 8 miesięcy.'], s='Twoje nagrania nie wychodzą z niej wcale. Offline.', size=104)},
 6: {'en': dict(k='SOUND FAMILIAR?', h=['1,434 clips.', 'Never watched.'], s='Every trip ends up in a folder.', size=124),
     'pl': dict(k='ZNASZ TO?', h=['1 434 nagrania.', 'Nieobejrzane.'], s='Każda podróż kończy w folderze.', size=112)},
}
END = {'en': dict(slogan='Hop from footage to film.', cta='Join the waitlist  ·  montaroo.com'),
       'pl': dict(slogan='Od nagrań do filmu jednym skokiem.', cta='Zapisz się na listę  ·  montaroo.com')}[LANG]
import rzad3
TXT.update({k: v for k, v in rzad3.TXT.items()})
R.TX = dict(TXT[POST][LANG], **END)
OP = lambda f: f' opacity="{f:.3f}"'

def drop_in(t, t_land, dur=0.4, height=480):
    """pozycja spadania (0 = na miejscu) i przysiad po lądowaniu."""
    if t < t_land - dur: return None, 0
    if t < t_land:
        v = (t - (t_land - dur)) / dur; return -height * (1 - v) ** 2, 0
    v = (t - t_land) / 0.2
    return 0, math.sin(clamp(v) * math.pi) if v < 1 else 0

def hopper(t, hops, times, hh=200, col=SAND):
    """joey przechodzący kolejne łuki; times[i] = (start, koniec) łuku i."""
    for (a, b, h), (t0, t1) in zip(hops, times):
        if t0 <= t < t1:
            x, y, ang = hop_point(*a, *b, h, (t - t0) / (t1 - t0))
            return joey(x, y - hh * 0.55, hh, fill=col, rot=ang * 0.35)
    return ''

def trail_upto(t, hops, times, fade):
    d = ''
    for (a, b, h), (t0, t1) in zip(hops, times):
        u = clamp((t - t0) / (t1 - t0))
        if u > 0: d += R.partial(a, b, h, u)
    return trail(d, w=11, dash='22 22', op=round(fade, 3)) if d else ''

# ---------- post 2: 5 telefonów → 1 film ----------
PHONES = [(325, -10, EUC), (445, -4, OCH), (565, 1, GOLD), (685, 6, SAND), (805, 11, '#2C5A4B')]
def scene2(t, fade):
    s = ''; merge = eio((t - 4.6) / 0.6)
    for i, (x, r, f) in enumerate(PHONES):
        dy, sq = drop_in(t, 1.5 + i * 0.5)
        if dy is None: continue
        xx = x + (565 - x) * merge; sc = 1 - 0.5 * merge
        y = G - 105 + dy - 120 * merge
        o = fade * (1 - merge)
        if o < 0.01: continue
        s += (f'<g{OP(o)} transform="translate({xx:.1f} {y:.1f}) scale({sc * (1 + 0.1 * sq):.3f} {sc * (1 - 0.1 * sq):.3f}) translate({-xx:.1f} {-y:.1f})">'
              + phone(xx, y, 108, 216, r * (1 - merge), f, INK)
              + f'<g transform="translate({xx:.1f} {y:.1f}) rotate({r * (1 - merge):.1f})"><path d="M-14 -22L24 0L-14 22Z" fill="{f}" stroke="{f}" stroke-width="8" stroke-linejoin="round"/></g></g>')
    # jeden film
    k = eback((t - 4.9) / 0.45, 1.8)
    if k > 0.01:
        cx, cy, w, h = 565, G - 230, 560 * k, 315 * k
        s += (f'<g{OP(fade)}><rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{28 * k:.1f}" fill="{OCH}"/>'
              f'<path d="M{cx - 40 * k:.1f} {cy - 52 * k:.1f}L{cx + 58 * k:.1f} {cy:.1f}L{cx - 40 * k:.1f} {cy + 52 * k:.1f}Z" fill="{INK}" stroke="{INK}" stroke-width="{14 * k:.1f}" stroke-linejoin="round"/></g>')
    hops = [((-60, G - 40), (1140, G - 40), 470)]; times = [(3.55, 4.55)]
    s += trail_upto(t, hops, times, fade * (1 - eio((t - 4.6) / 0.4)))
    s += hopper(t, hops, times)
    return s

# ---------- post 3: nie skaczemy do tyłu ----------
H3 = [((-330, G - 40), (250, G), 150), ((250, G), (560, G), 140), ((560, G), (870, G), 140), ((870, G), (1180, G), 140)]
T3 = [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
def scene3(t, fade):
    s = trail_upto(t, H3, T3, fade)
    for (a, b, h), (t0, t1) in list(zip(H3, T3))[1:]:
        if t > (t0 + t1) / 2:
            x, y, _ = hop_point(*a, *b, h, 0.5); k = eback((t - (t0 + t1) / 2) / 0.25, 2)
            s += (f'<g{OP(fade)} transform="translate({x:.1f} {y - 47:.1f}) scale({k:.3f})"><path d="M-12 -22l26 22l-26 22" fill="none" '
                  f'stroke="{GOLD}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></g>')
    s += hopper(t, H3, T3)
    # „do tyłu?” – przekreślona strzałka w lewo
    k = eback((t - 3.5) / 0.35, 2)
    if k > 0.01:
        cx, cy = 600, G - 345
        s += (f'<g{OP(fade)} transform="translate({cx} {cy}) scale({k:.3f})">'
              f'<path d="M150 0H-130M-60 -70L-140 0L-60 70" fill="none" stroke="{SAND}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/></g>')
    k2 = eback((t - 3.75) / 0.3, 2.4)
    if k2 > 0.01:
        cx, cy = 600, G - 345
        s += (f'<g{OP(fade)} transform="translate({cx} {cy}) scale({0.8*k2:.3f})">'
              f'<path d="M-120 -120L120 120M120 -120L-120 120" stroke="{OCH}" stroke-width="30" stroke-linecap="round"/></g>')
    return s

# ---------- post 4: joey w torbie, bez chmury ----------
MX, MY, MS = 440, G - 70, 540
def cloud(cx, cy, k, col):
    return (f'<g transform="translate({cx} {cy}) scale({k:.3f})"><path d="M-110 50H110A60 60 0 0 0 95 -55A80 80 0 0 0 -50 -70A70 70 0 0 0 -110 50Z" '
            f'fill="none" stroke="{col}" stroke-width="16" stroke-linejoin="round"/>'
            f'<path d="M0 30V-30M-28 -4L0 -32L28 -4" fill="none" stroke="{col}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>')
def scene4(t, fade):
    s = ''; kk = MS / 128
    jx, jy, jh = MX, MY - MS / 2 + 45.5 * kk, 69 * kk
    hops = [((-260, G - 120), (110, G - 60), 160), ((110, G - 60), (jx, jy + jh * 0.55 - 30), 330)]
    times = [(1.5, 2.3), (2.3, 3.5)]
    s += trail_upto(t, hops, times, fade * (1 - eio((t - 3.6) / 0.5)))
    if t < 3.5: s += hopper(t, hops, times, hh=230)
    else:
        v = (t - 3.5) / 0.35; dip = math.sin(clamp(v) * math.pi) * 40 if v < 1 else 0
        s += f'<g{OP(fade)}>' + joey(jx, jy + dip, jh, fill=SAND) + '</g>'
    wob = math.sin(clamp((t - 3.5) / 0.4) * math.pi * 2) * 0.04 if 3.5 <= t < 3.9 else 0
    s += (f'<g{OP(fade)} transform="translate({MX} {MY}) scale({1 + wob:.3f} {1 - wob:.3f}) translate({-MX} {-MY})">'
          + mark(MX, MY, MS, joeycol='none', pouchcol=OCH, stitchcol=INK) + '</g>')
    k = eback((t - 4.0) / 0.35, 1.8)
    if k > 0.01:
        s += f'<g{OP(fade)}>' + cloud(850, G - 330, k * 0.9, SAND) + '</g>'
    k2 = eback((t - 4.35) / 0.3, 2.2)
    if k2 > 0.01:
        s += f'<g{OP(fade)} transform="translate(850 {G - 330}) scale({k2:.3f})"><path d="M-130 -110L130 110" stroke="{OCH}" stroke-width="26" stroke-linecap="round"/></g>'
    return s

# ---------- post 6: 1 434 klipy ----------
PILE = [(150, 1240, -8), (300, 1250, 6), (450, 1245, -3), (220, 1160, 12), (380, 1170, -10), (300, 1088, 4),
        (470, 1150, 15), (140, 1310, 3), (420, 1325, -6), (260, 1330, 9)]
COLS = [OCH, GOLD, EUC, SAND, '#2C5A4B', OCH, GOLD, SAND, EUC, EUC]
def scene6(t, fade):
    s = ''; order = sorted(range(len(PILE)), key=lambda i: -PILE[i][1])
    for n, i in enumerate(order):
        x, y, r = PILE[i]; y = y - 1200 + G - 40
        tl = 1.5 + n * 0.2
        dy, sq = drop_in(t, tl, 0.35, 700)
        if dy is None: continue
        s += f'<g{OP(fade)}>' + clip_card(x, y + dy, 190, 124, r, COLS[n], INK) + '</g>'
    # licznik
    if t >= 1.5:
        u = clamp((t - 1.5) / 2.0); val = int(round(1434 * (1 - (1 - u) ** 2)))
        num = f'{val:,}' if LANG == 'en' else f'{val:,}'.replace(',', ' ')
        lab = 'clips' if LANG == 'en' else 'nagrania'
        p, _ = text(num, 'G', 120, 600, G - 70, track=-0.03, fill=GOLD, opacity=round(fade, 3))
        q, _ = text(lab, 'I6', 38, 604, G - 10, fill=SAND, opacity=round(0.7 * fade, 3))
        s += p + q
    hops = [((470, G - 230), (1180, G - 110), 300)]; times = [(3.6, 4.6)]
    if 3.5 <= t < 3.6:
        v = (t - 3.5) / 0.1; s += joey(470, G - 230 - 110 + (1 - v) * 80, 200, fill=SAND)
    s += trail_upto(t, hops, times, fade); s += hopper(t, hops, times)
    return s


# ---------- rząd 3: posty 7–9 ----------
def scene7(t, fade):
    s = f'<g{OP(fade)}>' + rzad3.scene_roll(t, 0, G, LANG) + '</g>'
    hops = [((-120, G + 20), (180, G + 20), 90), ((180, G + 20), (480, G + 20), 90), ((480, G + 20), (780, G + 20), 90), ((780, G + 20), (1180, G - 20), 110)]
    times = [(3.5, 3.75), (3.75, 4.0), (4.0, 4.25), (4.25, 4.6)]
    return s + trail_upto(t, hops, times, fade) + hopper(t, hops, times, hh=170)

def scene8(t, fade):
    s = f'<g{OP(fade)}>' + rzad3.scene_gauge(t, 0, G, LANG) + '</g>'
    hops = [((-140, G), (1220, G), 470)]; times = [(3.5, 4.5)]
    s += trail_upto(t, hops, times, fade)
    if 3.5 <= t < 4.5:
        x, y, ang = hop_point(*hops[0][0], *hops[0][1], hops[0][2], (t - 3.5))
        for i in range(3):
            s += f'<path d="M{x - 130 - i * 18:.1f} {y - 150 + i * 40:.1f}h-{70 - i * 15}" stroke="{SAND}" stroke-opacity=".5" stroke-width="8" stroke-linecap="round"/>'
        s += hopper(t, hops, times)
    return s

def scene9(t, fade):
    s = f'<g{OP(fade)}>' + rzad3.scene_chat(t, 0, G, LANG, show_joey=t < 3.8) + '</g>'
    _, bx, W = rzad3.bubble(996, G - 150, rzad3.BUB[LANG][3], GOLD, INK, True)
    hops = [((bx - 70, G - 102), (1200, G - 40), 260)]; times = [(3.8, 4.7)]
    return s + trail_upto(t, hops, times, fade) + hopper(t, hops, times, hh=96)

R.scene_layer = {2: scene2, 3: scene3, 4: scene4, 6: scene6, 7: scene7, 8: scene8, 9: scene9}[POST]
TILE = {2: 'T5', 3: 'T4', 4: 'T3', 6: 'T1', 7: 'T9', 8: 'T8', 9: 'T7'}[POST]

if __name__ == '__main__':
    bg = R.bg_image()
    if len(sys.argv) > 3:
        for ts in sys.argv[3:]: R.frame(float(ts), bg).save(f'/tmp/p{POST}_{ts}.png')
        sys.exit()
    name = f'{R.OUT}/reel-post-{POST}_{TILE}_{LANG}.mp4'
    mus = os.environ.get('MUZYKA', os.path.join(R.OUT, 'montaroo-hop_podklad.wav'))
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{R.W}x{R.H}', '-r', str(R.FPS), '-i', '-',
                          '-i', mus, '-t', str(R.DUR), '-af', f'afade=t=out:st={R.DUR-1.4}:d=1.4,loudnorm=I=-14:TP=-1:LRA=9,aresample=48000',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ac', '2',
                          '-movflags', '+faststart', '-shortest', name], stdin=subprocess.PIPE)
    for i in range(int(R.DUR * R.FPS)): p.stdin.write(R.frame(i / R.FPS, bg).tobytes())
    p.stdin.close(); p.wait(); print(name)
