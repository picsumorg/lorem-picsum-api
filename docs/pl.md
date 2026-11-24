[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · **Polski** · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/pl) to bezpłatny generator losowych obrazów i API zdjęć zastępczych. Udostępnia **100 000 zdjęć CC0** na licencji [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) w **33 kategoriach**. Adresy obrazów, własne wymiary, JPEG i WebP, skala szarości, rozmycie oraz punkty końcowe metadanych JSON nie wymagają konta ani klucza API. Możesz skopiować link do obrazu albo pobrać plik JPEG lub WebP.

Lorem Picsum (`picsum.org`) to niezależna usługa inspirowana otwartoźródłowym projektem Picsum Photos. Nie jest powiązana z `picsum.photos`. Ma własny katalog i własne identyfikatory zdjęć. Ścieżki z tamtego projektu, w tym ścieżka skali szarości w postaci `/g/{width}/{height}`, nie wchodzą w skład tego API.

Adres bazowy API to `https://picsum.org`. Nie dodawaj prefiksu wersji językowej witryny przed ścieżką API. `https://picsum.org/de/800/600` to ścieżka witryny, a nie adres obrazu. Prefiksy wersji językowych (`/de`, `/ja`, `/zh-tw` i pozostałe) należą do stron takich jak strona główna, przewodnik konfiguracji MCP i regulamin.

## Spis treści

- [Przegląd](#overview)
- [Szybki start](#quick-start)
- [Adresy obrazów](#image-urls)
- [Metadane JSON](#json)
- [Kategorie](#categories)
- [Nagłówki, pamięć podręczna i CORS](#headers)
- [Błędy i limity zapytań](#errors)
- [Przykłady kodu](#code)
- [Licencja i użytek komercyjny](#license)
- [Serwer MCP](#mcp)

<a id="overview"></a>

## Przegląd

Poproś o link do obrazu, gdy układ potrzebuje zdjęcia. Poproś o JSON, gdy potrzebujesz autora, opisu, kategorii, tagów, oryginalnych wymiarów, strony źródła albo licencji.

Losowy adres może wybrać inne zdjęcie przy każdym żądaniu. Seed albo identyfikator zdjęcia zachowuje to samo zdjęcie źródłowe. Szerokość i wysokość to liczby całkowite od **1 do 2000** pikseli. Każdy własny rozmiar z tego zakresu jest bezpłatny, podobnie jak skala szarości i rozmycie. Sześć rozmiarów na stronie głównej to wygodne gotowe rozmiary, a nie górny limit.

<a id="quick-start"></a>

## Szybki start

Ten losowy obraz 800×600 przekierowuje do konkretnego zdjęcia. Przekierowanie nie trafia do pamięci podręcznej, a odpowiedź podaje wybrany identyfikator w `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Użyj adresu ze stałym identyfikatorem, gdy zdjęcie ma się nie zmieniać:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Użyj seedu, gdy obraz ma być powtarzalny. Ten sam seed wskazuje to samo zdjęcie źródłowe w każdym rozmiarze. Seed `studio` odpowiada identyfikatorowi `1000561303`. Ten przykład żąda WebP, skali szarości i rozmycia:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Adresy obrazów

<a id="dimensions"></a>

### Wymiary i kadrowanie

`width` i `height` to segmenty ścieżki. Każdy jest liczbą całkowitą od 1 do 2000 włącznie. Usługa skaluje zdjęcie i przycina je od środka, aby wypełnić żądany prostokąt. Obraz nie jest rozciągany.

<a id="formats"></a>

### Formaty

| Rozszerzenie | Co otrzymujesz |
| --- | --- |
| *(brak)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` i `.avif` nie są przyjmowane. Odpowiedź ma status HTTP 400 i zawiera obiekt błędu obrazu podany niżej. `.jpeg` nie jest zamiennikiem `.jpg`.

<a id="random-rectangle"></a>

### Losowy prostokąt

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Odpowiedź to `302 Found`. `Location` wskazuje `/id/{id}/{width}/{height}.{ext}`. Gdy brakuje rozszerzenia, `{ext}` ma wartość `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` to identyfikator wybranego zdjęcia

`GET https://picsum.org/800/600` to standardowy gotowy rozmiar w tej postaci.

<a id="random-square"></a>

### Losowy kwadrat

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` to żądanie JPEG 640×640. Odpowiedź ma kod `302` i prowadzi do `/id/{id}/{width}/{width}.jpg`, z nagłówkami `Cache-Control: no-store` i `Picsum-ID`.

<a id="seeded"></a>

### Obraz z seedem

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Odpowiedź ma kod `302` i prowadzi do `/id/{id}/{width}/{height}.{ext}`. W kwadratowym adresie z seedem szerokość i wysokość są tą samą liczbą. Brak rozszerzenia oznacza `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` to wybrane zdjęcie
- Jeden seed zawsze wybiera to samo zdjęcie źródłowe, także po zmianie rozmiaru. `studio` wybiera `1000561303`.
- Seed działa też jako hasło wyszukiwania. `GET https://picsum.org/seed/cat/800/600` wybiera zdjęcie kota.
- Jeśli seed nie pasuje do żadnego tagu, usługa wybiera jedno stałe zdjęcie z kolekcji. Ten sam nieznany seed nadal prowadzi do tego samego zdjęcia.

<a id="pinned"></a>

### Obraz o stałym identyfikatorze

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Odpowiedź to `200 OK` i bajty obrazu, `image/jpeg` albo `image/webp`. Ścieżka kwadratowa używa jednego wymiaru dla obu boków. Brak rozszerzenia oznacza JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` powtarza `{id}`

Autora i stronę źródła dla danego identyfikatora odczytasz, wywołując [`/id/{id}/info`](#info-id). Udokumentowany kod `404` dla nieznanego identyfikatora dotyczy tej ścieżki metadanych, a nie ścieżki obrazu.

<a id="query"></a>

### Parametry zapytania

| Parametr | Gdzie obowiązuje | Reguła |
| --- | --- | --- |
| `tag` | Obrazy losowe, obrazy z seedem i `GET /v2/list` | Ciąg tematu. Zawęża pulę. Przykład: `?tag=forest`. |
| `category` | Obrazy losowe, obrazy z seedem i `GET /v2/list` | Jeden z 33 identyfikatorów kategorii. Przykład: `?category=woodlands`. |
| `grayscale` | Adresy obrazów | Flaga w zapisie `?grayscale`. Skala szarości jest wbudowana w plik obrazu. Ścieżka `/g/{width}/{height}` nie istnieje. |
| `blur` | Adresy obrazów | Liczba całkowita od 1 do 10. Samo `?blur` jest przyjmowane i oznacza `blur=5`. `blur=0` oraz `blur=11` zwracają HTTP 400. |

`tag` i `category` działają przy wyborze zdjęcia. Nie są dopisywane do `Location` w przekierowaniu.

Skala szarości i rozmycie są przenoszone razem z obrazem. To żądanie z seedem:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

zwraca `302` i te nagłówki:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Flaga `grayscale` jest zapisywana jako `grayscale=1` w adresie o stałym identyfikatorze. Wartość `blur=4` pozostaje. Sam plik jest w skali szarości i rozmyty. To nie jest filtr CSS.

<a id="presets"></a>

### Gotowe rozmiary ze strony głównej

Na stronie głównej widać te sześć gotowych rozmiarów. Każdy inny rozmiar od 1 do 2000 też jest bezpłatny.

| Nazwa | Piksele | URL |
| --- | --- | --- |
| Standardowy | 800×600 | `https://picsum.org/800/600` |
| Kwadrat | 640×640 | `https://picsum.org/640` |
| Poziomy | 1200×800 | `https://picsum.org/1200/800` |
| Pionowy | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Pierwsze żądanie nowego rozmiaru albo nowej kombinacji skali szarości lub rozmycia może potrwać nieco dłużej. Później plik o stałym identyfikatorze jest trzymany w pamięci podręcznej.

<a id="json"></a>

## Metadane JSON

Punkt końcowy `/list` w wersji v1 nie istnieje. Kolekcję udostępnia `/v2/list`.

`/v2/list` zwraca tablicę JSON. `/id/{id}/info` oraz `/seed/{seed}/info` zwracają jeden obiekt JSON. Wszystkie trzy wysyłają `Cache-Control: public, max-age=300` i `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Lista zdjęć

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Parametr | Reguła |
| --- | --- |
| `page` | Liczba całkowita większa lub równa 1. Domyślnie `1`. |
| `limit` | Liczba całkowita od 1 do 100. Domyślnie `30`. |
| `tag` | Opcjonalny ciąg tematu. |
| `category` | Opcjonalny identyfikator kategorii. |

Nagłówki odpowiedzi:

- `Link`, z `rel="next"`, a gdy istnieje poprzednia strona, także z `rel="prev"`.
- `Picsum-Total` podaje liczbę pasujących zdjęć. Bez `tag` i bez `category` wartość wynosi `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Żądanie z `page=1` i `limit=1` zwróciło ten nagłówek `Link` oraz `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Treść to tablica obiektów opisanych w sekcji [Pola obiektu](#fields). Każdy element to jedno zdjęcie. Kolejność może się zmienić. Nie zakładaj, że pierwszy wiersz to zawsze to samo zdjęcie.

<a id="info-id"></a>

### Jedno zdjęcie po identyfikatorze

```http
GET https://picsum.org/id/{id}/info
```

Znany identyfikator zwraca `200` i jeden obiekt JSON. Nieznany identyfikator zwraca `404` i dokładnie tę treść:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Jedno zdjęcie po seedzie

```http
GET https://picsum.org/seed/{seed}/info
```

Odpowiedź to `200`, jeden obiekt JSON i nagłówek `Picsum-ID`. Seed, który nie pasuje do żadnego tagu, nie zwraca błędu. Zwraca to samo stałe zdjęcie zapasowe co adres obrazu z seedem.

<a id="fields"></a>

### Pola obiektu

| Pole | Znaczenie |
| --- | --- |
| `id` | Identyfikator zdjęcia, jako ciąg znaków. |
| `author` | Nazwa twórcy. Ciąg może być pusty. |
| `width` | Oryginalna szerokość w pikselach. To nie jest szerokość obrazu, który chcesz otrzymać. |
| `height` | Oryginalna wysokość w pikselach. To nie jest wysokość obrazu, który chcesz otrzymać. |
| `description` | Krótki opis zdjęcia. |
| `category` | Jeden identyfikator kategorii. |
| `tags` | Tablica ciągów tematu. |
| `url` | Strona pierwotnego źródła. |
| `license` | Dokładny ciąg `"CC0 1.0"`. |
| `license_url` | Dokładny ciąg `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | Adres JPEG tego zdjęcia w rozmiarze 800×600. |

Adres WebP albo obrazu w skali szarości zbudujesz z `id`. Pole `download_url` to zawsze JPEG 800×600.

<a id="examples"></a>

### Przykłady

`GET https://picsum.org/id/179363399/info` zwraca:

```json
{
  "id": "179363399",
  "author": "Syony",
  "width": 3840,
  "height": 2160,
  "description": "Colorful mountain slopes in Landmannalaugar",
  "category": "landscapes",
  "tags": ["mountains", "highlands", "colorful", "iceland"],
  "url": "https://commons.wikimedia.org/wiki/File:Colorful_mountain_slope_in_Landmannalaugar.jpg",
  "license": "CC0 1.0",
  "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
  "download_url": "https://picsum.org/id/179363399/800/600.jpg"
}
```

Zdjęcie ma 3840×2160, autorem jest Syony, kategoria to `landscapes`, a opis brzmi „Colorful mountain slopes in Landmannalaugar”. Tagi to `mountains`, `highlands`, `colorful` i `iceland`.

`GET https://picsum.org/seed/studio/info` zwraca:

```json
{
  "id": "1000561303",
  "author": "",
  "width": 2400,
  "height": 1800,
  "description": "Meal · cuisine",
  "category": "food",
  "tags": ["meal", "cuisine", "dish", "food", "salad", "bread", "burger", "sandwich", "white", "seed", "isolated", "produce", "macro", "studio", "fresh"],
  "url": "https://pxhere.com/en/photo/561303",
  "license": "CC0 1.0",
  "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
  "download_url": "https://picsum.org/id/1000561303/800/600.jpg"
}
```

Nagłówek odpowiedzi `Picsum-ID` ma wartość `1000561303`. Oryginalny kadr ma 2400×1800, pole `author` jest puste, a `category` to `food`.

<a id="categories"></a>

## Kategorie

W parametrze `category` podaj jeden z tych identyfikatorów. Publiczny punkt końcowy HTTP `/categories` nie istnieje. Narzędzie MCP `list_categories` zwraca te same identyfikatory, każdy z angielską nazwą wyświetlaną i grupą. Nazwy w poniższych tabelach są tłumaczeniami dla czytelników. W żądaniu wysyłaj identyfikator, a nie nazwę wyświetlaną.

### Przyroda i krajobrazy

| ID | Nazwa |
| --- | --- |
| `coasts` | Wybrzeża i oceany |
| `deserts` | Pustynie i wydmy |
| `freshwater` | Jeziora i wodospady |
| `gardens` | Ogrody |
| `landscapes` | Krajobrazy |
| `macro` | Makrofotografia |
| `mountains` | Góry |
| `plants` | Rośliny i kwiaty |
| `skies` | Niebo i pogoda |
| `snow` | Śnieg i lód |
| `woodlands` | Lasy |

### Zwierzęta

| ID | Nazwa |
| --- | --- |
| `animals` | Inne zwierzęta |
| `birds` | Ptaki |
| `insects` | Owady |
| `marine` | Życie morskie |
| `pets` | Zwierzęta domowe |

### Miejsca i podróże

| ID | Nazwa |
| --- | --- |
| `aerial` | Zdjęcia lotnicze |
| `architecture` | Architektura |
| `city` | Miasta i ulice |
| `interiors` | Wnętrza |
| `landmarks` | Zabytki i atrakcje |
| `night` | Fotografia nocna |
| `transport` | Transport |

### Przedmioty i zajęcia

| ID | Nazwa |
| --- | --- |
| `agriculture` | Rolnictwo |
| `food` | Jedzenie i napoje |
| `industry` | Przemysł |
| `music` | Muzyka |
| `objects` | Przedmioty |
| `sculpture` | Rzeźba |
| `sports` | Sport |
| `technology` | Technologia |
| `textures` | Tekstury |
| `workspaces` | Miejsca pracy |

<a id="headers"></a>

## Nagłówki, pamięć podręczna i CORS

Odpowiedzi z obrazem oraz JSON wysyłają:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` obejmuje `Picsum-ID`, `Picsum-Total` i `Link`, dzięki czemu `fetch` wykonany w innym źródle może odczytać te trzy nagłówki.

| Odpowiedź | `Cache-Control` |
| --- | --- |
| Losowe przekierowanie, `/{width}` lub `/{width}/{height}` | `no-store` |
| Przekierowanie z seedem, `/seed/{seed}/...` | `public, max-age=3600` |
| Obraz o stałym identyfikatorze, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Losowe przekierowanie ma `no-store`, więc następne żądanie może wybrać inne zdjęcie. Adres `/id/...` w `Location` to plik, który można trzymać w pamięci podręcznej. Pierwsze żądanie nowego rozmiaru lub efektu może potrwać nieco dłużej, zanim ten plik zostanie zapisany.

Błędy JSON 400 i 404 opisane poniżej też są wysyłane z `Cache-Control: no-store` i `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Błędy i limity zapytań

Treść błędu jest w JSON. Te ciągi `error` porównuj co do znaku.

Nieprawidłowe wymiary obrazu, nieobsługiwane rozszerzenie albo wartość rozmycia spoza zakresu 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Nieprawidłowe `page` lub `limit` w `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Nieznany identyfikator zdjęcia w `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 oznacza, że zadziałał limit zapytań. Zastosuj się do nagłówka odpowiedzi `Retry-After`. Nie generuj zautomatyzowanego ruchu, który pogarsza działanie usługi, i nie obchodź limitów zapytań.

<a id="code"></a>

## Przykłady kodu

<a id="html"></a>

### HTML

Ustaw `width`, `height` i `alt`. Tekst `alt` powinien opisywać zdjęcie. Poniższy opis to pole `description` zdjęcia `179363399`.

```html
<img
  src="https://picsum.org/id/179363399/800/600.jpg"
  width="800"
  height="600"
  alt="Colorful mountain slopes in Landmannalaugar"
>
```

<a id="markdown"></a>

### Markdown

```markdown
![Colorful mountain slopes in Landmannalaugar](https://picsum.org/id/179363399/800/600.jpg)
```

<a id="curl"></a>

### cURL

Pierwsze polecenie wypisuje nagłówki przekierowania z seedem, w tym `Location` i `Picsum-ID`, i nie zapisuje obrazu. Drugie wypisuje jeden obiekt zdjęcia. Trzecie wypisuje nagłówki listy i tablicę JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` może wywołać punkty końcowe JSON z przeglądarki, ponieważ `Access-Control-Allow-Origin` ma wartość `*`. `Picsum-Total` jest udostępniony, więc `headers.get` może go odczytać.

```javascript
const infoResponse = await fetch("https://picsum.org/id/179363399/info");
if (!infoResponse.ok) {
  throw new Error(await infoResponse.text());
}
const info = await infoResponse.json();

const listResponse = await fetch(
  "https://picsum.org/v2/list?page=1&limit=10&category=landscapes",
);
const photos = await listResponse.json();
const total = listResponse.headers.get("Picsum-Total");

const imageUrl = `https://picsum.org/id/${info.id}/800/600.webp`;
```

<a id="python"></a>

### Python

Ten przykład korzysta z biblioteki `requests`.

```python
import requests

info = requests.get("https://picsum.org/id/179363399/info", timeout=30)
info.raise_for_status()
photo = info.json()

listing = requests.get(
    "https://picsum.org/v2/list",
    params={"page": 1, "limit": 10, "category": "landscapes"},
    timeout=30,
)
listing.raise_for_status()
photos = listing.json()
total = listing.headers.get("Picsum-Total")

image_url = f"https://picsum.org/id/{photo['id']}/800/600.webp"
```

<a id="license"></a>

## Licencja i użytek komercyjny

Zdjęcia są na licencji [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Korzystanie prywatne i komercyjne jest bezpłatne. Podanie autora jest dobrowolne. Gdy chcesz podać autora zdjęcia, pole `author` zawiera twórcę, a `url` stronę źródła. Oba pola są w obiekcie JSON.

Przy wrażliwym użyciu odpowiadasz za rozpoznawalne osoby, znaki towarowe i dane pierwotnego źródła. Przed takim użyciem sprawdź `url`.

Nie odsprzedawaj tej usługi ani nie rozpowszechniaj jej jako własnego API obrazów.

Pytania: [hello@picsum.org](mailto:hello@picsum.org).

Regulamin: [Regulamin korzystania z usługi](https://picsum.org/pl/terms).

<a id="mcp"></a>

## Serwer MCP

Zdalny serwer MCP obsługuje zapytania o zdjęcia tylko do odczytu dla klientów obsługujących protokół Model Context Protocol. Nie zastępuje opisanych wyżej adresów obrazów i nie generuje obrazów z opisu tekstowego. Adresy obrazów pozostają pod `https://picsum.org/{...}`. Punkt końcowy MCP jest osobny.

| | |
| --- | --- |
| Punkt końcowy | `https://picsum.org/mcp` |
| Transport | Streamable HTTP |
| Autoryzacja | OAuth 2.1 z PKCE |
| Zakres | `photos:read` |
| Przewodnik konfiguracji | [Połącz asystenta AI z Picsum](https://picsum.org/pl/connect) |
| Konfiguracja klienta | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Narzędzia są tylko do odczytu:

| Narzędzie | Działanie |
| --- | --- |
| `search_photos` | Wyszukuje według `tag`, według `category` albo według obu. |
| `get_photo` | Metadane jednego identyfikatora zdjęcia. |
| `list_categories` | Wszystkie identyfikatory kategorii, z angielską nazwą wyświetlaną i grupą. |
| `build_image_url` | Adres obrazu oraz fragment HTML `<img>` dla wybranego rozmiaru, formatu, skali szarości i rozmycia. |

Logowanie i konfiguracja klienta są opisane w przewodniku [Połącz asystenta AI z Picsum](https://picsum.org/pl/connect). W innych językach ta sama ścieżka `/connect` jest pod prefiksem wersji językowej. Nie wysyłaj żądań obrazów przez ten prefiks. Przykłady konfiguracji są w [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
