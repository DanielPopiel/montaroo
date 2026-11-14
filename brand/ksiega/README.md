# montaroo

**Hop from footage to film.** Montaroo to prywatny montażysta na Windows: z godzin nagrań z wyjazdu robi film z historią, zmontowany w rytm muzyki, na twoim komputerze, bez chmury.

Ta księga jest źródłem prawdy dla strony montaroo.com, programu, reklam i postów. Zaczynaj od niej; szczegóły logo są w sekcji **Logo**, a głos marki i hasła w sekcji **Ton i hasła**.

## Pozycjonowanie w jednym zdaniu

Dla ludzi, którzy wracają z podróży z setkami nagrań i nigdy ich nie oglądają: Montaroo zamienia je w film, do którego naprawdę się wraca, bez osi czasu i bez wysyłania rodzinnych nagrań do chmury.

**Cztery wyróżniki** (zawsze w tej kolejności ważności):
1. **Opowieść, nie tylko cięcia do beatu** – zapowiedź, rozdziały po dniach, kulminacja, klamra.
2. **Muzyka jako szkielet** – cięcia na taktach i frazach, przejścia według energii piosenki.
3. **Prywatnie i offline** – nagrania nie opuszczają komputera („never leaves the pouch”).
4. **Poprawki słowami** – „więcej drona nad Monument Valley” zamiast przesuwania klipów.

## Osobowość

Ciepła, pewna siebie, rzemieślnicza. Jak zaprzyjaźniony montażysta, który zna się na rzeczy i nie robi z tego magii. **Nie** „AI magic”, **nie** technologiczny chłód, **nie** dziecinna maskotka.

| Jesteśmy | Nie jesteśmy |
|---|---|
| konkretni („12 minut, 9 rozdziałów, 214 ujęć”) | napompowani („rewolucyjna AI”) |
| ciepli, z lekkim humorem kangura | infantylni, z emoji w każdym zdaniu |
| spokojnie pewni („gotowe w tle, zanim wrócisz z kawą”) | krzykliwi („NAJLEPSZY EDYTOR!!!”) |
| prywatni z zasady | „bezpieczni” tylko w przypisie |

## Kolory: „zachód słońca w buszu”

| Nazwa | HEX | Token | Rola |
|---|---|---|---|
| Eukaliptus noc | `#10251F` | `brand-noc` | tekst, napis w logo, ciemne tła |
| Ochra | `#E2642A` | `brand-ochra` | kolor marki: torba, główny przycisk |
| Złota godzina | `#F2B544` | `brand-zlota-godzina` | drugi akcent, wyróżnienia na ciemnym |
| Eukaliptus | `#3E7C68` | `brand-eukaliptus` | kolor pomocniczy, duże powierzchnie |
| Piasek | `#F4E9D6` | `brand-piasek` | jasne tło |

**Proporcje na stronie i w reklamie:** ok. 60% Piasek lub Noc (tło), 25% Noc/Piasek (tekst), 10% Ochra, 5% Złota godzina i Eukaliptus. Ochra ma być rzadka, żeby była znakiem.

**Zasady kontrastu (sprawdzone):**
- Drobny tekst: `tekst` na `tlo` (13,4:1) albo `brand-piasek` na `brand-noc`. Opisy: `tekst-cichy` (min. 6,3:1).
- Na ochrze piszemy kolorem **Noc** (4,7:1). Biały na ochrze tylko w napisach od 24 px.
- Eukaliptus jako tekst na Piasku tylko od 24 px. Drobne linki: token `link`.
- Etykiety w kolorze marki na jasnym: `akcent-tekst` (przyciemniona ochra 4,5:1), nie czysta ochra.
- Złota godzina nigdy jako tekst na jasnym tle (1,5:1).

## Typografia

- **Gabarito 800** – logo i nagłówki. Światło liter −0,02 do −0,035 em (logo −0,04 em). Zawsze małe litery w nazwie: `montaroo`.
- **Inter 400/600** – tekst, interfejs programu, przyciski, napisy w filmach.
- Nie używamy kroju Fraunces ani innych szeryfowych „premium” w materiałach podstawowych.
- Nagłówki krótkie, max 2 linie. Kropka na końcu hasła to część stylu („Hop from footage to film.”).

## Kształty i rytm

- **Zaokrąglenia** z tokenów: 8 / 14 / 22 / pigułka. Karty `radius-lg`, przyciski `radius-md`.
- **Motyw torby:** półkole i pas szwu (przerywana linia z pigułek) to drugi rozpoznawalny element po znaku. Używaj go jako dzielnika sekcji, podkreślenia albo ramki na wideo – oszczędnie, raz na ekran.
- **Rytm cięć:** w każdym materiale wideo cięcia na beat muzyki. Animacja znaku: joey wyskakuje z torby na pierwszym uderzeniu.
- Bez gradientów, cieni „glass”, neonów i fioletowo-niebieskich przejść. Płaskie kolory, prawdziwe kadry z podróży.

## Zdjęcia i wideo

Prawdziwe rodzinne ujęcia z wyjazdów (dron nad kanionem, dzieci na kempingu, okno samochodu), nie stocki z uśmiechniętymi modelami. Ciepłe światło złotej godziny pasuje do palety. Ludzie i miejsca w kadrze, interfejs programu jako dodatek.

## Ikonografia

Prosta, pełna (fill), zaokrąglone narożniki jak w znaku, grubość optyczna zbliżona do szwu. Ikona programu: kwadrat z zaokrągleniem 22%, tło Noc, znak w kolorach Piasek + Ochra.

## Pliki

Logo, znaki i ikony są w grupie zasobów **Logo** (SVG). Pełny eksport (SVG, PNG, favicon, `montaroo.ico`) leży w repozytorium strony: `GitHub/montaroo/brand/logo/`.
