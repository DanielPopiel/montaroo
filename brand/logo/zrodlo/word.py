from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
F=TTFont(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'fonts', 'gabarito-latin-800-normal.woff2'))
UPM=F['head'].unitsPerEm; gs=F.getGlyphSet(); cmap=F.getBestCmap(); hm=F['hmtx']
os2=F['OS/2']
XH=os2.sxHeight; CAP=os2.sCapHeight
def word(text='montaroo',size=100,x0=0,baseline=0,track=-0.04):
    """returns path d, width"""
    s=size/UPM; pen=SVGPathPen(gs); x=0
    for i,ch in enumerate(text):
        g=cmap[ord(ch)]
        tp=TransformPen(pen,(s,0,0,-s,x0+x,baseline))
        gs[g].draw(tp)
        x+=hm[g][0]*s + (track*size if i<len(text)-1 else 0)
    return pen.getCommands(),x
def bbox(text='montaroo'):
    from fontTools.pens.boundsPen import BoundsPen
    bp=BoundsPen(gs);x=0
    for i,ch in enumerate(text):
        g=cmap[ord(ch)];tp=TransformPen(bp,(1,0,0,1,x,0));gs[g].draw(tp);x+=hm[g][0]-0.04*UPM
    return bp.bounds
if __name__=='__main__':
    print(UPM,XH,CAP,bbox())
