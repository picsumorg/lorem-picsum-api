[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · **Eesti** · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/et) on tasuta juhupiltide generaator. See pakub **100 000 CC0-fotot** **33 kategoorias** litsentsi [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) alusel. Pildilingid, erimõõtmed, JPEG ja WebP, halltoonid, hägustus ning JSON-metaandmete otspunktid ei vaja kontot ega API-võtit.

Lorem Picsum (`picsum.org`) on eraldiseisev teenus, mis sai eeskuju avatud lähtekoodiga projektist Picsum Photos. See ei ole seotud teenusega `picsum.photos`. Sellel on oma fotokogu ja oma foto-ID-d. Selle teise projekti teed, kaasa arvatud halltoonide tee `/g/{width}/{height}`, ei kuulu sellesse API-sse.

API baasaadress on `https://picsum.org`. Ära lisa API tee ette veebisaidi keele-eesliidet. `https://picsum.org/de/800/600` on veebisaidi tee, mitte pildilink. Keele-eesliited (`/de`, `/ja`, `/zh-tw` ja ülejäänud) kuuluvad lehtede juurde, näiteks avalehele, MCP seadistusjuhendile ja kasutustingimustele.

## Sisukord

- [Ülevaade](#overview)
- [Kiire algus](#quick-start)
- [Pildilingid](#image-urls)
- [JSON-metaandmed](#json)
- [Kategooriad](#categories)
- [Päised, vahemälu ja CORS](#headers)
- [Vead ja päringupiirangud](#errors)
- [Koodinäited](#code)
- [Litsents ja äriline kasutus](#license)
- [MCP-server](#mcp)

<a id="overview"></a>

## Ülevaade

Kui kujundus vajab pilti, küsi pildilinki. Kui vajad autorit, kirjeldust, kategooriat, märksõnu, algseid mõõtmeid, allikalehte või litsentsi, küsi JSON-i.

Juhuslik URL võib iga päringuga valida teise foto. Seeme või foto ID hoiab alles sama lähtefoto. Laius ja kõrgus on täisarvud vahemikus **1 kuni 2000** pikslit. Kõik erimõõtmed selles vahemikus on tasuta, nagu ka halltoonid ja hägustus. Kuus mõõdet avalehel on mugavad eelseadistused, mitte ülempiir.

<a id="quick-start"></a>

## Kiire algus

See juhuslik pilt mõõtmetega 800×600 suunab ümber konkreetsele fotole. Ümbersuunamist vahemällu ei salvestata ning vastus kannab valitud ID-d päises `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Kasuta fikseeritud pildilinki, kui pilt peab paigale jääma:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Kasuta seemet, kui pilt peab olema korratav. Sama seeme annab iga mõõtme korral sama lähtefoto. Seeme `studio` vastab ID-le `1000561303`. See näide küsib WebP-vormingut, halltoone ja hägustust:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Pildilingid

<a id="dimensions"></a>

### Mõõtmed ja kärpimine

`width` ja `height` on tee osad. Kumbki on täisarv 1-st 2000-ni, otsad kaasa arvatud. Teenus muudab foto suurust ja kärbib selle keskelt, nii et küsitud ristkülik saab täis. Pilti ei venitata.

<a id="formats"></a>

### Vormingud

| Laiend | Mida saad |
| --- | --- |
| *(puudub)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` ja `.avif` ei ole lubatud. Vastus on HTTP 400 ja allpool toodud pildi veaobjekt. `.jpeg` ei kehti `.jpg` asemel.

<a id="random-rectangle"></a>

### Juhuslik ristkülik

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Vastus on `302 Found`. `Location` on `/id/{id}/{width}/{height}.{ext}`. Kui laiend puudub, on `{ext}` väärtus `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` on valitud foto

`GET https://picsum.org/800/600` on standardne eelseadistus selles vormis.

<a id="random-square"></a>

### Juhuslik ruut

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` küsib JPEG-i mõõtmetega 640×640. Vastus on `302` aadressile `/id/{id}/{width}/{width}.jpg`, päistega `Cache-Control: no-store` ja `Picsum-ID`.

<a id="seeded"></a>

### Seemnega foto

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Vastus on `302` aadressile `/id/{id}/{width}/{height}.{ext}`. Ruudu seemne-URL kasutab laiuse ja kõrguse jaoks sama arvu. Kui laiend puudub, on väärtus `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` on valitud foto
- Üks seeme valib alati sama lähtefoto, ka siis, kui mõõtmed muutuvad. `studio` valib `1000561303`.
- Seeme on ühtlasi teemamärksõna. `GET https://picsum.org/seed/cat/800/600` valib kassifoto.
- Kui seeme ei ühti ühegi märksõnaga, valib teenus kogust ühe püsiva foto. Sama tundmatu seeme tagastab alati selle sama foto.

<a id="pinned"></a>

### Fikseeritud foto

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Vastus on `200 OK` ja pildi baidid, `image/jpeg` või `image/webp`. Ruudu tee kasutab mõlema külje jaoks ühte mõõdet. Kui laiend puudub, on tulemus JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` kordab väärtust `{id}`

Autori ja allikalehe saamiseks ID järgi kutsu [`/id/{id}/info`](#info-id). Tundmatu ID korral on dokumenteeritud `404` sellel metaandmete teel, mitte pilditeel.

<a id="query"></a>

### Päringuparameetrid

| Parameeter | Kus kehtib | Reegel |
| --- | --- | --- |
| `tag` | Juhuslikud pildid, seemnega pildid ja `GET /v2/list` | Teemamärksõna. See kitsendab valikut. Näide: `?tag=forest`. |
| `category` | Juhuslikud pildid, seemnega pildid ja `GET /v2/list` | Üks neist 33 kategooria ID-st. Näide: `?category=woodlands`. |
| `grayscale` | Pildilingid | Lipp kujul `?grayscale`. Halltoonid on pildifaili sisse töödeldud. Teed `/g/{width}/{height}` ei ole. |
| `blur` | Pildilingid | Täisarv vahemikus 1 kuni 10. Ilma väärtuseta `?blur` on lubatud ja tähendab `blur=5`. `blur=0` ja `blur=11` tagastavad HTTP 400. |

`tag` ja `category` kehtivad foto valimise ajal. Neid ei kopeerita ümbersuunamise päisesse `Location`.

Halltoonid ja hägustus liiguvad pildiga kaasa. See seemnega päring:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

vastab staatusega `302` ja nende päistega:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Lipp `grayscale` kirjutatakse sellel fikseeritud URL-il kujul `grayscale=1`. `blur=4` jääb alles. Fail ise on halltoonides ja hägustatud. See ei ole CSS-i filter.

<a id="presets"></a>

### Avalehe mõõtmete eelseadistused

Need kuus mõõdet on eelseadistused, mida avaleht näitab. Iga muu mõõt vahemikus 1 kuni 2000 on samuti tasuta.

| Eelseadistus | Pikslid | URL |
| --- | --- | --- |
| Standardne | 800×600 | `https://picsum.org/800/600` |
| Ruut | 640×640 | `https://picsum.org/640` |
| Horisontaalne | 1200×800 | `https://picsum.org/1200/800` |
| Vertikaalne | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Uue mõõtme või uue halltooni või hägustuse esimene päring võib võtta veidi kauem. Pärast seda on fikseeritud fail vahemälus.

<a id="json"></a>

## JSON-metaandmed

Versiooni v1 otspunkti `/list` ei ole. Kogu on loetletud aadressil `/v2/list`.

`/v2/list` tagastab JSON-massiivi. `/id/{id}/info` ja `/seed/{seed}/info` tagastavad ühe JSON-objekti. Kõik kolm saadavad päised `Cache-Control: public, max-age=300` ja `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Fotode loend

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Päring | Reegel |
| --- | --- |
| `page` | Täisarv, mis on 1 või suurem. Vaikeväärtus on `1`. |
| `limit` | Täisarv vahemikus 1 kuni 100. Vaikeväärtus on `30`. |
| `tag` | Valikuline teemamärksõna. |
| `category` | Valikuline kategooria ID. |

Vastuse päised:

- Päises `Link` on `rel="next"` ja, kui eelmine leht on olemas, ka `rel="prev"`.
- `Picsum-Total`, sobivate fotode arv. Kui `tag` ja `category` puuduvad, on väärtus `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Esimese lehe päring, kus `limit=1`, tagastas selle `Link` päise ja `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Vastusekeha on massiiv objektidest, mida kirjeldab [Objekti väljad](#fields). Iga element on üks foto. Järjekord võib muutuda, seega ära võta esimest rida kindla fotona.

<a id="info-id"></a>

### Üks foto ID järgi

```http
GET https://picsum.org/id/{id}/info
```

Tuntud ID tagastab `200` ja ühe JSON-objekti. Tundmatu ID tagastab `404` ja täpselt selle keha:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Üks foto seemne järgi

```http
GET https://picsum.org/seed/{seed}/info
```

Vastus on `200` ja üks JSON-objekt ning päis `Picsum-ID`. Seeme, mis ei ühti ühegi märksõnaga, ei tagasta viga. See tagastab sama püsiva varufoto nagu seemnega pildi URL.

<a id="fields"></a>

### Objekti väljad

| Väli | Tähendus |
| --- | --- |
| `id` | Foto ID sõnena. |
| `author` | Autori nimi. Sõne võib olla tühi. |
| `width` | Algne laius pikslites. See ei ole kuvamiseks küsitud laius. |
| `height` | Algne kõrgus pikslites. See ei ole kuvamiseks küsitud kõrgus. |
| `description` | Foto lühike kirjeldus. |
| `category` | Üks kategooria ID. |
| `tags` | Teemamärksõnade massiiv. |
| `url` | Algallika leht. |
| `license` | Täpne sõne `"CC0 1.0"`. |
| `license_url` | Täpne sõne `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | Selle foto JPEG-i URL mõõtmetega 800×600. |

Koosta WebP või halltoonide URL välja `id` järgi. `download_url` on alati JPEG mõõtmetega 800×600.

<a id="examples"></a>

### Näited

`GET https://picsum.org/id/179363399/info` tagastab:

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

Foto on mõõtmetega 3840×2160, autor on Syony, kategooria on `landscapes` ja kirjeldus on „Colorful mountain slopes in Landmannalaugar“. Märksõnad on `mountains`, `highlands`, `colorful` ja `iceland`.

`GET https://picsum.org/seed/studio/info` tagastab:

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

Vastuse päis `Picsum-ID` on `1000561303`. Algne kaader on 2400×1800, `author` on tühi ja `category` on `food`.

<a id="categories"></a>

## Kategooriad

Anna parameetris `category` üks neist ID-dest. Avalikku HTTP-otspunkti `/categories` ei ole. MCP-tööriist `list_categories` tagastab samad ID-d koos ingliskeelse kuvatava nime ja rühmaga. Alloleva tabeli nimed on tõlked lugejale. Päringus tuleb saata ID, mitte kuvatav nimi.

### Loodus ja maastikud

| ID | Nimi |
| --- | --- |
| `coasts` | Rannikud ja ookeanid |
| `deserts` | Kõrbed ja luited |
| `freshwater` | Järved ja kosed |
| `gardens` | Aiad |
| `landscapes` | Maastikud |
| `macro` | Makrofotod |
| `mountains` | Mäed |
| `plants` | Taimed ja lilled |
| `skies` | Taevas ja ilm |
| `snow` | Lumi ja jää |
| `woodlands` | Metsad |

### Loomad

| ID | Nimi |
| --- | --- |
| `animals` | Muud loomad |
| `birds` | Linnud |
| `insects` | Putukad |
| `marine` | Mereelustik |
| `pets` | Lemmikloomad |

### Paigad ja reisimine

| ID | Nimi |
| --- | --- |
| `aerial` | Aerofotod |
| `architecture` | Arhitektuur |
| `city` | Linnad ja tänavad |
| `interiors` | Interjöörid |
| `landmarks` | Vaatamisväärsused |
| `night` | Ööfotod |
| `transport` | Transport |

### Esemed ja tegevused

| ID | Nimi |
| --- | --- |
| `agriculture` | Põllumajandus |
| `food` | Söök ja jook |
| `industry` | Tööstus |
| `music` | Muusika |
| `objects` | Esemed |
| `sculpture` | Skulptuurid |
| `sports` | Sport |
| `technology` | Tehnoloogia |
| `textures` | Tekstuurid |
| `workspaces` | Töökeskkond |

<a id="headers"></a>

## Päised, vahemälu ja CORS

Pildi- ja JSON-vastused saadavad:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` sisaldab päiseid `Picsum-ID`, `Picsum-Total` ja `Link`, nii et teise päritoluga leht saab need kolm päist `fetch`-päringuga lugeda.

| Vastus | `Cache-Control` |
| --- | --- |
| Juhuslik ümbersuunamine, `/{width}` või `/{width}/{height}` | `no-store` |
| Seemnega ümbersuunamine, `/seed/{seed}/...` | `public, max-age=3600` |
| Fikseeritud pilt, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Juhuslik ümbersuunamine on `no-store`, nii et järgmine päring võib valida teise foto. URL `/id/...` päises `Location` on fail, mida saab vahemällu panna. Uue mõõtme või efekti esimene päring võib võtta veidi kauem, enne kui see fail vahemällu jõuab.

Allpool kirjeldatud JSON-vead 400 ja 404 saadetakse samuti päistega `Cache-Control: no-store` ja `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Vead ja päringupiirangud

Veakehad on JSON-vormingus. Need `error`-sõned peavad kattuma täpselt.

Vigased pildi mõõtmed, toetamata laiend või hägustuse väärtus väljaspool vahemikku 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Vigane `page` või `limit` aadressil `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Tundmatu foto ID aadressil `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 tähendab, et rakendati päringupiirangut. Järgi vastuse päist `Retry-After`. Ära saada automaatliiklust, mis teenust halvendab, ja ära hoia päringupiirangutest kõrvale.

<a id="code"></a>

## Koodinäited

<a id="html"></a>

### HTML

Määra `width`, `height` ja `alt`. `alt` peaks fotot kirjeldama. Allolev tekst on foto `179363399` välja `description` väärtus.

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

Esimene käsk kuvab seemnega ümbersuunamise päised, sealhulgas `Location` ja `Picsum-ID`, ega salvesta pilti. Teine kuvab ühe foto objekti. Kolmas kuvab loendi päised ja JSON-massiivi.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

Brauserist saab `fetch`-iga JSON-otspunkte kutsuda, sest `Access-Control-Allow-Origin` on `*`. `Picsum-Total` on avalikustatud, nii et `headers.get` saab seda lugeda.

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

See näide kasutab teeki `requests`.

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

## Litsents ja äriline kasutus

Fotod on litsentsiga [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Kasutus era- ja ärieesmärgil on tasuta. Autori nimetamine on vabatahtlik. Kui soovid fotot tunnustada, on `author` autor ja `url` allikaleht. Mõlemad väljad on JSON-objektis.

Kui kasutus on tundlik, vastutad sina äratuntavate inimeste, kaubamärkide ja algallika kirje eest. Kontrolli enne sellist kasutust välja `url`.

Ära müü ega levita seda teenust enda pildi-API-na.

Küsimused: [hello@picsum.org](mailto:hello@picsum.org).

[Kasutustingimused](https://picsum.org/et/terms).

<a id="mcp"></a>

## MCP-server

Majutatud MCP-server võtab vastu ainult lugemiseks mõeldud fotopäringuid klientidelt, mis kasutavad mudeli konteksti protokolli. See ei asenda ülaltoodud pildilinke ega loo pilte tekstijuhise põhjal. Pildilingid jäävad aadressile `https://picsum.org/{...}`. MCP otspunkt on eraldi.

| | |
| --- | --- |
| Otspunkt | `https://picsum.org/mcp` |
| Transport | Streamable HTTP |
| Autoriseerimine | OAuth 2.1 koos PKCE-ga |
| Ulatus | `photos:read` |
| Seadistusjuhend | [Ühenda oma tehisaruabiline Picsumiga](https://picsum.org/et/connect) |
| Kliendi seadistus | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Tööriistad on ainult lugemiseks:

| Tööriist | Mida see teeb |
| --- | --- |
| `search_photos` | Otsib `tag` järgi, `category` järgi või mõlema järgi. |
| `get_photo` | Ühe foto ID metaandmed. |
| `list_categories` | Iga kategooria ID koos ingliskeelse kuvatava nime ja rühmaga. |
| `build_image_url` | Pildi URL ja HTML-i `<img>` lõik valitud mõõtme, vormingu, halltoonide ja hägustuse jaoks. |

Sisselogimine ja kliendi seadistus on kirjas lehel [Ühenda oma tehisaruabiline Picsumiga](https://picsum.org/et/connect). Teistes keeltes on sama tee `/connect` oma keele-eesliite all. Seadistusnäited on aadressil [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
