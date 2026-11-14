import math
INK,OCH,GOLD,EUC,SAND='#10251F','#E2642A','#F2B544','#3E7C68','#F4E9D6'
def f(v): return ('%.2f'%v).rstrip('0').rstrip('.')
def rtri(pts,r):
    # rounded polygon path
    n=len(pts);d=''
    for i in range(n):
        p0,p1,p2=pts[i-1],pts[i],pts[(i+1)%n]
        v1=(p0[0]-p1[0],p0[1]-p1[1]);v2=(p2[0]-p1[0],p2[1]-p1[1])
        l1=math.hypot(*v1);l2=math.hypot(*v2)
        ang=math.acos((v1[0]*v2[0]+v1[1]*v2[1])/l1/l2)
        t=r/math.tan(ang/2)
        a=(p1[0]+v1[0]/l1*t,p1[1]+v1[1]/l1*t);b=(p1[0]+v2[0]/l2*t,p1[1]+v2[1]/l2*t)
        d+=('M' if i==0 else 'L')+f(a[0])+' '+f(a[1])+'A'+f(r)+' '+f(r)+' 0 0 1 '+f(b[0])+' '+f(b[1])
    return d+'Z'
def ellipse_path(cx,cy,rx,ry,rot):
    # rotated ellipse as two arcs
    a=math.radians(rot);dx=math.sin(a)*ry;dy=-math.cos(a)*ry
    x1,y1=cx+dx,cy+dy;x2,y2=cx-dx,cy-dy
    return f"M{f(x1)} {f(y1)}A{f(rx)} {f(ry)} {f(rot)} 1 1 {f(x2)} {f(y2)}A{f(rx)} {f(ry)} {f(rot)} 1 1 {f(x1)} {f(y1)}Z"
# GRID 128, module 8
PT=64      # pouch top
PL,PR=16,112
PC=72      # center of bottom semicircle
PRAD=48
TRI=[(44,26),(92,53),(44,80)]
TRIR=6
EAR1=(49.6,22.6,5.2,11,-14); EAR2=(63,26,5.2,11,24)
def pouch(r=3):
    return (f"M{PL} {PT+r}A{r} {r} 0 0 1 {PL+r} {PT}H{PR-r}A{r} {r} 0 0 1 {PR} {PT+r}V{PC}"
            f"A{PRAD} {PRAD} 0 0 1 {PL} {PC}Z")
def stitch(col,w=3.4):
    return f'<path d="M27 75H101" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="5.2 6.2" fill="none"/>'
def joey():
    return ellipse_path(*EAR1)+ellipse_path(*EAR2)+rtri(TRI,TRIR)
def mark_body(joeycol=INK,pouchcol=OCH,stitchcol=SAND,mono=False,simple=False,bg=None):
    s=''
    if mono:
        # joey cut by gap above pouch
        s+=f'<defs><clipPath id="cj"><rect x="0" y="0" width="128" height="{PT-4.5}"/></clipPath><mask id="ms"><rect width="128" height="128" fill="#fff"/>{stitch("#000")}</mask></defs>'
        s+=f'<path d="{joey()}" fill="{joeycol}" clip-path="url(#cj)"/>'
        s+=f'<path d="{pouch()}" fill="{pouchcol}" mask="url(#ms)"/>'
    else:
        s+=f'<path d="{joey()}" fill="{joeycol}"/><path d="{pouch()}" fill="{pouchcol}"/>'
        if not simple: s+=stitch(stitchcol)
    return s
def svg(body,vb='0 0 128 128',w=None,h=None,title='Montaroo'):
    wh=f' width="{w}" height="{h}"' if w else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh}><title>{title}</title>{body}</svg>\n'
