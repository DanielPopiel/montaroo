import os
from mark import *
from word import word, UPM, XH
OUT='brand/logo'; os.makedirs(OUT+'/svg',exist_ok=True); os.makedirs(OUT+'/png',exist_ok=True)
FS=114           # x-height == pouch height (56)
GAP=24
def W(col,x0,base): d,w=word(size=FS,x0=x0,baseline=base); return f'<path d="{d}" fill="{col}"/>',w
LSB=48*FS/UPM
VARIANTS={ # name: (joey,pouch,stitch,text,mono,bg)
 'kolor':        (INK,OCH,SAND,INK,False,None),
 'kolor-ciemne': (SAND,OCH,INK,SAND,False,INK),
 'mono-ciemny':  (INK,INK,None,INK,True,None),   # jeden kolor, na jasnym tle
 'mono-jasny':   (SAND,SAND,None,SAND,True,INK), # jeden kolor, na ciemnym tle
}
def body(v,scale=1,tx=0,ty=0):
    j,p,s,t,mono,bg=VARIANTS[v]
    return f'<g transform="translate({tx} {ty}) scale({scale})">'+mark_body(j,p,s or SAND,mono=mono)+'</g>'
files={}
for v,(j,p,s,t,mono,bg) in VARIANTS.items():
    # sam znak (crop 16..112 x 8..120 + 0 margin) -> keep 128 box
    files[f'montaroo-znak-{v}']=('0 0 128 128',body(v))
    # pozioma
    x0=112+GAP-LSB
    tp,w=W(t,x0,120)
    right=x0+LSB+ (w-LSB) ; vb=f'14 6 {right-14+4} 118'
    files[f'montaroo-poziome-{v}']=(vb,body(v)+tp)
    # pionowa: znak x2 nad napisem
    tw=w; sc=2.25; mw=128*sc
    cx=(tw)/2
    tp2,_=W(t,0,0)
    top=8*sc; markbottom=120*sc; gapv=40; base=markbottom+gapv+XH*FS/UPM+0  # baseline after x-height... 't' asc
    base=markbottom+gapv+ (609*FS/UPM)
    g=f'<g transform="translate({cx-64*sc} 0)">'+body(v,sc)+'</g>'+f'<g transform="translate(0 {base})">{tp2}</g>'
    files[f'montaroo-pionowe-{v}']=(f'{LSB-4} {top-4} {tw-LSB+8} {base+16-top+4}',g)
for n,(vb,b) in files.items():
    bgcol=None
    open(f'{OUT}/svg/{n}.svg','w').write(svg(b,vb,title='montaroo'))
print(len(files))
