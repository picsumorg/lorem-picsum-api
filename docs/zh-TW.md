[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · **繁體中文**

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/zh-tw) 是免費的佔位圖片 API，也是隨機圖片產生器。它提供 **10 萬**張 CC0 照片，採用 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)，分成 **33** 個分類。圖片網址、自訂尺寸、JPEG 與 WebP、灰階、模糊，以及 JSON 中繼資料端點，都不需要帳號或 API 金鑰。

Lorem Picsum（`picsum.org`）是受開源專案 Picsum Photos 啟發而獨立營運的服務，與 `picsum.photos` 沒有從屬關係。它有自己的圖庫，也有自己的照片 ID。那個專案的路徑不屬於這套 API，包括灰階路徑 `/g/{width}/{height}`。

API 的基底網址是 `https://picsum.org`。不要在 API 路徑前面加上網站語系。`https://picsum.org/de/800/600` 是網站路由，不是圖片網址。語系前綴（`/de`、`/ja`、`/zh-tw`，以及其他語系）只用在首頁、MCP 設定指南與服務條款這類頁面。

## 目錄

- [概覽](#overview)
- [快速開始](#quick-start)
- [圖片網址](#image-urls)
- [JSON 中繼資料](#json)
- [分類](#categories)
- [標頭、快取與 CORS](#headers)
- [錯誤與速率限制](#errors)
- [程式範例](#code)
- [授權與商用](#license)
- [MCP 伺服器](#mcp)

<a id="overview"></a>

## 概覽

版面需要一張圖時，就請求圖片網址。若需要作者、說明、分類、標籤、原始尺寸、來源頁面或授權等資訊，則請求 JSON。

隨機網址每次請求都可能選到不同的照片。種子值或照片 ID 會固定同一張來源照片。寬度與高度是 **1 到 2000** 像素的整數。這個範圍內的每一種自訂尺寸都免費，灰階與模糊也免費。首頁上的六種尺寸是方便取用的預設尺寸，不是上限。

<a id="quick-start"></a>

## 快速開始

這張隨機的 800×600 圖片會重新導向到某一張照片。這次重新導向不會被快取保留，回應會在 `Picsum-ID` 帶上選中的 ID：

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

圖片必須固定不變時，請用釘選網址：

```text
https://picsum.org/id/179363399/800/600.jpg
```

圖片必須能夠重複取得時，請用種子值。同一個種子值在任何尺寸都對應同一張來源照片。種子值 `studio` 對應 `1000561303`。下面這個例子要求 WebP、灰階與模糊：

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## 圖片網址

<a id="dimensions"></a>

### 尺寸與裁切

`width` 與 `height` 是路徑區段，各自為 1 到 2000（含）的整數。服務會縮放照片，並以中心為基準裁切，填滿所要求的矩形。照片不會被拉長。

<a id="formats"></a>

### 格式

| 副檔名 | 取得內容 |
| --- | --- |
| *（無）* | JPEG，`image/jpeg` |
| `.jpg` | JPEG，`image/jpeg` |
| `.webp` | WebP，`image/webp` |

`.png`、`.jpeg`、`.gif` 與 `.avif` 都不接受。回應是 HTTP 400，並回傳下方的圖片錯誤物件。`.jpeg` 不是 `.jpg` 的別名。

<a id="random-rectangle"></a>

### 隨機矩形

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

回應是 `302 Found`。`Location` 為 `/id/{id}/{width}/{height}.{ext}`。省略副檔名時，`{ext}` 是 `jpg`。

- `Cache-Control: no-store`
- `Picsum-ID` 是這次選中的照片

`GET https://picsum.org/800/600` 是這種形式的標準預設尺寸。

<a id="random-square"></a>

### 隨機正方形

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` 請求的是一張 640×640 的 JPEG。回應是 `302`，導向 `/id/{id}/{width}/{width}.jpg`，並帶有 `Cache-Control: no-store` 與 `Picsum-ID` 標頭。

<a id="seeded"></a>

### 以種子值選圖

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

回應是 `302`，導向 `/id/{id}/{width}/{height}.{ext}`。正方形的種子網址以同一個數字作為寬與高。省略副檔名時為 `jpg`。

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` 是選中的照片
- 同一個種子值永遠選中同一張來源照片，就算尺寸改變也一樣。`studio` 選中的是 `1000561303`。
- 種子值也是主題詞。`GET https://picsum.org/seed/cat/800/600` 會選一張貓的照片。
- 若種子值對不上任何標籤，服務會改用圖庫中一張固定的照片。同一個未知的種子值會一直回傳同一張照片。

<a id="pinned"></a>

### 釘選照片

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

回應是 `200 OK`，內容是圖片的位元組，媒體類型為 `image/jpeg` 或 `image/webp`。正方形路徑只給一個邊長，寬與高都用這個值。省略副檔名時為 JPEG。

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` 的值就是 `{id}`

要讀取某個 ID 的作者與來源頁面，請呼叫 [`/id/{id}/info`](#info-id)。針對未知 ID，文件記載的 `404` 是這條中繼資料路由，不是圖片路由。

<a id="query"></a>

### 查詢參數

| 參數 | 適用範圍 | 規則 |
| --- | --- | --- |
| `tag` | 隨機圖片、種子圖片，以及 `GET /v2/list` | 主題字串，用來縮小候選照片的範圍。例如 `?tag=forest`。 |
| `category` | 隨機圖片、種子圖片，以及 `GET /v2/list` | 33 個分類 ID 之一。例如 `?category=woodlands`。 |
| `grayscale` | 圖片網址 | 旗標形式為 `?grayscale`。灰階會直接做進圖片檔案。沒有 `/g/{width}/{height}` 這條路徑。 |
| `blur` | 圖片網址 | 1 到 10 的整數。單獨的 `?blur` 也可接受，意思是 `blur=5`。`blur=0` 與 `blur=11` 會回傳 HTTP 400。 |

`tag` 與 `category` 只在挑選照片時使用。它們不會出現在重新導向的 `Location` 上。

灰階與模糊會跟著圖片走。下面這個種子請求：

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

會以 `302` 回應，標頭為：

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

在該釘選網址上，旗標 `grayscale` 會寫成 `grayscale=1`。`blur=4` 會保留。檔案本身就是灰階，而且已經模糊。這不是 CSS 濾鏡。

<a id="presets"></a>

### 首頁預設尺寸

這六種尺寸是首頁上的預設尺寸。1 到 2000 的其他尺寸同樣免費。

| 預設 | 像素 | 網址 |
| --- | --- | --- |
| 標準 | 800×600 | `https://picsum.org/800/600` |
| 正方形 | 640×640 | `https://picsum.org/640` |
| 橫式 | 1200×800 | `https://picsum.org/1200/800` |
| 直式 | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

第一次要求新的尺寸，或新的灰階與模糊組合時，可能會稍久一點。之後，釘選的檔案會進入快取。

<a id="json"></a>

## JSON 中繼資料

沒有 `/list` 這個 v1 端點。圖庫清單位於 `/v2/list`。

`/v2/list` 回傳 JSON 陣列。`/id/{id}/info` 與 `/seed/{seed}/info` 各回傳一個 JSON 物件。三者都會送出 `Cache-Control: public, max-age=300` 與 `Access-Control-Allow-Origin: *`。

<a id="list"></a>

### 列出照片

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| 查詢參數 | 規則 |
| --- | --- |
| `page` | 大於或等於 1 的整數。預設為 `1`。 |
| `limit` | 1 到 100 的整數。預設為 `30`。 |
| `tag` | 可省略的主題字串。 |
| `category` | 可省略的分類 ID。 |

回應標頭：

- `Link` 提供分頁連結，使用 `rel="next"`；若有上一頁，則一併提供 `rel="prev"`。
- `Picsum-Total` 是符合條件的照片數。沒有 `tag` 也沒有 `category` 時，值為 `100000`。
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

`limit=1` 的第 1 頁請求，回傳了下面這個 `Link` 標頭，以及 `Picsum-Total: 100000`：

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

回應本文是 [物件欄位](#fields) 所描述的物件陣列。每個元素是一張照片。順序可能改變，不要把第一行當成固定的照片。

<a id="info-id"></a>

### 以 ID 取得單張照片

```http
GET https://picsum.org/id/{id}/info
```

已知的 ID 回傳 `200` 與一個 JSON 物件。未知的 ID 回傳 `404`，內容正好是：

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### 以種子值取得單張照片

```http
GET https://picsum.org/seed/{seed}/info
```

回應是 `200` 與一個 JSON 物件，並附上 `Picsum-ID` 標頭。對不上任何標籤的種子值不會回傳錯誤，而會回傳與種子圖片網址相同的那張固定後備照片。

<a id="fields"></a>

### 物件欄位

| 欄位 | 意義 |
| --- | --- |
| `id` | 照片 ID，以字串表示。 |
| `author` | 創作者名稱。字串可以是空的。 |
| `width` | 原始寬度，單位是像素。這不是你要求輸出的寬度。 |
| `height` | 原始高度，單位是像素。這不是你要求輸出的高度。 |
| `description` | 照片的簡短說明。 |
| `category` | 一個分類 ID。 |
| `tags` | 主題字串陣列。 |
| `url` | 原始來源的頁面。 |
| `license` | 精確字串 `"CC0 1.0"`。 |
| `license_url` | 精確字串 `"https://creativecommons.org/publicdomain/zero/1.0/"`。 |
| `download_url` | 這張照片 800×600 的 JPEG 網址。 |

WebP 或灰階網址請用 `id` 自行組出。`download_url` 一律是 800×600 的 JPEG。

<a id="examples"></a>

### 範例

`GET https://picsum.org/id/179363399/info` 回傳：

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

這張照片是 3840×2160，作者為 Syony，分類是 `landscapes`，說明為「Colorful mountain slopes in Landmannalaugar」。標籤是 `mountains`、`highlands`、`colorful` 與 `iceland`。

`GET https://picsum.org/seed/studio/info` 回傳：

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

回應標頭 `Picsum-ID` 是 `1000561303`。原始畫面是 2400×1800，`author` 是空的，`category` 是 `food`。

<a id="categories"></a>

## 分類

請在 `category` 傳入下列 ID 之一。沒有公開的 HTTP `/categories` 端點。下表的名稱是給讀者看的中文譯名。MCP 工具 `list_categories` 回傳同一組 ID，但顯示名稱是英文，並附有群組。請求必須傳送 ID，不要傳顯示名稱。

### 自然與風景

| ID | 名稱 |
| --- | --- |
| `coasts` | 海岸與海洋 |
| `deserts` | 沙漠與沙丘 |
| `freshwater` | 湖泊與瀑布 |
| `gardens` | 花園 |
| `landscapes` | 風景 |
| `macro` | 微距 |
| `mountains` | 山嶽 |
| `plants` | 植物與花卉 |
| `skies` | 天空與天氣 |
| `snow` | 雪與冰 |
| `woodlands` | 林地 |

### 動物

| ID | 名稱 |
| --- | --- |
| `animals` | 其他動物 |
| `birds` | 鳥類 |
| `insects` | 昆蟲 |
| `marine` | 海洋生物 |
| `pets` | 寵物 |

### 地點與旅遊

| ID | 名稱 |
| --- | --- |
| `aerial` | 空拍 |
| `architecture` | 建築 |
| `city` | 城市與街道 |
| `interiors` | 室內 |
| `landmarks` | 地標 |
| `night` | 夜景 |
| `transport` | 交通 |

### 物件與活動

| ID | 名稱 |
| --- | --- |
| `agriculture` | 農業 |
| `food` | 飲食 |
| `industry` | 工業 |
| `music` | 音樂 |
| `objects` | 物件 |
| `sculpture` | 雕塑 |
| `sports` | 運動 |
| `technology` | 科技 |
| `textures` | 紋理 |
| `workspaces` | 工作空間 |

<a id="headers"></a>

## 標頭、快取與 CORS

圖片與 JSON 回應都會送出：

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` 包含 `Picsum-ID`、`Picsum-Total` 與 `Link`，因此其他來源的頁面可以從 `fetch` 讀取這三個標頭。

| 回應 | `Cache-Control` |
| --- | --- |
| 隨機重新導向，`/{width}` 或 `/{width}/{height}` | `no-store` |
| 種子重新導向，`/seed/{seed}/...` | `public, max-age=3600` |
| 釘選圖片，`/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`、`/id/{id}/info`、`/seed/{seed}/info` | `public, max-age=300` |

隨機重新導向是 `no-store`，所以下一次請求可以選到另一張照片。`Location` 裡的 `/id/...` 網址才是可快取的檔案。新尺寸或新效果的第一次請求，在該檔案進入快取之前，可能會稍久一點。

下方記載的 400 與 404 JSON 錯誤，同樣以 `Cache-Control: no-store` 與 `Access-Control-Allow-Origin: *` 送出。

<a id="errors"></a>

## 錯誤與速率限制

錯誤內容是 JSON。請與這些 `error` 字串完全一致。

圖片尺寸無效、副檔名不受支援，或模糊值不在 1 到 10 之內（HTTP 400）：

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`/v2/list` 的 `page` 或 `limit` 無效（HTTP 400）：

```json
{"error":"Invalid page or limit."}
```

`/id/{id}/info` 遇到未知的照片 ID（HTTP 404）：

```json
{"error":"Unknown image ID."}
```

HTTP 429 表示速率限制已生效。請遵守回應標頭 `Retry-After`。不要執行會降低服務品質的自動化流量，也不要規避速率限制。

<a id="code"></a>

## 程式範例

<a id="html"></a>

### HTML

設定 `width`、`height` 與 `alt`。`alt` 應描述這張照片。下面的說明是照片 `179363399` 的 `description`。

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

第一個指令印出種子重新導向的標頭，包含 `Location` 與 `Picsum-ID`，不會把圖片存下來。第二個印出單張照片的物件。第三個印出清單標頭與 JSON 陣列。

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

瀏覽器裡的 `fetch` 可以呼叫 JSON 端點，因為 `Access-Control-Allow-Origin` 是 `*`。`Picsum-Total` 已開放讀取，所以 `headers.get` 讀得到它。

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

這個範例使用 `requests` 程式庫。

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

## 授權與商用

這些照片採用 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)。個人使用與商用都免費。署名由你決定。若要為照片署名，JSON 物件裡的 `author` 是創作者，`url` 是來源頁面。

用途若較敏感，可辨識的人物、商標與原始來源紀錄由你負責。這類使用前請先查看 `url`。

不要轉售這項服務，也不要把它再散佈成你自己的圖片 API。

若有問題，請寫信至 [hello@picsum.org](mailto:hello@picsum.org)。

服務條款：[服務條款](https://picsum.org/zh-tw/terms)。

<a id="mcp"></a>

## MCP 伺服器

託管的 MCP 伺服器讓支援 Model Context Protocol 的用戶端以唯讀方式查詢照片。它不取代上方的圖片網址，也不會依文字提示產生圖片。圖片網址維持 `https://picsum.org/{...}`。MCP 端點是分開的。

| | |
| --- | --- |
| 端點 | `https://picsum.org/mcp` |
| 傳輸 | Streamable HTTP |
| 授權 | OAuth 2.1，搭配 PKCE |
| 範圍 | `photos:read` |
| 設定指南 | [將 AI 助理連線至 Picsum](https://picsum.org/zh-tw/connect) |
| 用戶端設定 | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

這些工具都是唯讀的：

| 工具 | 作用 |
| --- | --- |
| `search_photos` | 依 `tag`、`category` 或兩者一起搜尋。 |
| `get_photo` | 取得單張照片 ID 的中繼資料。 |
| `list_categories` | 每個分類 ID，附上英文顯示名稱與群組。 |
| `build_image_url` | 依選定的尺寸、格式、灰階與模糊，產生圖片網址，以及一段 HTML `<img>` 片段。 |

登入與用戶端設定見[將 AI 助理連線至 Picsum](https://picsum.org/zh-tw/connect)。其他語言在各自的語系前綴底下，使用同一條 `/connect` 路徑。圖片網址不要加上語系前綴。設定範例位於 [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp)。
