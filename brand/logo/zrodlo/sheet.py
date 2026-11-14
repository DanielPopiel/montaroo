from mark import *
import mark, word
L='brand/logo/svg/'
def rd(n): return open(L+n+'.svg').read()
# construction drawing
grid=''.join(f'<path d="M{i} 0V128M0 {i}H128" stroke="#3E7C68" stroke-opacity=".28" stroke-width=".25"/>' for i in range(0,129,8))
c='#10251F'
cons=(f'<circle cx="64" cy="72" r="48" fill="none" stroke="{c}" stroke-width=".45" stroke-dasharray="1.2 1"/>'
 f'<path d="M16 64H112M16 120H112M64 4V124M44 26V80M44 26L92 53L44 80" stroke="{c}" stroke-width=".45" fill="none" stroke-dasharray="1.2 1"/>'
 f'<circle cx="64" cy="72" r="1.2" fill="{c}"/>')
lab=lambda x,y,t:f'<text x="{x}" y="{y}" font-family="Inter" font-size="3.2" fill="#10251F">{t}</text>'
txt=lab(114,63,'góra torby')+lab(114,121,'dno torby')+lab(66,76.5,'R 48')+lab(93,52,'play: trójkąt 48×54, r 6')+lab(70,12,'uszy: elipsy 5,2×11')
con=svg(f'<rect width="150" height="128" fill="#FBF6EC"/>'+grid+'<g opacity=".32">'+mark_body()+'</g>'+cons+txt,vb='0 0 150 128')
open('brand/logo/montaroo-konstrukcja.svg','w').write(con)
