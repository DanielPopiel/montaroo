// Test strony głównej w Chrome bez okna (CDP): node _zrodlo/test_strona.mjs <adres, np. http://127.0.0.1:8870/pl/> <W> <H> <folder zrzutów> [mobile]
// Sprawdza: błędy w konsoli i sieci, język napisów sceny, zaproszenie „Tap me”, dźwięk po dotknięciu, przebieg do filmu, brak przewijania poziomego, walidację formularza (bez wysyłki).
// Serwer: python -m http.server 8870 --bind 127.0.0.1 (z katalogu repozytorium)
import { spawn } from 'node:child_process'; import { writeFileSync, mkdirSync } from 'node:fs';
const [url, W, H, out, mob] = [process.argv[2], +process.argv[3], +process.argv[4], process.argv[5], process.argv[6] === 'mobile']; mkdirSync(out, { recursive: true });
const port = 9800 + Math.floor(Math.random() * 90), sleep = ms => new Promise(r => setTimeout(r, ms));
const ch = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=C:/Users/popek/AppData/Local/Temp/claude/ts${port}`, `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' });
let tabs; for (let i = 0; i < 80; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (tabs.find(t => t.type === 'page')) break } catch (e) { } await sleep(250) }
const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = new Map(); const logs = [], zle = new Set();
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result || d); pend.delete(d.id) }
  if (d.method === 'Runtime.exceptionThrown') logs.push('WYJĄTEK ' + JSON.stringify(d.params.exceptionDetails).slice(0, 300));
  if (d.method === 'Runtime.consoleAPICalled' && ['error', 'warning'].includes(d.params.type)) logs.push('konsola ' + d.params.type + ': ' + d.params.args.map(a => a.value || a.description).join(' ').slice(0, 200));
  if (d.method === 'Log.entryAdded' && d.params.entry.level === 'error') logs.push('log: ' + d.params.entry.text + ' ' + (d.params.entry.url || ''));
  if (d.method === 'Network.loadingFailed' && !d.params.canceled) zle.add('sieć: ' + d.params.errorText + ' ' + d.params.requestId);
  if (d.method === 'Network.responseReceived' && d.params.response.status >= 400) zle.add('HTTP ' + d.params.response.status + ' ' + d.params.response.url) };
const send = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({ id, method, params })) });
await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: mob });
const ev = async e => { const r = await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) logs.push('EV ' + JSON.stringify(r.exceptionDetails).slice(0, 200)); return r.result && r.result.value };
const shot = async n => { const s = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(`${out}/${n}.png`, Buffer.from(s.data, 'base64')) };
const wyn = []; const ok = (n, w, o = '') => { wyn.push(!!w); console.log(w ? 'OK  ' : 'BŁĄD', n, o) };
const pl = url.includes('/pl'); const reduce = process.argv[7] === 'reduce';
if (reduce) await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
const T0 = Date.now(); await send('Page.navigate', { url });
for (let i = 0; i < 100; i++) { if (reduce || await ev('!!window.GOTOWE')) break; await sleep(200) }  // GOTOWE to znacznik testowy (nie ustawia się przy reduced-motion)
const t0 = Date.now(); const at = async s => { while ((Date.now() - t0) / 1000 < s) await sleep(30) };
ok('scena wystartowała (GOTOWE)', reduce || await ev('!!window.GOTOWE'), ((Date.now() - T0) / 1000).toFixed(1) + ' s od nawigacji');
ok('język strony', (await ev('document.documentElement.lang')) === (pl ? 'pl' : 'en'));
const h1 = await ev('document.querySelector("h1").textContent'); ok('nagłówek', pl ? /Zamień/.test(h1) : /Turn your trip/.test(h1), h1);
if (reduce) { await sleep(2500); ok('reduced-motion: od razu film, bez animacji', await ev('document.querySelector("#stage").classList.contains("film")'));
  ok('reduced-motion: brak zaproszenia „Tap me” i pauzy', !(await ev('document.querySelector("#stage").classList.contains("czeka")'))); await shot('6_reduce');
  ok('brak błędów w konsoli', logs.length === 0, logs.join(' | ').slice(0, 300)); ws.close(); ch.kill(); const b = wyn.filter(x => !x).length; console.log(`
${wyn.length - b}/${wyn.length} OK`); process.exit(b ? 1 : 0); }
await at(1.0); await shot('1_intro');
await at(2.45); const czeka = await ev('document.querySelector("#stage").classList.contains("czeka")');
ok('zaproszenie „Tap me” (pauza po intro)', czeka); await shot('2_tap');
const tap = await ev('document.querySelector(".h-tap")?.textContent||""'); ok('dymek zaproszenia w języku strony', pl ? /Dotknij/.test(tap) : /Tap me/.test(tap), tap);
const r = JSON.parse(await ev('JSON.stringify(document.querySelector("#stage").getBoundingClientRect())'));
for (const type of ['mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x: r.x + r.width / 2, y: r.y + r.height * .3, button: 'left', clickCount: 1 });
await sleep(500);
ok('dotknięcie włącza muzykę', await ev('!document.querySelector("#aud").paused'), 'czas utworu ' + (await ev('document.querySelector("#aud").currentTime.toFixed(2)')));
const sn = await ev('document.querySelector("#snd").textContent');
ok('przycisk dźwięku zmienia napis', pl ? /Wycisz/.test(sn) : /Mute/.test(sn), sn);
const t1 = Date.now(); const etapy = []; let lastTxt = '';
for (let s = 1; s < 24; s += .5) {
  while ((Date.now() - t1) / 1000 < s) await sleep(40);
  const txt = await ev('(document.querySelector(".h-et .tx")||{}).textContent||""');
  if (txt !== lastTxt && /Oglądamy|Watching every|Każdy|Every phone|Dobieramy|Picking|Tniemy|Cutting/.test(txt)) etapy.push(txt.slice(0, 60)); lastTxt = txt;
  if (Math.abs(s - 4) < .26 || Math.abs(s - 8) < .26 || Math.abs(s - 11.5) < .26) await shot('3_t' + s.toFixed(0));
  if (await ev('document.querySelector("#stage").classList.contains("film")')) break;
}
ok('scena doszła do filmu', await ev('document.querySelector("#stage").classList.contains("film")'));
await sleep(2500); await shot('4_film');
const vid = JSON.parse(await ev('JSON.stringify({t:document.querySelector("#vid").currentTime,paused:document.querySelector("#vid").paused,w:document.querySelector("#vid").videoWidth,src:document.querySelector("#vid").currentSrc.split("/").pop()})'));
ok('film gra w scenie', !vid.paused && vid.t > 0 && vid.w > 0, JSON.stringify(vid));
ok('napisy etapów w języku strony', etapy.length >= 2 && etapy.some(x => pl ? /Oglądamy|Każdy|Dobieramy|Tniemy/.test(x) : /Watching|Every|Picking|Cutting/.test(x)), etapy.join(' | '));
if (pl) ok('brak angielskich napisów sceny', !/Coming soon|Watching every|Tap me|Got clips|drone card|Shorter|Swap/.test(await ev('document.querySelector("#fx").textContent')));
ok('brak przewijania poziomego', await ev('document.scrollingElement.scrollWidth<=innerWidth+1'), await ev('document.scrollingElement.scrollWidth+" / "+innerWidth'));
await ev('document.querySelector("#wl-e").value="to-nie-email";document.querySelector("#wl button").click()'); await sleep(300);
const wm = await ev('document.querySelector("#wl-m").textContent');
ok('walidacja formularza (bez wysyłki)', /(valid|poprawny)/i.test(wm), wm);
await ev('window.scrollTo(0,0)'); await shot('5_calosc');
ok('stopka z linkami prawnymi', /(Privacy|Prywatność)/.test(await ev('document.querySelector("footer").textContent')));
ok('brak błędów w konsoli', logs.length === 0, logs.join(' | ').slice(0, 500));
ok('brak nieudanych żądań', zle.size === 0, [...zle].join(' | ').slice(0, 500));
ws.close(); ch.kill(); const bad = wyn.filter(x => !x).length; console.log(`\n${wyn.length - bad}/${wyn.length} OK`); process.exit(bad ? 1 : 0);
