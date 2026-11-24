[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · **Deutsch** · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/de) ist ein kostenloser Zufallsbildgenerator für CC0-Fotos. Er stellt **100.000 CC0-Fotos** unter [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) in **33 Kategorien** bereit. Bildlinks, eigene Größen, JPEG und WebP, Graustufen, Unschärfe und die Endpunkte für JSON-Metadaten gibt es ohne Konto und ohne API-Schlüssel.

Lorem Picsum (`picsum.org`) ist ein unabhängiger Dienst, inspiriert vom Open-Source-Projekt Picsum Photos. Zu `picsum.photos` besteht keine Zugehörigkeit. Er hat einen eigenen Katalog und eigene Foto-IDs. Pfade aus jenem anderen Projekt, darunter ein Graustufenpfad wie `/g/{width}/{height}`, gehören nicht zu dieser API.

Die Basis-URL der API lautet `https://picsum.org`. Setzen Sie kein Locale der Website vor einen API-Pfad. `https://picsum.org/de/800/600` ist ein Pfad der Website, kein Bildlink. Locale-Präfixe (`/de`, `/ja`, `/zh-tw` und die übrigen) gehören zu Seiten wie der Startseite, der MCP-Anleitung und den Nutzungsbedingungen.

## Inhalt

- [Überblick](#overview)
- [Schnellstart](#quick-start)
- [Bild-URLs](#image-urls)
- [JSON-Metadaten](#json)
- [Kategorien](#categories)
- [Header, Zwischenspeicher und CORS](#headers)
- [Fehler und Ratenbegrenzung](#errors)
- [Codebeispiele](#code)
- [Lizenz und kommerzielle Nutzung](#license)
- [MCP-Server](#mcp)

<a id="overview"></a>

## Überblick

Fordern Sie einen Bildlink an, wenn das Layout ein Bild braucht. Fordern Sie JSON an, wenn Sie Urheber, Beschreibung, Kategorie, Stichwörter, Originalmaße, Quellseite oder Lizenz benötigen.

Eine zufällige URL kann bei jeder Anfrage ein anderes Foto wählen. Mit einem Seed oder einer Foto-ID bleibt dasselbe Ausgangsfoto erhalten. Breite und Höhe sind ganze Zahlen von **1 bis 2000** Pixeln. Jede eigene Größe in diesem Bereich ist kostenlos, ebenso Graustufen und Unschärfe. Die sechs Bildgrößen auf der Startseite sind Voreinstellungen, keine Obergrenze.

<a id="quick-start"></a>

## Schnellstart

Dieses zufällige Bild mit 800×600 Pixeln leitet auf ein bestimmtes Foto weiter. Die Weiterleitung wird nicht zwischengespeichert, und die Antwort nennt die gewählte ID in `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Verwenden Sie einen festen Bildlink, wenn das Bild unverändert bleiben soll:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Verwenden Sie einen Seed, wenn das Bild wiederholbar sein soll. Derselbe Seed liefert bei jedem Maß dasselbe Ausgangsfoto. Der Seed `studio` verweist auf `1000561303`. Dieses Beispiel fordert WebP, Graustufen und Unschärfe an:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Bild-URLs

<a id="dimensions"></a>

### Abmessungen und Zuschnitt

`width` und `height` sind Pfadsegmente. Jede der beiden Angaben ist eine ganze Zahl von 1 bis einschließlich 2000. Der Dienst skaliert das Foto und schneidet es aus der Bildmitte zu, sodass das angeforderte Rechteck gefüllt ist. Das Bild wird nicht gestreckt.

<a id="formats"></a>

### Formate

| Erweiterung | Was Sie erhalten |
| --- | --- |
| *(keine)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` und `.avif` werden nicht angenommen. Die Antwort ist HTTP 400 und das weiter unten stehende Fehlerobjekt für Bilder. `.jpeg` steht nicht für dasselbe wie `.jpg`.

<a id="random-rectangle"></a>

### Zufälliges Rechteck

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Die Antwort ist `302 Found`. `Location` lautet `/id/{id}/{width}/{height}.{ext}`. Fehlt die Erweiterung, ist `{ext}` gleich `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` nennt das gewählte Foto

`GET https://picsum.org/800/600` ist in dieser Form die übliche Vorgabe.

<a id="random-square"></a>

### Zufälliges Quadrat

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` fordert ein JPEG mit 640×640 Pixeln an. Die Antwort ist `302` auf `/id/{id}/{width}/{width}.jpg`, mit `Cache-Control: no-store` und einem Header `Picsum-ID`.

<a id="seeded"></a>

### Foto mit Seed

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Die Antwort ist `302` auf `/id/{id}/{width}/{height}.{ext}`. Eine quadratische Seed-URL setzt Breite und Höhe auf dieselbe Zahl. Fehlt die Erweiterung, gilt `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` nennt das gewählte Foto
- Ein Seed wählt immer dasselbe Ausgangsfoto, auch wenn sich das Maß ändert. `studio` wählt `1000561303`.
- Der Seed dient zugleich als Suchwort. `GET https://picsum.org/seed/cat/800/600` wählt ein Katzenfoto.
- Passt der Seed zu keinem Stichwort, wählt der Dienst ein festes Foto aus der Sammlung. Derselbe unbekannte Seed liefert weiterhin dieses Foto.

<a id="pinned"></a>

### Festes Foto

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Die Antwort ist `200 OK` und die Bildbytes, `image/jpeg` oder `image/webp`. Ein quadratischer Pfad verwendet ein Maß für beide Seiten. Fehlt die Erweiterung, ist das Format JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` wiederholt `{id}`

Urheber und Quellseite einer ID lesen Sie über [`/id/{id}/info`](#info-id). Diese Metadatenroute, nicht die Bildroute, ist der dokumentierte `404` für eine unbekannte ID.

<a id="query"></a>

### Abfrageparameter

| Parameter | Geltungsbereich | Regel |
| --- | --- | --- |
| `tag` | Zufallsbilder, Bilder mit Seed und `GET /v2/list` | Stichwort. Es grenzt die Auswahl ein. Beispiel: `?tag=forest`. |
| `category` | Zufallsbilder, Bilder mit Seed und `GET /v2/list` | Eine der 33 Kategorie-IDs. Beispiel: `?category=woodlands`. |
| `grayscale` | Bild-URLs | Schalter ohne Wert: `?grayscale`. Die Graustufen sind in die Bilddatei eingebrannt. Einen Pfad `/g/{width}/{height}` gibt es nicht. |
| `blur` | Bild-URLs | Ganze Zahl von 1 bis 10. Ein bloßes `?blur` wird angenommen und bedeutet `blur=5`. `blur=0` und `blur=11` liefern HTTP 400. |

`tag` und `category` gelten, während das Foto gewählt wird. Auf die `Location` der Weiterleitung werden sie nicht übernommen.

Graustufen und Unschärfe werden mit dem Bild weitergegeben. Diese Anfrage mit Seed:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

antwortet mit `302` und:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Auf dieser festen URL wird `grayscale` als `grayscale=1` geschrieben. `blur=4` bleibt erhalten. Die Datei selbst ist in Graustufen und weichgezeichnet. Das ist kein CSS-Filter.

<a id="presets"></a>

### Bildgrößen der Startseite

Diese sechs Bildgrößen sind die Vorgaben auf der Startseite. Jede andere Größe von 1 bis 2000 ist ebenfalls kostenlos.

| Vorgabe | Pixel | URL |
| --- | --- | --- |
| Standard | 800×600 | `https://picsum.org/800/600` |
| Quadrat | 640×640 | `https://picsum.org/640` |
| Querformat | 1200×800 | `https://picsum.org/1200/800` |
| Hochformat | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Die erste Anfrage einer neuen Größe oder einer neuen Kombination aus Graustufen und Unschärfe kann etwas länger dauern. Danach ist die feste Datei zwischengespeichert.

<a id="json"></a>

## JSON-Metadaten

Einen Endpunkt `/list` in v1 gibt es nicht. Die Sammlung steht unter `/v2/list`.

`/v2/list` liefert ein JSON-Array. `/id/{id}/info` und `/seed/{seed}/info` liefern je ein JSON-Objekt. Alle drei senden `Cache-Control: public, max-age=300` und `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Fotos auflisten

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Abfrage | Regel |
| --- | --- |
| `page` | Ganze Zahl größer oder gleich 1. Voreinstellung `1`. |
| `limit` | Ganze Zahl von 1 bis 100. Voreinstellung `30`. |
| `tag` | Optionales Stichwort. |
| `category` | Optionale Kategorie-ID. |

Antwortheader:

- `Link`, mit `rel="next"` und, wenn eine vorherige Seite vorhanden ist, `rel="prev"`.
- `Picsum-Total`, die Anzahl der passenden Fotos. Ohne `tag` und ohne `category` beträgt der Wert `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Eine Anfrage für Seite 1 mit `limit=1` lieferte diesen Header `Link` und `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Der Antwortkörper ist ein Array aus dem Objekt, das unter [Objektfelder](#fields) beschrieben ist. Jedes Element ist ein Foto. Die Reihenfolge kann sich ändern. Behandeln Sie die erste Zeile nicht als festes Foto.

<a id="info-id"></a>

### Ein Foto nach ID

```http
GET https://picsum.org/id/{id}/info
```

Eine bekannte ID liefert `200` und ein JSON-Objekt. Eine unbekannte ID liefert `404` und genau diesen Antwortkörper:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Ein Foto nach Seed

```http
GET https://picsum.org/seed/{seed}/info
```

Die Antwort ist `200` und ein JSON-Objekt, dazu der Header `Picsum-ID`. Ein Seed ohne passendes Stichwort ergibt keinen Fehler. Er liefert dasselbe feste Foto wie die Bild-URL mit Seed.

<a id="fields"></a>

### Objektfelder

| Feld | Bedeutung |
| --- | --- |
| `id` | Foto-ID als Zeichenkette. |
| `author` | Urhebername. Die Zeichenkette kann leer sein. |
| `width` | Originalbreite in Pixeln. Das ist nicht die angeforderte Ausgabebreite. |
| `height` | Originalhöhe in Pixeln. Das ist nicht die angeforderte Ausgabehöhe. |
| `description` | Kurze Beschreibung des Fotos. |
| `category` | Eine Kategorie-ID. |
| `tags` | Array aus Stichwörtern. |
| `url` | Seite der Originalquelle. |
| `license` | Genau die Zeichenkette `"CC0 1.0"`. |
| `license_url` | Genau die Zeichenkette `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | JPEG-URL dieses Fotos mit 800×600 Pixeln. |

Eine URL für WebP oder Graustufen bilden Sie aus `id`. `download_url` ist immer das JPEG mit 800×600 Pixeln.

<a id="examples"></a>

### Beispiele

`GET https://picsum.org/id/179363399/info` liefert:

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

Das Foto hat 3840×2160 Pixel, stammt von Syony, gehört zur Kategorie `landscapes` und ist beschrieben als „Colorful mountain slopes in Landmannalaugar“. Die Stichwörter sind `mountains`, `highlands`, `colorful` und `iceland`.

`GET https://picsum.org/seed/studio/info` liefert:

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

Der Antwortheader `Picsum-ID` lautet `1000561303`. Im Original misst das Foto 2400×1800 Pixel, `author` ist leer und `category` ist `food`.

<a id="categories"></a>

## Kategorien

Übergeben Sie in `category` eine dieser IDs. Einen öffentlichen HTTP-Endpunkt `/categories` gibt es nicht. Das MCP-Werkzeug `list_categories` liefert dieselben IDs, jeweils mit dem englischen Anzeigenamen und einer Gruppe. Die Namen in dieser Tabelle sind Übersetzungen für die Leserinnen und Leser. Senden Sie die ID, nicht den Anzeigenamen.

### Natur und Landschaft

| ID | Name |
| --- | --- |
| `coasts` | Küsten und Meere |
| `deserts` | Wüsten und Dünen |
| `freshwater` | Seen und Wasserfälle |
| `gardens` | Gärten |
| `landscapes` | Landschaften |
| `macro` | Makrofotografie |
| `mountains` | Berge |
| `plants` | Pflanzen und Blumen |
| `skies` | Himmel und Wetter |
| `snow` | Schnee und Eis |
| `woodlands` | Wälder |

### Tiere

| ID | Name |
| --- | --- |
| `animals` | Weitere Tiere |
| `birds` | Vögel |
| `insects` | Insekten |
| `marine` | Meeresleben |
| `pets` | Haustiere |

### Orte und Reisen

| ID | Name |
| --- | --- |
| `aerial` | Luftaufnahmen |
| `architecture` | Architektur |
| `city` | Städte und Straßen |
| `interiors` | Innenräume |
| `landmarks` | Sehenswürdigkeiten |
| `night` | Nachtaufnahmen |
| `transport` | Verkehr |

### Objekte und Aktivitäten

| ID | Name |
| --- | --- |
| `agriculture` | Landwirtschaft |
| `food` | Essen und Trinken |
| `industry` | Industrie |
| `music` | Musik |
| `objects` | Gegenstände |
| `sculpture` | Skulpturen |
| `sports` | Sport |
| `technology` | Technik |
| `textures` | Texturen |
| `workspaces` | Arbeitsplätze |

<a id="headers"></a>

## Header, Zwischenspeicher und CORS

Bild- und JSON-Antworten senden:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` enthält `Picsum-ID`, `Picsum-Total` und `Link`, sodass eine Seite auf einem anderen Origin diese drei Header über `fetch` lesen kann.

| Antwort | `Cache-Control` |
| --- | --- |
| Zufällige Weiterleitung, `/{width}` oder `/{width}/{height}` | `no-store` |
| Weiterleitung mit Seed, `/seed/{seed}/...` | `public, max-age=3600` |
| Festes Bild, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Eine zufällige Weiterleitung ist `no-store`, damit die nächste Anfrage ein anderes Foto wählen kann. Die URL `/id/...` in `Location` ist die Datei, die sich zwischenspeichern lässt. Die erste Anfrage einer neuen Größe oder eines neuen Effekts kann etwas länger dauern, bevor diese Datei zwischengespeichert ist.

Die unten beschriebenen JSON-Fehler 400 und 404 werden ebenfalls mit `Cache-Control: no-store` und `Access-Control-Allow-Origin: *` gesendet.

<a id="errors"></a>

## Fehler und Ratenbegrenzung

Die Fehlerkörper sind JSON. Diese `error`-Zeichenketten müssen exakt übereinstimmen.

Ungültige Bildmaße, eine nicht unterstützte Erweiterung oder ein `blur`-Wert außerhalb von 1 bis 10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Ungültiges `page` oder `limit` bei `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Unbekannte Foto-ID bei `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 bedeutet, dass die Ratenbegrenzung gegriffen hat. Halten Sie sich an den Antwortheader `Retry-After`. Erzeugen Sie keinen automatisierten Datenverkehr, der den Dienst beeinträchtigt, und umgehen Sie die Ratenbegrenzung nicht.

<a id="code"></a>

## Codebeispiele

<a id="html"></a>

### HTML

Setzen Sie `width`, `height` und `alt`. `alt` soll das Foto beschreiben. Der Text unten ist die `description` des Fotos `179363399`.

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

Der erste Befehl gibt die Header der Weiterleitung mit Seed aus, darunter `Location` und `Picsum-ID`, und speichert das Bild nicht. Der zweite gibt ein Fotoobjekt aus. Der dritte gibt die Header der Liste und ein JSON-Array aus.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` kann die JSON-Endpunkte aus einem Browser aufrufen, weil `Access-Control-Allow-Origin` auf `*` steht. `Picsum-Total` ist freigegeben, daher kann `headers.get` den Wert lesen.

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

Dieses Beispiel verwendet die Bibliothek `requests`.

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

## Lizenz und kommerzielle Nutzung

Die Fotos stehen unter [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Die private und die kommerzielle Nutzung sind kostenlos. Eine Namensnennung ist freiwillig. Wenn Sie ein Foto nennen möchten, steht der Urheber in `author` und die Quellseite in `url`, beides im JSON-Objekt.

Bei einer sensiblen Nutzung tragen Sie die Verantwortung für erkennbare Personen, Marken und den Datensatz der Originalquelle. Prüfen Sie `url` vor einer solchen Nutzung.

Verkaufen Sie diesen Dienst nicht weiter und bieten Sie ihn nicht als eigene Bild-API an.

Fragen: [hello@picsum.org](mailto:hello@picsum.org).

Siehe die [Nutzungsbedingungen](https://picsum.org/de/terms).

<a id="mcp"></a>

## MCP-Server

Ein gehosteter MCP-Server beantwortet nur lesende Abfragen zu Fotos. Er richtet sich an Clients, die das Model Context Protocol unterstützen. Er ersetzt die Bildlinks oben nicht und erzeugt keine Bilder aus einer Texteingabe. Bildlinks bleiben bei `https://picsum.org/{...}`. Der MCP-Endpunkt ist davon getrennt.

| | |
| --- | --- |
| Endpunkt | `https://picsum.org/mcp` |
| Transport | Streamable HTTP |
| Autorisierung | OAuth 2.1 mit PKCE |
| Scope | `photos:read` |
| Anleitung | [KI-Assistent mit Picsum verbinden](https://picsum.org/de/connect) |
| Client-Konfiguration | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Die Werkzeuge haben ausschließlich Lesezugriff:

| Werkzeug | Funktion |
| --- | --- |
| `search_photos` | Suche nach `tag`, nach `category` oder nach beiden. |
| `get_photo` | Metadaten zu einer Foto-ID. |
| `list_categories` | Jede Kategorie-ID mit englischem Anzeigenamen und Gruppe. |
| `build_image_url` | Ein Bildlink und ein HTML-Fragment `<img>` für eine gewählte Größe, ein Format, Graustufen und Unschärfe. |

Anmeldung und Einrichtung des Clients sind in [KI-Assistent mit Picsum verbinden](https://picsum.org/de/connect) beschrieben. Andere Sprachen verwenden denselben Pfad `/connect` unter ihrem Locale-Präfix. Die Konfigurationsbeispiele stehen in [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
