[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · **Lietuvių** · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/lt) yra nemokamas atsitiktinių vaizdų generatorius. Jis pateikia **100 000** CC0 nuotraukų **33 kategorijose** pagal [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Be paskyros ir be API rakto veikia vaizdų nuorodos, pasirinktiniai matmenys, JPEG ir WebP, pilkieji atspalviai, suliejimas ir JSON metaduomenų galiniai taškai.

Lorem Picsum (`picsum.org`) yra savarankiška paslauga, įkvėpta atvirojo kodo projekto „Picsum Photos“. Ji nėra susijusi su `picsum.photos`. Ji turi savo katalogą ir savo nuotraukų ID. Kito projekto keliai, tarp jų pilkųjų atspalvių kelias `/g/{width}/{height}`, šiai API nepriklauso.

API bazinis adresas yra `https://picsum.org`. Svetainės lokalės prieš API kelią nedėkite. `https://picsum.org/de/800/600` yra svetainės maršrutas, ne vaizdo nuoroda. Lokalės priešdėliai (`/de`, `/ja`, `/zh-tw` ir kiti) skirti svetainės puslapiams: pagrindiniam puslapiui, MCP sąrankos vadovui ir naudojimosi sąlygoms.

## Turinys

- [Apžvalga](#overview)
- [Greita pradžia](#quick-start)
- [Vaizdų nuorodos](#image-urls)
- [JSON metaduomenys](#json)
- [Kategorijos](#categories)
- [Antraštės, podėlis ir CORS](#headers)
- [Klaidos ir užklausų limitai](#errors)
- [Kodo pavyzdžiai](#code)
- [Licencija ir komercinis naudojimas](#license)
- [MCP serveris](#mcp)

<a id="overview"></a>

## Apžvalga

Kai maketui reikia nuotraukos, naudokite vaizdo nuorodą. Kai reikia autoriaus, aprašymo, kategorijos, žymų, originalių matmenų, šaltinio puslapio ar licencijos, naudokite JSON.

Atsitiktinė nuoroda kiekvienoje užklausoje gali parinkti kitą nuotrauką. Su pradine reikšme arba nuotraukos ID šaltinio nuotrauka lieka ta pati. Plotis ir aukštis yra sveikieji skaičiai nuo **1** iki **2000** pikselių. Visi pasirinktiniai matmenys šiame intervale nemokami, kaip ir pilkieji atspalviai bei suliejimas. Šeši pagrindinio puslapio matmenys yra patogios parinktys, o ne viršutinė riba.

<a id="quick-start"></a>

## Greita pradžia

Šis atsitiktinis 800×600 vaizdas peradresuoja į konkrečią nuotrauką. Peradresavimas podėlyje nekaupiamas, o atsakyme pasirinktas ID pateikiamas antraštėje `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Fiksuotą nuorodą naudokite, kai nuotrauka turi nesikeisti:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Pradinę reikšmę naudokite, kai tą patį vaizdą reikia pakartoti. Ta pati reikšmė visuose matmenyse atitinka tą pačią šaltinio nuotrauką. Reikšmė `studio` atitinka `1000561303`. Šiame pavyzdyje prašoma WebP, pilkųjų atspalvių ir suliejimo:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Vaizdų nuorodos

<a id="dimensions"></a>

### Matmenys ir apkarpymas

`width` ir `height` yra kelio segmentai. Abu yra sveikieji skaičiai nuo 1 iki 2000 imtinai. Paslauga keičia nuotraukos mastelį ir apkarpo ją nuo centro, kad prašomas stačiakampis būtų užpildytas. Vaizdas neištempiamas.

<a id="formats"></a>

### Formatai

| Plėtinys | Ką gaunate |
| --- | --- |
| *(nėra)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

Plėtiniai `.png`, `.jpeg`, `.gif` ir `.avif` nepriimami. Atsakymas yra HTTP 400 ir žemiau pateiktas vaizdo klaidos objektas. `.jpeg` nėra `.jpg` sinonimas.

<a id="random-rectangle"></a>

### Atsitiktinis stačiakampis

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Atsakymas yra `302 Found`. `Location` yra `/id/{id}/{width}/{height}.{ext}`. Kai plėtinys praleistas, `{ext}` yra `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` nurodo parinktą nuotrauką

`GET https://picsum.org/800/600` yra standartinė šios formos parinktis.

<a id="random-square"></a>

### Atsitiktinis kvadratas

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` yra 640×640 JPEG užklausa. Atsakymas yra `302` ir nukreipia į `/id/{id}/{width}/{width}.jpg`, su `Cache-Control: no-store` ir antrašte `Picsum-ID`.

<a id="seeded"></a>

### Nuotrauka su pradine reikšme

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Atsakymas yra `302` ir nukreipia į `/id/{id}/{width}/{height}.{ext}`. Kvadratinėje nuorodoje su pradine reikšme plotis ir aukštis yra tas pats skaičius. Praleistas plėtinys yra `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` nurodo parinktą nuotrauką
- Viena pradinė reikšmė visada parenka tą pačią šaltinio nuotrauką, taip pat ir pakeitus matmenis. `studio` parenka `1000561303`.
- Pradinė reikšmė veikia ir kaip temos žodis. `GET https://picsum.org/seed/cat/800/600` parenka katės nuotrauką.
- Jei reikšmė neatitinka nė vienos žymos, paslauga parenka vieną pastovią nuotrauką iš kolekcijos. Ta pati nežinoma reikšmė visada grąžina tą pačią nuotrauką.

<a id="pinned"></a>

### Fiksuota nuotrauka

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Atsakymas yra `200 OK`, o turinys – vaizdo baitai, `image/jpeg` arba `image/webp`. Kvadratiniame kelyje vienas matmuo taikomas abiem kraštinėms. Praleistas plėtinys reiškia JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` pakartoja `{id}`

Norėdami sužinoti autorių ir šaltinio puslapį pagal ID, kvieskite [`/id/{id}/info`](#info-id). Būtent šis metaduomenų kelias, o ne vaizdo kelias, yra dokumentuotas `404` nežinomam ID.

<a id="query"></a>

### Užklausos parametrai

| Parametras | Kur taikoma | Taisyklė |
| --- | --- | --- |
| `tag` | Atsitiktiniai vaizdai, vaizdai su pradine reikšme ir `GET /v2/list` | Temos eilutė. Ji susiaurina rinkinį. Pavyzdys: `?tag=forest`. |
| `category` | Atsitiktiniai vaizdai, vaizdai su pradine reikšme ir `GET /v2/list` | Vienas iš 33 kategorijų ID. Pavyzdys: `?category=woodlands`. |
| `grayscale` | Vaizdų nuorodos | Forma be reikšmės: `?grayscale`. Pilkieji atspalviai įrašomi į vaizdo failą. Kelio `/g/{width}/{height}` nėra. |
| `blur` | Vaizdų nuorodos | Sveikasis skaičius nuo 1 iki 10. Vien `?blur`, be reikšmės, priimamas ir reiškia `blur=5`. `blur=0` ir `blur=11` grąžina HTTP 400. |

`tag` ir `category` naudojami renkantis nuotrauką. Į peradresavimo `Location` jie neperkeliami.

Pilkieji atspalviai ir suliejimas perduodami kartu su vaizdu. Ši užklausa su pradine reikšme:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

atsako `302` ir pateikia:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Požymis `grayscale` toje fiksuotoje nuorodoje užrašomas kaip `grayscale=1`. `blur=4` išlieka. Pats failas pateikiamas pilkais atspalviais ir su suliejimu. Tai nėra CSS filtras.

<a id="presets"></a>

### Pagrindinio puslapio matmenų parinktys

Šie šeši matmenys rodomi pagrindiniame puslapyje. Bet kurie kiti matmenys nuo 1 iki 2000 taip pat nemokami.

| Parinktis | Pikseliai | Nuoroda |
| --- | --- | --- |
| Standartinis | 800×600 | `https://picsum.org/800/600` |
| Kvadratas | 640×640 | `https://picsum.org/640` |
| Horizontalus | 1200×800 | `https://picsum.org/1200/800` |
| Vertikalus | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Pirmoji naujų matmenų arba naujo pilkųjų atspalvių ar suliejimo derinio užklausa gali užtrukti šiek tiek ilgiau. Paskui fiksuotas failas laikomas podėlyje.

<a id="json"></a>

## JSON metaduomenys

Versijos v1 galinio taško `/list` nėra. Kolekcija pateikiama per `/v2/list`.

`/v2/list` grąžina JSON masyvą. `/id/{id}/info` ir `/seed/{seed}/info` grąžina vieną JSON objektą. Visi trys siunčia `Cache-Control: public, max-age=300` ir `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Nuotraukų sąrašas

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Užklausa | Taisyklė |
| --- | --- |
| `page` | Sveikasis skaičius, ne mažesnis kaip 1. Numatytoji reikšmė `1`. |
| `limit` | Sveikasis skaičius nuo 1 iki 100. Numatytoji reikšmė `30`. |
| `tag` | Neprivaloma temos eilutė. |
| `category` | Neprivalomas kategorijos ID. |

Atsakymo antraštės:

- `Link`, su `rel="next"` ir, kai yra ankstesnis puslapis, `rel="prev"`.
- `Picsum-Total` – atitinkančių nuotraukų skaičius. Be `tag` ir be `category` reikšmė yra `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Pirmo puslapio užklausa su `limit=1` grąžino šią `Link` antraštę ir `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Turinys yra masyvas objektų, aprašytų skyriuje [Objekto laukai](#fields). Kiekvienas elementas yra viena nuotrauka. Tvarka gali keistis. Pirmos eilutės nelaikykite fiksuota nuotrauka.

<a id="info-id"></a>

### Viena nuotrauka pagal ID

```http
GET https://picsum.org/id/{id}/info
```

Žinomas ID grąžina `200` ir vieną JSON objektą. Nežinomas ID grąžina `404` ir tiksliai šį turinį:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Viena nuotrauka pagal pradinę reikšmę

```http
GET https://picsum.org/seed/{seed}/info
```

Atsakymas yra `200` ir vienas JSON objektas, taip pat antraštė `Picsum-ID`. Pradinė reikšmė, neatitinkanti nė vienos žymos, klaidos negrąžina. Ji grąžina tą pačią pastovią atsarginę nuotrauką kaip ir vaizdo nuoroda su ta reikšme.

<a id="fields"></a>

### Objekto laukai

| Laukas | Reikšmė |
| --- | --- |
| `id` | Nuotraukos ID, pateiktas kaip eilutė. |
| `author` | Kūrėjo vardas. Eilutė gali būti tuščia. |
| `width` | Originalus plotis pikseliais. Tai nėra plotis, kurį prašėte atvaizduoti. |
| `height` | Originalus aukštis pikseliais. Tai nėra aukštis, kurį prašėte atvaizduoti. |
| `description` | Trumpas nuotraukos aprašymas. |
| `category` | Vienas kategorijos ID. |
| `tags` | Temos eilučių masyvas. |
| `url` | Originalaus šaltinio puslapis. |
| `license` | Tiksli eilutė `"CC0 1.0"`. |
| `license_url` | Tiksli eilutė `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | Šios nuotraukos JPEG nuoroda 800×600 matmenimis. |

WebP arba pilkųjų atspalvių nuorodą sudarykite iš `id`. `download_url` visada yra 800×600 JPEG.

<a id="examples"></a>

### Pavyzdžiai

`GET https://picsum.org/id/179363399/info` grąžina:

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

Nuotrauka yra 3840×2160, autorius Syony, kategorija `landscapes`, aprašymas – „Colorful mountain slopes in Landmannalaugar“. Žymos yra `mountains`, `highlands`, `colorful` ir `iceland`.

`GET https://picsum.org/seed/studio/info` grąžina:

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

Atsakymo antraštė `Picsum-ID` yra `1000561303`. Originalus kadras yra 2400×1800, `author` yra tuščias, o `category` yra `food`.

<a id="categories"></a>

## Kategorijos

Į parametrą `category` perduokite vieną iš šių ID. Viešo HTTP galinio taško `/categories` nėra. MCP įrankis `list_categories` grąžina tuos pačius ID, kiekvieną su anglišku rodomu pavadinimu ir grupe. Šių lentelių pavadinimai yra vertimai skaitytojams. Užklausoje siųskite ID, ne rodomą pavadinimą.

### Gamta ir kraštovaizdžiai

| ID | Pavadinimas |
| --- | --- |
| `coasts` | Pakrantės ir vandenynai |
| `deserts` | Dykumos ir kopos |
| `freshwater` | Ežerai ir kriokliai |
| `gardens` | Sodai |
| `landscapes` | Kraštovaizdžiai |
| `macro` | Makrofotografija |
| `mountains` | Kalnai |
| `plants` | Augalai ir gėlės |
| `skies` | Dangus ir orai |
| `snow` | Sniegas ir ledas |
| `woodlands` | Miškai |

### Gyvūnai

| ID | Pavadinimas |
| --- | --- |
| `animals` | Kiti gyvūnai |
| `birds` | Paukščiai |
| `insects` | Vabzdžiai |
| `marine` | Jūrų gyvūnija |
| `pets` | Augintiniai |

### Vietos ir kelionės

| ID | Pavadinimas |
| --- | --- |
| `aerial` | Aerofotografija |
| `architecture` | Architektūra |
| `city` | Miestai ir gatvės |
| `interiors` | Interjeras |
| `landmarks` | Lankytinos vietos |
| `night` | Naktinė fotografija |
| `transport` | Transportas |

### Daiktai ir veiklos

| ID | Pavadinimas |
| --- | --- |
| `agriculture` | Žemės ūkis |
| `food` | Maistas ir gėrimai |
| `industry` | Pramonė |
| `music` | Muzika |
| `objects` | Daiktai |
| `sculpture` | Skulptūros |
| `sports` | Sportas |
| `technology` | Technologijos |
| `textures` | Tekstūros |
| `workspaces` | Darbo erdvės |

<a id="headers"></a>

## Antraštės, podėlis ir CORS

Vaizdų ir JSON atsakymai siunčia:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

Į `Access-Control-Expose-Headers` įeina `Picsum-ID`, `Picsum-Total` ir `Link`, todėl kitos kilmės puslapis šias tris antraštes gali perskaityti per `fetch`.

| Atsakymas | `Cache-Control` |
| --- | --- |
| Atsitiktinis peradresavimas, `/{width}` arba `/{width}/{height}` | `no-store` |
| Peradresavimas su pradine reikšme, `/seed/{seed}/...` | `public, max-age=3600` |
| Fiksuotas vaizdas, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Atsitiktinis peradresavimas yra `no-store`, todėl kita užklausa gali parinkti kitą nuotrauką. Adresas `/id/...` antraštėje `Location` yra failas, kurį galima laikyti podėlyje. Pirmoji naujų matmenų ar efekto užklausa gali užtrukti šiek tiek ilgiau, kol tas failas dar nėra podėlyje.

Žemiau aprašytos 400 ir 404 JSON klaidos taip pat siunčiamos su `Cache-Control: no-store` ir `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Klaidos ir užklausų limitai

Klaidų turiniai yra JSON. Šias `error` eilutes lyginkite tiksliai.

Netinkami vaizdo matmenys, nepalaikomas plėtinys arba suliejimo reikšmė už 1–10 ribų (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Netinkamas `page` arba `limit` užklausoje `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Nežinomas nuotraukos ID kelyje `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 reiškia, kad pritaikytas užklausų limitas. Laikykitės atsakymo antraštės `Retry-After`. Nevykdykite automatinio srauto, kuris blogina paslaugą, ir neapeikite užklausų limitų.

<a id="code"></a>

## Kodo pavyzdžiai

<a id="html"></a>

### HTML

Nustatykite `width`, `height` ir `alt`. `alt` turi aprašyti nuotrauką. Žemiau esantis tekstas yra nuotraukos `179363399` laukas `description`.

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

Pirmoji komanda išveda peradresavimo su pradine reikšme antraštes, įskaitant `Location` ir `Picsum-ID`, ir vaizdo neišsaugo. Antroji išveda vieną nuotraukos objektą. Trečioji išveda sąrašo antraštes ir JSON masyvą.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` gali kviesti JSON galinius taškus iš naršyklės, nes `Access-Control-Allow-Origin` yra `*`. Antraštė `Picsum-Total` yra atskleista, todėl `headers.get` gali ją perskaityti.

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

Šiame pavyzdyje naudojama biblioteka `requests`.

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

## Licencija ir komercinis naudojimas

Tai CC0 nuotraukos pagal [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Asmeninis ir komercinis naudojimas nemokamas. Autorystę nurodyti neprivaloma. Jei norite nurodyti autorystę, `author` yra kūrėjas, o `url` – šaltinio puslapis. Abu laukai yra JSON objekte.

Kai naudojimas jautrus, atsakote už atpažįstamus žmones, prekių ženklus ir pirminį šaltinio įrašą. Prieš tokį naudojimą patikrinkite `url`.

Neperparduokite ir neplatinkite šios paslaugos kaip savo vaizdų API.

Klausimai: [hello@picsum.org](mailto:hello@picsum.org).

Sąlygos: [Naudojimosi sąlygos](https://picsum.org/lt/terms).

<a id="mcp"></a>

## MCP serveris

Priglobtas MCP serveris atsako į tik skaitymo užklausas apie nuotraukas klientams, kurie naudoja Model Context Protocol. Jis nepakeičia aukščiau aprašytų vaizdų nuorodų ir negeneruoja vaizdų pagal teksto raginimą. Vaizdų nuorodos lieka `https://picsum.org/{...}`. MCP galinis taškas yra atskiras.

| | |
| --- | --- |
| Galinis taškas | `https://picsum.org/mcp` |
| Transportas | Streamable HTTP |
| Autorizacija | OAuth 2.1 su PKCE |
| Aprėptis | `photos:read` |
| Sąrankos vadovas | [Susiekite DI asistentą su „Picsum“](https://picsum.org/lt/connect) |
| Kliento konfigūracija | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Įrankiai skirti tik skaitymui:

| Įrankis | Ką daro |
| --- | --- |
| `search_photos` | Ieško pagal `tag`, pagal `category` arba pagal abu. |
| `get_photo` | Vienos nuotraukos metaduomenys pagal jos ID. |
| `list_categories` | Visi kategorijų ID su anglišku rodomu pavadinimu ir grupe. |
| `build_image_url` | Vaizdo nuoroda ir HTML fragmentas `<img>` pasirinktiems matmenims, formatui, pilkiesiems atspalviams ir suliejimui. |

Prisijungimas ir kliento sąranka aprašyti puslapyje [Susiekite DI asistentą su „Picsum“](https://picsum.org/lt/connect). Kitose kalbose tas pats kelias `/connect` eina po lokalės priešdėlio. Konfigūracijos pavyzdžiai yra [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
