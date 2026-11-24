**English** · [العربية](docs/ar.md) · [Čeština](docs/cs.md) · [Deutsch](docs/de.md) · [Español](docs/es.md) · [Eesti](docs/et.md) · [हिन्दी](docs/hi.md) · [Bahasa Indonesia](docs/id.md) · [日本語](docs/ja.md) · [한국어](docs/ko.md) · [Lietuvių](docs/lt.md) · [Nederlands](docs/nl.md) · [Polski](docs/pl.md) · [Português (Portugal)](docs/pt-PT.md) · [Ikinyarwanda](docs/rw.md) · [Svenska](docs/sv.md) · [Türkçe](docs/tr.md) · [Українська](docs/uk.md) · [اردو](docs/ur.md) · [Tiếng Việt](docs/vi.md) · [繁體中文](docs/zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/) is a free placeholder-photo API. It serves **100,000 photographs** under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) in **33 categories**. Image URLs, custom sizes, JPEG and WebP, grayscale, blur, and the JSON metadata endpoints do not need an account or an API key.

Lorem Picsum (`picsum.org`) is an independent service inspired by the open-source Picsum Photos project. It is not affiliated with `picsum.photos`. It has its own catalog and its own photo IDs. Paths from that other project, including a grayscale path such as `/g/{width}/{height}`, are not part of this API.

The API base URL is `https://picsum.org`. Do not put a website locale in front of an API path. `https://picsum.org/de/800/600` is a website route, not an image URL. Locale prefixes (`/de`, `/ja`, `/zh-tw`, and the rest) belong to pages such as the homepage, the MCP setup guide, and the terms.

## Contents

- [Overview](#overview)
- [Quick start](#quick-start)
- [Image URLs](#image-urls)
- [JSON metadata](#json)
- [Categories](#categories)
- [Headers, caching, and CORS](#headers)
- [Errors and rate limits](#errors)
- [Code examples](#code)
- [License and commercial use](#license)
- [MCP server](#mcp)

<a id="overview"></a>

## Overview

Request an image URL when a layout needs a picture. Request JSON when you need the author, description, category, tags, original dimensions, source page, or license.

A random URL can select a different photo on every request. A seed, or a photo ID, keeps the same source photograph. Width and height are integers from **1 to 2000** pixels. Every custom size in that range is free, and so are grayscale and blur. The six sizes on the homepage are convenience presets, not a cap.

<a id="quick-start"></a>

## Quick start

This random 800×600 image redirects to a specific photo. The redirect is not stored by caches, and the response carries the chosen ID in `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Use a pinned URL when the picture must stay put:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Use a seed when the picture must be repeatable. The same seed maps to the same source photo at every size. The seed `studio` maps to `1000561303`. This example asks for WebP, grayscale, and blur:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Image URLs

<a id="dimensions"></a>

### Dimensions and cropping

`width` and `height` are path segments. Each one is an integer from 1 to 2000 inclusive. The service scales the photograph and center-crops it so the requested rectangle is filled. The picture is not stretched.

<a id="formats"></a>

### Formats

| Extension | What you get |
| --- | --- |
| *(none)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif`, and `.avif` are not accepted. The response is HTTP 400 and the image error object below. `.jpeg` is not an alias of `.jpg`.

<a id="random-rectangle"></a>

### Random rectangle

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

The response is `302 Found`. `Location` is `/id/{id}/{width}/{height}.{ext}`. When the extension is omitted, `{ext}` is `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` is the photo that was selected

`GET https://picsum.org/800/600` is the standard preset in this form.

<a id="random-square"></a>

### Random square

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` requests a 640×640 JPEG. The response is `302` to `/id/{id}/{width}/{width}.jpg`, with `Cache-Control: no-store` and a `Picsum-ID` header.

<a id="seeded"></a>

### Seeded photo

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

The response is `302` to `/id/{id}/{width}/{height}.{ext}`. A square seed URL uses the same number for width and height. An omitted extension is `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` is the selected photo
- One seed always selects the same source photo, including when the size changes. `studio` selects `1000561303`.
- The seed is also a subject word. `GET https://picsum.org/seed/cat/800/600` selects a cat photograph.
- If the seed matches no tag, the service falls back to one stable photograph from the collection. The same unknown seed keeps returning that same photograph.

<a id="pinned"></a>

### Pinned photo

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

The response is `200 OK` and the image bytes, `image/jpeg` or `image/webp`. A square path uses one dimension for both sides. An omitted extension is JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` echoes `{id}`

To read the author and the source page for an ID, call [`/id/{id}/info`](#info-id). That metadata route, not the image route, is the documented `404` for an unknown ID.

<a id="query"></a>

### Query parameters

| Parameter | Where it applies | Rule |
| --- | --- | --- |
| `tag` | Random images, seeded images, and `GET /v2/list` | Subject string. It narrows the pool. Example: `?tag=forest`. |
| `category` | Random images, seeded images, and `GET /v2/list` | One of the 33 category IDs. Example: `?category=woodlands`. |
| `grayscale` | Image URLs | Flag form `?grayscale`. Grayscale is baked into the image file. There is no `/g/{width}/{height}` path. |
| `blur` | Image URLs | Integer from 1 to 10. A bare `?blur` is accepted and means `blur=5`. `blur=0` and `blur=11` return HTTP 400. |

`tag` and `category` are used while the photo is being chosen. They are not copied onto the redirect `Location`.

Grayscale and blur travel with the image. This seeded request:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

responds `302` with:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

The flag `grayscale` is written as `grayscale=1` on that pinned URL. `blur=4` is kept. The file itself is grayscale and blurred; this is not a CSS filter.

<a id="presets"></a>

### Homepage size presets

These six sizes are the presets shown on the homepage. Any other size from 1 to 2000 is free as well.

| Preset | Pixels | URL |
| --- | --- | --- |
| Standard | 800×600 | `https://picsum.org/800/600` |
| Square | 640×640 | `https://picsum.org/640` |
| Landscape | 1200×800 | `https://picsum.org/1200/800` |
| Portrait | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

The first request for a new size, or a new grayscale or blur combination, can take a little longer. After that, the pinned file is cached.

<a id="json"></a>

## JSON metadata

There is no `/list` v1 endpoint. The collection is listed at `/v2/list`.

`/v2/list` returns a JSON array. `/id/{id}/info` and `/seed/{seed}/info` return one JSON object. All three send `Cache-Control: public, max-age=300` and `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### List photos

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Query | Rule |
| --- | --- |
| `page` | Integer greater than or equal to 1. Default `1`. |
| `limit` | Integer from 1 to 100. Default `30`. |
| `tag` | Optional subject string. |
| `category` | Optional category ID. |

Response headers:

- `Link`, using `rel="next"` and, when a previous page exists, `rel="prev"`.
- `Picsum-Total`, the number of photos that match. With no `tag` and no `category`, the value is `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

A page-1 request with `limit=1` returned this `Link` header and `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

The body is an array of the object described in [Object fields](#fields). Each element is one photo. Order can change; do not treat the first row as a fixed photo.

<a id="info-id"></a>

### One photo by ID

```http
GET https://picsum.org/id/{id}/info
```

A known ID returns `200` and one JSON object. An unknown ID returns `404` and this exact body:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### One photo by seed

```http
GET https://picsum.org/seed/{seed}/info
```

The response is `200` and one JSON object, plus a `Picsum-ID` header. A seed that matches no tag does not return an error. It returns the same stable fallback photo as the seeded image URL.

<a id="fields"></a>

### Object fields

| Field | Meaning |
| --- | --- |
| `id` | Photo ID, as a string. |
| `author` | Creator name. The string can be empty. |
| `width` | Original width in pixels. This is not the width you asked to render. |
| `height` | Original height in pixels. This is not the height you asked to render. |
| `description` | Short description of the photograph. |
| `category` | One category ID. |
| `tags` | Array of subject strings. |
| `url` | Page of the original source. |
| `license` | The exact string `"CC0 1.0"`. |
| `license_url` | The exact string `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | JPEG URL of this photo at 800×600. |

Build a WebP or grayscale URL from `id`. `download_url` is always the 800×600 JPEG.

<a id="examples"></a>

### Examples

`GET https://picsum.org/id/179363399/info` returns:

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

The photograph is 3840×2160, by Syony, in `landscapes`, described as “Colorful mountain slopes in Landmannalaugar”. The tags are `mountains`, `highlands`, `colorful`, and `iceland`.

`GET https://picsum.org/seed/studio/info` returns:

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

The response header `Picsum-ID` is `1000561303`. The original frame is 2400×1800, `author` is empty, and `category` is `food`.

<a id="categories"></a>

## Categories

Pass one of these IDs in `category`. There is no public HTTP `/categories` endpoint. The MCP tool `list_categories` returns the same IDs, each with the English display name and a group. Send the ID, not the display name.

### Nature and landscapes

| ID | Name |
| --- | --- |
| `coasts` | Coasts & oceans |
| `deserts` | Deserts & dunes |
| `freshwater` | Lakes & waterfalls |
| `gardens` | Gardens |
| `landscapes` | Landscapes |
| `macro` | Macro |
| `mountains` | Mountains |
| `plants` | Plants & flowers |
| `skies` | Skies & weather |
| `snow` | Snow & ice |
| `woodlands` | Woodlands |

### Animals

| ID | Name |
| --- | --- |
| `animals` | Other animals |
| `birds` | Birds |
| `insects` | Insects |
| `marine` | Marine life |
| `pets` | Pets |

### Places and travel

| ID | Name |
| --- | --- |
| `aerial` | Aerial |
| `architecture` | Architecture |
| `city` | Cities & streets |
| `interiors` | Interiors |
| `landmarks` | Landmarks |
| `night` | Night |
| `transport` | Transport |

### Objects and activities

| ID | Name |
| --- | --- |
| `agriculture` | Agriculture |
| `food` | Food & drink |
| `industry` | Industry |
| `music` | Music |
| `objects` | Objects |
| `sculpture` | Sculpture |
| `sports` | Sports |
| `technology` | Technology |
| `textures` | Textures |
| `workspaces` | Workspaces |

<a id="headers"></a>

## Headers, caching, and CORS

Image and JSON responses send:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` includes `Picsum-ID`, `Picsum-Total`, and `Link`, so a page on another origin can read those three headers from `fetch`.

| Response | `Cache-Control` |
| --- | --- |
| Random redirect, `/{width}` or `/{width}/{height}` | `no-store` |
| Seeded redirect, `/seed/{seed}/...` | `public, max-age=3600` |
| Pinned image, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

A random redirect is `no-store`, so the next request can select another photo. The `/id/...` URL in `Location` is the cacheable file. The first request for a new size or effect can take a little longer, before that file is cached.

The 400 and 404 JSON errors documented below are also sent with `Cache-Control: no-store` and `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Errors and rate limits

Error bodies are JSON. Match these `error` strings exactly.

Invalid image dimensions, an unsupported extension, or a blur value outside 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Invalid `page` or `limit` on `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Unknown photo ID on `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 means the rate limit applied. Honor the `Retry-After` response header. Do not run automated traffic that degrades the service, and do not circumvent rate limits.

<a id="code"></a>

## Code examples

<a id="html"></a>

### HTML

Set `width`, `height`, and `alt`. `alt` should describe the photograph. The description below is the `description` of photo `179363399`.

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

The first command prints the seeded redirect headers, including `Location` and `Picsum-ID`, and does not save the image. The second prints one photo object. The third prints list headers and a JSON array.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` can call the JSON endpoints from a browser because `Access-Control-Allow-Origin` is `*`. `Picsum-Total` is exposed, so `headers.get` can read it.

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

This example uses the `requests` library.

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

## License and commercial use

The photographs are [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Personal use and commercial use are free. Attribution is optional. When you want to credit a photo, `author` is the creator and `url` is the source page, both in the JSON object.

You are responsible for recognizable people, trademarks, and the original source record when a use is sensitive. Check `url` before that kind of use.

Do not resell or redistribute this service as your own image API.

Questions: [hello@picsum.org](mailto:hello@picsum.org).

Terms of service: [https://picsum.org/terms](https://picsum.org/terms).

<a id="mcp"></a>

## MCP server

A hosted MCP server answers read-only photo queries for clients that speak the Model Context Protocol. It does not replace the image URLs above, and it does not generate pictures from a text prompt. Image URLs stay on `https://picsum.org/{...}`. The MCP endpoint is separate.

| | |
| --- | --- |
| Endpoint | `https://picsum.org/mcp` |
| Transport | Streamable HTTP |
| Authorization | OAuth 2.1 with PKCE |
| Scope | `photos:read` |
| Setup guide | [Connect Claude Code, Codex and Grok Bot](https://picsum.org/connect) |
| Client configuration | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

The tools are read-only:

| Tool | What it does |
| --- | --- |
| `search_photos` | Search by `tag`, by `category`, or by both. |
| `get_photo` | Metadata for one photo ID. |
| `list_categories` | Every category ID, with its English display name and group. |
| `build_image_url` | An image URL, and an HTML `<img>` snippet, for a chosen size, format, grayscale, and blur. |

Sign-in and client setup are documented on the [setup guide](https://picsum.org/connect). Pages in other languages use a locale prefix, for example [https://picsum.org/de/connect](https://picsum.org/de/connect). The configuration examples live in [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
