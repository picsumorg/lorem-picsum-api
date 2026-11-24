[English](../README.md) · [العربية](./ar.md) · **Čeština** · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/cs) je bezplatný generátor náhodných obrázků a API pro zástupné fotografie. Poskytuje **100 000** skutečných fotografií pod licencí [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) ve **33 kategoriích**. Adresy obrázků, vlastní rozměry, JPEG a WebP, odstíny šedi, rozostření ani koncové body JSON s metadaty nevyžadují účet ani klíč API.

Lorem Picsum (`picsum.org`) je samostatná služba inspirovaná otevřeným projektem Picsum Photos. Tato služba s projektem `picsum.photos` propojena není. Má vlastní sbírku a vlastní ID fotografií. Cesty z toho druhého projektu, včetně cesty pro odstíny šedi `/g/{width}/{height}`, nejsou součástí tohoto API.

Základní adresa API je `https://picsum.org`. Před cestu API jazykovou předponu webu nedávejte. `https://picsum.org/de/800/600` je adresa stránky webu, ne adresa obrázku. Jazykové předpony (`/de`, `/ja`, `/zh-tw` a ostatní) patří stránkám, například úvodní stránce, návodu k nastavení MCP a podmínkám používání.

## Obsah

- [Přehled](#overview)
- [Rychlý začátek](#quick-start)
- [Adresy obrázků](#image-urls)
- [Metadata JSON](#json)
- [Kategorie](#categories)
- [Hlavičky, mezipaměť a CORS](#headers)
- [Chyby a limity požadavků](#errors)
- [Ukázky kódu](#code)
- [Licence a komerční použití](#license)
- [Server MCP](#mcp)

<a id="overview"></a>

## Přehled

Když rozvržení potřebuje fotografii, vyžádejte si adresu obrázku. Když potřebujete autora, popis, kategorii, štítky, původní rozměry, stránku zdroje nebo licenci, vyžádejte si JSON.

Náhodná adresa může při každém požadavku vybrat jinou fotografii. Seed nebo ID fotografie ponechává stejnou zdrojovou fotografii. Šířka a výška jsou celá čísla od **1 do 2000** pixelů. Každý vlastní rozměr v tomto rozsahu je zdarma, stejně jako odstíny šedi a rozostření. Šest rozměrů na úvodní stránce slouží jako předvolby pro pohodlí a horní mez nestanovuje.

<a id="quick-start"></a>

## Rychlý začátek

Tento náhodný obrázek 800×600 přesměruje na konkrétní fotografii. Mezipaměti toto přesměrování neukládají a odpověď nese zvolené ID v `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Když se fotografie nemá měnit, použijte pevnou adresu:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Když se má fotografie opakovat, použijte seed. Stejný seed vede na stejnou zdrojovou fotografii v každém rozměru. Seed `studio` odpovídá `1000561303`. Tato ukázka žádá WebP, odstíny šedi a rozostření:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Adresy obrázků

<a id="dimensions"></a>

### Rozměry a ořez

`width` a `height` jsou části cesty. Každá z nich je celé číslo od 1 do 2000 včetně. Služba fotografii zmenší a ořízne od středu tak, aby požadovaný obdélník byl vyplněný. Snímek se nenatahuje.

<a id="formats"></a>

### Formáty

| Přípona | Co dostanete |
| --- | --- |
| *(žádná)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` a `.avif` se nepřijímají. Odpověď je HTTP 400 a objekt chyby obrázku uvedený níže. `.jpeg` neznamená totéž co `.jpg`.

<a id="random-rectangle"></a>

### Náhodný obdélník

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Odpověď je `302 Found`. `Location` je `/id/{id}/{width}/{height}.{ext}`. Když přípona chybí, `{ext}` je `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` označuje vybranou fotografii

`GET https://picsum.org/800/600` je v tomto tvaru standardní předvolba.

<a id="random-square"></a>

### Náhodný čtverec

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` požaduje JPEG 640×640. Odpověď je `302` na `/id/{id}/{width}/{width}.jpg`, s `Cache-Control: no-store` a hlavičkou `Picsum-ID`.

<a id="seeded"></a>

### Fotografie podle seedu

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Odpověď je `302` na `/id/{id}/{width}/{height}.{ext}`. Čtvercová adresa se seedem používá stejné číslo pro šířku i výšku. Chybějící přípona znamená `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` označuje vybranou fotografii
- Jeden seed vybere vždy stejnou zdrojovou fotografii, i když se rozměr změní. `studio` vybere `1000561303`.
- Seed zároveň slouží jako hledaný výraz. `GET https://picsum.org/seed/cat/800/600` vybere fotografii kočky.
- Když seed neodpovídá žádnému štítku, služba zvolí jednu stálou fotografii ze sbírky. Stejný neznámý seed vrací stále tutéž fotografii.

<a id="pinned"></a>

### Pevná fotografie

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Odpověď je `200 OK` a bajty obrázku, `image/jpeg` nebo `image/webp`. Čtvercová cesta použije jeden rozměr pro obě strany. Chybějící přípona znamená JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` opakuje `{id}`

Pro autora a stránku zdroje k ID zavolejte [`/id/{id}/info`](#info-id). Dokumentovaná odpověď `404` pro neznámé ID patří této cestě metadat, ne cestě obrázku.

<a id="query"></a>

### Parametry dotazu

| Parametr | Kde platí | Pravidlo |
| --- | --- | --- |
| `tag` | Náhodné obrázky, obrázky se seedem a `GET /v2/list` | Řetězec námětu. Zužuje výběr. Příklad: `?tag=forest`. |
| `category` | Náhodné obrázky, obrázky se seedem a `GET /v2/list` | Jedno z 33 ID kategorií. Příklad: `?category=woodlands`. |
| `grayscale` | Adresy obrázků | Tvar příznaku `?grayscale`. Odstíny šedi se zapíšou do souboru obrázku. Cesta `/g/{width}/{height}` neexistuje. |
| `blur` | Adresy obrázků | Celé číslo od 1 do 10. Samotné `?blur` se přijímá a znamená `blur=5`. `blur=0` a `blur=11` vracejí HTTP 400. |

`tag` a `category` se použijí při výběru fotografie. Na přesměrovací `Location` se nekopírují.

Odstíny šedi a rozostření se přenášejí s obrázkem. Tento požadavek se seedem:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

Služba na něj odpoví `302` a uvede:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Příznak `grayscale` se na této pevné adrese zapíše jako `grayscale=1`. `blur=4` zůstane. Samotný soubor má odstíny šedi a je rozostřený. Nejde o filtr CSS.

<a id="presets"></a>

### Přednastavené rozměry na úvodní stránce

Úvodní stránka ukazuje těchto šest rozměrů jako předvolby. Libovolný jiný rozměr od 1 do 2000 je také zdarma.

| Předvolba | Pixely | Adresa |
| --- | --- | --- |
| Standardní | 800×600 | `https://picsum.org/800/600` |
| Čtverec | 640×640 | `https://picsum.org/640` |
| Na šířku | 1200×800 | `https://picsum.org/1200/800` |
| Na výšku | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

První požadavek na nový rozměr nebo na novou kombinaci odstínů šedi a rozostření může trvat o něco déle. Potom se pevný soubor uloží do mezipaměti.

<a id="json"></a>

## Metadata JSON

Koncový bod `/list` ve verzi v1 neexistuje. Sbírka se vypisuje na `/v2/list`.

`/v2/list` vrací pole JSON. `/id/{id}/info` a `/seed/{seed}/info` vracejí jeden objekt JSON. Všechny tři posílají `Cache-Control: public, max-age=300` a `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Seznam fotografií

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Dotaz | Pravidlo |
| --- | --- |
| `page` | Celé číslo větší nebo rovné 1. Výchozí hodnota je `1`. |
| `limit` | Celé číslo od 1 do 100. Výchozí hodnota je `30`. |
| `tag` | Volitelný řetězec námětu. |
| `category` | Volitelné ID kategorie. |

Hlavičky odpovědi:

- `Link`, s `rel="next"` a, pokud existuje předchozí stránka, také s `rel="prev"`.
- `Picsum-Total` je počet fotografií, které vyhovují. Bez `tag` a bez `category` je hodnota `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Požadavek na první stránku s `limit=1` vrátil tuto hlavičku `Link` a `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Tělo je pole objektů popsaných v části [Pole objektu](#fields). Každý prvek je jedna fotografie. Pořadí se může změnit. První položku nepovažujte za pevně danou fotografii.

<a id="info-id"></a>

### Jedna fotografie podle ID

```http
GET https://picsum.org/id/{id}/info
```

Známé ID vrací `200` a jeden objekt JSON. Neznámé ID vrací `404` a přesně toto tělo:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Jedna fotografie podle seedu

```http
GET https://picsum.org/seed/{seed}/info
```

Odpověď je `200` a jeden objekt JSON, spolu s hlavičkou `Picsum-ID`. Seed, který neodpovídá žádnému štítku, chybu nevrací. Vrací stejnou stálou náhradní fotografii jako adresa obrázku se seedem.

<a id="fields"></a>

### Pole objektu

| Pole | Význam |
| --- | --- |
| `id` | ID fotografie, jako řetězec. |
| `author` | Jméno autora. Řetězec může být prázdný. |
| `width` | Původní šířka v pixelech. Nejde o šířku, kterou jste požadovali k vykreslení. |
| `height` | Původní výška v pixelech. Nejde o výšku, kterou jste požadovali k vykreslení. |
| `description` | Krátký popis fotografie. |
| `category` | Jedno ID kategorie. |
| `tags` | Pole řetězců námětu. |
| `url` | Stránka původního zdroje. |
| `license` | Přesný řetězec `"CC0 1.0"`. |
| `license_url` | Přesný řetězec `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | Adresa JPEG této fotografie v rozměru 800×600. |

Adresu WebP nebo adresu v odstínech šedi sestavte z `id`. `download_url` je vždy JPEG 800×600.

<a id="examples"></a>

### Příklady

`GET https://picsum.org/id/179363399/info` vrací:

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

Fotografie má 3840×2160, autorem je Syony, kategorie je `landscapes` a popis zní „Colorful mountain slopes in Landmannalaugar“. Štítky jsou `mountains`, `highlands`, `colorful` a `iceland`.

`GET https://picsum.org/seed/studio/info` vrací:

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

Hlavička odpovědi `Picsum-ID` je `1000561303`. Původní snímek má rozměry 2400×1800, `author` je prázdný a `category` je `food`.

<a id="categories"></a>

## Kategorie

Do parametru `category` předejte jedno z těchto ID. Veřejný koncový bod HTTP `/categories` neexistuje. Nástroj MCP `list_categories` vrací stejná ID, každé s anglickým zobrazovaným názvem a skupinou. Názvy v této tabulce jsou překladem pro čtenáře. V požadavku posílejte ID, ne zobrazovaný název.

### Příroda a krajina

| ID | Název |
| --- | --- |
| `coasts` | Pobřeží a oceány |
| `deserts` | Pouště a duny |
| `freshwater` | Jezera a vodopády |
| `gardens` | Zahrady |
| `landscapes` | Krajina |
| `macro` | Makro |
| `mountains` | Hory |
| `plants` | Rostliny a květiny |
| `skies` | Obloha a počasí |
| `snow` | Sníh a led |
| `woodlands` | Lesy |

### Zvířata

| ID | Název |
| --- | --- |
| `animals` | Ostatní zvířata |
| `birds` | Ptáci |
| `insects` | Hmyz |
| `marine` | Mořský život |
| `pets` | Domácí mazlíčci |

### Místa a cestování

| ID | Název |
| --- | --- |
| `aerial` | Letecké snímky |
| `architecture` | Architektura |
| `city` | Města a ulice |
| `interiors` | Interiéry |
| `landmarks` | Památky |
| `night` | Noc |
| `transport` | Doprava |

### Předměty a činnosti

| ID | Název |
| --- | --- |
| `agriculture` | Zemědělství |
| `food` | Jídlo a nápoje |
| `industry` | Průmysl |
| `music` | Hudba |
| `objects` | Předměty |
| `sculpture` | Sochy |
| `sports` | Sport |
| `technology` | Technologie |
| `textures` | Textury |
| `workspaces` | Pracoviště |

<a id="headers"></a>

## Hlavičky, mezipaměť a CORS

Odpovědi s obrázkem i s JSON posílají:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` zahrnuje `Picsum-ID`, `Picsum-Total` a `Link`, takže stránka z jiného původu může tyto tři hlavičky přečíst z `fetch`.

| Odpověď | `Cache-Control` |
| --- | --- |
| Náhodné přesměrování, `/{width}` nebo `/{width}/{height}` | `no-store` |
| Přesměrování podle seedu, `/seed/{seed}/...` | `public, max-age=3600` |
| Pevný obrázek, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Náhodné přesměrování má `no-store`, takže další požadavek může vybrat jinou fotografii. Adresa `/id/...` v `Location` je soubor, který lze uložit do mezipaměti. První požadavek na nový rozměr nebo efekt může trvat o něco déle, než se tento soubor uloží do mezipaměti.

Chybové odpovědi JSON se stavy 400 a 404 popsané níže se také posílají s `Cache-Control: no-store` a `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Chyby a limity požadavků

Těla chyb jsou JSON. Řetězce `error` se musí přesně shodovat s textem níže.

Neplatné rozměry obrázku, nepodporovaná přípona nebo hodnota rozostření mimo rozsah 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Neplatné `page` nebo `limit` na `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Neznámé ID fotografie na `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 znamená, že se uplatnil limit požadavků. Řiďte se hlavičkou odpovědi `Retry-After`. Nespouštějte automatizovaný provoz, který službu zhoršuje, a limity požadavků neobcházejte.

<a id="code"></a>

## Ukázky kódu

<a id="html"></a>

### HTML

Nastavte `width`, `height` a `alt`. Atribut `alt` má fotografii popisovat. Text níže je hodnota `description` fotografie `179363399`.

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

První příkaz vypíše hlavičky přesměrování podle seedu, včetně `Location` a `Picsum-ID`, a obrázek neuloží. Druhý vypíše jeden objekt fotografie. Třetí vypíše hlavičky seznamu a pole JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` může volat koncové body JSON z prohlížeče, protože `Access-Control-Allow-Origin` je `*`. Hlavička `Picsum-Total` je vystavená, takže ji `headers.get` přečte.

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

Tato ukázka používá knihovnu `requests`.

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

## Licence a komerční použití

Fotografie jsou [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Osobní i komerční použití je zdarma. Uvedení autora je dobrovolné. Chcete-li fotografii uvést, `author` v objektu JSON je autor a `url` je stránka zdroje.

Za rozpoznatelné osoby, ochranné známky a původní záznam zdroje při citlivém použití odpovídáte vy. Před takovým použitím zkontrolujte `url`.

Tuto službu dále neprodávejte ani nešiřte jako vlastní obrazové API.

Dotazy: [hello@picsum.org](mailto:hello@picsum.org).

Podmínky používání služby: [Podmínky používání služby](https://picsum.org/cs/terms).

<a id="mcp"></a>

## Server MCP

Hostovaný server MCP slouží klientům, kteří používají Model Context Protocol, a na dotazy k fotografiím odpovídá jen pro čtení. Adresy obrázků uvedené výše nenahrazuje a z textového zadání obrázky nevytváří. Adresy obrázků zůstávají na `https://picsum.org/{...}`. Koncový bod MCP je oddělený.

| | |
| --- | --- |
| Koncový bod | `https://picsum.org/mcp` |
| Přenos | Streamable HTTP |
| Autorizace | OAuth 2.1 s PKCE |
| Rozsah | `photos:read` |
| Návod k nastavení | [Připojte svého asistenta k Picsum](https://picsum.org/cs/connect) |
| Konfigurace klienta | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Nástroje jsou jen pro čtení:

| Nástroj | Co dělá |
| --- | --- |
| `search_photos` | Vyhledá podle `tag`, podle `category` nebo podle obojího. |
| `get_photo` | Metadata k jednomu ID fotografie. |
| `list_categories` | Každé ID kategorie s anglickým zobrazovaným názvem a skupinou. |
| `build_image_url` | Adresu obrázku a úryvek HTML `<img>` pro zvolený rozměr, formát, odstíny šedi a rozostření. |

Přihlášení a nastavení klienta popisuje stránka [Připojte svého asistenta k Picsum](https://picsum.org/cs/connect). Ostatní jazyky používají stejnou cestu `/connect` pod svou jazykovou předponou. Ukázky konfigurace jsou v [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
