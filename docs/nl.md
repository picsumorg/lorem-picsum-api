[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · **Nederlands** · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/nl) is een gratis API voor willekeurige afbeeldingen. De dienst levert **100.000 CC0-foto’s** onder [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) in **33 categorieën**. Voor afbeeldingslinks, eigen formaten, JPEG en WebP, grijstinten, vervaging en de JSON-eindpunten voor metagegevens heb je geen account of API-sleutel nodig.

Lorem Picsum (`picsum.org`) is een onafhankelijke dienst, geïnspireerd op het opensourceproject Picsum Photos. De dienst is niet verbonden met `picsum.photos` en heeft een eigen catalogus en eigen foto-ID’s. Paden van dat andere project, waaronder een pad voor grijstinten zoals `/g/{width}/{height}`, horen niet bij deze API.

De basis-URL van de API is `https://picsum.org`. Zet geen locale van de website vóór een API-pad. `https://picsum.org/de/800/600` is een route van de website, geen afbeeldingslink. Localeprefixen (`/de`, `/ja`, `/zh-tw` en de rest) horen bij pagina’s zoals de startpagina, de handleiding voor MCP en de gebruiksvoorwaarden.

## Inhoud

- [Overzicht](#overview)
- [Snel aan de slag](#quick-start)
- [Afbeeldings-URL’s](#image-urls)
- [JSON-metagegevens](#json)
- [Categorieën](#categories)
- [Headers, cache en CORS](#headers)
- [Fouten en aanvraaglimieten](#errors)
- [Codevoorbeelden](#code)
- [Licentie en commercieel gebruik](#license)
- [MCP-server](#mcp)

<a id="overview"></a>

## Overzicht

Vraag een afbeeldingslink op wanneer een lay-out een foto nodig heeft. Vraag JSON op wanneer je de maker, de beschrijving, de categorie, de trefwoorden, de oorspronkelijke afmetingen, de bronpagina of de licentie nodig hebt.

Een willekeurige URL kan bij elk verzoek een andere foto kiezen. Met een seed of een foto-ID blijft de bronfoto dezelfde. Breedte en hoogte zijn gehele getallen van **1 tot 2000** pixels. Elk eigen formaat in dat bereik is gratis, net als grijstinten en vervaging. De zes formaten op de startpagina zijn kant-en-klare standaardformaten. Ze leggen geen bovengrens op.

<a id="quick-start"></a>

## Snel aan de slag

Deze willekeurige afbeelding van 800×600 verwijst door naar een specifieke foto. De omleiding wordt niet in de cache opgeslagen, en het antwoord geeft het gekozen ID mee in `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Gebruik een vastgezette URL wanneer het beeld moet blijven staan:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Gebruik een seed wanneer het beeld herhaalbaar moet zijn. Dezelfde seed wijst bij elk formaat naar dezelfde bronfoto. De seed `studio` wijst naar `1000561303`. Dit voorbeeld vraagt WebP, grijstinten en vervaging:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Afbeeldings-URL’s

<a id="dimensions"></a>

### Afmetingen en bijsnijden

`width` en `height` zijn segmenten van het pad. Elk is een geheel getal van 1 tot en met 2000. De dienst schaalt de foto en snijdt die vanuit het midden bij, zodat de gevraagde rechthoek gevuld is. De foto wordt niet uitgerekt.

<a id="formats"></a>

### Formaten

| Extensie | Wat je krijgt |
| --- | --- |
| *(geen)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` en `.avif` worden niet geaccepteerd. Het antwoord is HTTP 400 en het foutobject voor afbeeldingen hieronder. `.jpeg` is geen synoniem van `.jpg`.

<a id="random-rectangle"></a>

### Willekeurige rechthoek

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Het antwoord is `302 Found`. `Location` is `/id/{id}/{width}/{height}.{ext}`. Ontbreekt de extensie, dan is `{ext}` `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` is de gekozen foto

`GET https://picsum.org/800/600` is het standaardformaat in deze vorm.

<a id="random-square"></a>

### Willekeurig vierkant

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` vraagt een JPEG van 640×640. Het antwoord is `302` naar `/id/{id}/{width}/{width}.jpg`, met `Cache-Control: no-store` en een header `Picsum-ID`.

<a id="seeded"></a>

### Foto via seed

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Het antwoord is `302` naar `/id/{id}/{width}/{height}.{ext}`. Een vierkante seed-URL gebruikt hetzelfde getal voor breedte en hoogte. Een weggelaten extensie is `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` is de gekozen foto
- Eén seed kiest altijd dezelfde bronfoto, ook wanneer het formaat verandert. `studio` kiest `1000561303`.
- De seed is ook een trefwoord. `GET https://picsum.org/seed/cat/800/600` kiest een foto van een kat.
- Past de seed bij geen enkele tag, dan valt de dienst terug op één vaste foto uit de collectie. Dezelfde onbekende seed blijft die foto teruggeven.

<a id="pinned"></a>

### Vastgezette foto

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Het antwoord is `200 OK` en bevat de bytes van de afbeelding, `image/jpeg` of `image/webp`. Een vierkant pad gebruikt één afmeting voor beide zijden. Een weggelaten extensie is JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` herhaalt `{id}`

Voor de maker en de bronpagina bij een ID roep je [`/id/{id}/info`](#info-id) aan. Die route voor metagegevens, en niet de route voor de afbeelding, is de gedocumenteerde `404` bij een onbekend ID.

<a id="query"></a>

### Queryparameters

| Parameter | Waar die geldt | Regel |
| --- | --- | --- |
| `tag` | Willekeurige afbeeldingen, afbeeldingen met seed en `GET /v2/list` | Trefwoord. Het beperkt de verzameling. Voorbeeld: `?tag=forest`. |
| `category` | Willekeurige afbeeldingen, afbeeldingen met seed en `GET /v2/list` | Een van de 33 categorie-ID’s. Voorbeeld: `?category=woodlands`. |
| `grayscale` | Afbeeldings-URL’s | Zonder waarde, als `?grayscale`. De grijstinten zitten in het beeldbestand. Een pad `/g/{width}/{height}` bestaat niet. |
| `blur` | Afbeeldings-URL’s | Geheel getal van 1 tot 10. Een `?blur` zonder waarde is geldig en betekent `blur=5`. `blur=0` en `blur=11` geven HTTP 400. |

`tag` en `category` worden gebruikt terwijl de foto wordt gekozen. Ze worden niet op de `Location` van de omleiding gezet.

Grijstinten en vervaging gaan mee naar de vastgezette URL. Dit verzoek met seed:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

geeft `302` terug, met:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Op die vastgezette URL staat `grayscale` als `grayscale=1`. `blur=4` blijft staan. Het bestand zelf is in grijstinten en vervaagd. Dit is geen CSS-filter.

<a id="presets"></a>

### Standaardformaten op de startpagina

Dit zijn de zes standaardformaten op de startpagina. Elk ander formaat van 1 tot 2000 is ook gratis.

| Standaardformaat | Pixels | URL |
| --- | --- | --- |
| Standaard | 800×600 | `https://picsum.org/800/600` |
| Vierkant | 640×640 | `https://picsum.org/640` |
| Liggend | 1200×800 | `https://picsum.org/1200/800` |
| Staand | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Het eerste verzoek voor een nieuw formaat, of voor een nieuwe combinatie van grijstinten of vervaging, kan iets langer duren. Daarna staat het vastgezette bestand in de cache.

<a id="json"></a>

## JSON-metagegevens

Een v1-eindpunt `/list` bestaat niet. De collectie staat op `/v2/list`.

`/v2/list` geeft een lijst in JSON terug. `/id/{id}/info` en `/seed/{seed}/info` geven één JSON-object terug. Alle drie sturen `Cache-Control: public, max-age=300` en `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Foto’s opvragen

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Parameter | Regel |
| --- | --- |
| `page` | Geheel getal groter dan of gelijk aan 1. Standaard `1`. |
| `limit` | Geheel getal van 1 tot 100. Standaard `30`. |
| `tag` | Optioneel trefwoord. |
| `category` | Optioneel categorie-ID. |

Antwoordheaders:

- `Link`, met `rel="next"` en, wanneer er een vorige pagina is, `rel="prev"`.
- `Picsum-Total`, het aantal foto’s dat voldoet. Zonder `tag` en zonder `category` is de waarde `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Een verzoek voor pagina 1 met `limit=1` gaf deze header `Link` en `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

De inhoud is een lijst. Elk item is het object uit [Objectvelden](#fields), dus één foto. De volgorde kan veranderen. Beschouw de eerste rij niet als een vaste foto.

<a id="info-id"></a>

### Eén foto op ID

```http
GET https://picsum.org/id/{id}/info
```

Een bekend ID geeft `200` en één JSON-object. Een onbekend ID geeft `404` en exact deze inhoud:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Eén foto op seed

```http
GET https://picsum.org/seed/{seed}/info
```

Het antwoord is `200` en één JSON-object, plus een header `Picsum-ID`. Een seed die bij geen tag past, geeft geen fout. Je krijgt dezelfde vaste foto als bij de afbeeldingslink met die seed.

<a id="fields"></a>

### Objectvelden

| Veld | Betekenis |
| --- | --- |
| `id` | Foto-ID, als tekenreeks. |
| `author` | Naam van de maker. De tekenreeks kan leeg zijn. |
| `width` | Oorspronkelijke breedte in pixels. Dit is niet de breedte die je wilt laten weergeven. |
| `height` | Oorspronkelijke hoogte in pixels. Dit is niet de hoogte die je wilt laten weergeven. |
| `description` | Korte beschrijving van de foto. |
| `category` | Eén categorie-ID. |
| `tags` | Lijst met trefwoorden. |
| `url` | Pagina van de oorspronkelijke bron. |
| `license` | De exacte tekenreeks `"CC0 1.0"`. |
| `license_url` | De exacte tekenreeks `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | JPEG-URL van deze foto op 800×600. |

Bouw een WebP- of grijstinten-URL op vanuit `id`. `download_url` is altijd de JPEG van 800×600.

<a id="examples"></a>

### Voorbeelden

`GET https://picsum.org/id/179363399/info` geeft dit terug:

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

De foto meet 3840×2160, is van Syony, staat in `landscapes` en heeft als beschrijving “Colorful mountain slopes in Landmannalaugar”. De trefwoorden zijn `mountains`, `highlands`, `colorful` en `iceland`.

`GET https://picsum.org/seed/studio/info` geeft dit terug:

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

De antwoordheader `Picsum-ID` is `1000561303`. Het oorspronkelijke kader is 2400×1800, `author` is leeg en `category` is `food`.

<a id="categories"></a>

## Categorieën

Geef in `category` een van deze ID’s mee. Een openbaar HTTP-eindpunt `/categories` bestaat niet. De namen in deze tabel zijn vertalingen voor lezers. De MCP-tool `list_categories` geeft dezelfde ID’s terug, elk met de Engelse weergavenaam en een groep. Stuur het ID, niet de weergavenaam.

### Natuur en landschappen

| ID | Naam |
| --- | --- |
| `coasts` | Kusten en oceanen |
| `deserts` | Woestijnen en duinen |
| `freshwater` | Meren en watervallen |
| `gardens` | Tuinen |
| `landscapes` | Landschappen |
| `macro` | Macrofotografie |
| `mountains` | Bergen |
| `plants` | Planten en bloemen |
| `skies` | Luchten en weer |
| `snow` | Sneeuw en ijs |
| `woodlands` | Bossen |

### Dieren

| ID | Naam |
| --- | --- |
| `animals` | Overige dieren |
| `birds` | Vogels |
| `insects` | Insecten |
| `marine` | Zeeleven |
| `pets` | Huisdieren |

### Plaatsen en reizen

| ID | Naam |
| --- | --- |
| `aerial` | Luchtfotografie |
| `architecture` | Architectuur |
| `city` | Steden en straten |
| `interiors` | Interieurs |
| `landmarks` | Bezienswaardigheden |
| `night` | Nachtfotografie |
| `transport` | Vervoer |

### Voorwerpen en activiteiten

| ID | Naam |
| --- | --- |
| `agriculture` | Landbouw |
| `food` | Eten en drinken |
| `industry` | Industrie |
| `music` | Muziek |
| `objects` | Voorwerpen |
| `sculpture` | Beeldhouwwerk |
| `sports` | Sport |
| `technology` | Technologie |
| `textures` | Texturen |
| `workspaces` | Werkplekken |

<a id="headers"></a>

## Headers, cache en CORS

Antwoorden met een afbeelding of met JSON sturen:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` bevat `Picsum-ID`, `Picsum-Total` en `Link`, zodat een pagina op een andere origin die drie headers uit `fetch` kan lezen.

| Antwoord | `Cache-Control` |
| --- | --- |
| Willekeurige omleiding, `/{width}` of `/{width}/{height}` | `no-store` |
| Omleiding via seed, `/seed/{seed}/...` | `public, max-age=3600` |
| Vastgezette afbeelding, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Een willekeurige omleiding is `no-store`, zodat het volgende verzoek een andere foto kan kiezen. De URL `/id/...` in `Location` is het bestand dat in de cache mag staan. Het eerste verzoek voor een nieuw formaat of een nieuw effect kan iets langer duren, voordat dat bestand in de cache staat.

De JSON-fouten 400 en 404 hieronder worden ook verstuurd met `Cache-Control: no-store` en `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Fouten en aanvraaglimieten

Foutantwoorden zijn JSON. De waarde van `error` moet exact overeenkomen.

Ongeldige afbeeldingsafmetingen, een niet-ondersteunde extensie of een `blur`-waarde buiten 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Ongeldige `page` of `limit` op `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Een onbekend foto-ID op `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 betekent dat de aanvraaglimiet geldt. Houd je aan de antwoordheader `Retry-After`. Verstuur geen geautomatiseerd verkeer dat de dienst verslechtert, en omzeil de aanvraaglimieten niet.

<a id="code"></a>

## Codevoorbeelden

<a id="html"></a>

### HTML

Zet `width`, `height` en `alt`. `alt` hoort de foto te beschrijven. De beschrijving hieronder is de `description` van foto `179363399`.

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

De eerste opdracht toont de headers van de omleiding via seed, waaronder `Location` en `Picsum-ID`, en slaat de afbeelding niet op. De tweede toont één foto-object. De derde toont de headers van de lijst en een lijst in JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` kan de JSON-eindpunten vanuit een browser aanroepen, omdat `Access-Control-Allow-Origin` op `*` staat. `Picsum-Total` is vrijgegeven, dus `headers.get` kan de waarde lezen.

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

Dit voorbeeld gebruikt de bibliotheek `requests`.

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

## Licentie en commercieel gebruik

De foto’s vallen onder [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Privégebruik en commercieel gebruik zijn gratis. De maker vermelden is optioneel. Wil je de maker toch noemen, gebruik dan `author` voor de naam en `url` voor de bronpagina. Beide staan in het JSON-object.

Bij gevoelig gebruik ben jij verantwoordelijk voor herkenbare personen, merken en de oorspronkelijke brongegevens. Controleer dan eerst `url`.

Verkoop of verspreid deze dienst niet als je eigen afbeeldings-API.

Vragen: [hello@picsum.org](mailto:hello@picsum.org).

Gebruiksvoorwaarden: [Gebruiksvoorwaarden](https://picsum.org/nl/terms).

<a id="mcp"></a>

## MCP-server

Een gehoste MCP-server beantwoordt alleen-lezen vragen over foto’s voor clients die het Model Context Protocol spreken. De server vervangt de afbeeldingslinks hierboven niet en maakt geen beelden uit een tekstprompt. Afbeeldingslinks blijven op `https://picsum.org/{...}`. Het MCP-eindpunt is apart.

| | |
| --- | --- |
| Eindpunt | `https://picsum.org/mcp` |
| Transport | Streamable HTTP |
| Autorisatie | OAuth 2.1 met PKCE |
| Scope | `photos:read` |
| Handleiding | [Koppel je AI-assistent aan Picsum](https://picsum.org/nl/connect) |
| Clientconfiguratie | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

De tools zijn alleen-lezen:

| Tool | Wat die doet |
| --- | --- |
| `search_photos` | Zoekt op `tag`, op `category` of op beide. |
| `get_photo` | Metagegevens van één foto-ID. |
| `list_categories` | Elk categorie-ID, met de Engelse weergavenaam en de groep. |
| `build_image_url` | Een afbeeldingslink en een HTML-fragment `<img>`, voor een gekozen afmeting, bestandsformaat, grijstinten en vervaging. |

Aanmelden en de client instellen staat beschreven in [Koppel je AI-assistent aan Picsum](https://picsum.org/nl/connect). Andere talen gebruiken hetzelfde pad `/connect` onder hun localeprefix. De configuratievoorbeelden staan in [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
