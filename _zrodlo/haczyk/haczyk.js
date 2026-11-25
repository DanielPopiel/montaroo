/* Bramka na starcie sceny „Historia”: na całej stronie przyciemnione tło, trzy zdania, przycisk „Show me” (z dźwiękiem) i „No sound”,
   odliczanie paskiem; po odliczeniu scena rusza sama – próbuje z dźwiękiem, a gdy przeglądarka nie pozwoli, bez dźwięku + „Tap for sound”.
   Ustawienia: AB_PROC (ile % odwiedzających widzi bramkę; reszta dostaje scenę bez bramki), ?hak=1 wymusza, ?hak=0 wyłącza.
   Ruch z reklam Meta (fbclid / utm_source=fb,ig,meta / referrer IG,FB) pomija bramkę.
   Raz na sesję (sessionStorage), bez bramki przy prefers-reduced-motion. Zdarzenie okna „haczyk” + Meta (fbq trackCustom), gdy piksel jest włączony. */
(() => {
  const AB_PROC = 100, ODL = 4, START_PRZYCISKOW = 5;
  const Q = new URLSearchParams(location.search), wym = Q.get('hak');
  const PL = document.documentElement.lang === 'pl';
  const magazyn = { get: (s, k) => { try { return s.getItem(k) } catch (e) { return null } }, set: (s, k, v) => { try { s.setItem(k, v) } catch (e) {} } };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || wym === '0') return;
  // Ruch z reklam Meta (fbclid, utm_source=fb/ig/meta albo referrer z Instagrama/Facebooka) dostaje stronę od razu, bez bramki:
  // bramka zasłania formularz i baner cookies (piksel nie startuje bez zgody), a ?hak=1 nadal ją wymusza.
  let host = ''; try { host = new URL(document.referrer).hostname } catch (e) {}
  const zReklamy = Q.has('fbclid') || /^(fb|ig|facebook|instagram|meta)/i.test(Q.get('utm_source') || '') || /(^|\.)(instagram|facebook)\.com$/i.test(host);
  if (zReklamy && wym !== '1') return;
  if (wym !== '1') {
    if (magazyn.get(sessionStorage, 'mHak')) return;                                   // raz na sesję
    let g = magazyn.get(localStorage, 'mHakGrupa');
    if (g !== 'z' && g !== 'bez') { g = Math.random() * 100 < AB_PROC ? 'z' : 'bez'; magazyn.set(localStorage, 'mHakGrupa', g); }
    window.HAK_GRUPA = g; if (g === 'bez') return;
  } else window.HAK_GRUPA = 'z';
  document.body.setAttribute('data-hak', '');                                           // scena nie pokazuje własnego „Tap me”, gdy jest bramka

  const L = PL ? { l: ['Twoje nagrania z wyjazdu leżą na dysku.', 'Zapomniane.', 'Zobaczmy, co z nimi zrobi Montaroo.'], yes: 'Pokaż', no: 'Bez dźwięku',
                   cd: n => `Start za ${n} s`, nota: 'z dźwiękiem, jeśli przeglądarka pozwoli', hint: 'Dotknij, by włączyć dźwięk', mute: 'Wycisz', snd: 'Dźwięk' }
                 : { l: ['Your trip footage is sitting on a hard drive.', 'Forgotten.', 'Let’s see what Montaroo does with it.'], yes: 'Show me', no: 'No sound',
                   cd: n => `Starts in ${n} s`, nota: 'with sound, if your browser allows', hint: 'Tap for sound', mute: 'Mute', snd: 'Sound on' };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const USZY = 'M46.94 11.93A5.2 11 -14 1 1 52.26 33.27A5.2 11 -14 1 1 46.94 11.93ZM67.47 15.95A5.2 11 24 1 1 58.53 36.05A5.2 11 24 1 1 67.47 15.95Z';
  const CIALO = 'M44 36.26A6 6 0 0 1 52.94 31.03L82.7 47.77A6 6 0 0 1 82.7 58.23L52.94 74.97A6 6 0 0 1 44 69.74Z';
  const ikona = on => `<svg class="hk-ik" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 17.5V6.3l9.5-2v11.2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6.6" cy="17.6" r="2.7" fill="currentColor"/><circle cx="16.1" cy="15.6" r="2.7" fill="currentColor"/>${on ? '' : '<path d="M4 4l16 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'}</svg>`;
  window.HIKON = on => `${ikona(on)}<span>${esc(on ? L.mute : L.snd)}</span>`;     // przycisk „Sound on / Mute” w scenie w tym samym stylu
  const sndBtn = document.getElementById('snd'); if (sndBtn) sndBtn.innerHTML = window.HIKON(false);

  const czekaj = setInterval(() => { if (window.GOTOWE && window.HIST) { clearInterval(czekaj); pokaz(); } }, 60);
  function pokaz() {
    const H = window.HIST, st = H.stage; let koniec = false, tm = 0, tk = 0;
    const ov = document.createElement('div'); ov.className = 'hak'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', L.l.join(' '));
    ov.innerHTML = `<p class="hk-q hk-l1">${esc(L.l[0])}</p><p class="hk-q hk-l2">${esc(L.l[1])}</p><p class="hk-q hk-l3">${esc(L.l[2])}</p>
      <div class="hk-rz"><span class="hk-bw"><svg class="hk-jy" viewBox="40 8 48 70" aria-hidden="true"><path d="${USZY}"/><path d="${CIALO}"/></svg><i class="hk-cien"></i><button type="button" class="hk-btn hk-y" data-s="1">${esc(L.yes)} ${ikona(true)}</button></span><button type="button" class="hk-btn hk-n" data-s="0">${esc(L.no)}</button></div>
      <div class="hk-cd" aria-hidden="true"><div class="hk-bar"><i></i></div><p><b class="hk-n0">${esc(L.cd(ODL))}</b><small>${esc(L.nota)}</small></p></div>`;
    document.body.appendChild(ov); document.documentElement.style.overflow = 'hidden';
    ov.addEventListener('pointerdown', e => e.stopPropagation());
    H.zamroz(0.2);
    const zdarzenie = d => {
      const det = { wariant: 'd', grupa: window.HAK_GRUPA, ...d };
      try { window.dispatchEvent(new CustomEvent('haczyk', { detail: det })); } catch (e) {}
      try { if (window.fbq) fbq('trackCustom', 'HaczykStart', det); } catch (e) {}
    };
    function zamknij() {
      koniec = true; clearTimeout(tm); clearInterval(tk); ov.classList.add('out'); setTimeout(() => ov.remove(), 450);
      document.documentElement.style.overflow = ''; document.removeEventListener('keydown', klaw); magazyn.set(sessionStorage, 'mHak', '1');
      const r = st.getBoundingClientRect(); if (r.top < 0 || r.bottom > innerHeight) st.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    function start(dzwiek) { if (koniec) return; zamknij(); H.skocz(0); H.dzwiek(!!dzwiek); zdarzenie({ dzwiek: !!dzwiek, auto: false }); }
    function autostart() {                                                               // koniec odliczania: próba z dźwiękiem, inaczej bez + podpowiedź
      if (koniec) return; zamknij(); H.skocz(0); H.dzwiek(true);
      setTimeout(() => {
        const a = document.getElementById('aud');
        if (a && !a.paused) { zdarzenie({ dzwiek: true, auto: true }); return; }
        H.dzwiek(false); zdarzenie({ dzwiek: false, auto: true });
        const h = document.createElement('button'); h.type = 'button'; h.className = 'hk-hint'; h.innerHTML = `${ikona(false)}<span>${esc(L.hint)}</span>`;
        const zdejmij = () => h.remove(); h.onclick = () => { H.dzwiek(true); zdejmij(); }; if (sndBtn) sndBtn.addEventListener('click', zdejmij, { once: true });
        st.appendChild(h);
      }, 500);
    }
    function klaw(e) {                                                                   // Esc = bez dźwięku; Tab krąży tylko po dwóch przyciskach
      if (e.key === 'Escape') { start(false); return; }
      if (e.key === 'Tab') { const b = [...ov.querySelectorAll('button')], i = b.indexOf(document.activeElement);
        e.preventDefault(); b[(i + (e.shiftKey ? b.length - 1 : 1)) % b.length].focus(); }
    }
    document.addEventListener('keydown', klaw);
    ov.querySelectorAll('[data-s]').forEach(b => b.onclick = () => start(b.dataset.s === '1'));
    tm = setTimeout(autostart, (START_PRZYCISKOW + ODL) * 1000);
    const t0 = performance.now() + START_PRZYCISKOW * 1000, cd = ov.querySelector('.hk-cd'), n0 = ov.querySelector('.hk-n0');
    tk = setInterval(() => {
      const s = (performance.now() - t0) / 1000; if (s < 0) return;
      cd.style.setProperty('--p', Math.min(1, s / ODL).toFixed(3)); cd.classList.add('on'); n0.textContent = L.cd(Math.max(0, Math.ceil(ODL - s)));
    }, 80);
    setTimeout(() => { try { ov.querySelector('.hk-y').focus({ preventScroll: true }); } catch (e) {} }, 60);
    window.HAK = { start, autostart, koniec: () => koniec };
    zdarzenie({ pokazana: true });
  }
})();
