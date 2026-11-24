[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · **Svenska** · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/sv) är ett kostnadsfritt API för slumpmässiga bilder som du kan använda som platshållare. Varje bild är ett CC0-foto. Urvalet omfattar **100 000 fotografier** under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) i **33 kategorier**. Bildlänk, egna mått, JPEG, WebP, gråskala, oskärpa och JSON-metadata kräver varken konto eller API-nyckel.

Lorem Picsum (`picsum.org`) är en fristående tjänst. Den är inspirerad av det öppna projektet Picsum Photos och har ingen anknytning till `picsum.photos`. Tjänsten har en egen samling och egna foto-ID:n. Sökvägar från det andra projektet, inklusive gråskalesökvägen `/g/{width}/{height}`, ingår inte i det här API:et.

Basadressen för API:et är `https://picsum.org`. Sätt inte ett språkprefix från webbplatsen framför en API-sökväg. `https://picsum.org/de/800/600` är en sökväg på webbplatsen, inte en bildlänk. Språkprefix (`/de`, `/ja`, `/zh-tw` och övriga) hör till sidor som startsidan, installationsguiden för MCP och användarvillkoren.

## Innehåll

- [Översikt](#overview)
- [Snabbstart](#quick-start)
- [Bildlänkar](#image-urls)
- [JSON-metadata](#json)
- [Kategorier](#categories)
- [Huvuden, cache och CORS](#headers)
- [Fel och anropsgränser](#errors)
- [Kodexempel](#code)
- [Licens och kommersiell användning](#license)
- [MCP-server](#mcp)

<a id="overview"></a>

## Översikt

Hämta en bildlänk när layouten behöver en bild. Hämta JSON när du behöver fotograf, beskrivning, kategori, taggar, ursprungliga mått, källsida eller licens.

En slumpmässig adress kan ge ett annat foto vid varje anrop. Ett startvärde (`seed`) eller ett foto-ID behåller samma källfotografi. Bredd och höjd är heltal från **1 till 2000** pixlar. Alla egna mått i det intervallet är kostnadsfria. Det gäller även gråskala och oskärpa. De sex måtten på startsidan är färdiga förval, inte en övre gräns.

<a id="quick-start"></a>

## Snabbstart

Den här slumpmässiga bilden i 800×600 omdirigerar till ett bestämt foto. Omdirigeringen sparas inte i cache, och svaret skickar det valda ID:t i `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Använd en låst bildlänk när bilden ska ligga kvar:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Använd ett startvärde när bilden ska gå att upprepa. Samma startvärde ger samma källfoto i alla mått. Startvärdet `studio` pekar på `1000561303`. Exemplet ber om WebP, gråskala och oskärpa:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Bildlänkar

<a id="dimensions"></a>

### Mått och beskärning

`width` och `height` är delar av sökvägen. Vart och ett är ett heltal från 1 till och med 2000. Fotot skalas och beskärs från mitten så att den begärda rektangeln fylls. Bilden sträcks inte.

<a id="formats"></a>

### Format

| Filändelse | Vad du får |
| --- | --- |
| *(ingen)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` och `.avif` accepteras inte. Svaret är HTTP 400 och bildfelsobjektet nedan. `.jpeg` är inte ett annat namn för `.jpg`.

<a id="random-rectangle"></a>

### Slumpmässig rektangel

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Svaret är `302 Found`. `Location` är `/id/{id}/{width}/{height}.{ext}`. Utan filändelse är `{ext}` `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` är det foto som valdes

`GET https://picsum.org/800/600` är standardförvalet i den här formen.

<a id="random-square"></a>

### Slumpmässig kvadrat

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` begär en JPEG i 640×640. Svaret är `302` till `/id/{id}/{width}/{width}.jpg`, med `Cache-Control: no-store` och huvudet `Picsum-ID`.

<a id="seeded"></a>

### Foto med startvärde

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Svaret är `302` till `/id/{id}/{width}/{height}.{ext}`. En kvadratisk adress med startvärde använder samma tal för bredd och höjd. En utelämnad filändelse är `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` är det valda fotot
- Ett startvärde väljer alltid samma källfoto, även när måtten ändras. `studio` väljer `1000561303`.
- Startvärdet är också ett sökord. `GET https://picsum.org/seed/cat/800/600` väljer ett foto av en katt.
- Om startvärdet inte matchar någon tagg faller tjänsten tillbaka på ett fast foto ur samlingen. Samma okända startvärde ger alltid det fotografiet.

<a id="pinned"></a>

### Låst foto

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Svaret är `200 OK` med bilddata, `image/jpeg` eller `image/webp`. En kvadratisk sökväg använder ett och samma mått för båda sidorna. Utan filändelse blir svaret JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` återger `{id}`

För att läsa fotograf och källsida för ett ID anropar du [`/id/{id}/info`](#info-id). Den metadatarutten, inte bildrutten, är den dokumenterade `404` för ett okänt ID.

<a id="query"></a>

### Frågeparametrar

| Parameter | Var den gäller | Regel |
| --- | --- | --- |
| `tag` | Slumpmässiga bilder, bilder med startvärde och `GET /v2/list` | Sökord som avgränsar urvalet. Exempel: `?tag=forest`. |
| `category` | Slumpmässiga bilder, bilder med startvärde och `GET /v2/list` | Ett av de 33 kategori-ID:na. Exempel: `?category=woodlands`. |
| `grayscale` | Bildlänkar | Flaggformen `?grayscale`. Gråskalan bakas in i bildfilen. Det finns ingen sökväg `/g/{width}/{height}`. |
| `blur` | Bildlänkar | Heltal från 1 till 10. Ett ensamt `?blur` accepteras och betyder `blur=5`. `blur=0` och `blur=11` ger HTTP 400. |

`tag` och `category` används när fotot väljs. De kopieras inte till `Location` i omdirigeringen.

Gråskala och oskärpa följer med bilden. Den här förfrågan med startvärde:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

svarar `302` med:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Flaggan `grayscale` skrivs som `grayscale=1` på den låsta bildlänken. `blur=4` behålls. Själva filen är gråskalig och oskarp. Det är inte ett CSS-filter.

<a id="presets"></a>

### Förval på startsidan

De här sex måtten är förvalen som visas på startsidan. Alla andra mått från 1 till 2000 är också kostnadsfria.

| Förval | Pixlar | Adress |
| --- | --- | --- |
| Standard | 800×600 | `https://picsum.org/800/600` |
| Kvadrat | 640×640 | `https://picsum.org/640` |
| Liggande | 1200×800 | `https://picsum.org/1200/800` |
| Stående | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Första anropet för ett nytt mått, eller för en ny kombination av gråskala och oskärpa, kan ta lite längre tid. Därefter ligger den låsta filen i cache.

<a id="json"></a>

## JSON-metadata

Det finns ingen `/list`-slutpunkt i v1. Samlingen listas på `/v2/list`.

`/v2/list` returnerar en JSON-array. `/id/{id}/info` och `/seed/{seed}/info` returnerar ett JSON-objekt. Alla tre skickar `Cache-Control: public, max-age=300` och `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Lista foton

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Parameter | Regel |
| --- | --- |
| `page` | Heltal större än eller lika med 1. Standard är `1`. |
| `limit` | Heltal från 1 till 100. Standard är `30`. |
| `tag` | Valfritt sökord. |
| `category` | Valfritt kategori-ID. |

Svarshuvuden:

- `Link`, med `rel="next"` och, när en föregående sida finns, `rel="prev"`.
- `Picsum-Total`, antalet foton som matchar. Utan `tag` och utan `category` är värdet `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

En förfrågan om sida 1 med `limit=1` returnerade det här `Link`-huvudet och `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Svarskroppen är en JSON-array med det objekt som beskrivs i [Objektfält](#fields). Varje objekt i listan är ett foto. Ordningen kan ändras. Behandla inte den första raden som ett fast foto.

<a id="info-id"></a>

### Ett foto via ID

```http
GET https://picsum.org/id/{id}/info
```

Ett känt ID ger `200` och ett JSON-objekt. Ett okänt ID ger `404` och exakt den här svarskroppen:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Ett foto via startvärde

```http
GET https://picsum.org/seed/{seed}/info
```

Svaret är `200`, ett JSON-objekt och huvudet `Picsum-ID`. Ett startvärde som inte matchar någon tagg ger inget fel. Det ger samma fasta reservfoto som bildlänken med startvärde.

<a id="fields"></a>

### Objektfält

| Fält | Betydelse |
| --- | --- |
| `id` | Foto-ID, som sträng. |
| `author` | Fotografens namn. Strängen kan vara tom. |
| `width` | Ursprunglig bredd i pixlar. Det är inte den bredd du begärde för bilden. |
| `height` | Ursprunglig höjd i pixlar. Det är inte den höjd du begärde för bilden. |
| `description` | Kort beskrivning av fotografiet. |
| `category` | Ett kategori-ID. |
| `tags` | Lista med sökord. |
| `url` | Sida för den ursprungliga källan. |
| `license` | Den exakta strängen `"CC0 1.0"`. |
| `license_url` | Den exakta strängen `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | JPEG-bildlänk för det här fotot i 800×600. |

Bygg en bildlänk för WebP eller gråskala från `id`. `download_url` är alltid JPEG i 800×600.

<a id="examples"></a>

### Exempel

`GET https://picsum.org/id/179363399/info` returnerar:

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

Fotografiet är 3840×2160, av Syony, i kategorin `landscapes` och beskrivs som ”Colorful mountain slopes in Landmannalaugar”. Taggarna är `mountains`, `highlands`, `colorful` och `iceland`.

`GET https://picsum.org/seed/studio/info` returnerar:

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

Svarshuvudet `Picsum-ID` är `1000561303`. Ursprungsmåttet är 2400×1800, `author` är tom och `category` är `food`.

<a id="categories"></a>

## Kategorier

Skicka ett av de här ID:na i `category`. Det finns ingen publik HTTP-slutpunkt `/categories`. Namnen i tabellerna nedan är översättningar för dig som läser. MCP-verktyget `list_categories` returnerar samma ID, men med de engelska visningsnamnen och en grupp. I anropet ska du skicka ID:t, inte visningsnamnet.

### Natur och landskap

| ID | Namn |
| --- | --- |
| `coasts` | Kuster och hav |
| `deserts` | Öknar och sanddyner |
| `freshwater` | Sjöar och vattenfall |
| `gardens` | Trädgårdar |
| `landscapes` | Landskap |
| `macro` | Makro |
| `mountains` | Berg |
| `plants` | Växter och blommor |
| `skies` | Himmel och väder |
| `snow` | Snö och is |
| `woodlands` | Skog |

### Djur

| ID | Namn |
| --- | --- |
| `animals` | Övriga djur |
| `birds` | Fåglar |
| `insects` | Insekter |
| `marine` | Marint liv |
| `pets` | Husdjur |

### Platser och resor

| ID | Namn |
| --- | --- |
| `aerial` | Flygfoto |
| `architecture` | Arkitektur |
| `city` | Städer och gator |
| `interiors` | Interiörer |
| `landmarks` | Landmärken |
| `night` | Natt |
| `transport` | Transport |

### Föremål och aktiviteter

| ID | Namn |
| --- | --- |
| `agriculture` | Jordbruk |
| `food` | Mat och dryck |
| `industry` | Industri |
| `music` | Musik |
| `objects` | Föremål |
| `sculpture` | Skulptur |
| `sports` | Sport |
| `technology` | Teknik |
| `textures` | Texturer |
| `workspaces` | Arbetsytor |

<a id="headers"></a>

## Huvuden, cache och CORS

Bildsvar och JSON-svar skickar:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` innehåller `Picsum-ID`, `Picsum-Total` och `Link`, så en sida på ett annat ursprung kan läsa de tre huvudena från `fetch`.

| Svar | `Cache-Control` |
| --- | --- |
| Slumpmässig omdirigering, `/{width}` eller `/{width}/{height}` | `no-store` |
| Omdirigering med startvärde, `/seed/{seed}/...` | `public, max-age=3600` |
| Låst bild, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

En slumpmässig omdirigering är `no-store`, så nästa anrop kan välja ett annat foto. Adressen `/id/...` i `Location` är filen som kan cachas. Första anropet för ett nytt mått eller en ny effekt kan ta lite längre tid, innan den filen ligger i cache.

JSON-felen 400 och 404 som dokumenteras nedan skickas också med `Cache-Control: no-store` och `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Fel och anropsgränser

Svarskroppen vid fel är JSON. Matcha de här `error`-strängarna exakt.

Ogiltiga bildmått, en filändelse som inte stöds eller ett oskärpevärde utanför 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Ogiltigt `page` eller `limit` på `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Okänt foto-ID på `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 betyder att du har nått anropsgränsen. Följ svarshuvudet `Retry-After`. Kör inte automatiserad trafik som försämrar tjänsten. Kringgå inte anropsgränser.

<a id="code"></a>

## Kodexempel

<a id="html"></a>

### HTML

Sätt `width`, `height` och `alt`. `alt` ska beskriva fotografiet. Beskrivningen nedan är `description` för fotot `179363399`.

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

Det första kommandot skriver ut huvudena för omdirigeringen med startvärde, bland annat `Location` och `Picsum-ID`, och sparar inte bilden. Det andra skriver ut ett fotoobjekt. Det tredje skriver ut huvudena för listan och en JSON-array.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` kan anropa JSON-slutpunkterna från en webbläsare, eftersom `Access-Control-Allow-Origin` är `*`. `Picsum-Total` är exponerat, så `headers.get` kan läsa värdet.

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

Exemplet använder biblioteket `requests`.

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

## Licens och kommersiell användning

Fotografierna är [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Privat och kommersiell användning är kostnadsfri. Du väljer själv om du anger fotografens namn. När du vill namnge ett foto är `author` fotografen och `url` källsidan, båda i JSON-objektet.

Du ansvarar för igenkännbara personer, varumärken och den ursprungliga källposten när användningen är känslig. Kontrollera `url` före sådan användning.

Sälj inte tjänsten vidare och distribuera den inte som ditt eget bild-API.

Frågor: [hello@picsum.org](mailto:hello@picsum.org).

Användarvillkor: [Användarvillkor](https://picsum.org/sv/terms).

<a id="mcp"></a>

## MCP-server

En MCP-server hos Picsum svarar på skrivskyddade frågor om foton för klienter som använder Model Context Protocol. Den ersätter inte bildlänkarna ovan och skapar inte bilder utifrån en textbeskrivning. Bildlänkar ligger kvar på `https://picsum.org/{...}`. MCP-slutpunkten är separat.

| | |
| --- | --- |
| Slutpunkt | `https://picsum.org/mcp` |
| Transport | Streamable HTTP |
| Auktorisering | OAuth 2.1 med PKCE |
| Omfång | `photos:read` |
| Installationsguide | [Anslut din AI-assistent till Picsum](https://picsum.org/sv/connect) |
| Klientkonfiguration | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Verktygen är skrivskyddade:

| Verktyg | Vad det gör |
| --- | --- |
| `search_photos` | Sök med `tag`, med `category` eller med båda. |
| `get_photo` | Metadata för ett foto-ID. |
| `list_categories` | Alla kategori-ID:n, med engelskt visningsnamn och grupp. |
| `build_image_url` | En bildlänk och ett HTML-utdrag med `<img>`, för valt mått, format, gråskala och oskärpa. |

Inloggning och klientinstallation beskrivs i [Anslut din AI-assistent till Picsum](https://picsum.org/sv/connect). Andra språk använder samma sökväg `/connect` under sitt språkprefix. Konfigurationsexemplen finns i [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
