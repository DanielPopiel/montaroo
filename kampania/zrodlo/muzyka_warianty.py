"""Warianty podkładu do Reeli (10 s, 120 BPM, ta sama konstrukcja co „Montaroo Hop”):
drop 1.5 s = skok joeya, 3.5 s lądowanie, 6.0–6.5 przerwa, 6.5 logo, 9.5 akord końcowy.
Uruchom: python muzyka_warianty.py <styl> <plik.wav>   style: house, future, funk, tropical"""
import sys, os, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import muzyka_hop as M
from muzyka_hop import (SR, B, S16, N, DUR, DROP, LAND, POP, END, hz, bus, put, lp, hp, bp, polyblep_saw, env_adsr,
                        kick, clap, snare16, hat, crash, boom, boing, riser, supersaw_chord, bass_note, sidechain, fxchain)
from pedalboard import (Pedalboard, Reverb, Delay, Compressor, Limiter, Chorus, HighpassFilter, LowpassFilter, Gain,
                        Distortion, HighShelfFilter, Phaser)
rng = np.random.default_rng(11)

# ---------- nowe instrumenty ----------
def piano(freq, dur, vel=1.0):
    L = int((dur + 0.6) * SR); x = np.arange(L) / SR; s = np.zeros(L)
    for k, a in enumerate((1, .55, .32, .2, .12, .07, .04), 1):
        fk = freq * k * np.sqrt(1 + 0.0004 * k * k)
        s += a * np.sin(2 * np.pi * fk * x) * np.exp(-x * (2.2 + k * 1.1))
    s += hp(rng.standard_normal(L), 3000) * np.exp(-x * 300) * 0.05
    e = np.minimum(1, x * 800); e[int(dur * SR):] *= np.exp(-(x[int(dur * SR):] - dur) * 18)
    return s * e * 0.28 * vel

def organ_bass(freq, dur):
    L = int(dur * SR); x = np.arange(L) / SR
    s = np.sin(2 * np.pi * freq * x) + 0.45 * np.sin(4 * np.pi * freq * x) + 0.15 * np.sin(6 * np.pi * freq * x)
    return np.tanh(s * 1.2) * env_adsr(L, 0.004, 0.05, 0.85, 0.02) * 0.5

def whistle(freq, dur, prev=None):
    L = int((dur + 0.08) * SR); x = np.arange(L) / SR
    f = np.full(L, freq)
    if prev: g = np.minimum(1, x / 0.05); f = prev + (freq - prev) * g
    f = f * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * x) * np.minimum(1, x * 4))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.08 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    s += bp(rng.standard_normal(L), freq * 0.9, min(freq * 1.6, 15000), 1) * 0.12
    e = env_adsr(L, 0.02, 0.05, 0.9, 0.07)
    return s * e * 0.22

def clav(freq, dur):
    L = int((dur + 0.05) * SR); x = np.arange(L) / SR
    ph = (x * freq) % 1; s = np.where(ph < 0.22, 1.0, -0.28)
    s = bp(s, freq * 0.9, min(freq * 8, 9000), 1)
    e = np.exp(-x * 9) * np.minimum(1, x * 1500); e[int(dur * SR):] *= np.exp(-(x[int(dur * SR):] - dur) * 60)
    return s * e * 0.5

def marimba(freq, dur):
    L = int((dur + 0.4) * SR); x = np.arange(L) / SR
    s = np.sin(2 * np.pi * freq * x) * np.exp(-x * 7) + 0.35 * np.sin(2 * np.pi * freq * 3.93 * x) * np.exp(-x * 26)
    s += np.sin(2 * np.pi * freq * 9.2 * x) * np.exp(-x * 90) * 0.1
    return s * np.minimum(1, x * 1200) * 0.42

def brass(notes, dur):
    L = int((dur + 0.1) * SR); x = np.arange(L) / SR; s = np.zeros(L)
    for n in notes:
        f = hz(n)
        for d in (-0.08, 0, 0.08): s += polyblep_saw(f * 2 ** (d / 12), L, rng.random())
    fc = 900 + 3500 * np.minimum(1, x / 0.04) * np.exp(-x * 4)
    out = np.zeros(L)
    for i in range(0, L, 256): out[i:i + 256] = lp(s[i:i + 256], float(fc[i]), 1)
    return out * env_adsr(L, 0.01, 0.1, 0.7, 0.06) * 0.06

def shaker(acc=1.0):
    L = int(0.07 * SR); x = np.arange(L) / SR
    return bp(rng.standard_normal(L), 5000, 11000) * np.minimum(1, x * 300) * np.exp(-x * 60) * 0.12 * acc

def rim():
    L = int(0.06 * SR); x = np.arange(L) / SR
    return (np.sin(2 * np.pi * 1700 * x) * 0.6 + bp(rng.standard_normal(L), 2000, 6000) * 0.4) * np.exp(-x * 80) * 0.35

def sub808(freq, dur):
    L = int(dur * SR); x = np.arange(L) / SR
    f = freq * (1 + 0.9 * np.exp(-x * 40))
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 1.8) * env_adsr(L, 0.003, 0.1, 0.8, 0.05) * 0.5

def in_break(t): return 6.0 <= t < POP

# ---------- style ----------
def common_fx(fx, drums):
    put(fx, riser(1.45, 400, 11000), 0.05, 0.6)
    put(fx, boing(), DROP - 0.02, 0.9, pan=0.15)
    put(fx, riser(0.5, 800, 12000), 6.0, 0.8)
    put(fx, boing(392, 1176, 0.3), POP - 0.02, 0.85, pan=-0.15)
    for t in (DROP, LAND, POP, END):
        put(fx, crash(), t, 1.0); put(drums, boom(), t, 0.3)
    for k in range(8): put(drums, snare16(), DROP - 1.0 + k * S16, 0.15 + 0.45 * k / 7, pan=0.1)

def four_floor(drums, kicks, clap_on=(1, 3), openhat=True, closed=True, kick_g=1.0):
    for bar in range(4):
        tb = DROP + bar * 2.0
        for beat in range(4):
            t = tb + beat * B
            if in_break(t): continue
            put(drums, kick(kick_g), t); kicks.append(t)
            if beat in clap_on: put(drums, clap(), t, 0.85)
            if openhat: put(drums, hat(True), t + B / 2, 0.9, pan=0.25)
            if closed:
                for s in (1, 3): put(drums, hat(), t + s * S16, 0.8, pan=-0.3)

def style_house():
    """Piano house: radosne akordy fortepianu na „off-beatach”, organowy bas, klaśnięcia."""
    drums, bass, pad, lead, fx = bus(), bus(), bus(), bus(), bus(); kicks = []
    CH = [(['A3', 'C4', 'E4', 'A4'], 'A1'), (['F3', 'A3', 'C4', 'F4'], 'F1'), (['G3', 'C4', 'E4', 'G4'], 'C2'), (['G3', 'B3', 'D4', 'G4'], 'G1')]
    STAB = [0, 3, 6, 8, 11, 14]            # synkopowany rytm akordów (16-tki)
    for i, st in enumerate(STAB):          # intro: fortepian stłumiony
        if st * S16 < DROP:
            for n in CH[3][0]: put(lead, lp(piano(hz(n), 0.22, 0.8), 1500), st * S16 * 0.75, 0.9)
    common_fx(fx, drums); four_floor(drums, kicks)
    for bar in range(4):
        tb = DROP + bar * 2.0; chord, root = CH[bar]
        for half in range(2):
            for st in STAB:
                t = tb + half * 1.0 + st * S16 / 2
                if in_break(t): continue
                for n in chord: put(lead, piano(hz(n), 0.2, 1.0 if st == 0 else 0.85), t, 1.0, pan=0.1)
        for i in range(8):
            t = tb + i * B / 2 + B / 4 * 0
            if i % 2 == 1 and not in_break(t): put(bass, organ_bass(hz(root) * (2 if i % 4 == 3 else 1), B / 2 * 0.85), t)
        put(pad, supersaw_chord(chord, 2.0, cutoff=1800), tb, 0.5)
    for n in ['C4', 'E4', 'G4', 'C5']: put(lead, piano(hz(n), 0.45), END, 1.1)
    put(bass, organ_bass(hz('C2'), 0.5), END)
    return drums, bass, pad, lead, fx, kicks, dict(lg=0.38, bg=1.5, lead=Pedalboard([HighpassFilter(220), Reverb(room_size=0.5, wet_level=0.18, dry_level=0.9)]))

def style_future():
    """Future bass: „gwizdana” melodia (motyw skoków), pulsujące szerokie akordy, trapowe hi-haty, 808."""
    drums, bass, pad, lead, fx = bus(), bus(), bus(), bus(), bus(); kicks = []
    CH = [(['C4', 'E4', 'G4', 'B4', 'D5'], 'C2'), (['B3', 'D4', 'G4', 'A4'], 'G1'), (['C4', 'E4', 'A4', 'B4'], 'A1'), (['C4', 'F4', 'A4', 'E5'], 'F1')]
    MEL = M.HOOK
    put(pad, supersaw_chord(CH[3][0], DROP, cutoff=800), 0, 1.0)
    common_fx(fx, drums)
    for bar in range(4):
        tb = DROP + bar * 2.0; chord, root = CH[bar]
        for beat in range(4):
            t = tb + beat * B
            if in_break(t): continue
            if beat in (0, 2) or (beat == 3 and bar % 2): put(drums, kick(), t); kicks.append(t)
            if beat in (1, 3): put(drums, clap(), t, 0.95)
            trip = beat == 3 and bar % 2 == 0
            for s in range(6 if trip else 4):
                put(drums, hat(), t + s * (B / (6 if trip else 4)), 0.9, pan=-0.2)
        # akordy „pulsujące” w ósemkach (mocny sidechain)
        for i in range(8):
            t = tb + i * B
            if not in_break(t) and t < tb + 2.0: put(pad, supersaw_chord(chord, B * 0.95, cutoff=4200), t, 1.25)
        if not in_break(tb + 0.5): put(bass, sub808(hz(root), 1.9), tb, 1.1)
        prev = None
        for st, n, ln in MEL[bar]:
            t = tb + st * S16
            if in_break(t): continue
            put(lead, whistle(hz(n), ln * S16, prev), t, 1.0); prev = hz(n)
    put(pad, supersaw_chord(['C4', 'E4', 'G4', 'B4', 'D5'], DUR - END, cutoff=3500), END, 1.3)
    put(lead, whistle(hz('C6'), 0.45), END); put(bass, sub808(hz('C2'), 0.5), END); put(drums, kick(1.1), END); kicks.append(END)
    return drums, bass, pad, lead, fx, kicks, dict(sc=0.8, lg=0.75, lead=Pedalboard([HighpassFilter(300), Delay(0.375, 0.3, 0.25), Reverb(room_size=0.7, wet_level=0.25, dry_level=0.85)]))

def style_funk():
    """Funk / nu-disco: klawinet w szesnastkach, skaczący bas, dęciaki na akcentach."""
    drums, bass, pad, lead, fx = bus(), bus(), bus(), bus(), bus(); kicks = []
    CH = [('E', ['E3', 'G3', 'B3', 'D4'], 'E1'), ('A', ['E3', 'G3', 'A3', 'C#4'], 'A1'), ('E', ['E3', 'G3', 'B3', 'D4'], 'E1'), ('B', ['D#3', 'F#3', 'A3', 'B3'], 'B1')]
    RIFF = [(0, 'E4'), (2, 'G4'), (3, 'E4'), (5, 'A4'), (6, 'B4'), (8, 'D5'), (10, 'B4'), (11, 'A4'), (13, 'G4'), (14, 'E4')]
    BASS = [(0, 0), (3, 12), (4, 0), (6, 7), (8, 0), (10, 12), (11, 10), (14, 7)]
    for st, n in RIFF:
        if st * S16 < DROP: put(lead, lp(clav(hz(n), S16 * 0.9), 1300), st * S16 + 0.25, 0.9)
    common_fx(fx, drums)
    for bar in range(4):
        tb = DROP + bar * 2.0; _, chord, root = CH[bar]
        for beat in range(4):
            t = tb + beat * B
            if in_break(t): continue
            if beat in (0, 2) or beat == 3: put(drums, kick(0.95), t if beat != 3 else t + S16 * 2); kicks.append(t)
            if beat in (1, 3): put(drums, clap(), t, 0.9)
            for s in range(4): put(drums, hat(s == 2), t + s * S16, 0.75 if s % 2 else 0.95, pan=-0.25)
        for st, n in RIFF:
            t = tb + st * S16
            if in_break(t): continue
            f = hz(n) * (2 ** (5 / 12) if bar == 1 else 2 ** (7 / 12) if bar == 3 else 1)
            put(lead, clav(f, S16 * 0.8), t, 1.0, pan=-0.15)
        for st, iv in BASS:
            t = tb + st * S16
            if in_break(t): continue
            put(bass, bass_note(hz(root) * 2 ** (iv / 12) * 2, S16 * 1.6), t, 1.1)
        if not in_break(tb): put(pad, brass(chord, 0.25), tb, 1.0)
        if not in_break(tb + 1.75): put(pad, brass(chord, 0.15), tb + 1.75, 0.8)
    for t in (LAND, POP): put(pad, brass(['E4', 'G#4', 'B4', 'D5'], 0.35), t, 1.1)
    put(pad, brass(['E3', 'G#3', 'B3', 'D4', 'F#4'], 0.45), END, 1.3); put(bass, bass_note(hz('E2'), 0.5), END)
    put(drums, kick(1.1), END); kicks.append(END)
    return drums, bass, pad, lead, fx, kicks, dict(sc=0.35, lg=0.85, lead=Pedalboard([HighpassFilter(200), Phaser(rate_hz=0.8, mix=0.25), Reverb(room_size=0.3, wet_level=0.12, dry_level=0.95)]))

def style_tropical():
    """Tropical house: marimba z synkopowanym motywem, shaker, miękka stopa, ciepłe akordy."""
    drums, bass, pad, lead, fx = bus(), bus(), bus(), bus(), bus(); kicks = []
    CH = [(['C4', 'E4', 'G4'], 'C2'), (['A3', 'C4', 'E4'], 'A1'), (['F3', 'A3', 'C4'], 'F1'), (['G3', 'B3', 'D4'], 'G1')]
    MAR = [  # skoki o oktawę w każdym takcie
        [(0, 'G5'), (2, 'E5'), (3, 'G5'), (6, 'C6'), (8, 'G5'), (10, 'E5'), (11, 'D5'), (14, 'E5')],
        [(0, 'E5'), (2, 'C5'), (3, 'E5'), (6, 'A5'), (8, 'E5'), (10, 'C5'), (11, 'B4'), (14, 'C5')],
        [(0, 'F5'), (2, 'C5'), (3, 'F5'), (6, 'A5'), (8, 'C6'), (10, 'A5'), (11, 'G5'), (14, 'F5')],
        [(0, 'G5'), (2, 'D5'), (3, 'G5'), (6, 'B5'), (8, 'D6'), (10, 'B5'), (12, 'A5'), (14, 'G5')]]
    for st, n in MAR[3]:
        if st * S16 < DROP: put(lead, lp(marimba(hz(n), 0.2), 1800), st * S16, 0.85)
    put(pad, supersaw_chord(CH[3][0], DROP, cutoff=900), 0, 0.8)
    common_fx(fx, drums)
    for bar in range(4):
        tb = DROP + bar * 2.0; chord, root = CH[bar]
        for beat in range(4):
            t = tb + beat * B
            if in_break(t): continue
            put(drums, kick(0.85), t); kicks.append(t)
            if beat in (1, 3): put(drums, rim(), t + S16 * (1 if beat == 3 else 0), 0.9); put(drums, clap(), t, 0.45)
            for s in range(4): put(drums, shaker(1.0 if s % 2 else 0.6), t + s * S16 + (0.012 if s % 2 else 0), 1.0, pan=0.3)
        for st, n in MAR[bar]:
            t = tb + st * S16
            if not in_break(t): put(lead, marimba(hz(n), 0.2), t, 1.0, pan=0.1)
            t2 = t + 1.0
            if not in_break(t2) and st < 16: put(lead, marimba(hz(n), 0.2), t2, 0.9, pan=-0.1)
        for i, st in enumerate((0, 3, 6, 8, 11, 14)):
            t = tb + st * S16
            if not in_break(t): put(bass, bass_note(hz(root) * (2 if i in (2, 5) else 1), S16 * 2), t, 1.0)
        put(pad, supersaw_chord(chord, 2.0, cutoff=1600), tb, 0.8)
    put(pad, supersaw_chord(['C4', 'E4', 'G4', 'C5'], DUR - END, cutoff=2000), END, 1.1)
    for n in ('C5', 'G5', 'C6'): put(lead, marimba(hz(n), 0.4), END)
    put(bass, bass_note(hz('C2'), 0.5), END); put(drums, kick(1.0), END); kicks.append(END)
    return drums, bass, pad, lead, fx, kicks, dict(sc=0.45, lg=0.42, bg=1.3, lead=Pedalboard([HighpassFilter(200), Delay(0.375, 0.25, 0.2), Reverb(room_size=0.55, wet_level=0.2, dry_level=0.9)]))

def chord_keys(notes, dur, bright=1.0):
    """ciepłe, wybrzmiewające akordy (jak w pierwszym podkładzie, ale z filtrem, detune i stereo)."""
    L = int((dur + 0.4) * SR); x = np.arange(L) / SR; l = np.zeros(L); r = np.zeros(L)
    for n in notes:
        f = hz(n)
        for k, d in enumerate((-0.07, 0, 0.07)):
            sg = polyblep_saw(f * 2 ** (d / 12), L, rng.random()) * 0.6 + np.sin(2 * np.pi * f * x) * 0.8
            (l if k != 2 else r)[:] += sg; (r if k != 0 else l)[:] += sg * 0.6
    fc = 600 + 3800 * bright * np.exp(-x * 2.2)
    for ch in (l, r):
        o = np.zeros(L)
        for i in range(0, L, 512): o[i:i + 512] = lp(ch[i:i + 512], float(fc[i]), 1)
        ch[:] = o
    e = np.exp(-x * 0.9) * np.minimum(1, x * 300); e[int(dur * SR):] *= np.exp(-(x[int(dur * SR):] - dur) * 12)
    return np.stack([l, r]) * e * 0.05

def style_oryginal():
    """Wierny „remaster” pierwszego podkładu: A–F–C–G (dur), stopa na każdą ćwierćnutę, klaśnięcie na 2 i 4,
    hi-hat na „i”, wybrzmiewające akordy i bas z korzeniem – tylko lepsze brzmienia, sidechain, pogłos i mastering."""
    drums, bass, pad, lead, fx = bus(), bus(), bus(), bus(), bus(); kicks = []
    CH = [(['A3', 'C#4', 'E4'], 'A1'), (['F3', 'A3', 'C4'], 'F1'), (['C4', 'E4', 'G4'], 'C2'), (['G3', 'B3', 'D4'], 'G1')]
    put(fx, riser(1.45, 300, 10000), 0.05, 0.8)
    put(pad, chord_keys(['A3', 'C#4', 'E4'], 1.4, 0.4), 0.0, 0.7); put(bass, bass_note(hz('A1'), 1.4), 0.0, 0.6)
    for k in range(8): put(drums, snare16(), DROP - 1.0 + k * S16, 0.12 + 0.4 * k / 7, pan=0.1)
    put(fx, boing(), DROP - 0.02, 0.6, pan=0.15)
    for bar in range(4):
        tb = DROP + bar * 2.0; chord, root = CH[bar]
        for beat in range(4):
            t = tb + beat * B
            if in_break(t):
                if beat == 0: put(drums, kick(0.8), t); kicks.append(t)
                continue
            put(drums, kick(1.05), t); kicks.append(t)
            if beat in (1, 3): put(drums, clap(), t, 0.95)
            put(drums, hat(True), t + B / 2, 1.2, pan=0.2)
            if bar == 3: put(drums, hat(), t + B / 4, 0.8, pan=-0.25); put(drums, hat(), t + 3 * B / 4, 0.8, pan=-0.25)
        put(pad, chord_keys(chord, 2.0), tb, 1.0)
        for i in range(4):
            t = tb + i * B
            if not in_break(t): put(bass, bass_note(hz(root) * 2, B * 0.95), t, 1.0)
        put(bass, bass_note(hz(root), 2.0), tb, 0.55)
    put(fx, riser(0.5, 800, 12000), 6.0, 0.7)
    put(fx, boing(392, 1176, 0.3), POP - 0.02, 0.6, pan=-0.15)
    for t in (DROP, LAND, POP):
        put(fx, crash(), t, 0.9); put(drums, boom(), t, 0.3)
    put(drums, kick(1.1), END); put(drums, clap(), END, 0.7); put(fx, crash(), END, 0.9); kicks.append(END)
    put(pad, chord_keys(['A3', 'C#4', 'E4', 'A4', 'E5'], DUR - END, 0.8), END, 1.3); put(bass, bass_note(hz('A1'), DUR - END), END, 1.0)
    return drums, bass, pad, lead, fx, kicks, dict(sc=0.5, bg=1.1)

STYLES = dict(house=style_house, future=style_future, funk=style_funk, tropical=style_tropical, oryginal=style_oryginal)

def mixdown(parts):
    drums, bass, pad, lead, fx, kicks, opt = parts
    sc = sidechain(kicks, depth=opt.get('sc', 0.55))
    drums = fxchain(drums, Pedalboard([Compressor(threshold_db=-14, ratio=3, attack_ms=8, release_ms=90), Gain(2)]))
    bass = fxchain(bass * sc, Pedalboard([HighpassFilter(32), Compressor(threshold_db=-16, ratio=3), Distortion(drive_db=3), Gain(-2)]))
    pad = fxchain(pad * sc, Pedalboard([HighpassFilter(170), Chorus(rate_hz=0.6, depth=0.25, mix=0.3), Reverb(room_size=0.6, wet_level=0.2, dry_level=0.85, width=1.0)]))
    lead = fxchain(lead, opt.get('lead', Pedalboard([HighpassFilter(200), Reverb(room_size=0.4, wet_level=0.15, dry_level=0.9)])))
    fx = fxchain(fx, Pedalboard([Reverb(room_size=0.7, wet_level=0.25, dry_level=0.8)]))
    mix = (drums * 0.9 + bass * 1.2 * opt.get('bg', 1) + pad * 0.9 + lead * 0.95 * opt.get('lg', 1) + fx * 0.6) * 0.42
    mix = fxchain(mix, Pedalboard([HighpassFilter(30), HighShelfFilter(cutoff_frequency_hz=7000, gain_db=-4), LowpassFilter(15500),
                                   Compressor(threshold_db=-10, ratio=2.2, attack_ms=15, release_ms=120), Limiter(threshold_db=-3, release_ms=80), Gain(-1.5)]))
    fl = int(0.35 * SR); mix[:, -fl:] *= np.linspace(1, 0, fl)
    return mix

if __name__ == '__main__':
    style, out = sys.argv[1], sys.argv[2]
    mix = mixdown(STYLES[style]())
    pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2')
    w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
    print(out)
