"""Wspólne elementy kampanii „Trasa skoku”: fonty jako ścieżki, joey, torba, klipy, telefony, tło z poziomicami."""
import math, os, io, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FD = os.path.join(ROOT, 'brand', 'fonts')
INK, OCH, GOLD, EUC, SAND = '#10251F', '#E2642A', '#F2B544', '#3E7C68', '#F4E9D6'
LINE = '#183429'      # poziomice na tle

_F = {}
def font(name):
    if name not in _F:
        f = TTFont(os.path.join(FD, name))
        _F[name] = (f, f.getGlyphSet(), f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    return _F[name]
FONTS = {'G': ['gabarito-latin-800-normal.woff2', 'gabarito-latin-ext-800-normal.woff2'],
         'I4': ['inter-latin-400-normal.woff2', 'inter-latin-ext-400-normal.woff2'],
         'I5': ['inter-latin-500-normal.woff2', 'inter-latin-ext-500-normal.woff2'],
         'I6': ['inter-latin-600-normal.woff2', 'inter-latin-ext-600-normal.woff2'],
         'I7': ['inter-latin-700-normal.woff2', 'inter-latin-ext-700-normal.woff2']}

def text(s, fam='G', size=100, x=0, y=0, track=0.0, fill=SAND, opacity=1, anchor='start'):
    """tekst jako ścieżka SVG; zwraca (svg, szerokość)."""
    pen = SVGPathPen(None); cx = 0; parts = []
    for i, ch in enumerate(s):
        for fn in FONTS[fam]:
            f, gs, cm, hm, upm = font(fn)
            if ord(ch) in cm: break
        g = cm[ord(ch)]; k = size / upm
        p = SVGPathPen(gs); gs[g].draw(TransformPen(p, (k, 0, 0, -k, cx, 0)))
        parts.append(p.getCommands())
        cx += hm[g][0] * k + (track * size if i < len(s) - 1 else 0)
    dx = {'start': 0, 'middle': -cx / 2, 'end': -cx}[anchor]
    d = ''.join(parts)
    op = f' opacity="{opacity}"' if opacity != 1 else ''
    return f'<path transform="translate({x+dx:.1f} {y:.1f})" d="{d}" fill="{fill}"{op}/>', cx

def width(s, fam='G', size=100, track=0.0):
    return text(s, fam, size, track=track)[1]

# --- znak (siatka 128, jak w brand/logo/zrodlo/mark.py) ---
def _f(v): return ('%.2f' % v).rstrip('0').rstrip('.')
def _rtri(pts, r):
    n = len(pts); d = ''
    for i in range(n):
        p0, p1, p2 = pts[i-1], pts[i], pts[(i+1) % n]
        v1 = (p0[0]-p1[0], p0[1]-p1[1]); v2 = (p2[0]-p1[0], p2[1]-p1[1])
        l1 = math.hypot(*v1); l2 = math.hypot(*v2)
        ang = math.acos((v1[0]*v2[0]+v1[1]*v2[1])/l1/l2); t = r/math.tan(ang/2)
        a = (p1[0]+v1[0]/l1*t, p1[1]+v1[1]/l1*t); b = (p1[0]+v2[0]/l2*t, p1[1]+v2[1]/l2*t)
        d += ('M' if i == 0 else 'L')+_f(a[0])+' '+_f(a[1])+'A'+_f(r)+' '+_f(r)+' 0 0 1 '+_f(b[0])+' '+_f(b[1])
    return d+'Z'
def _ell(cx, cy, rx, ry, rot):
    a = math.radians(rot); dx = math.sin(a)*ry; dy = -math.cos(a)*ry
    x1, y1 = cx+dx, cy+dy; x2, y2 = cx-dx, cy-dy
    return f"M{_f(x1)} {_f(y1)}A{_f(rx)} {_f(ry)} {_f(rot)} 1 1 {_f(x2)} {_f(y2)}A{_f(rx)} {_f(ry)} {_f(rot)} 1 1 {_f(x1)} {_f(y1)}Z"
JOEY = _ell(49.6, 22.6, 5.2, 11, -14) + _ell(63, 26, 5.2, 11, 24) + _rtri([(44, 26), (92, 53), (44, 80)], 6)
POUCH = "M16 67A3 3 0 0 1 19 64H109A3 3 0 0 1 112 67V72A48 48 0 0 1 16 72Z"
# punkt „stóp” joeya w siatce 128: środek dolnej krawędzi trójkąta ~ (60, 80)

def joey(cx, cy, h, fill=SAND, rot=0, sx=1.0, sy=1.0, opacity=1):
    """joey wyśrodkowany w (cx,cy); h = wysokość postaci (uszy..dół trójkąta ~69 jednostek)."""
    k = h / 69.0
    op = f' opacity="{opacity}"' if opacity != 1 else ''
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot:.1f}) scale({k*sx:.4f} {k*sy:.4f}) translate(-64 -45.5)"{op}>'
            f'<path d="{JOEY}" fill="{fill}"/></g>')

def mark(cx, cy, size, joeycol=SAND, pouchcol=OCH, stitchcol=INK, joey_dy=0):
    """pełny znak (joey w torbie), size = bok kwadratu 128."""
    k = size / 128
    return (f'<g transform="translate({cx-size/2:.1f} {cy-size/2:.1f}) scale({k:.4f})">'
            f'<g transform="translate(0 {joey_dy:.2f})"><path d="{JOEY}" fill="{joeycol}"/></g>'
            f'<path d="{POUCH}" fill="{pouchcol}"/>'
            f'<path d="M27 75H101" stroke="{stitchcol}" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="5.2 6.2" fill="none"/></g>')

def clip_card(cx, cy, w, h, rot, fill, play=INK):
    r = h * 0.12; t = h * 0.22
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})">'
            f'<rect x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="{fill}"/>'
            f'<path d="M{-t*0.6:.1f} {-t:.1f}L{t:.1f} 0L{-t*0.6:.1f} {t:.1f}Z" fill="{play}" opacity=".85" stroke="{play}" stroke-width="{t*0.25:.1f}" stroke-linejoin="round"/></g>')

def phone(cx, cy, w, h, rot, fill, screen):
    r = w * 0.2; m = w * 0.07
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})">'
            f'<rect x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="{fill}"/>'
            f'<rect x="{-w/2+m:.1f}" y="{-h/2+m:.1f}" width="{w-2*m:.1f}" height="{h-2*m:.1f}" rx="{r-m:.1f}" fill="{screen}"/>'
            f'<rect x="{-w*0.14:.1f}" y="{-h/2+m*1.6:.1f}" width="{w*0.28:.1f}" height="{m*0.9:.1f}" rx="{m*0.45:.1f}" fill="{fill}"/></g>')

def contours(W, Y0, Y1, centers, seed=3, step=46, n=34, sw=2.4, col=LINE):
    """poziomice (jak na mapie) – ciągłe przez wszystkie kafelki."""
    rnd = random.Random(seed); out = []
    for (cx, cy, r0, ph) in centers:
        for k in range(n):
            r = r0 + k * step; pts = []
            for i in range(181):
                a = 2 * math.pi * i / 180
                q = r * (1 + 0.10 * math.sin(3 * a + ph + k * 0.17) + 0.05 * math.sin(5 * a - ph * 2 + k * 0.11)
                         + 0.0 * math.sin(9 * a + k * 0.3))
                pts.append((cx + q * math.cos(a) * 1.25, cy + q * math.sin(a)))
            d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    return f'<g>{"".join(out)}</g>'

def hop(x1, y1, x2, y2, h):
    """łuk skoku (parabola jako krzywa kwadratowa), h = wysokość nad wyższym punktem."""
    mx = (x1 + x2) / 2; top = min(y1, y2) - h
    cy = 2 * top - (y1 + y2) / 2
    return f'M{x1:.1f} {y1:.1f}Q{mx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}'

def hop_point(x1, y1, x2, y2, h, t):
    mx = (x1 + x2) / 2; top = min(y1, y2) - h; cy = 2 * top - (y1 + y2) / 2
    x = (1-t)**2*x1 + 2*(1-t)*t*mx + t*t*x2; y = (1-t)**2*y1 + 2*(1-t)*t*cy + t*t*y2
    dx = 2*(1-t)*(mx-x1) + 2*t*(x2-mx); dy = 2*(1-t)*(cy-y1) + 2*t*(y2-cy)
    return x, y, math.degrees(math.atan2(dy, dx))

def trail(d, col=GOLD, w=10, dash='4 26', op=1):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-dasharray="{dash}" opacity="{op}"/>')
