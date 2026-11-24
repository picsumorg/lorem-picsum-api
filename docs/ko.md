[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · **한국어** · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/ko)은 실제 CC0 사진을 쓰는 무료 자리 표시자 사진 API이자 랜덤 이미지 생성기예요. [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 사진 **10만 장**을 **33개 카테고리**로 제공해요. 이미지 링크, 맞춤 크기, JPEG와 WebP, 회색조, 흐림, JSON 메타데이터 엔드포인트는 계정이나 API 키 없이 쓸 수 있어요.

Lorem Picsum (`picsum.org`)은 오픈소스 프로젝트 Picsum Photos에서 영감을 받은 독립 서비스예요. `picsum.photos`와는 제휴하지 않아요. 사진 모음과 사진 ID도 이 서비스의 것이에요. 그 프로젝트의 경로는 이 API에 없고, `/g/{width}/{height}` 같은 회색조 경로도 마찬가지예요.

API의 기본 URL은 `https://picsum.org`예요. API 경로 앞에 웹사이트 로케일을 붙이지 마세요. `https://picsum.org/de/800/600`은 웹사이트 경로이고, 이미지 URL이 아니에요. 로케일 접두사(`/de`, `/ja`, `/zh-tw` 등)는 홈페이지, MCP 설정 안내, 이용약관 같은 페이지에 쓰여요.

## 목차

- [개요](#overview)
- [빠른 시작](#quick-start)
- [이미지 URL](#image-urls)
- [JSON 메타데이터](#json)
- [카테고리](#categories)
- [헤더, 캐시, CORS](#headers)
- [오류와 요청 한도](#errors)
- [코드 예제](#code)
- [라이선스와 상업적 이용](#license)
- [MCP 서버](#mcp)

<a id="overview"></a>

## 개요

레이아웃에 사진이 필요하면 이미지 링크를 요청하세요. 촬영자, 설명, 카테고리, 태그, 원본 크기, 출처 페이지, 라이선스가 필요하면 JSON을 요청하세요.

랜덤 URL은 요청마다 다른 사진을 고를 수 있어요. 시드나 사진 ID를 쓰면 원본 사진은 같아요. 가로와 세로는 **1부터 2000**픽셀까지의 정수예요. 그 범위의 맞춤 크기는 모두 무료이고, 회색조와 흐림도 무료예요. 홈페이지의 여섯 가지 크기는 고르기 쉽게 둔 기본 크기일 뿐, 상한이 아니에요.

<a id="quick-start"></a>

## 빠른 시작

이 800×600 랜덤 이미지는 특정 사진으로 리다이렉트돼요. 리다이렉트는 캐시에 저장되지 않고, 응답의 `Picsum-ID`에는 고른 ID가 들어 있어요.

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

사진이 그대로 있어야 하면 고정 URL을 쓰세요.

```text
https://picsum.org/id/179363399/800/600.jpg
```

같은 사진을 반복해서 받으려면 시드를 쓰세요. 같은 시드는 크기가 달라도 같은 원본 사진에 연결돼요. 시드 `studio`는 `1000561303`에 연결돼요. 이 예제는 WebP, 회색조, 흐림을 함께 요청해요.

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## 이미지 URL

<a id="dimensions"></a>

### 크기와 자르기

`width`와 `height`는 경로 구간이에요. 각각 1 이상 2000 이하의 정수예요. 서비스는 사진을 키우거나 줄인 뒤 가운데를 기준으로 잘라, 요청한 직사각형을 채워요. 사진은 늘리지 않아요.

<a id="formats"></a>

### 형식

| 확장자 | 결과 |
| --- | --- |
| *(없음)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif`, `.avif`는 허용하지 않아요. 응답은 HTTP 400이고, 본문은 아래의 이미지 오류 객체예요. `.jpeg`는 `.jpg`의 별칭이 아니에요.

<a id="random-rectangle"></a>

### 랜덤 직사각형

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

응답은 `302 Found`예요. `Location`은 `/id/{id}/{width}/{height}.{ext}`예요. 확장자를 빼면 `{ext}`는 `jpg`예요.

- `Cache-Control: no-store`
- `Picsum-ID`는 선택된 사진이에요

`GET https://picsum.org/800/600`은 이 형식의 기본 크기예요.

<a id="random-square"></a>

### 랜덤 정사각형

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640`은 640×640 JPEG를 요청해요. 응답은 `/id/{id}/{width}/{width}.jpg`로 가는 `302`이고, `Cache-Control: no-store`와 `Picsum-ID` 헤더가 붙어요.

<a id="seeded"></a>

### 시드 사진

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

응답은 `/id/{id}/{width}/{height}.{ext}`로 가는 `302`예요. 정사각형 시드 URL은 가로와 세로에 같은 수를 써요. 확장자를 빼면 `jpg`예요.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID`는 선택된 사진이에요
- 시드 하나는 크기가 바뀌어도 항상 같은 원본 사진을 골라요. `studio`는 `1000561303`을 골라요.
- 시드는 주제 단어이기도 해요. `GET https://picsum.org/seed/cat/800/600`은 고양이 사진을 골라요.
- 시드와 맞는 태그가 없으면 컬렉션에서 정해 둔 사진 한 장으로 돌아가요. 시드가 같으면, 태그가 없어도 항상 그 사진을 돌려줘요.

<a id="pinned"></a>

### 고정 사진

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

응답은 `200 OK`와 이미지 바이트이고, 형식은 `image/jpeg` 또는 `image/webp`예요. 정사각형 경로는 치수 하나를 양쪽에 써요. 확장자를 빼면 JPEG예요.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID`에는 `{id}`가 그대로 실려요

촬영자와 출처 페이지를 보려면 [`/id/{id}/info`](#info-id)를 호출하세요. 알 수 없는 ID에 대해 문서에 적힌 `404`는 이미지 경로가 아니라 이 메타데이터 경로예요.

<a id="query"></a>

### 쿼리 매개변수

| 매개변수 | 쓰는 곳 | 규칙 |
| --- | --- | --- |
| `tag` | 랜덤 이미지, 시드 이미지, `GET /v2/list` | 주제 문자열이에요. 후보를 좁혀요. 예: `?tag=forest`. |
| `category` | 랜덤 이미지, 시드 이미지, `GET /v2/list` | 33개 카테고리 ID 중 하나예요. 예: `?category=woodlands`. |
| `grayscale` | 이미지 URL | `?grayscale`처럼 값 없이 붙이는 플래그예요. 회색조는 이미지 파일에 적용돼요. `/g/{width}/{height}` 경로는 없어요. |
| `blur` | 이미지 URL | 1부터 10까지의 정수예요. `?blur`만 적어도 되고, 그때는 `blur=5`를 뜻해요. `blur=0`과 `blur=11`은 HTTP 400을 돌려줘요. |

`tag`와 `category`는 사진을 고르는 동안 쓰여요. 리다이렉트의 `Location`에는 복사되지 않아요.

회색조와 흐림은 이미지와 함께 전달돼요. 예를 들어 이 시드 요청은

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

`302`로 응답하고, 헤더는 다음과 같아요.

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

플래그 `grayscale`은 그 고정 URL에서 `grayscale=1`로 적혀요. `blur=4`는 그대로예요. 파일 자체가 회색조이고 흐림이 들어가 있어요. CSS 필터가 아니에요.

<a id="presets"></a>

### 홈페이지 크기 기본값

이 여섯 가지가 홈페이지에 나오는 기본 크기예요. 1부터 2000까지의 다른 크기도 모두 무료예요.

| 기본 크기 | 픽셀 | URL |
| --- | --- | --- |
| 기본 | 800×600 | `https://picsum.org/800/600` |
| 정사각형 | 640×640 | `https://picsum.org/640` |
| 가로형 | 1200×800 | `https://picsum.org/1200/800` |
| 세로형 | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

새 크기나 새로운 회색조·흐림 조합은 처음 요청할 때 조금 더 걸릴 수 있어요. 그다음부터는 고정된 파일이 캐시돼요.

<a id="json"></a>

## JSON 메타데이터

`/list` v1 엔드포인트는 없어요. 컬렉션 목록은 `/v2/list`에 있어요.

`/v2/list`는 JSON 배열을 돌려줘요. `/id/{id}/info`와 `/seed/{seed}/info`는 JSON 객체 하나를 돌려줘요. 셋 모두 `Cache-Control: public, max-age=300`과 `Access-Control-Allow-Origin: *`를 보내요.

<a id="list"></a>

### 사진 목록

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| 쿼리 | 규칙 |
| --- | --- |
| `page` | 1 이상의 정수예요. 기본값은 `1`이에요. |
| `limit` | 1부터 100까지의 정수예요. 기본값은 `30`이에요. |
| `tag` | 선택 사항인 주제 문자열이에요. |
| `category` | 선택 사항인 카테고리 ID예요. |

응답 헤더:

- `Link`는 `rel="next"`를 쓰고, 이전 페이지가 있으면 `rel="prev"`도 써요.
- `Picsum-Total`은 조건에 맞는 사진 수예요. `tag`와 `category`가 없으면 값은 `100000`이에요.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

`limit=1`인 1페이지 요청은 아래 `Link` 헤더와 `Picsum-Total: 100000`을 돌려줬어요.

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

본문은 [객체 필드](#fields)에서 설명하는 객체의 배열이에요. 요소 하나가 사진 한 장이에요. 순서는 바뀔 수 있으니, 첫 행을 고정된 사진으로 두지 마세요.

<a id="info-id"></a>

### ID로 보는 사진 하나

```http
GET https://picsum.org/id/{id}/info
```

컬렉션에 있는 ID는 `200`과 JSON 객체 하나를 돌려줘요. 컬렉션에 없는 ID는 `404`와 이 본문을 그대로 돌려줘요.

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### 시드로 보는 사진 하나

```http
GET https://picsum.org/seed/{seed}/info
```

응답은 `200`과 JSON 객체 하나이고, `Picsum-ID` 헤더가 함께 와요. 태그와 맞지 않는 시드는 오류가 아니에요. 시드 이미지 URL과 같은 고정 대체 사진을 돌려줘요.

<a id="fields"></a>

### 객체 필드

| 필드 | 의미 |
| --- | --- |
| `id` | 사진 ID이며, 문자열이에요. |
| `author` | 촬영자 이름이에요. 빈 문자열일 수 있어요. |
| `width` | 원본 가로 픽셀이에요. 이미지로 만들 때 요청한 가로가 아니에요. |
| `height` | 원본 세로 픽셀이에요. 이미지로 만들 때 요청한 세로가 아니에요. |
| `description` | 사진에 대한 짧은 설명이에요. |
| `category` | 카테고리 ID 하나예요. |
| `tags` | 주제 문자열의 배열이에요. |
| `url` | 원본 출처 페이지예요. |
| `license` | 정확한 문자열 `"CC0 1.0"`이에요. |
| `license_url` | 정확한 문자열 `"https://creativecommons.org/publicdomain/zero/1.0/"`이에요. |
| `download_url` | 이 사진의 800×600 JPEG URL이에요. |

WebP나 회색조 URL은 `id`로 만드세요. `download_url`은 언제나 800×600 JPEG예요.

<a id="examples"></a>

### 예제

`GET https://picsum.org/id/179363399/info`는 다음을 돌려줘요.

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

이 사진은 3840×2160이고 촬영자는 Syony예요. 카테고리는 `landscapes`이고, 설명은 “Colorful mountain slopes in Landmannalaugar”예요. 태그는 `mountains`, `highlands`, `colorful`, `iceland`예요.

`GET https://picsum.org/seed/studio/info`는 다음을 돌려줘요.

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

응답 헤더 `Picsum-ID`는 `1000561303`이에요. 원본 프레임은 2400×1800이고, `author`는 비어 있으며, `category`는 `food`예요.

<a id="categories"></a>

## 카테고리

`category`에는 아래 ID 중 하나를 넣으세요. 공개 HTTP `/categories` 엔드포인트는 없어요. 이 표의 이름은 문서를 읽는 사람을 위한 번역이에요. MCP 도구 `list_categories`는 같은 ID를 영어 표시 이름과 그룹과 함께 돌려줘요. 요청에는 표시 이름이 아니라 ID를 보내세요.

### 자연과 풍경

| ID | 이름 |
| --- | --- |
| `coasts` | 해안과 바다 |
| `deserts` | 사막과 모래언덕 |
| `freshwater` | 호수와 폭포 |
| `gardens` | 정원 |
| `landscapes` | 풍경 |
| `macro` | 접사 사진 |
| `mountains` | 산 |
| `plants` | 식물과 꽃 |
| `skies` | 하늘과 날씨 |
| `snow` | 눈과 얼음 |
| `woodlands` | 숲 |

### 동물

| ID | 이름 |
| --- | --- |
| `animals` | 기타 동물 |
| `birds` | 새 |
| `insects` | 곤충 |
| `marine` | 해양 생물 |
| `pets` | 반려동물 |

### 장소와 여행

| ID | 이름 |
| --- | --- |
| `aerial` | 항공 사진 |
| `architecture` | 건축 |
| `city` | 도시와 거리 |
| `interiors` | 인테리어 |
| `landmarks` | 명소 |
| `night` | 야경 |
| `transport` | 교통수단 |

### 사물과 활동

| ID | 이름 |
| --- | --- |
| `agriculture` | 농업 |
| `food` | 음식과 음료 |
| `industry` | 산업 |
| `music` | 음악 |
| `objects` | 사물 |
| `sculpture` | 조각 |
| `sports` | 스포츠 |
| `technology` | 기술 |
| `textures` | 질감 |
| `workspaces` | 작업 공간 |

<a id="headers"></a>

## 헤더, 캐시, CORS

이미지 응답과 JSON 응답은 다음을 보내요.

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers`에는 `Picsum-ID`, `Picsum-Total`, `Link`가 들어 있어서, 다른 출처의 페이지도 `fetch`로 이 세 헤더를 읽을 수 있어요.

| 응답 | `Cache-Control` |
| --- | --- |
| 랜덤 리다이렉트, `/{width}` 또는 `/{width}/{height}` | `no-store` |
| 시드 리다이렉트, `/seed/{seed}/...` | `public, max-age=3600` |
| 고정 이미지, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

랜덤 리다이렉트는 `no-store`라서 다음 요청은 다른 사진을 고를 수 있어요. `Location`의 `/id/...` URL이 캐시되는 파일이에요. 새 크기나 효과는 그 파일이 캐시되기 전, 처음 요청할 때 조금 더 걸릴 수 있어요.

아래에서 설명하는 400과 404 JSON 오류도 `Cache-Control: no-store`와 `Access-Control-Allow-Origin: *`와 함께 보내요.

<a id="errors"></a>

## 오류와 요청 한도

오류 본문은 JSON이에요. 이 `error` 문자열과 정확히 같아야 해요.

이미지 크기가 잘못되었거나, 확장자를 지원하지 않거나, 흐림이 1–10 밖이면 HTTP 400이에요.

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`/v2/list`의 `page`나 `limit`가 잘못되면 HTTP 400이에요.

```json
{"error":"Invalid page or limit."}
```

`/id/{id}/info`에서 알 수 없는 사진 ID는 HTTP 404예요.

```json
{"error":"Unknown image ID."}
```

HTTP 429는 요청 한도가 적용되었다는 뜻이에요. 응답 헤더 `Retry-After`를 따르세요. 서비스에 지장을 주는 자동 트래픽을 보내지 말고, 요청 한도를 우회하지 마세요.

<a id="code"></a>

## 코드 예제

<a id="html"></a>

### HTML

`width`, `height`, `alt`를 넣으세요. `alt`는 사진을 설명해야 해요. 아래 문장은 사진 `179363399`의 `description`이에요.

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

첫 명령은 이미지를 저장하지 않고, `Location`과 `Picsum-ID`가 들어 있는 시드 리다이렉트 헤더를 출력해요. 둘째는 사진 객체 하나를 출력해요. 셋째는 목록 헤더와 JSON 배열을 출력해요.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`Access-Control-Allow-Origin`이 `*`라서 브라우저의 `fetch`로 JSON 엔드포인트를 호출할 수 있어요. `Picsum-Total`이 노출되어 있어서 `headers.get`으로 읽을 수 있어요.

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

이 예제는 `requests` 라이브러리를 써요.

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

## 라이선스와 상업적 이용

사진은 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)이에요. 개인 이용과 상업적 이용은 무료예요. 촬영자 표기는 선택 사항이에요. 사진을 밝힐 때는 JSON 객체의 `author`가 촬영자이고, `url`이 출처 페이지예요.

민감한 용도에서는 알아볼 수 있는 사람, 상표, 원본 출처 기록을 이용자가 확인해야 해요. 그런 용도 전에 `url`을 확인하세요.

이 서비스를 자신의 이미지 API인 것처럼 재판매하거나 재배포하지 마세요.

문의: [hello@picsum.org](mailto:hello@picsum.org).

이용 조건은 [서비스 이용약관](https://picsum.org/ko/terms)에 있어요.

<a id="mcp"></a>

## MCP 서버

호스팅된 MCP 서버는 모델 컨텍스트 프로토콜을 쓰는 클라이언트의 읽기 전용 사진 조회를 처리해요. 위의 이미지 URL을 대신하지 않고, 텍스트 프롬프트로 그림을 만들지도 않아요. 이미지 URL은 `https://picsum.org/{...}`에 그대로 있어요. MCP 엔드포인트는 따로 있어요.

| | |
| --- | --- |
| 엔드포인트 | `https://picsum.org/mcp` |
| 전송 | Streamable HTTP |
| 인가 | PKCE를 쓰는 OAuth 2.1 |
| 스코프 | `photos:read` |
| 설정 안내 | [AI 도우미를 Picsum에 연결](https://picsum.org/ko/connect) |
| 클라이언트 설정 | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

도구는 읽기 전용이에요.

| 도구 | 하는 일 |
| --- | --- |
| `search_photos` | `tag`, `category`, 또는 둘 다로 검색해요. |
| `get_photo` | 사진 ID 하나의 메타데이터예요. |
| `list_categories` | 카테고리 ID 전부와, 각각의 영어 표시 이름과 그룹을 돌려줘요. |
| `build_image_url` | 고른 크기, 형식, 회색조, 흐림에 대한 이미지 URL과 HTML `<img>` 조각이에요. |

로그인과 클라이언트 설정은 [AI 도우미를 Picsum에 연결](https://picsum.org/ko/connect)에 있어요. 다른 언어의 안내도 로케일 접두사 아래 같은 `/connect` 경로를 써요. 설정 예제는 [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp)에 있어요.
