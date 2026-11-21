// Montaroo · „Historia” – scena na stronę i do spotu. Cała animacja to funkcja czasu render(t):
// 0–2 intro (torba + logo) · 2–6 telefony przez QR do torby · 6–10 ściana, kangurek wybiera ★ · 10–11,6 muzyka
// · 11,6–14 montaż (podgląd = prawdziwy film) · 14,03 podgląd rośnie w film. Cięcia na bitach „bouncy brass a” (118,8 BPM).
(() => {
const $ = s => document.querySelector(s);
const stage = $('#stage'), fx = $('#fx'), vid = $('#vid'), aud = $('#aud'), pl = vid.parentElement;
const snd = $('#snd'), again = $('#again'), rozd = $('#rozd');
const Q = new URLSearchParams(location.search), CAP = Q.has('cap');
const T_FILM = 14.025, V_OFF = 11.494;                 // film: czas filmu = t − V_OFF (pierwsze cięcie filmu 2,531 s = T_FILM)
const BEATS = [0.534, 1.022, 1.533, 2.02, 2.508, 3.019, 3.529, 4.017, 4.505, 5.016, 5.526, 6.014, 6.502, 7.012, 7.523, 8.011, 8.522, 9.033, 9.52, 10.008, 10.519, 11.029, 11.517, 12.005, 12.516, 13.026, 13.514, 14.025];
const CUTS = [0, 2.5, 4.5, 5.5, 6.5, 7.5, 8.5, 10.5, 11.5, 12.467, 13.467, 14.467, 17.5];     // ujęcia filmu (s)
const USZY = 'M46.94 11.93A5.2 11 -14 1 1 52.26 33.27A5.2 11 -14 1 1 46.94 11.93ZM67.47 15.95A5.2 11 24 1 1 58.53 36.05A5.2 11 24 1 1 67.47 15.95Z';
const CIALO = 'M44 36.26A6 6 0 0 1 52.94 31.03L82.7 47.77A6 6 0 0 1 82.7 58.23L52.94 74.97A6 6 0 0 1 44 69.74Z';
const MARK = `<svg viewBox="0 0 128 128" class="mark"><g fill="#F4E9D6"><path d="${USZY}"/><path d="${CIALO}"/></g><path fill="#E2642A" d="M16 67A3 3 0 0 1 19 64H109A3 3 0 0 1 112 67V72A48 48 0 0 1 16 72Z"/><path d="M27 75H101" stroke="#10251F" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="5.2 6.2"/></svg>`;

// ---------- narzędzia ----------
const cl = (x, a = 0, b = 1) => x < a ? a : x > b ? b : x, seg = (t, a, b) => cl((t - a) / (b - a)), lerp = (a, b, p) => a + (b - a) * p;
const eo = p => 1 - Math.pow(1 - p, 3), ei = p => p * p * p, eio = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
const back = p => { const c = 1.9; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2) };
const dec = (t, a, d = .18) => t < a ? 0 : Math.exp(-(t - a) / d);           // impuls po zdarzeniu
const hopY = (t, a, d, h) => t < a || t > a + d ? 0 : -Math.sin(Math.PI * (t - a) / d) * h;
const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let x = Math.imul(s ^ s >>> 15, 1 | s); x = x + Math.imul(x ^ x >>> 7, 61 | x) ^ x; return ((x ^ x >>> 14) >>> 0) / 4294967296 };
const el = (cls, html = '', par = fx) => { const d = document.createElement('div'); d.className = cls; if (html) d.innerHTML = html; par.appendChild(d); return d };
const tr = (e, x, y, s = 1, r = 0, sx) => { e.style.transform = `translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0)${r ? ` rotate(${r.toFixed(2)}deg)` : ''}${sx !== undefined ? ` scale(${sx.toFixed(4)},${s.toFixed(4)})` : s !== 1 ? ` scale(${s.toFixed(4)})` : ''}` };
const op = (e, o) => { const v = o <= 0.001 ? 0 : o >= .999 ? 1 : +o.toFixed(3); if (e._o !== v) { e._o = v; e.style.opacity = v; e.style.visibility = v ? '' : 'hidden' } };
const kl = (e, c, on) => { if (e['_' + c] !== on) { e['_' + c] = on; e.classList.toggle(c, on) } };
const hex = (a, b, p) => { const A = parseInt(a.slice(1), 16), B = parseInt(b.slice(1), 16); const m = s => Math.round(lerp(A >> s & 255, B >> s & 255, p)); return `rgb(${m(16)},${m(8)},${m(0)})` };
const arc = (x0, y0, x1, y1, h, e) => [lerp(x0, x1, e), (1 - e) * (1 - e) * y0 + 2 * (1 - e) * e * (Math.min(y0, y1) - h) + e * e * y1];

// QR (wzór jak kod – w makiecie bez prawdziwego adresu)
function qrPath(x0, y0, s) {
  const N = 21, r = rng(7), m = (i, j) => { const f = (a, b) => i >= a && i < a + 7 && j >= b && j < b + 7;
    for (const [a, b] of [[0, 0], [14, 0], [0, 14]]) if (f(a, b)) { const u = i - a, v = j - b; return u == 0 || u == 6 || v == 0 || v == 6 || (u > 1 && u < 5 && v > 1 && v < 5) }
    if ((i < 8 && j < 8) || (i > 12 && j < 8) || (i < 8 && j > 12)) return false; return r() < .5 };
  let d = ''; for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if (m(i, j)) d += `M${(x0 + j * s).toFixed(2)} ${(y0 + i * s).toFixed(2)}h${s}v${s}h-${s}z`; return d;
}

let K = null, L = null, E = null;      // atlas kafli, układ, elementy

// ---------- układ (zależy od kształtu sceny) ----------
function uklad() {
  const r = stage.getBoundingClientRect(), W = r.width, H = r.height, tall = W / H < 1.25, u = Math.min(W, H) / 100;
  stage.style.setProperty('--u', u + 'px');
  const hh = Math.max(u * 9, 30);
  const o = { W, H, tall, u, hh };
  // torba: start (intro), telefony, róg
  o.bw = tall ? W * .8 : W * .4;
  o.bag = {
    intro: { cx: W / 2, rim: H * (tall ? .43 : .42), w: Math.min(W, H) * .26 },
    tel: { cx: W / 2, rim: H * (tall ? (H / W > 1.5 ? .74 : .71) : .6), w: o.bw },
    rog: { cx: W - (tall ? W * .17 : W * .085), rim: 0, w: tall ? W * .3 : W * .14 },
  };
  o.bag.rog.rim = H - o.bag.rog.w * .36 - u * 1.5;
  // telefony
  if (tall) {
    const ph = Math.min(H * .33, W * .27 * 2.05), pw = ph * .49, py = hh + u * 2 + ph / 2;
    o.ph = [{ cx: W * .19, cy: py + u * 2, s: 1, side: -1 }, { cx: W * .5, cy: py, s: 1, side: 0 }, { cx: W * .81, cy: py + u * 2, s: 1, side: 1 }].map(p => ({ ...p, w: pw, h: ph }));
    const jTop = o.bag.tel.rim - o.bw * .17;
    o.sd = { x: W / 2, y: (py + ph / 2 + jTop) / 2 - u * 3, mid: true };
  } else {
    const ph = H * .5, pw = ph * .49;
    o.ph = [{ cx: W * .115, cy: H * .57, s: 1, side: -1 }, { cx: W * .27, cy: H * .43, s: .84, side: -1 }, { cx: W * .885, cy: H * .57, s: 1, side: 1 }].map(p => ({ ...p, w: pw, h: ph }));
    o.sd = { x: W * .735, y: hh + u * 4, mid: false };
  }
  // ściana
  const wTop = hh + u * 2, wBot = H - u * 2, tw = tall ? W * .3 : W * .155, th = tw * 9 / 16, gap = u * 1.1;
  const R = Math.max(3, Math.floor((wBot - wTop + gap) / (th + gap))), C = Math.ceil(W * (tall ? 2.4 : 1.95) / (tw + gap));
  o.wall = { top: wTop + ((wBot - wTop) - (R * (th + gap) - gap)) / 2, tw, th, gap, R, C, Ww: C * (tw + gap) - gap };
  // muzyka
  const cols = tall ? 2 : 4, rows = tall ? 3 : 2, mx = W * (tall ? .07 : .075), cg = u * 1.8;
  const cw = (W - 2 * mx - (cols - 1) * cg) / cols, ch = cw * (tall ? .6 : .5), mtop = hh + u * (tall ? 6 : 7);
  o.song = { cols, rows, cw, ch, mx, cg, mtop, gold: tall ? 3 : 5, A: tall ? 0 : 2 };
  // montaż
  const k = tall ? (H / W > 1.5 ? .44 : .4) : .43;
  o.pv = { w: W * k, h: H * k, x: (W - W * k) / 2, y: hh + u * 1.2, k, r: u * 1.4 };
  const ty = o.pv.y + o.pv.h + u * 2.2;
  o.tl = { x: W * .035, y: ty, w: W * .93, h: H - ty - u * 2.2 };
  const lw = tall ? W * .16 : W * .085, ax = o.tl.x + lw, aw = o.tl.x + o.tl.w - ax - u * 1.6, ry = o.tl.y + u * 1.1;
  const t0 = ry + u * 3.6, avail = o.tl.y + o.tl.h - u * 1.4 - t0, g2 = u * .8;
  const hs = [.33, .19, .17, .31].map(f => f * (avail - 3 * g2)); let yy = t0; const tracks = hs.map(h => { const r = { y: yy, h }; yy += h + g2; return r });
  o.ed = { lw, ax, aw, ry, tracks, WIN: tall ? 7 : 9.5 };
  return o;
}

// ---------- budowa elementów ----------
function buduj() {
  fx.innerHTML = ''; L = uklad(); const { W, H, u, tall } = L; E = {};
  const R = rng(11);
  E.glow = el('h-glow');
  E.vig = el('h-vig');
  // ŚCIANA
  const w = L.wall; E.wall = el('h-wall'); E.tiles = [];
  const rows = Math.ceil(K.n / K.cols), bs = `${K.cols * w.tw}px ${rows * w.th}px`;
  const kol = [...Array(K.n).keys()].sort(() => R() - .5);
  for (let c = 0; c < w.C; c++) for (let r = 0; r < w.R; r++) {
    const k = K.k[kol[(c * w.R + r) % K.n]], t = el('h-wt', '<i></i>', E.wall);
    const x = c * (w.tw + w.gap), y = r * (w.th + w.gap);
    Object.assign(t.style, { left: x + 'px', top: y + 'px', width: w.tw + 'px', height: w.th + 'px', backgroundSize: bs, backgroundPosition: `${-(k.i % K.cols) * w.tw}px ${-Math.floor(k.i / K.cols) * w.th}px` });
    E.tiles.push({ e: t, c, r, x, y, k: k.i });
  }
  E.scan = el('h-scan', '', E.wall); E.scan.style.display = 'none';   // w aplikacji skaner jest niewidoczny – kafle tylko „wywołują się”
  // wybory kangurka na ścianie – na bitach
  E.LT = [6.502, 7.012, 7.523, 8.011, 8.522, 9.033, 9.52];
  const rowsSeq = [1, 2, 0, 2, 1, 3, 0, 1, 2].map(x => x % w.R);
  E.picks = E.LT.map((lt, i) => {
    const sx = scanX(lt), c = cl(Math.floor((sx - w.tw * 1.25) / (w.tw + w.gap)), 0, w.C - 1);
    return E.tiles.find(t => t.c === c && t.r === rowsSeq[i]);
  });
  E.stars = E.LT.map(() => el('h-star', '★'));
  E.wfly = E.picks.map(p => { const f = el('h-fly z'); Object.assign(f.style, { width: w.tw + 'px', height: w.th + 'px', backgroundSize: bs, backgroundPosition: p.e.style.backgroundPosition }); return f });
  // TELEFONY
  E.lines = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); E.lines.setAttribute('class', 'h-lines'); fx.appendChild(E.lines);
  const KOL = ['#F2B544', '#8FC3AE', '#E2642A'], KTO = ['Ty', 'Anna', 'Tata'], TIN = [2.508, 3.019, 3.529];
  const fw = tall ? W * .13 : W * .058, fh = fw * 9 / 16;
  E.flights = [];
  E.ph = L.ph.map((p, i) => {
    const e = el('h-ph', `<div class="who"><i></i>${KTO[i]}<span>0%</span></div><div class="gr"></div><div class="bar"><b></b></div>`);
    Object.assign(e.style, { width: p.w + 'px', height: p.h + 'px', '--k': KOL[i] }); e.style.setProperty('--k', KOL[i]);
    const gr = e.querySelector('.gr'), cells = [];
    const cw = (p.w - u * 2.2 - u * .9) / 3, chh = cw * 1.0;
    for (let j = 0; j < 15; j++) { const c = document.createElement('i'), k = K.k[(i * 37 + j * 7) % K.n].i;
      c.style.backgroundSize = `${K.cols * cw}px ${rows * chh}px`; c.style.backgroundPosition = `${-(k % K.cols) * cw}px ${-Math.floor(k / K.cols) * chh}px`; gr.appendChild(c); cells.push({ c, k }) }
    const ln = document.createElementNS('http://www.w3.org/2000/svg', 'path'); E.lines.appendChild(ln);
    ln.setAttribute('stroke-width', (u * .42).toFixed(2)); ln.setAttribute('stroke-dasharray', `${(u * .35).toFixed(1)} ${(u * 1.7).toFixed(1)}`);
    const tin = TIN[i], n = Math.floor((5.15 - (tin + .35)) / .21);
    for (let j = 0; j < n; j++) { const cell = cells[j % 15], f = el('h-fly');
      Object.assign(f.style, { width: fw + 'px', height: fh + 'px', backgroundSize: `${K.cols * fw}px ${rows * fh}px`, backgroundPosition: `${-(cell.k % K.cols) * fw}px ${-Math.floor(cell.k / K.cols) * fh}px` });
      E.flights.push({ f, i, j, cell, t0: tin + .35 + j * .21 + R() * .05, d: .58 + R() * .1, jx: R() * 2 - 1, jy: R() * 2 - 1, r0: R() * 30 - 15, r1: R() * 10 - 5 }) }
    return { e, p, cells, ln, tin, kol: KOL[i], pc: e.querySelector('.who span'), bar: e.querySelector('.bar b') };
  });
  E.sd = el('h-sd', `<span class="h-card"></span><span><b>Wykryto kartę drona DJI</b><small>212 nagrań · dodaję…</small></span>`);
  E.sdS = E.sd.querySelector('small'); E.sdFly = el('h-sdfly', '<span class="h-card"></span>');
  // TORBA (kształty z aplikacji) + telefon z kodem QR w łapkach
  E.bag = el('h-bag', `<svg viewBox="0 0 600 330" aria-hidden="true"><defs>
    <linearGradient id="hg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9733C"/><stop offset="1" stop-color="#C7521F"/></linearGradient>
    <radialGradient id="hc" cx=".5" cy="0" r="1"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#5a1e05" stop-opacity=".35"/></radialGradient>
    <clipPath id="hk"><rect x="-200" y="-600" width="1000" height="726"/></clipPath></defs>
    <ellipse class="t-ust" cx="300" cy="108" rx="256" ry="17"/>
    <g clip-path="url(#hk)"><g transform="translate(300 126) scale(1.95) translate(-63.5 -75)"><g class="t-j"><g class="t-joey"><g class="t-uszy"><path d="${USZY}"/></g><path d="${CIALO}"/></g>
      <g class="t-tel"><rect x="71" y="22" width="32" height="54" rx="6" fill="#F4E9D6" stroke="#10251F" stroke-width="1.6"/><rect x="74" y="27" width="26" height="40" rx="2.5" fill="#fff"/>
      <path d="${qrPath(75.2, 34.6, 1.14)}" fill="#10251F"/><ellipse cx="72" cy="60" rx="5" ry="4" fill="#F4E9D6"/></g></g></g></g>
    <g class="t-przod"><path d="M24 118H576V128A276 190 0 0 1 24 128Z" fill="url(#hg)"/><path d="M24 128H576A276 190 0 0 1 24 128Z" fill="url(#hc)"/>
      <rect class="t-brzeg" x="20" y="106" width="560" height="22" rx="11"/><path class="t-szew" d="M70 150H530"/></g></svg>
    <div class="h-nap"><small>IN THE BAG</small><b>0</b></div>`);
  E.bag.style.width = L.bw + 'px'; E.bag.style.setProperty('--bw', L.bw + 'px');
  E.bj = E.bag.querySelector('.t-j'); E.bu = E.bag.querySelector('.t-uszy'); E.bp = E.bag.querySelector('.t-przod'); E.bm = E.bag.querySelector('.t-ust');
  E.btel = E.bag.querySelector('.t-tel'); E.bnap = E.bag.querySelector('.h-nap'); E.bnum = E.bnap.querySelector('b');
  E.badge = el('h-badge', '★ 0');
  E.bub = el('h-bub', `Masz nagrania w telefonie?<small>Zeskanuj kod w moich łapkach.</small>`);
  E.tap = el('h-bub h-tap', `Dotknij mnie 🎵<small>Obejrzyj z muzyką</small>`);
  // INTRO: napis + hasło
  E.word = el('h-word', [...'montaroo'].map(c => `<i>${c}</i>`).join('')); E.letters = [...E.word.children];
  E.tag = el('h-tag', 'Od nagrań do filmu jednym skokiem.');
  // PASEK
  E.bar = el('h-bar', `${MARK}<div class="h-mid"><svg class="h-ring" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15" stroke="#f4e9d61f"/><circle class="pr" cx="18" cy="18" r="15" stroke="#F2B544" stroke-dasharray="0 100" pathLength="100" transform="rotate(-90 18 18)" stroke-linecap="round"/></svg><span class="h-et"><span class="tx"></span><em></em><span class="soon">Wkrótce</span></span></div>`);
  E.bar.style.height = L.hh + 'px'; E.bar.classList.toggle('wys', tall); E.barMark = E.bar.querySelector('.mark'); E.ring = E.bar.querySelector('.pr'); E.et = E.bar.querySelector('.h-et'); E.etx = E.et.querySelector('.tx'); E.etp = E.et.querySelector('em'); E.soon = E.et.querySelector('.soon');
  // MUZYKA
  const S = L.song, TYT = [['Sunday Drive', 'Spokojny'], ['Golden Hour', 'Filmowy'], ['Night Owl', 'Pogodny'], ['Desert Wind', 'Filmowy'], ['Highway Lights', 'Energiczny'], ['Canyon Echo', 'Epicki'], ['Big Sky', 'Radosny']];
  const fala = (n, s) => [...Array(n)].map((_, i) => .22 + .78 * Math.abs(Math.sin(i * .61 + s) * Math.cos(i * .23 + s * 2) + (i % 6 === 0 ? .28 : 0)));
  E.songs = []; let ti = 0;
  for (let i = 0; i < S.cols * S.rows; i++) {
    const gold = i === S.gold, [nm, md] = gold ? ['Bouncy Brass', 'Pogodny · 119 BPM'] : TYT[ti++ % TYT.length];
    const hs = fala(28, i * 1.7 + 1);
    const e = el('h-song', `<b>♪ ${nm}</b><small>${md}</small><div class="wv">${hs.map(h => `<i style="height:${(h * 100).toFixed(0)}%"></i>`).join('')}</div><span class="pl">♪</span>`);
    const c = i % S.cols, r = Math.floor(i / S.cols), x = S.mx + c * (S.cw + S.cg), y = S.mtop + r * (S.ch + S.cg);
    Object.assign(e.style, { width: S.cw + 'px', height: S.ch + 'px' });
    E.songs.push({ e, x, y, gold, bars: [...e.querySelectorAll('.wv i')], pl: e.querySelector('.pl') });
  }
  // MONTAŻ
  const D = L.ed, P = L.pv; E.ed = el('h-ed');
  E.pv = el('h-pv', '', E.ed); Object.assign(E.pv.style, { left: P.x + 'px', top: P.y + 'px', width: P.w + 'px', height: P.h + 'px', borderRadius: P.r + 'px' });
  E.tl = el('h-tl', '', E.ed); Object.assign(E.tl.style, { left: L.tl.x + 'px', top: L.tl.y + 'px', width: L.tl.w + 'px', height: L.tl.h + 'px' });
  const X = s => D.ax + s / D.WIN * D.aw;
  ['Wideo', 'Tekst', 'Dźwięk', 'Muzyka'].forEach((n, i) => { const tk = D.tracks[i], l = el('h-lab', n, E.ed); Object.assign(l.style, { left: (L.tl.x + u * 1.6) + 'px', top: tk.y + 'px', height: tk.h + 'px' }) });
  const rul = el('h-rul', '', E.ed); Object.assign(rul.style, { left: 0, top: D.ry + 'px', width: W + 'px', height: u * 2.4 + 'px' });
  for (let s = 0; s <= D.WIN; s += (tall ? 2 : 1)) { const sp = document.createElement('span'); sp.style.left = X(s) + 'px'; sp.textContent = `0:${String(s).padStart(2, '0')}`; rul.appendChild(sp) }
  E.beats = CUTS.slice(1).filter(c => c < D.WIN).map(c => { const b = el('h-beat', '', E.ed); Object.assign(b.style, { left: X(c) + 'px', top: D.tracks[0].y + 'px', height: (D.tracks[3].y + D.tracks[3].h - D.tracks[0].y) + 'px' }); return b });
  const v = D.tracks[0], kw = v.h * 16 / 9;
  E.clips = []; for (let i = 0; i < CUTS.length - 1 && CUTS[i] < D.WIN; i++) {
    const x0 = X(CUTS[i]) + 1, x1 = Math.min(X(CUTS[i + 1]), D.ax + D.aw) - 1, c = el('h-clip', '', E.ed);
    Object.assign(c.style, { left: x0 + 'px', top: v.y + 'px', width: (x1 - x0) + 'px', height: v.h + 'px', backgroundSize: `${12 * kw}px ${v.h}px`, backgroundPosition: `${-i * kw}px 0`, backgroundRepeat: 'no-repeat' });
    // klisza: ta sama klatka powtórzona
    const reps = Math.ceil((x1 - x0) / kw); let bg = [], pos = [];
    for (let j = 0; j < reps; j++) { bg.push(('url(' + HB + 'klatki.jpg)')); pos.push(`${j * kw - i * kw}px 0`) }
    c.style.backgroundImage = bg.join(','); c.style.backgroundPosition = pos.join(','); c.style.backgroundSize = bg.map(() => `${12 * kw}px ${v.h}px`).join(',');
    // każda warstwa przycięta do jednej klatki – przez clip na szerokość klatki nie da się, więc dzielimy na kafelki
    c.style.backgroundImage = 'none'; c.style.overflow = 'hidden'; c.style.display = 'flex';
    for (let j = 0; j < reps; j++) { const s = document.createElement('i'); Object.assign(s.style, { flex: 'none', width: kw + 'px', height: '100%', backgroundImage: ('url(' + HB + 'klatki.jpg)'), backgroundSize: `${12 * kw}px ${v.h}px`, backgroundPosition: `${-i * kw}px 0`, boxShadow: '1px 0 0 #0006' }); c.appendChild(s) }
    E.clips.push({ e: c, i, x0, x1 });
  }
  const tk = D.tracks[1];
  E.chips = [[0.1, 2.35, 'USA 2026', 't'], [2.55, 4.42, 'DZIEŃ 3 · W drodze', ''], [6.55, 8.42, 'DZIEŃ 4 · Grand Canyon', '']].filter(c => c[0] < D.WIN).map(([a, b, n, k], i) => {
    const c = el('h-chip ' + k, n, E.ed); Object.assign(c.style, { left: X(a) + 'px', top: (tk.y + tk.h * .12) + 'px', width: (Math.min(X(b), D.ax + D.aw) - X(a)) + 'px', height: tk.h * .76 + 'px' }); return c });
  const sk = D.tracks[2];
  E.snds = [[4.6, 5.4], [7.6, 8.4]].map(([a, b]) => { const s = el('h-snd', '', E.ed); Object.assign(s.style, { left: X(a) + 'px', top: (sk.y + sk.h * .15) + 'px', width: (X(b) - X(a)) + 'px', height: sk.h * .7 + 'px' }); return s });
  const mk = D.tracks[3];
  E.wave = el('h-wave', fala(tall ? 60 : 110, 3.3).map(h => `<i style="height:${(h * 100).toFixed(0)}%"></i>`).join(''));
  E.waveTo = { x: D.ax, y: mk.y, w: D.aw, h: mk.h };
  E.plaq = el('h-plaq', '♪ Bouncy Brass', E.ed); Object.assign(E.plaq.style, { left: (D.ax + u) + 'px', top: (mk.y + mk.h / 2) + 'px', transform: 'translateY(-50%)' });
  E.ph2 = el('h-ph2', '', E.ed); Object.assign(E.ph2.style, { top: (D.ry + u * 2.6) + 'px', height: (mk.y + mk.h - D.ry - u * 2.6) + 'px' });
  E.X = X;
  E.tb = el('h-tb', ['− Krócej', '+ Dłużej', '♪ Dźwięk', 'T Tekst', '⇄ Zamień'].map(n => `<i>${n}</i>`).join(''), E.ed); E.tbi = [...E.tb.children];
  E.cur = el('h-cur', `<svg viewBox="0 0 24 28" width="100%"><path d="M2 1.5v21l5.6-5.2 3.6 8.2 3.4-1.5-3.6-8h7.6z" fill="#fff" stroke="#10251F" stroke-width="1.6" stroke-linejoin="round"/></svg>`);
  // KANGUREK (jeden przez całą historię)
  E.joey = el('h-joey', `<svg viewBox="40 8 46 70"><g fill="#F4E9D6"><g class="ju"><path d="${USZY}"/></g><path d="${CIALO}"/></g></svg>`);
  E.ju = E.joey.querySelector('.ju');
  E.flash = el('h-flash');
  E.trasa = joeyTrasa();
  // pierwsza klatka telefonów/kafli musi znać rozmiar siatki
  ostatnie = -1;
}

// ---------- ruch w czasie ----------
function scanX(t) { const w = L.wall; return lerp(w.tw * 1.6, w.Ww + w.tw * .2, eio(seg(t, 5.95, 9.85)) * .15 + seg(t, 5.95, 9.85) * .85) }
function camX(t) { const w = L.wall; return cl(L.W * .6 - scanX(t), L.W - w.Ww - L.u * 2, L.u * 2) }
function wallXY(t) {           // przesunięcie ściany (wjazd, jazda kamery, wyjazd w górę)
  const inn = eo(seg(t, 5.9, 6.5)), out = ei(seg(t, 9.75, 10.2));
  return { x: camX(t), y: L.wall.top + (1 - inn) * L.u * 10 - out * L.u * 14, s: 1 - out * .05, o: inn * (1 - out) };
}
function tilePos(tile, t) { const w = wallXY(t); return { x: w.x + tile.x, y: w.y + tile.y, w: L.wall.tw, h: L.wall.th } }
function bagState(t) {        // {cx, rim, w} torby w czasie
  const B = L.bag, mix = (a, b, p) => ({ cx: lerp(a.cx, b.cx, p), rim: lerp(a.rim, b.rim, p), w: lerp(a.w, b.w, p) });
  if (t < 2.02) return B.intro;
  if (t < 2.55) return mix(B.intro, B.tel, eio(seg(t, 2.02, 2.55)));
  if (t < 5.92) return B.tel;
  if (t < 6.45) return mix(B.tel, B.rog, eio(seg(t, 5.92, 6.45)));
  return B.rog;
}
const mouth = t => { const b = bagState(t); return { x: b.cx, y: b.rim + b.w * .03 } };
function songPos(i) { const s = E.songs[i]; return { x: s.x, y: s.y, w: L.song.cw, h: L.song.ch } }
function playX(t) { return E.X(Math.max(0, t - V_OFF)) }

// trasa kangurka: odcinki [t0, t1, skąd(t), dokąd(t), rozmiar0, rozmiar1]
function joeyTrasa() {
  const w = L.wall, jw = w.th * .62, sj = Math.min(L.song.ch * .62, L.u * 10), ej = L.u * 6.2;
  const naKaflu = p => t => { const q = tilePos(p, t); return { x: q.x + q.w * .5, y: q.y + q.h * .78 } };
  const naPiosence = i => () => { const q = songPos(i); return { x: q.x + q.w * .78, y: q.y + L.u * .4 } };
  const naGlowicy = t => ({ x: playX(t), y: L.ed.ry + L.u * .5 });
  const T = []; let prev = t => mouth(t), ps = L.bag.rog.w * .3;
  E.picks.forEach((p, i) => { const lt = E.LT[i], a = i ? lt - .4 : 6.06; T.push({ a, b: lt, from: prev, to: naKaflu(p), s0: i ? jw : ps, s1: jw, h: i ? w.th * .55 : L.H * .22 }); prev = naKaflu(p) });
  T.push({ a: 10.12, b: 10.519, from: prev, to: naPiosence(L.song.A), s0: jw, s1: sj, h: L.H * .04 });
  T.push({ a: 10.62, b: 11.029, from: naPiosence(L.song.A), to: naPiosence(L.song.gold), s0: sj, s1: sj, h: L.H * .05 });
  T.push({ a: 11.6, b: 12.005, from: naPiosence(L.song.gold), to: naGlowicy, s0: sj, s1: ej, h: L.H * .06 });
  T.push({ a: 99, b: 99, from: naGlowicy, to: naGlowicy, s0: ej, s1: ej, h: 0 });
  return T;
}
function joeyAt(t) {
  const T = E.trasa; if (t < T[0].a || t > 13.5) return null;
  for (let i = 0; i < T.length; i++) {
    const s = T[i];
    if (t <= s.b) {           // w locie
      const p = seg(t, s.a, s.b), e = eio(p) * .6 + p * .4, A = s.from(s.a), B = s.to(s.b);
      const [x, y] = arc(A.x, A.y, B.x, B.y, s.h, e);
      return { x, y: Math.max(y, L.hh + lerp(s.s0, s.s1, e) * .9), s: lerp(s.s0, s.s1, e), sy: 1 + .12 * Math.sin(Math.PI * p), sx: 1 - .06 * Math.sin(Math.PI * p), dir: B.x >= A.x ? 1 : -1, r: (B.x >= A.x ? 1 : -1) * 10 * Math.sin(Math.PI * 2 * p) };
    }
    const n = T[i + 1];
    if (!n || t < n.a) {      // stoi na celu (przysiad po lądowaniu, podskoki na bitach przy głowicy)
      const B = s.to(t), l = dec(t, s.b, .12), A = s.from(s.a);
      let y = B.y; if (i >= T.length - 2) { for (const b of BEATS) if (b > 12.3 && b < 13.6) y += hopY(t, b - .04, .26, L.u * 2.4) }
      return { x: B.x, y, s: s.s1, sy: 1 - .2 * l, sx: 1 + .12 * l, dir: B.x >= A.x ? 1 : -1, r: 0 };
    }
  }
  return null;
}

// ---------- jedna klatka ----------
const ETAPY = [[2.02, 'Każdy telefon wskakuje do torby', true], [6.01, 'Oglądamy każde nagranie'], [10.0, 'Dobieramy muzykę'], [11.6, 'Tniemy do rytmu'], [13.45, 'Twój film']];
let ostatnie = -1;
function render(t) {
  const { W, H, u, tall } = L;
  // ---- tło: poświata za torbą
  const b = bagState(t), glowO = t < 6.2 ? (.55 + .45 * BEATS.reduce((a, x) => a + dec(t, x, .25), 0) * .5) * (1 - seg(t, 5.9, 6.3)) * seg(t, .1, .8) : 0;
  op(E.glow, cl(glowO)); if (glowO > 0) { const gs = b.w * 1.9; tr(E.glow, b.cx - gs / 2, b.rim - gs * .42, 1); E.glow.style.width = E.glow.style.height = gs + 'px' }
  // ---- TORBA
  const bs = b.w / L.bw, gulp = cl(E.flights.reduce((a, f) => a + dec(t, f.t0 + f.d, .09), 0) + dec(t, 5.05, .12) + E.LT.reduce((a, x) => a + dec(t, x + .7, .1), 0) + dec(t, 11.75, .1), 0, 1.3);
  const bagO = 1 - seg(t, 11.95, 12.1), bagZ = t < 11.75 ? 1 : 1 + .12 * Math.sin(Math.PI * seg(t, 11.75, 11.88)) - ei(seg(t, 11.85, 12.1)) * .85;
  op(E.bag, bagO);
  if (bagO) {
    const bz = bs * bagZ; tr(E.bag, b.cx - L.bw * bz / 2, b.rim - L.bw * .1767 * bz, bz);
    E.bp.style.transform = `scale(${(1 + .03 * gulp).toFixed(4)},${(1 - .05 * gulp).toFixed(4)})`;
    E.bm.style.transform = `scaleY(${(seg(t, 2.6, 2.9) * (1 - seg(t, 5.5, 5.8)) + seg(t, 6.6, 6.8) * (1 - seg(t, 9.9, 10.1))).toFixed(3)})`;
    // kangurek w torbie: zerka → wyskakuje na bit → trzyma telefon z kodem → cieszy się → wyskakuje na ścianę
    let jy = 64, jr = 0;
    if (t < 1.02) jy = lerp(64, 36, eo(seg(t, .45, .9)));
    else if (t < 5.95) jy = lerp(36, 0, back(seg(t, 1.02, 1.4))) + hopY(t, 1.533, .42, 20) + hopY(t, 5.526, .45, 34) - BEATS.filter(x => x > 2.6 && x < 5.4).reduce((a, x) => a + dec(t, x, .12) * 3, 0) * -1;
    else if (t < 6.1) jy = lerp(0, 64, seg(t, 5.95, 6.06));
    else jy = 64;
    jr = t > 5.5 && t < 5.98 ? 8 * Math.sin(Math.PI * 2 * seg(t, 5.526, 5.98)) : 0;
    // w intro kangurek w proporcjach logo (większy), przy rośnięciu torby wraca do proporcji torby z aplikacji
    const js = t < 2.02 ? 2.5 : lerp(2.5, 1, eio(seg(t, 2.02, 2.55)));
    E.bj.style.transform = `translateY(${(jy * js).toFixed(2)}px) rotate(${jr.toFixed(2)}deg) scale(${js.toFixed(3)})`;
    E.bu.style.transform = `rotate(${(-10 * dec(t, 1.05, .25) + 8 * Math.sin(t * 9) * dec(t, 2.2, .4) + 7 * dec(t, 5.55, .2)).toFixed(2)}deg)`;
    const telO = seg(t, 2.15, 2.4) * (1 - seg(t, 5.4, 5.55));
    E.btel.style.opacity = telO.toFixed(3); E.btel.style.transform = `translate(0,${((1 - eo(seg(t, 2.15, 2.45))) * 20).toFixed(2)}px) rotate(${(-8 + 4 * Math.sin(t * 3)).toFixed(2)}deg)`;
    // licznik na torbie
    const n = Math.round(1434 * eo(seg(t, 2.8, 5.45)));
    const napO = seg(t, 2.55, 2.85) * (1 - seg(t, 5.85, 6.0)); op(E.bnap, napO);
    if (napO) E.bnum.textContent = n.toLocaleString('en-US');
  }
  // ---- INTRO: napis „montaroo” → leci do paska
  const wf = u * 11, wSc = (u * 3.4) / wf;
  if (t < 2.6) {
    op(E.word, tall ? 1 - seg(t, 2.25, 2.5) : 1); E.word.style.display = '';
    const wWidth = E.word._w || (E.word._w = E.word.getBoundingClientRect().width / (E.word._s || 1));
    const ix = W / 2 - wWidth / 2, iy = L.bag.intro.rim + L.bag.intro.w * .4 + u * 2;
    const hx = u * 3.2 + u * 6 + u * 1.3, hy = L.hh / 2 - wf / 2;
    const p = eio(seg(t, 2.02, 2.5)), s = lerp(1, wSc, p); E.word._s = s;
    tr(E.word, lerp(ix, hx, p), lerp(iy, hy, p), s);
    E.letters.forEach((l, i) => { const q = seg(t, .95 + i * .045, 1.35 + i * .045); l.style.opacity = q.toFixed(3); l.style.transform = `translateY(${((1 - back(q)) * u * 4).toFixed(2)}px)` });
    const tg = seg(t, 1.35, 1.7) * (1 - seg(t, 2.02, 2.2)); op(E.tag, tg);
    if (tg) { const tw = E.tag._w || (E.tag._w = E.tag.getBoundingClientRect().width); tr(E.tag, W / 2 - tw / 2, iy + wf * 1.25, 1) }
  } else if (t < 13.6) { op(E.word, tall ? 0 : 1 - seg(t, 13.45, 13.6)); op(E.tag, 0); const hx = u * 3.2 + u * 6 + u * 1.3; tr(E.word, hx, L.hh / 2 - wf / 2, wSc); E.letters.forEach(l => { l.style.opacity = 1; l.style.transform = '' }) }
  else op(E.word, 0);
  // ---- PASEK
  const barO = seg(t, 2.3, 2.6) * (1 - seg(t, 13.5, 13.9)); op(E.bar, barO);
  if (barO) {
    E.barMark.style.opacity = seg(t, 2.35, 2.55) * (t > 12.3 ? 1 : 1); E.barMark.style.transform = `scale(${(1 + .25 * dec(t, 12.45, .15)).toFixed(3)})`;
    const prog = seg(t, 2.02, 13.45); E.ring.setAttribute('stroke-dasharray', `${(prog * 100).toFixed(1)} 100`);
    let ei_ = 0; ETAPY.forEach((e, i) => { if (t >= e[0]) ei_ = i }); const et = ETAPY[ei_];
    if (E.etx._i !== ei_) { E.etx._i = ei_; E.etx.textContent = et[1] }
    E.soon.style.display = et[2] ? '' : 'none';
    E.etp.textContent = Math.round(prog * 100) + '%';
    const q = eo(seg(t, et[0], et[0] + .3)); E.et.style.opacity = q.toFixed(3); E.et.style.transform = `translateY(${((1 - q) * u * 1.2).toFixed(2)}px)`;
  }
  // ---- TELEFONY
  const telOn = t > 2.3 && t < 6.5;
  E.ph.forEach((P, i) => {
    const p = P.p, inn = seg(t, P.tin, P.tin + .5), out = seg(t, 5.92, 6.35), o = Math.min(seg(t, P.tin, P.tin + .2), 1 - out);
    op(P.e, telOn ? o : 0);
    if (!telOn || !o) { P.ln.style.opacity = 0; return }
    const side = p.side || (i === 1 ? 0 : 1), dx = side ? side * W * .25 : 0, dy = side ? 0 : -H * .4;
    const e = back(inn), x = p.cx - p.w / 2 + (1 - e) * dx + ei(out) * (side || 1) * W * .3, y = p.cy - p.h / 2 + (1 - e) * dy + (side ? 0 : -ei(out) * H * .3);
    tr(P.e, x, y, p.s * lerp(.86, 1, eo(inn)), (1 - eo(inn)) * (side || 1) * 14);
    const pr = seg(t, P.tin + .35, 5.2); P.bar.style.width = (pr * 100).toFixed(1) + '%'; P.pc.textContent = Math.round(pr * 100) + '%';
    const ok = Math.floor(pr * 15.99); P.cells.forEach((c, j) => kl(c.c, 'ok', j < ok));
    // linia telefon → torba
    const m = mouth(t), ax = side < 0 || (!side && false) ? x + p.w * p.s : side > 0 ? x : x + p.w / 2, ay = side ? y + p.h * .45 : y + p.h * p.s;
    const cx = (ax + m.x) / 2, cy = Math.min(ay, m.y) - H * (side ? .1 : -.02);
    P.ln.setAttribute('d', `M${ax.toFixed(1)} ${ay.toFixed(1)}Q${cx.toFixed(1)} ${cy.toFixed(1)} ${m.x.toFixed(1)} ${(m.y - u).toFixed(1)}`);
    const done = seg(t, 5.2, 5.5);
    P.ln.setAttribute('stroke', done > .5 ? '#8FC3AE' : P.kol);
    P.ln.style.opacity = (seg(t, P.tin + .2, P.tin + .5) * (1 - out) * (1 - done * .6)).toFixed(3);
    P.ln.style.strokeDashoffset = (-t * u * 14).toFixed(1);
    P._x = x; P._y = y;
  });
  E.lines.style.display = telOn ? '' : 'none';
  // pliki lecą z telefonów do torby
  E.flights.forEach(F => {
    const p = (t - F.t0) / F.d; if (p < 0 || p >= 1 || !telOn) { op(F.f, 0); return }
    const P = E.ph[F.i], ph = P.p, e = eio(p), m = mouth(F.t0 + F.d);
    const x0 = P._x + ph.w * p0(F.jx), y0 = P._y + ph.h * (.4 + .2 * F.jy), x1 = m.x + F.jx * b.w * .28, y1 = m.y + b.w * .05;
    const [x, y] = arc(x0, y0, x1, y1, H * (tall ? .08 : .16), e);
    op(F.f, Math.min(1, p / .1)); const fw = parseFloat(F.f.style.width), fh = parseFloat(F.f.style.height);
    tr(F.f, x - fw / 2, y - fh / 2, lerp(1.05, .55, e), lerp(F.r0, F.r1, e));
  });
  // karta z drona
  const sdIn = eo(seg(t, 4.25, 4.6)), sdOut = seg(t, 5.45, 5.75), sdO = seg(t, 4.25, 4.4) * (1 - sdOut);
  op(E.sd, sdO);
  if (sdO) { const sw = E.sd._w || (E.sd._w = E.sd.getBoundingClientRect().width); const sx = L.sd.x - sw / 2;
    tr(E.sd, sx, L.sd.y - (1 - sdIn) * u * 6, 1); E.sdS.textContent = t > 5.08 ? '212 nagrań · dodano ✓' : '212 nagrań · dodaję…'; E._sdx = sx + u * 4; E._sdy = L.sd.y + u * 4 }
  const cf = seg(t, 4.62, 5.08); op(E.sdFly, cf > 0 && cf < 1 ? 1 : 0);
  if (cf > 0 && cf < 1) { const m = mouth(5.08), [x, y] = arc(E._sdx || L.sd.x, E._sdy || L.sd.y, m.x, m.y + b.w * .04, H * .1, eio(cf)); tr(E.sdFly, x - u * 2.3, y - u * 3, lerp(1, .6, cf), 200 * cf) }
  // dymek kangurka
  const bo = seg(t, 2.38, 2.6) * (1 - seg(t, 3.45, 3.65)); op(E.bub, bo);
  if (bo) { const bw = E.bub._w || (E.bub._w = E.bub.getBoundingClientRect().width), bh = E.bub._h || (E.bub._h = E.bub.getBoundingClientRect().height);
    const bx = b.cx - b.w * .085 - bw - u * 1.6, by = b.rim - b.w * .14 - bh / 2; tr(E.bub, Math.max(u * 2, bx), by, lerp(.7, 1, back(seg(t, 2.38, 2.7)))) }
  // ---- ŚCIANA
  const wallOn = t > 5.85 && t < 10.3;
  E.wall.style.display = wallOn ? '' : 'none'; op(E.vig, wallOn ? seg(t, 5.9, 6.4) * (1 - seg(t, 9.8, 10.2)) : 0);
  if (wallOn) {
    const wx = wallXY(t); tr(E.wall, wx.x, wx.y, wx.s); E.wall.style.opacity = wx.o.toFixed(3);
    const sx = scanX(t), vis0 = -wx.x - L.wall.tw, vis1 = -wx.x + W;
    E.tiles.forEach(T => {
      const on = T.x > vis0 && T.x < vis1; if (T._on !== on) { T._on = on; T.e.style.display = on ? '' : 'none' } if (!on) return;
      const c = seg(t, 5.95 + Math.min(T.c, 10) * .035, 6.3 + Math.min(T.c, 10) * .035); T.e.style.opacity = c.toFixed(3);
      const dv = seg(sx - (T.x + L.wall.tw * .5), -L.wall.tw * .3, L.wall.tw * .9); T.e.firstChild.style.opacity = dv.toFixed(3);
    });
    E.picks.forEach((p, i) => kl(p.e, 'gw', t >= E.LT[i]));
  }
  E.picks.forEach((p, i) => {
    const lt = E.LT[i], s = seg(t, lt, lt + .45); op(E.stars[i], s > 0 && s < 1 ? 1 - s : 0);
    if (s > 0 && s < 1) { const q = tilePos(p, lt); tr(E.stars[i], q.x + q.w * .5 - u * 2, q.y - u * 1.5 - s * u * 5, .6 + s * 1.2) }
    const f = seg(t, lt + .14, lt + .7); op(E.wfly[i], f > 0 && f < 1 ? 1 : 0);
    if (f > 0 && f < 1) { const q = tilePos(p, lt + .14), m = mouth(t), [x, y] = arc(q.x + q.w / 2, q.y + q.h / 2, m.x, m.y + b.w * .06, H * .14, eio(f));
      tr(E.wfly[i], x - q.w / 2, y - q.h / 2, lerp(1, .22, eio(f)), lerp(0, 18, f)) }
  });
  const nb = E.LT.filter(x => t >= x + .7).length, bgO = seg(t, 7.1, 7.3) * (1 - seg(t, 11.7, 11.85));
  op(E.badge, bgO); if (bgO) { E.badge.textContent = '★ ' + nb; const bw2 = E.badge._w || (E.badge._w = E.badge.getBoundingClientRect().width + u * 2);
    tr(E.badge, b.cx - bw2 / 2, b.rim - b.w * .24 - u * 4, 1 + .25 * E.LT.reduce((a, x) => a + dec(t, x + .7, .12), 0)) }
  // ---- MUZYKA
  const musOn = t > 9.9 && t < 12.1;
  E.songs.forEach((S, i) => {
    if (!musOn) { op(S.e, 0); return }
    const inn = seg(t, 9.95 + i * .045, 10.3 + i * .045), dim = S.gold ? 0 : seg(t, 11.1, 11.35) * .75, out = S.gold ? seg(t, 11.5, 11.68) : seg(t, 11.4, 11.62);
    op(S.e, inn * (1 - dim) * (1 - out));
    const pop = S.gold ? dec(t, 11.029, .18) : 0;
    tr(S.e, S.x, S.y + (1 - eo(inn)) * u * 5 + out * u * 3, lerp(.9, 1, back(inn)) * (1 + .06 * pop) * (1 - out * .05));
    kl(S.e, 'gold', S.gold && t >= 11.029);
    const playA = i === L.song.A && t > 10.519 && t < 11.08, playG = S.gold && t > 11.029;
    S.pl.style.opacity = playA || playG ? .5 + .5 * Math.sin(t * 14) ** 2 : 0;
    if (playA || playG || S._anim) { S._anim = playA || playG; S.bars.forEach((x, j) => x.style.transform = S._anim ? `scaleY(${(.45 + .55 * Math.abs(Math.sin(t * 7 + j * .8))).toFixed(3)})` : '') }
  });
  // fala piosenki zjeżdża na ścieżkę Muzyka
  const wv = seg(t, 11.12, 11.62), wO = t < 11.12 ? 0 : t < 13.5 ? 1 : 1 - seg(t, 13.5, 13.9);
  op(E.wave, wO);
  if (wO) { const S = E.songs[L.song.gold], from = { x: S.x + L.u * 1.6, y: S.y + L.song.ch * .52, w: L.song.cw - L.u * 3.2, h: L.song.ch * .36 }, to = E.waveTo, e = eio(wv);
    tr(E.wave, lerp(from.x, to.x, e), lerp(from.y, to.y, e), 1); E.wave.style.width = lerp(from.w, to.w, e) + 'px'; E.wave.style.height = lerp(from.h, to.h, e) + 'px';
    E.wave.style.color = hex('#F2B544', '#8FC3AE', seg(t, 11.5, 11.9)); if (!E.wave._c) { E.wave._c = 1; [...E.wave.children].forEach(x => x.style.background = 'currentColor') } }
  // ---- MONTAŻ
  const edOn = t > 11.5 && t < 14.3;
  const edO = seg(t, 11.55, 11.85) * (1 - seg(t, 13.6, 14.0)); op(E.ed, edOn ? edO : 0);
  if (edOn) {
    E.pv.style.opacity = (1 - seg(t, 13.45, 13.6)).toFixed(3);
    E.clips.forEach((c, i) => { const a = 11.62 + i * .085, q = seg(t, a, a + .28); op(c.e, Math.min(1, q * 3)); c.e.style.transform = `translateY(${((1 - back(q)) * -L.ed.tracks[0].h * .9).toFixed(2)}px)`; kl(c.e, 'sel', i === 1 && t >= 12.62 && t < 13.4) });
    E.beats.forEach((x, i) => op(x, seg(t, 12.0 + i * .03, 12.2 + i * .03)));
    E.chips.forEach((c, i) => { const q = seg(t, 11.95 + i * .1, 12.2 + i * .1); op(c, q); c.style.transform = `scaleX(${eo(q).toFixed(3)})`; c.style.transformOrigin = '0 50%' });
    E.snds.forEach((c, i) => op(c, seg(t, 12.1 + i * .1, 12.3 + i * .1)));
    op(E.plaq, seg(t, 11.7, 11.9)); op(E.ph2, seg(t, 11.85, 12.05)); E.ph2.style.left = playX(t) + 'px';
    // kursor: klik w ujęcie → pasek ujęcia → „+ Longer”
    const c1 = E.clips[1], cx1 = (c1.x0 + c1.x1) / 2, cy1 = L.ed.tracks[0].y + L.ed.tracks[0].h * .55;
    const tbw = E.tb._w || (E.tb._w = E.tb.getBoundingClientRect().width), tbh = E.tb._h || (E.tb._h = E.tb.getBoundingClientRect().height);
    const tbx = cl(cx1 - tbw / 2, u * 2, W - tbw - u * 2), tby = L.ed.tracks[0].y - tbh - u * 1.1;
    const tbo = seg(t, 12.66, 12.8) * (1 - seg(t, 13.3, 13.42)); op(E.tb, tbo); tr(E.tb, tbx, tby, lerp(.8, 1, back(seg(t, 12.66, 12.86))));
    const it = E.tbi[1].offsetLeft + E.tbi[1].offsetWidth / 2;
    E.tbi.forEach((x, i) => kl(x, 'on', i === 1 && t >= 13.02 && t < 13.35));
    let kx, ky; const k0 = { x: W * .86, y: H * .97 }, k1 = { x: cx1, y: cy1 }, k2 = { x: tbx + it, y: tby + tbh * .6 };
    if (t < 12.6) { const p = eio(seg(t, 12.3, 12.6)); kx = lerp(k0.x, k1.x, p); ky = lerp(k0.y, k1.y, p) } else if (t < 12.82) { kx = k1.x; ky = k1.y } else { const p = eio(seg(t, 12.82, 13.0)); kx = lerp(k1.x, k2.x, p); ky = lerp(k1.y, k2.y, p) }
    const klik = Math.max(dec(t, 12.6, .07), dec(t, 13.0, .07));
    op(E.cur, seg(t, 12.3, 12.4) * (1 - seg(t, 13.3, 13.42))); tr(E.cur, kx, ky, 1 - .18 * klik);
  } else { op(E.tb, 0); op(E.cur, 0) }
  // ---- KANGUREK
  const J = joeyAt(t);
  op(E.joey, J ? (t > 13.3 ? 1 - seg(t, 13.3, 13.5) : 1) : 0);
  if (J) { const h = J.s, w = h * 46 / 70; E.joey.style.width = w + 'px'; E.joey.style.height = h + 'px';
    E.joey.style.transform = `translate3d(${(J.x - w / 2).toFixed(1)}px,${(J.y - h).toFixed(1)}px,0) rotate(${J.r.toFixed(2)}deg) scale(${(J.sx * J.dir).toFixed(3)},${J.sy.toFixed(3)})`;
    E.ju.style.transform = `rotate(${(6 * Math.sin(t * 11)).toFixed(1)}deg)`; E.ju.style.transformOrigin = '55px 36px' }
  // ---- PODGLĄD → FILM (prawdziwe wideo w okienku podglądu rośnie na całą scenę)
  return gracz(t);
}
const p0 = j => .5 + .25 * j;

function gracz(t) {
  const P = L.pv, { W, H } = L;
  if (t < 11.75) return { o: 0 };
  const g = eio(seg(t, 13.45, T_FILM)), x = lerp(P.x, 0, g), y = lerp(P.y, 0, g), k = lerp(P.k, 1, g), r = lerp(P.r, 0, g);
  return { o: seg(t, 11.75, 12.0), x, y, k, r, w: W * k, h: H * k, fl: dec(t, T_FILM, .12) };
}
function ustawGracza(G) {
  if (!G.o) { pl.style.opacity = 0; return }
  pl.style.opacity = G.o.toFixed(3);
  pl.style.clipPath = `inset(${G.y.toFixed(1)}px ${(L.W - G.x - G.w).toFixed(1)}px ${(L.H - G.y - G.h).toFixed(1)}px ${G.x.toFixed(1)}px round ${G.r.toFixed(1)}px)`;
  vid.style.transform = G.k < .999 ? `translate3d(${G.x.toFixed(1)}px,${G.y.toFixed(1)}px,0) scale(${G.k.toFixed(4)})` : '';
  vid.style.filter = G.fl > .01 ? `brightness(${(1 + .45 * G.fl).toFixed(3)})` : '';
}

// ---------- odtwarzanie ----------
// Jedna muzyka: utwór z filmu (strona_20s_bouncy-brass_a). Pod animacją gra jego początek 0–14,512 s (intro → drop 10,52),
// na takcie 14,512 przechodzi w muzykę filmu od jego pierwszego cięcia (2,531). Harmonia powtarza się co 2 takty – szwu nie słychać.
// Czas strony t → czas sceny τ: bit k sceny = bit k+1 utworu (siatka 119,5 BPM), więc wszystko pada równo na bity.
const NOWE = [0.534, 1.022, 1.533, 2.043, 2.531, 3.019, 3.529, 4.04, 4.528, 5.016, 5.526, 6.014, 6.525, 7.012, 7.523, 8.011, 8.522, 9.033, 9.52, 10.008, 10.519, 11.029, 11.517, 12.028, 12.516, 13.026, 13.514, 14.025, 14.512];
const P_FILM = 14.512, P_VOFF = P_FILM - 2.531, P_KONIEC = P_VOFF + 19.95;
function scena(t) {
  if (t <= NOWE[1]) return t - (NOWE[1] - BEATS[0]);
  if (t >= NOWE[28]) return BEATS[27] + (t - NOWE[28]);
  let k = 1; while (NOWE[k + 1] < t) k++;
  return BEATS[k - 1] + (t - NOWE[k]) / (NOWE[k + 1] - NOWE[k]) * (BEATS[k] - BEATS[k - 1]);
}
let t0 = performance.now(), dzwiek = false, film = false, raf = 0, pauza = null;
const teraz = () => pauza !== null ? pauza : (performance.now() - t0) / 1000;
function zrodlo() { const f = L && L.tall ? '9x16' : '16x9'; if (vid.dataset.f === f) return; vid.dataset.f = f; vid.poster = HV + `film-20s-${f}.jpg`; vid.src = HV + `film-20s-${f}.mp4` }
function wFilm(on) {
  if (film === on) return; film = on; stage.classList.toggle('film', on);
  if (on) { pl.style.opacity = 1; pl.style.clipPath = ''; vid.style.transform = ''; vid.style.filter = '' }
}
const graj = e => { const p = e.play(); if (p) p.catch(() => {}) };
function petla() {
  raf = requestAnimationFrame(petla);
  if (!czekal && !dzwiek && !CAP && teraz() >= T_CZEKA) zaproszenie();
  if (czeka) dymekZaproszenia();
  let t = teraz();
  if (dzwiek && !aud.paused && !aud.ended) { const d = aud.currentTime - t; if (Math.abs(d) > .05) { t0 -= d * 1000; t = teraz() } }
  // wideo (zawsze wyciszone – dźwięk to jedna ścieżka aud): od P_VOFF gra w podglądzie, zgrane z czasem strony
  const want = t - P_VOFF;
  if (want >= -.25 && t < P_KONIEC) { if (vid.paused) { vid.currentTime = Math.max(0, want); graj(vid) } else if (Math.abs(vid.currentTime - want) > .2) vid.currentTime = Math.max(0, want) }
  else if (want < -.25 && !vid.paused) { vid.pause(); vid.currentTime = 0 }
  if (t < P_FILM + .02) { wFilm(false); ustawGracza(render(scena(t))) }
  else if (!film) { ustawGracza({ o: 1, x: 0, y: 0, k: 1, r: 0, w: L.W, h: L.H, fl: 0 }); wFilm(true) }
  const ri = t >= P_FILM ? 5 : t >= 12.06 ? 4 : t >= 10.519 ? 3 : t >= 6.525 ? 2 : t >= 2.531 ? 1 : 0;
  [...rozd.children].forEach((b, i) => kl(b, 'on', i === ri));
}
function skocz(t) {
  t0 = performance.now() - t * 1000; pauza = null;
  wFilm(t >= P_FILM); vid.pause();
  if (t >= P_FILM) { vid.currentTime = t - P_VOFF; graj(vid) }
  if (dzwiek) { aud.currentTime = t; graj(aud) }
}
function ustawDzwiek(on) {
  dzwiek = on; snd.textContent = dzwiek ? '🔇 Wycisz' : '🔊 Włącz dźwięk'; stage.classList.toggle('gra', on);
  const t = teraz();
  if (dzwiek && t < P_KONIEC) { aud.currentTime = t; graj(aud) } else aud.pause();
}
snd.onclick = e => { e.stopPropagation(); if (czeka) { zaproszenieKoniec(); ustawDzwiek(true); skocz(0); return } wyciszony = dzwiek; ustawDzwiek(!dzwiek) };
// A: w intro kangurek wychodzi z torby i czeka ok. 2,6 s z dymkiem „Tap me 🎵” – dotknięcie = intro od początku z muzyką,
// brak dotknięcia = historia leci dalej po cichu. B: później każde dotknięcie sceny włącza muzykę od bieżącej chwili
// (chyba że ktoś sam wyciszył). Przeglądarki nie pozwalają grać bez pierwszego dotknięcia – stąd zaproszenie.
const T_CZEKA = 1.98, CZEKA_MS = 2600;
let czeka = false, czekal = false, czekaT = 0, wyciszony = false;
function zaproszenie() {
  czeka = czekal = true; pauza = T_CZEKA; stage.classList.add('czeka');
  czekaT = setTimeout(() => { zaproszenieKoniec(); t0 = performance.now() - T_CZEKA * 1000; pauza = null }, CZEKA_MS);
}
function zaproszenieKoniec() { clearTimeout(czekaT); czeka = false; stage.classList.remove('czeka') }
function dymekZaproszenia() {
  const b = bagState(scena(T_CZEKA)), u = L.u, bw = E.tap._w || (E.tap._w = E.tap.offsetWidth), bh = E.tap._h || (E.tap._h = E.tap.offsetHeight);
  const x = b.cx - b.w * .3 - bw - u * 1.2, y = b.rim - b.w * .38 - bh / 2;
  E.tap.style.transform = `translate(${Math.max(u * 2, x).toFixed(1)}px,${Math.max(L.hh || 0, y).toFixed(1)}px)`;
}
stage.addEventListener('pointerdown', e => {
  if (e.target.closest('button,a,input')) return;
  if (czeka) { zaproszenieKoniec(); ustawDzwiek(true); skocz(0); return }
  if (!dzwiek && !wyciszony && teraz() < P_KONIEC) ustawDzwiek(true);
});
again.onclick = e => { e.stopPropagation(); skocz(0) };
rozd.addEventListener('click', e => { const b = e.target.closest('button'); if (b) skocz(+b.dataset.t) });
document.addEventListener('visibilitychange', () => { if (czeka) return; if (document.hidden) { pauza = teraz(); aud.pause(); vid.pause() } else if (pauza !== null) { const t = pauza; skocz(t) } });
let szer = 0, rt;
addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { const r = stage.getBoundingClientRect(); if (Math.abs(r.width - szer) < 40) return; szer = r.width; buduj(); zrodlo() }, 250) });

// nagrywanie klatek (spot): ?cap → window.ustaw(t) rysuje klatkę dla czasu strony t i zwraca okienko filmu
window.ustaw = t => render(scena(t));
window.CZASY = { P_FILM, P_VOFF };

Promise.all([fetch(HB + 'kafle.json').then(r => r.json()).then(j => K = j), ...['kafle.jpg', 'kafle-szary.jpg', 'klatki.jpg'].map(s => new Promise(ok => { const i = new Image(); i.onload = i.onerror = ok; i.src = HB + s })), document.fonts.ready]).then(() => {
  if (CAP) document.body.classList.add('cap');
  szer = stage.getBoundingClientRect().width; buduj(); zrodlo();
  if (CAP) { window.GOTOWE = true; return }
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { czekal = true; skocz(P_FILM); petla(); return }
  t0 = performance.now(); petla(); window.GOTOWE = true;
});
})();
