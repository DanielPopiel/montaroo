# prosty, własny podkład 120 BPM (bez licencji zewnętrznych): stopa, klaśnięcie, hi-hat, bas, akord
import numpy as np, wave
SR=48000; DUR=20.0; BPM=120; B=60/BPM; T0=1.0
n=int(SR*DUR); out=np.zeros(n)
t=np.arange(n)/SR
def add(sig,at,g=1.0):
    i=int(at*SR); j=min(n,i+len(sig)); out[i:j]+=sig[:j-i]*g
def kick():
    L=int(.35*SR); x=np.arange(L)/SR; f=50+90*np.exp(-x*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-x*7)
def clap():
    L=int(.22*SR); x=np.arange(L)/SR; r=np.random.default_rng(1).standard_normal(L)
    env=np.exp(-x*22)*(1+0.6*np.sin(2*np.pi*90*x))
    return r*env*0.5
def hat():
    L=int(.06*SR); x=np.arange(L)/SR; r=np.random.default_rng(2).standard_normal(L); r=np.diff(np.concatenate([[0],r]))
    return r*np.exp(-x*70)*0.25
def tone(fr,L,dec=3,harm=(1,.5,.25)):
    x=np.arange(int(L*SR))/SR; s=sum(a*np.sin(2*np.pi*fr*(k+1)*x) for k,a in enumerate(harm))
    return s*np.exp(-x*dec)*np.minimum(1,x*200)
# riser przed pierwszym uderzeniem
x=t[:int(T0*SR)]; add(np.random.default_rng(3).standard_normal(len(x))*(x/T0)**3*0.12,0)
add(tone(110,1.0,1.5,(0.6,0.3)),0.0,0.3)
end=17.0
bar_roots=[110,87.31,130.81,98.0]  # A2 F2 C3 G2
k=0; tb=T0
while tb<DUR-0.01:
    beat=int(round((tb-T0)/B))
    if 9.0<=tb<13.0:   # przerwa: tylko akordy i stopa na 1
        if beat%4==0: add(kick(),tb,.7)
    else:
        add(kick(),tb,0.95)
        if beat%2==1: add(clap(),tb,0.7)
        add(hat(),tb+B/2,1.0)
        if tb>=15.0 and tb<17.0: add(hat(),tb+B/4,.7); add(hat(),tb+3*B/4,.7)
    if beat%4==0:
        r=bar_roots[(beat//4)%4]
        add(tone(r,B*4,1.2,(1,.4,.15)),tb,0.38)
        for m in (2,2.5198,2.9966): add(tone(r*m,B*4,0.9,(1,.2)),tb,0.09)
    if tb>=end: break
    tb+=B
# akcent końcowy na 17.0 + wybrzmienie
add(kick(),end,1.0); add(clap(),end,.6)
for m in (1,2,2.5198,2.9966,4): add(tone(110*m,3.0,0.8,(1,.3)),end,0.16 if m>1 else .4)
out=np.tanh(out*1.2); out/=np.max(np.abs(out))*1.12
fade=np.ones(n); fl=int(.4*SR); fade[-fl:]=np.linspace(1,0,fl); out*=fade
st=np.stack([out,out],1); pcm=(st*32767).astype('<i2')
w=wave.open('podklad.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close(); print('ok')
