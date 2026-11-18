# Kampania Montaroo – wszystko w jednym miejscu

Stan na 18.11.2026. Konta: Instagram i TikTok **@montarooapp**, YouTube **Montaroo**.
Kolory i kroje: ciemna zieleń #10251F, ochra #E2642A, złoto #F2B544, piasek #F4E9D6; Gabarito + Inter (bez Fraunces).

## Plany i harmonogram
| Plik | Co to jest |
|---|---|
| `trasa/PLAN_PUBLIKACJI.md` | Daty i opisy wszystkich postów (IG 1–12, TikTok, YT) |
| `PLAN_ROZKRECANIA_SOCIAL.md` | Analiza tempa i strategia rozkręcania kont, plan na premierę |
| `trasa/PREZENTACJA_trasa_skoku.html` | Podgląd profilu IG z siatką i reelsami (otwórz w przeglądarce) |

## Gotowe filmy (`trasa/`)
**Reelsy kampanii „Trasa skoku” (siatka IG, posty 1–9)** – `reel-post-N_T*_en/pl.mp4`, 10 s, 9:16.
Okładki: `okladka-post-N_T*.png`, kafelki siatki: `kafel-T*_post-N.png`, panoramy: `panorama*.png` (`panorama_12.png` = cały profil po 12 postach).

**Spoty z kangurem AI** (9:16, 10 s, EN i PL):
| Plik | Pomysł | Źródło klipu |
|---|---|---|
| `spot-hop_*` | The Hop – droga, kanion, joey | Higgsfield (3 klipy, 60 kredytów) |
| `spot-laptop_*` | Noc przy laptopie, joey wciska klawisz | Gemini |
| `spot-telefon_*` | „47 GB z jednego wyjazdu” | Gemini |
| `spot-ognisko_*` | „Kto zmontuje film z wyjazdu?” | Gemini |
| `spot-lotnisko_*` | „200 GB wspomnień. I co teraz?” | Gemini |

**Trailery** (26 s, EN i PL):
- `trailer-yt_*` – poziom 16:9 (YouTube, trailer kanału)
- `trailer-pion_*` – pion 9:16 na pełnym kadrze (Reels / TikTok / Shorts)

`trasa/tiktok/` – lżejsze kopie spotów (<3,8 MB) do wrzucania przez przeglądarkę.

## Muzyka
- `trasa/montaroo-hop_podklad.wav` – „Montaroo Hop” (remaster, 10 s), używana wszędzie
- `trasa/montaroo-hop_podklad_26s.wav` – wersja 26 s do trailerów
- `trasa/dzwieki/` – 6 wariantów, z których wybrałeś remaster (nr 6)

## Surowe materiały
- `higgsfield/` – surowe klipy AI (mimo nazwy są tu też klipy z Gemini: `gemini_*.mp4`)
- `kadry/` – 9 kadrów do kolejnych spotów + zbiorcza plansza `kadry_9_pomyslow.jpg`
  1 Wyścig z żółwiem · 2 Galeria bez końca · 3 Urodziny · 4 Joey reżyser · 5 Powrót z wakacji (✔ spot) · 6 Dron · 7 Wieczór filmowy · 8 Kto to zmontuje? (✔ spot) · 9 Joey tłumaczy
- `posty/`, `montaroo-spot-*`, `podklad.wav` – pierwsze materiały sprzed kampanii

## Skrypty (`zrodlo/`) – z nich da się odtworzyć każdy plik
| Skrypt | Robi |
|---|---|
| `trasa.py`, `rzad3.py`, `rzad4.py` | Panorama, kafelki i okładki siatki (rzędy 1–4) |
| `reel_t2.py`, `reel_t6.py`, `reels.py` | Reelsy postów 1–9 (`python reels.py en 7`) |
| `spot_hop.py` | Spoty z klipów AI; wariant przez `WARIANT=laptop/telefon/ognisko/lotnisko` |
| `trailer_yt.py`, `trailer_pion.py` | Trailery poziomy i pionowy |
| `muzyka_hop.py`, `muzyka_warianty.py` | Generowanie muzyki |
| `prezentacja_trasa.py` | Plik PREZENTACJA z podglądem profilu |
| `trasa_lib.py` | Wspólne: kolory, napisy, joey, szlak |

Dźwięk zawsze 48 kHz (96 kHz nie grał w Windows).

## Kredyty i koszty
- Higgsfield (konto odnova): zostało **77 / 1200**. Obrazy w trybie Unlimited = 0 kredytów. Wideo Seedance 2.5 Flash 4 s: 720p = 20, 480p = 8.
- Gemini: filmy za darmo w dziennym limicie (ok. 2–3 dziennie, odnawia się nad ranem).
