[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · **Ikinyarwanda** · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/rw) ni API y’ubuntu y’amafoto y’agateganyo. Itanga **amafoto 100.000** ya CC0. Ayo mafoto afite [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) kandi akaba mu **byiciro 33**. Amahuza y’amafoto, ingano wihitiyemo, JPEG na WebP, ibara ry’ikijuju, gupfuka, n’inzira za JSON zitanga amakuru, byose ntibisaba konti cyangwa urufunguzo rwa API.

Lorem Picsum (`picsum.org`) ni serivisi yigenga yakuye igitekerezo ku mushinga Picsum Photos ufite kode ifunguye. Nta isano ifitanye na `picsum.photos`. Ifite ububiko bw’amafoto na ID byayo. Inzira z’uwo mushinga, harimo inzira y’ibara ry’ikijuju nka `/g/{width}/{height}`, ntiziri muri iyi API.

URL y’ibanze ya API ni `https://picsum.org`. Ntushyire ururimi rw’urubuga imbere y’inzira ya API. `https://picsum.org/de/800/600` ni inzira y’urubuga, si URL y’ifoto. Intangiriro z’ururimi (`/de`, `/ja`, `/zh-tw`, n’izindi) zigenewe amapaji nk’urupapuro rw’ibanze, inyandiko yo guhuza, n’amabwiriza yo gukoresha serivisi.

## Ibirimo

- [Incamake](#overview)
- [Gutangira vuba](#quick-start)
- [Amahuza y’amafoto](#image-urls)
- [Amakuru ya JSON](#json)
- [Ibyiciro](#categories)
- [Imitwe, kubika, na CORS](#headers)
- [Amakosa n’imipaka y’ubusabe](#errors)
- [Ingero za kode](#code)
- [Uruhushya n’ikoreshwa mu bucuruzi](#license)
- [Seriveri ya MCP](#mcp)

<a id="overview"></a>

## Incamake

Saba ihuza ry’ifoto iyo umwanya ukeneye ifoto. Saba JSON iyo ukeneye uwafashe ifoto, ibisobanuro, icyiciro, amagambo y’ishakisha, ingano z’umwimerere, urupapuro yaturutseho, cyangwa uruhushya.

Ihuza ry’amafoto atoranywa ku buryo bw’amahirwe rishobora guhitamo ifoto itandukanye kuri buri busabe. Seed cyangwa ID y’ifoto biguma ku ifoto imwe y’umwimerere. Ubugari n’uburebure ni imibare yuzuye, kuva kuri pigiseli **1 kugera kuri 2000**. Buri ngano muri iyo mipaka ni ubuntu. Ibara ry’ikijuju na gupfuka na byo ni ubuntu. Ingano esheshatu zo ku rupapuro rw’ibanze ni ingano ziteguye zo korohera. Ntabwo ari umupaka.

<a id="quick-start"></a>

## Gutangira vuba

Iyi URL ya 800×600 itoranywa ku buryo bw’amahirwe yohereza ku ifoto runaka binyuze muri `302`. Icyo gisubizo ntikibikwa, kandi gifite ID yatoranyijwe muri `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Koresha ihuza rifunze ku ID iyo ifoto igomba kuguma ari yo:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Koresha seed iyo ifoto igomba kongera kuboneka. Seed imwe ihuza n’ifoto imwe y’umwimerere mu ngano zose. Seed `studio` ihuza na `1000561303`. Iki gitekerezo gisaba WebP, ibara ry’ikijuju, na gupfuka:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Amahuza y’amafoto

<a id="dimensions"></a>

### Ingano no gukata

`width` na `height` ni ibice by’inzira. Buri kimwe ni umubare wuzuye kuva kuri 1 kugera kuri 2000, harimo n’iyo mpera yombi. Serivisi ihindura ingano y’ifoto ikayikata ahereye hagati, kugira ngo urukiramende wasabye rwuzure. Ifoto ntiramburwa.

<a id="formats"></a>

### Imiterere ya dosiye

| Umugereka | Ibyo ubona |
| --- | --- |
| *(nta mugereka)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif`, na `.avif` ntizemerwa. Igisubizo ni HTTP 400 n’ikintu cy’ikosa cy’ifoto kiri hasi. `.jpeg` si izina rindi rya `.jpg`.

<a id="random-rectangle"></a>

### Urukiramende rutoranywa ku buryo bw’amahirwe

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Igisubizo ni `302 Found`. `Location` ni `/id/{id}/{width}/{height}.{ext}`. Iyo umugereka utashyizweho, `{ext}` ni `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` ni ifoto yatoranyijwe

`GET https://picsum.org/800/600` ni ingano isanzwe y’iyi miterere.

<a id="random-square"></a>

### Impande zingana zitoranywa ku buryo bw’amahirwe

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` isaba JPEG ifite 640×640. Igisubizo ni `302` kijya kuri `/id/{id}/{width}/{width}.jpg`, gifite `Cache-Control: no-store` n’umutwe `Picsum-ID`.

<a id="seeded"></a>

### Ifoto ya seed

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Igisubizo ni `302` kijya kuri `/id/{id}/{width}/{height}.{ext}`. URL ya seed ifite impande zingana ikoresha umubare umwe ku bugari no ku burebure. Umugereka utashyizweho ni `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` ni ifoto yatoranyijwe
- Seed imwe ihora ihitamo ifoto imwe y’umwimerere, n’iyo ingano ihindutse. `studio` ihitamo `1000561303`.
- Seed ni n’ijambo ry’insanganyamatsiko. `GET https://picsum.org/seed/cat/800/600` ihitamo ifoto y’injangwe.
- Niba seed itahuye n’ijambo ry’ishakisha, hatoranywa ifoto imwe idahinduka mu bubiko. Seed imwe itazwi ihora igarura iyo foto imwe.

<a id="pinned"></a>

### Ifoto ifunze ku ID

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Igisubizo ni `200 OK` n’ifoto ubwayo, `image/jpeg` cyangwa `image/webp`. Inzira ifite impande zingana ikoresha ingano imwe ku mpande zombi. Umugereka utashyizweho ni JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` igarura `{id}`

Kugira ngo ubone uwafashe ifoto n’urupapuro yaturutseho kuri ID, hamagara [`/id/{id}/info`](#info-id). Iyo nzira y’amakuru, si inzira y’ifoto, ni yo yanditswe nka `404` y’ID itazwi.

<a id="query"></a>

### Ibipimo byo mu URL

| Ikipimo | Aho gikoreshwa | Itegeko |
| --- | --- | --- |
| `tag` | Amafoto atoranywa ku buryo bw’amahirwe, amafoto ya seed, na `GET /v2/list` | Umurongo w’insanganyamatsiko. Ugabanya amafoto ashakishwa. Urugero: `?tag=forest`. |
| `category` | Amafoto atoranywa ku buryo bw’amahirwe, amafoto ya seed, na `GET /v2/list` | ID imwe mu byiciro 33. Urugero: `?category=woodlands`. |
| `grayscale` | Amahuza y’amafoto | Ikimenyetso `?grayscale`. Ibara ry’ikijuju rishyirwa muri dosiye y’ifoto. Nta nzira `/g/{width}/{height}`. |
| `blur` | Amahuza y’amafoto | Umubare wuzuye kuva kuri 1 kugera ku 10. `?blur` yonyine yemerwa, kandi isobanura `blur=5`. `blur=0` na `blur=11` bisubiza HTTP 400. |

`tag` na `category` bikoreshwa mu gihe ifoto irimo guhitamwa. Ntibikopororwa ku `Location` y’igisubizo cya `302`.

Ibara ry’ikijuju na gupfuka bijyana n’ifoto. Ubu busabe bwa seed:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

busubiza `302` bufite:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Ikimenyetso `grayscale` cyandikwa nka `grayscale=1` kuri iyo URL ifunze. `blur=4` igumaho. Dosiye ubwayo ifite ibara ry’ikijuju kandi ipfutse; ibi ntibikorwa na CSS.

<a id="presets"></a>

### Ingano ziteguye zo ku rupapuro rw’ibanze

Ingano esheshatu zigaragara ku rupapuro rw’ibanze ni ingano ziteguye. Iyindi yose kuva kuri 1 kugera kuri 2000 na yo ni ubuntu.

| Ingano iteguye | Pigiseli | URL |
| --- | --- | --- |
| Isanzwe | 800×600 | `https://picsum.org/800/600` |
| Impande zingana | 640×640 | `https://picsum.org/640` |
| Itambitse | 1200×800 | `https://picsum.org/1200/800` |
| Ihagaze | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Ubusabe bwa mbere bw’ingano nshya, cyangwa bw’ihuriro rishya ry’ibara ry’ikijuju na gupfuka, bushobora gutinda gato. Nyuma y’aho, dosiye ifunze irabikwa.

<a id="json"></a>

## Amakuru ya JSON

Nta nzira ya `/list` ya v1. Icyegeranyo kiragaragazwa kuri `/v2/list`.

`/v2/list` igarura urutonde rwa JSON. `/id/{id}/info` na `/seed/{seed}/info` bigarura ikintu cya JSON kimwe. Zose zitatu zohereza `Cache-Control: public, max-age=300` na `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Urutonde rw’amafoto

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Ikipimo | Itegeko |
| --- | --- |
| `page` | Umubare wuzuye ungana cyangwa uruta 1. Isanzwe ni `1`. |
| `limit` | Umubare wuzuye kuva kuri 1 kugera ku 100. Isanzwe ni `30`. |
| `tag` | Umurongo w’insanganyamatsiko utari ngombwa. |
| `category` | ID y’icyiciro itari ngombwa. |

Imitwe y’igisubizo:

- `Link`, ikoresheje `rel="next"` kandi, iyo hari urupapuro rubanziriza, `rel="prev"`.
- `Picsum-Total`, umubare w’amafoto ahuye. Iyo nta `tag` na nta `category`, agaciro ni `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Ubusabe bw’urupapuro rwa 1 bufite `limit=1` bwagaruye uyu mutwe `Link` na `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Umubiri ni urutonde rw’ikintu gisobanurwa mu [Imyanya y’ikintu](#fields). Buri kintu ni ifoto imwe. Urutonde rushobora guhinduka; ntufate umurongo wa mbere nk’ifoto idahinduka.

<a id="info-id"></a>

### Ifoto imwe ukoresheje ID

```http
GET https://picsum.org/id/{id}/info
```

ID izwi igarura `200` n’ikintu cya JSON kimwe. ID itazwi igarura `404` n’uyu mubiri nk’uko wanditswe:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Ifoto imwe ukoresheje seed

```http
GET https://picsum.org/seed/{seed}/info
```

Igisubizo ni `200` n’ikintu cya JSON kimwe, hamwe n’umutwe `Picsum-ID`. Seed itahuye n’ijambo ry’ishakisha ntisubiza ikosa. Igarura ifoto imwe idahinduka, nk’uko URL y’ifoto ya seed ibikora.

<a id="fields"></a>

### Imyanya y’ikintu

| Umwanya | Ibisobanuro |
| --- | --- |
| `id` | ID y’ifoto, nk’umurongo. |
| `author` | Izina ry’uwafashe ifoto. Umurongo ushobora kuba ubusa. |
| `width` | Ubugari bw’umwimerere mu pigiseli. Si ubugari wasabye ko ifoto igaragara. |
| `height` | Uburebure bw’umwimerere mu pigiseli. Si uburebure wasabye ko ifoto igaragara. |
| `description` | Ibisobanuro bigufi by’ifoto. |
| `category` | ID imwe y’icyiciro. |
| `tags` | Urutonde rw’imirongo y’insanganyamatsiko. |
| `url` | Urupapuro rw’aho ifoto yaturutse. |
| `license` | Umurongo nk’uko uri `"CC0 1.0"`. |
| `license_url` | Umurongo nk’uko uri `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | Ihuza rya JPEG ry’iyi foto muri 800×600. |

Kora URL ya WebP cyangwa y’ibara ry’ikijuju uvuye kuri `id`. `download_url` ihora ari JPEG ya 800×600.

<a id="examples"></a>

### Ingero

`GET https://picsum.org/id/179363399/info` igarura:

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

Ifoto ifite 3840×2160, yafashwe na Syony, iri muri `landscapes`, isobanuwe nka “Colorful mountain slopes in Landmannalaugar”. Amagambo y’ishakisha ni `mountains`, `highlands`, `colorful`, na `iceland`.

`GET https://picsum.org/seed/studio/info` igarura:

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

Umutwe w’igisubizo `Picsum-ID` ni `1000561303`. Ifoto y’umwimerere ifite 2400×1800, `author` ni ubusa, kandi `category` ni `food`.

<a id="categories"></a>

## Ibyiciro

Ohereza imwe muri izi ID ukoresheje `category`. Nta nzira ya HTTP ifunguye `/categories`. Amazina agiye hasi ni ubuhinduzi bw’abasoma iyi nyandiko. Igikoresho cya MCP `list_categories` kigarura izo ID nyine, buri imwe ifite izina ry’icyongereza rigaragara n’itsinda. Ibyifuzo bigomba kohereza ID, atari izina rigaragara.

### Kamere n’imiterere y’ahantu

| ID | Izina |
| --- | --- |
| `coasts` | Inkombe n’inyanja |
| `deserts` | Ubutayu n’imisozi y’umucanga |
| `freshwater` | Ibiyaga n’amasumo |
| `gardens` | Ubusitani |
| `landscapes` | Imiterere y’ahantu |
| `macro` | Amafoto y’ibintu bito yafashwe hafi |
| `mountains` | Imisozi |
| `plants` | Ibimera n’indabo |
| `skies` | Ijuru n’ikirere |
| `snow` | Urubura |
| `woodlands` | Amashyamba |

### Amatungo n’inyamaswa

| ID | Izina |
| --- | --- |
| `animals` | Izindi nyamaswa |
| `birds` | Inyoni |
| `insects` | Udukoko |
| `marine` | Ibinyabuzima byo mu nyanja |
| `pets` | Amatungo yo mu rugo |

### Ahantu n’ingendo

| ID | Izina |
| --- | --- |
| `aerial` | Amafoto yafatiwe mu kirere |
| `architecture` | Imyubakire |
| `city` | Imijyi n’imihanda |
| `interiors` | Imbere mu nyubako |
| `landmarks` | Ahantu hazwi |
| `night` | Amafoto yafashwe nijoro |
| `transport` | Ubwikorezi |

### Ibintu n’ibikorwa

| ID | Izina |
| --- | --- |
| `agriculture` | Ubuhinzi |
| `food` | Ibiribwa n’ibinyobwa |
| `industry` | Inganda |
| `music` | Umuziki |
| `objects` | Ibintu |
| `sculpture` | Ibishushanyo bibajwe |
| `sports` | Imikino |
| `technology` | Ikoranabuhanga |
| `textures` | Imiterere y’ubuso |
| `workspaces` | Ahakorerwa |

<a id="headers"></a>

## Imitwe, kubika, na CORS

Ibisubizo by’amafoto na bya JSON byohereza:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` irimo `Picsum-ID`, `Picsum-Total`, na `Link`, bityo urupapuro ruri ku rundi rubuga rushobora gusoma iyo mitwe itatu ukoresheje `fetch`.

| Igisubizo | `Cache-Control` |
| --- | --- |
| Igisubizo cya `302` cy’amafoto atoranywa ku buryo bw’amahirwe, `/{width}` cyangwa `/{width}/{height}` | `no-store` |
| Igisubizo cya `302` cya seed, `/seed/{seed}/...` | `public, max-age=3600` |
| Ifoto ifunze, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Igisubizo cy’amafoto atoranywa ku buryo bw’amahirwe gifite `no-store`, bityo ubusabe bukurikira bushobora guhitamo iyindi ifoto. URL ya `/id/...` iri muri `Location` ni dosiye ishobora kubikwa. Ubusabe bwa mbere bw’ingano nshya cyangwa bw’ihuriro rishya ry’ibara ry’ikijuju na gupfuka bushobora gutinda gato, mbere y’uko iyo dosiye ibikwa.

Amakosa ya JSON ya 400 na 404 yanditswe hasi nayo yoherezwa hamwe na `Cache-Control: no-store` na `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Amakosa n’imipaka y’ubusabe

Imibiri y’amakosa ni JSON. Hura n’iyi mirongo ya `error` nk’uko yanditswe.

Ingano z’ifoto zitemewe, umugereka utemerewe, cyangwa agaciro ka `blur` kari hanze ya 1 kugera ku 10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`page` cyangwa `limit` itemewe kuri `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

ID y’ifoto itazwi kuri `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 bisobanura ko umupaka w’ubusabe wakoreshejwe. Kurikiza umutwe w’igisubizo `Retry-After`. Ntukohereze ubusabe bukora ubwabyo bubangamira serivisi, kandi ntunyure imipaka y’ubusabe.

<a id="code"></a>

## Ingero za kode

<a id="html"></a>

### HTML

Shyira `width`, `height`, na `alt`. `alt` igomba gusobanura ifoto. Ibisobanuro biri hasi ni `description` y’ifoto `179363399`.

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

Itegeko rya mbere ryerekana imitwe y’igisubizo cya `302` cya seed, harimo `Location` na `Picsum-ID`, kandi ntiribika ifoto. Itegeko rya kabiri ryerekana ikintu cy’ifoto imwe. Itegeko rya gatatu ryerekana imitwe y’urutonde n’urutonde rwa JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` ishobora guhamagara inzira za JSON mu mushakisha kuko `Access-Control-Allow-Origin` ari `*`. `Picsum-Total` yerekanwe, bityo `headers.get` ishobora kuyisoma.

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

Iki gitekerezo gikoresha isomero `requests`.

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

## Uruhushya n’ikoreshwa mu bucuruzi

Amafoto afite [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Buri ifoto ya CC0 ikoreshwa ku buntu, haba mu mirimo yawe bwite cyangwa iy’ubucuruzi. Kuvuga uwafashe ifoto ni ubushake. Iyo ushaka kwerekana uwafashe ifoto, `author` ni uwafashe ifoto kandi `url` ni urupapuro yaturutseho, byombi biri mu kintu cya JSON.

Iyo ikoreshwa risaba kwitonda, ni wowe ubazwa abantu bashobora kumenyekana, ibirango by’ubucuruzi, n’inyandiko y’aho ifoto yaturutse. Reba `url` mbere y’ubwo bwoko bw’ikoreshwa.

Ntukongere kugurisha cyangwa gukwirakwiza iyi serivisi nk’API yawe y’amafoto.

Ibibazo: [hello@picsum.org](mailto:hello@picsum.org).

Amabwiriza yo gukoresha serivisi: [Amabwiriza yo gukoresha serivisi](https://picsum.org/rw/terms).

<a id="mcp"></a>

## Seriveri ya MCP

Seriveri ya MCP yatanzwe isubiza ibibazo by’amafoto asomwa gusa, ku bakiriya bakoresha Model Context Protocol. Ntisimbuza amahuza y’amafoto ari hejuru, kandi ntikora amafoto ashingiye ku mwandiko. Amahuza y’amafoto aguma kuri `https://picsum.org/{...}`. Aderesi ya MCP ni iyindi.

| | |
| --- | --- |
| Aderesi | `https://picsum.org/mcp` |
| Itumanaho | Streamable HTTP |
| Kwemeza | OAuth 2.1 hamwe na PKCE |
| Ububasha | `photos:read` |
| Inyandiko yo gushyiraho | [Huza umufasha wawe wa AI na Picsum](https://picsum.org/rw/connect) |
| Igenamiterere ry’umukiriya | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Ibikoresho bisoma gusa:

| Igikoresho | Icyo gikora |
| --- | --- |
| `search_photos` | Ishakisha ukoresheje `tag`, `category`, cyangwa byombi. |
| `get_photo` | Amakuru y’ID imwe y’ifoto. |
| `list_categories` | Buri ID y’icyiciro, ifite izina ry’icyongereza rigaragara n’itsinda. |
| `build_image_url` | URL y’ifoto, n’igice cya HTML `<img>`, ku ngingo yahiswemo, imiterere ya dosiye, ibara ry’ikijuju, na gupfuka. |

Kwinjira no gushyiraho umukiriya bisobanurwa ku [Huza umufasha wawe wa AI na Picsum](https://picsum.org/rw/connect). Izindi ndimi zikoresha inzira imwe `/connect` munsi y’intangiriro y’ururimi rwazo. Ingero z’igenamiterere ziri muri [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
