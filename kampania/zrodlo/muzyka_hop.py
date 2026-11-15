"""„Montaroo Hop” – własny, chwytliwy podkład 120 BPM (10 s) zgrany z animacją Reela.
0.0–1.5 intro (stłumiony motyw, riser, werbel)  ·  1.5 DROP = skok joeya („boing”)
3.5 lądowanie (uderzenie)  ·  6.0–6.5 przerwa  ·  6.5 joey wyskakuje z torby (logo)  ·  9.5 akord końcowy.
Motyw: skoki o oktawę w melodii = kangurze susy. Akordy C–G–Am–F. Brak licencji zewnętrznych."""
import numpy as np, os, sys, wave
from scipy.signal import butter, sosfilt
from pedalboard import HighShelfFilter, Pedalboard, Reverb, Delay, Compressor, Limiter, Chorus, HighpassFilter, LowpassFilter, Gain, Distortion

SR = 48000; BPM = 120; B = 60 / BPM; S16 = B / 4; DUR = 10.0
N = int(SR * DUR)
DROP, LAND, POP, END = 1.5, 3.5, 6.5, 9.5
rng = np.random.default_rng(7)

def hz(n):
    names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    o = int(n[-1]); k = names[n[:-1]]
    return 440 * 2 ** ((k + 12 * (o + 1) - 69) / 12)

def bus(): return np.zeros((2, N))
def put(b, sig, at, g=1.0, pan=0.0):
    i = int(round(at * SR))
    if i >= N: return
    if sig.ndim == 1: sig = np.stack([sig * np.sqrt((1 - pan) / 2) * 1.414, sig * np.sqrt((1 + pan) / 2) * 1.414])
    j = min(N, i + sig.shape[1]); b[:, i:j] += sig[:, :j - i] * g

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)

def polyblep_saw(freq, L, phase0=0.0):
    t = np.arange(L); dt = freq / SR
    ph = (phase0 + t * dt) % 1.0
    s = 2 * ph - 1
    m = ph < dt; x = ph[m] / dt; s[m] -= x + x - x * x - 1
    m = ph > 1 - dt; x = (ph[m] - 1) / dt; s[m] -= x * x + x + x + 1
    return s

def env_adsr(L, a=0.005, d=0.1, s=0.6, r=0.05):
    e = np.full(L, s); ia = max(1, int(a * SR)); idd = max(1, int(d * SR)); ir = max(1, int(r * SR))
    e[:ia] = np.linspace(0, 1, ia)[:L] if L >= ia else np.linspace(0, 1, L)
    if L > ia: e[ia:ia + idd] = np.linspace(1, s, idd)[:max(0, min(idd, L - ia))]
    if L > ir: e[-ir:] *= np.linspace(1, 0, ir)
    return e

# ---------- bębny ----------
def kick(g=1.0):
    L = int(0.42 * SR); x = np.arange(L) / SR
    f = 54 + 120 * np.exp(-x * 34) + 40 * np.exp(-x * 300)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 9)
    click = hp(rng.standard_normal(L), 2500) * np.exp(-x * 900) * 0.18
    return np.tanh((body + click) * 1.6) * g

def clap():
    L = int(0.35 * SR); x = np.arange(L) / SR; nz = bp(rng.standard_normal(L), 900, 4500)
    e = np.zeros(L)
    for k, dly in enumerate((0, 0.009, 0.018, 0.027)):
        i = int(dly * SR); e[i:] += np.exp(-(x[: L - i]) * (60 if k < 3 else 14)) * (0.7 if k < 3 else 1)
    body = np.sin(2 * np.pi * 190 * x) * np.exp(-x * 30) * 0.5
    return (nz * e * 0.38 + body) * 0.9

def snare16():
    L = int(0.12 * SR); x = np.arange(L) / SR
    return (bp(rng.standard_normal(L), 1200, 5000) * np.exp(-x * 40) * 0.35 + np.sin(2 * np.pi * 210 * x) * np.exp(-x * 35) * 0.3)

def hat(open_=False):
    L = int((0.22 if open_ else 0.05) * SR); x = np.arange(L) / SR
    return hp(rng.standard_normal(L), 7500, 4) * np.exp(-x * (14 if open_ else 95)) * (0.13 if open_ else 0.09)

def crash():
    L = int(2.2 * SR); x = np.arange(L) / SR
    return hp(rng.standard_normal(L), 5000, 2) * np.exp(-x * 4.5) * 0.07

def boom():
    L = int(1.2 * SR); x = np.arange(L) / SR
    return np.tanh(np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-x * 10)) / SR) * np.exp(-x * 2.6) * 1.4)

def boing(f0=330, f1=990, L_s=0.32):
    """„sus” joeya – szybki wznoszący się dźwięk z lekkim wibrato."""
    L = int(L_s * SR); x = np.arange(L) / SR; u = x / L_s
    f = f0 * (f1 / f0) ** (np.sin(u * np.pi / 2)) * (1 + 0.03 * np.sin(2 * np.pi * 22 * x))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return s * np.minimum(1, x * 400) * np.exp(-x * 7) * 0.5

def riser(L_s, f_from=300, f_to=9000):
    L = int(L_s * SR); x = np.arange(L) / SR; u = x / L_s
    nz = rng.standard_normal(L); out = np.zeros(L); seg = 2048
    for i in range(0, L, seg):
        fc = f_from * (f_to / f_from) ** (i / L)
        out[i:i + seg] = bp(nz[i:i + seg + 0], max(60, fc * 0.6), min(SR / 2 - 100, fc * 1.4), 1)[: len(out[i:i + seg])]
    return out * u ** 2 * 0.22

# ---------- instrumenty ----------
def pluck(freq, dur, bright=1.0):
    L = int((dur + 0.25) * SR); x = np.arange(L) / SR
    s = 0.6 * polyblep_saw(freq, L) + 0.4 * polyblep_saw(freq * 1.005, L, 0.3) + 0.25 * np.sign(np.sin(2 * np.pi * freq * x))
    # filtr z obwiednią: jasny atak, szybkie zamknięcie
    out = np.zeros(L); seg = 256
    for i in range(0, L, seg):
        fc = 700 + 5200 * bright * np.exp(-x[i] * 14)
        out[i:i + seg] = lp(s[i:i + seg], min(fc, 15000), 1)
    e = np.exp(-x * 5.5) * np.minimum(1, x * 600); e[int(dur * SR):] *= np.exp(-(x[int(dur * SR):] - dur) * 30)
    return out * e * 0.5

def supersaw_chord(notes, dur, cutoff=2600):
    L = int(dur * SR); l = np.zeros(L); r = np.zeros(L)
    for n in notes:
        f = hz(n)
        for k, det in enumerate((-0.11, -0.06, -0.025, 0, 0.025, 0.06, 0.11)):
            s = polyblep_saw(f * 2 ** (det / 12), L, rng.random())
            (l if k % 2 == 0 else r)[:] += s * (0.9 if det == 0 else 0.55)
            if det == 0: r += s * 0.5
    e = env_adsr(L, 0.02, 0.4, 0.75, 0.12)
    return np.stack([lp(l, cutoff), lp(r, cutoff)]) * e * 0.045

def bass_note(freq, dur):
    L = int(dur * SR); x = np.arange(L) / SR
    s = polyblep_saw(freq, L) * 0.6 + np.sin(2 * np.pi * freq * x) * 0.9
    s = lp(s, 1100, 2)
    return np.tanh(s * 1.4) * env_adsr(L, 0.004, 0.08, 0.8, 0.03) * 0.55

# ---------- aranżacja ----------
CH = [('C', ['C4', 'E4', 'G4', 'C5'], 'C2'), ('G', ['B3', 'D4', 'G4', 'D5'], 'G1'),
      ('Am', ['C4', 'E4', 'A4', 'C5'], 'A1'), ('F', ['C4', 'F4', 'A4', 'C5'], 'F1')]
HOOK = [  # (krok 1/16, nuta, długość w krokach) – skoki o oktawę = susy kangura
 [(0, 'C5', 2), (2, 'E5', 2), (4, 'G5', 1), (6, 'C6', 2), (9, 'G5', 1), (10, 'A5', 2), (12, 'G5', 2), (14, 'E5', 2)],
 [(0, 'D5', 2), (2, 'G5', 2), (4, 'B5', 1), (6, 'D6', 2), (9, 'B5', 1), (10, 'A5', 2), (12, 'G5', 2), (14, 'D5', 2)],
 [(0, 'C5', 2), (2, 'E5', 2), (4, 'A5', 1), (6, 'C6', 2), (9, 'A5', 1), (10, 'G5', 2), (12, 'E5', 2), (14, 'D5', 1), (15, 'E5', 1)],
 [(0, 'C5', 2), (2, 'F5', 2), (4, 'A5', 1), (6, 'C6', 3), (10, 'D6', 2), (12, 'E6', 4)],
]

def build():
    drums, bass, pad, lead, fx = bus(), bus(), bus(), bus(), bus()
    kicks = []
    # INTRO 0–1.5: stłumiony motyw (bar 4 → zapowiedź), riser, werbel
    t0 = DROP - 4 * B * 2  # motyw intro zaczyna się „przed” 0 – bierzemy końcówkę taktu
    for st, n, ln in HOOK[3]:
        at = st * S16                      # 0.0–1.4 s: stłumiona zapowiedź motywu na akordzie F
        if 0 <= at < DROP - 0.1:
            put(lead, lp(pluck(hz(n), ln * S16, 0.5), 1400), at, 0.8, pan=-0.1)
    put(pad, supersaw_chord(CH[3][1], DROP, cutoff=900), 0, 0.9)
    put(fx, riser(1.45, 400, 11000), 0.05, 0.6)
    for k in range(8):  # werbel 16-tki przyspieszający w ostatnim takcie przed dropem
        put(drums, snare16(), DROP - 1.0 + k * S16, 0.15 + 0.45 * k / 7, pan=0.1)
    put(fx, boing(), DROP - 0.02, 0.9, pan=0.15)
    # GŁÓWNA CZĘŚĆ 1.5–9.5
    for bar in range(4):
        tb = DROP + bar * 2.0; name, chord, root = CH[bar]
        for beat in range(4):
            t = tb + beat * B
            in_break = 6.0 <= t < POP
            if not in_break:
                put(drums, kick(), t, 1.0); kicks.append(t)
                put(drums, hat(open_=True), t + B / 2, 0.8, pan=0.25)
            if beat in (1, 3) and not in_break: put(drums, clap(), t, 0.85, pan=-0.05)
            for s16 in range(4):
                tt = t + s16 * S16
                if s16 != 2 and not in_break: put(drums, hat(), tt, 0.55 + 0.25 * (s16 == 0), pan=-0.3)
        # bas: ósemki z oktawą (podskok)
        pat = [0, 0, 12, 0, 0, 12, 0, 7]
        for i in range(16):
            t = tb + i * B / 2
            if 6.0 <= t < POP: continue
            put(bass, bass_note(hz(root) * 2 ** (pat[i % 8] / 12), B / 2 * 0.9), t, 1.0)
        # akordy
        put(pad, supersaw_chord(chord, 2.0), tb, 1.0)
        # motyw
        for st, n, ln in HOOK[bar]:
            t = tb + st * S16
            if 6.0 <= t < POP: continue
            put(lead, pluck(hz(n), ln * S16 * 0.95), t, 1.0, pan=0.05)
    # przerwa 6.0–6.5: riser + rolka, potem POP
    put(fx, riser(0.5, 800, 12000), 6.0, 0.8)
    for k in range(4): put(drums, snare16(), 6.0 + k * S16 * 2 * 0.5 + 0.25, 0.4 + 0.15 * k)
    put(fx, boing(392, 1176, 0.3), POP - 0.02, 0.85, pan=-0.15)
    # akcenty: lądowanie (3.5), pop logo (6.5)
    for t in (DROP, LAND, POP):
        put(fx, crash(), t, 0.9 if t != LAND else 1.0, pan=0.2)
        put(drums, boom(), t, 0.3)
    # FINAŁ 9.5: akord C + kick + crash, wybrzmienie
    put(drums, kick(1.1), END); put(drums, clap(), END, 0.7); put(fx, crash(), END, 0.9)
    put(pad, supersaw_chord(['C4', 'E4', 'G4', 'C5', 'E5'], DUR - END, cutoff=3200), END, 1.3)
    put(lead, pluck(hz('C6'), 0.45), END, 0.9); put(bass, bass_note(hz('C2'), DUR - END), END, 1.0)
    kicks.append(END)
    return drums, bass, pad, lead, fx, kicks

def sidechain(kicks, depth=0.55, rel=7.5):
    g = np.ones(N); x = np.arange(int(0.45 * SR)) / SR; dip = 1 - depth * np.exp(-x * rel) * np.minimum(1, x * 2000 + 0.6)
    for t in kicks:
        i = int(t * SR); j = min(N, i + len(dip)); g[i:j] = np.minimum(g[i:j], dip[: j - i])
    return g

def fxchain(x, board): return board(x.astype(np.float32), SR)

if __name__ == '__main__':
    out_path = sys.argv[1] if len(sys.argv) > 1 else 'montaroo_hop.wav'
    drums, bass, pad, lead, fx, kicks = build()
    sc = sidechain(kicks)
    drums = fxchain(drums, Pedalboard([Compressor(threshold_db=-14, ratio=3, attack_ms=8, release_ms=90), Gain(2)]))
    bass = fxchain(bass * sc, Pedalboard([HighpassFilter(32), Compressor(threshold_db=-16, ratio=3), Distortion(drive_db=4), Gain(-2)]))
    pad = fxchain(pad * sc, Pedalboard([HighpassFilter(180), Chorus(rate_hz=0.6, depth=0.25, mix=0.35), Reverb(room_size=0.6, wet_level=0.22, dry_level=0.85, width=1.0)]))
    lead = fxchain(lead, Pedalboard([HighpassFilter(250), Delay(delay_seconds=0.375, feedback=0.28, mix=0.22), Reverb(room_size=0.45, wet_level=0.16, dry_level=0.9)]))
    fx = fxchain(fx, Pedalboard([Reverb(room_size=0.7, wet_level=0.25, dry_level=0.8)]))
    mix = (drums * 0.9 + bass * 1.25 + pad * 0.9 + lead * 0.85 + fx * 0.6) * 0.42
    mix = fxchain(mix, Pedalboard([HighpassFilter(30), HighShelfFilter(cutoff_frequency_hz=7000, gain_db=-5), LowpassFilter(15500), Compressor(threshold_db=-10, ratio=2.2, attack_ms=15, release_ms=120), Limiter(threshold_db=-3, release_ms=80), Gain(-1.5)]))
    fl = int(0.35 * SR); mix[:, -fl:] *= np.linspace(1, 0, fl)
    pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2')
    w = wave.open(out_path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
    print(out_path, 'peak', float(np.abs(mix).max()))
