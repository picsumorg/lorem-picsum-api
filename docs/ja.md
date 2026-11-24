[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · **日本語** · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/ja)は、無料のプレースホルダー写真APIです。ランダム画像ジェネレーターとして、[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)のCC0写真を**10万枚**、**33カテゴリ**で配信します。画像URL、任意のサイズ、JPEGとWebP、グレースケール、ぼかし、JSONのメタデータエンドポイントは、登録なしで使えます。アカウントもAPIキーも不要です。

Lorem Picsum（`picsum.org`）は、オープンソースのPicsum Photosを参考にした独立したサービスです。`picsum.photos`との提携関係はありません。カタログも写真IDも独自です。Picsum Photos側のパス、たとえばグレースケール用の`/g/{width}/{height}`は、このAPIには含まれません。

APIのベースURLは`https://picsum.org`です。APIのパスの前に、ウェブサイトのロケールを付けないでください。`https://picsum.org/de/800/600`はウェブサイトのページ用URLであり、画像URLではありません。ロケールの接頭辞（`/de`、`/ja`、`/zh-tw`など）は、ホームページ、MCPのセットアップガイド、利用規約のようなページに使います。

## 目次

- [概要](#overview)
- [クイックスタート](#quick-start)
- [画像URL](#image-urls)
- [JSONメタデータ](#json)
- [カテゴリ](#categories)
- [ヘッダー、キャッシュ、CORS](#headers)
- [エラーとレート制限](#errors)
- [コード例](#code)
- [ライセンスと商用利用](#license)
- [MCPサーバー](#mcp)

<a id="overview"></a>

## 概要

レイアウトに写真が必要なときは、画像URLをリクエストします。撮影者、説明、カテゴリ、タグ、元の寸法、出典ページ、ライセンスが必要なときは、JSONをリクエストします。

ランダムなURLは、リクエストのたびに別の写真を選ぶことがあります。シードか写真IDを指定すると、元の写真は同じままです。幅と高さは**1〜2000**ピクセルの整数です。この範囲の任意のサイズは無料で、グレースケールとぼかしも無料です。ホームページにある6つのサイズは、便宜上のプリセットであり、上限ではありません。

<a id="quick-start"></a>

## クイックスタート

この800×600のランダム画像は、特定の写真へリダイレクトします。リダイレクトはキャッシュに保存されず、選ばれたIDはレスポンスの`Picsum-ID`に入ります。

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

写真を固定するときは、IDで固定したURLを使います。

```text
https://picsum.org/id/179363399/800/600.jpg
```

同じ写真を繰り返したいときは、シードを使います。同じシードは、どのサイズでも同じ元写真に対応します。シード`studio`は`1000561303`に対応します。次の例は、WebP、グレースケール、ぼかしを指定しています。

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## 画像URL

<a id="dimensions"></a>

### 寸法と切り抜き

`width`と`height`は、パスのセグメントです。それぞれ1以上2000以下の整数です。サービスは写真を拡大または縮小し、中央を基準に切り抜いて、指定した矩形を埋めます。写真を引き伸ばすことはしません。

<a id="formats"></a>

### 形式

| 拡張子 | 取得できるもの |
| --- | --- |
| *(なし)* | JPEG、`image/jpeg` |
| `.jpg` | JPEG、`image/jpeg` |
| `.webp` | WebP、`image/webp` |

`.png`、`.jpeg`、`.gif`、`.avif`は受け付けません。レスポンスはHTTP 400で、本文は下に示す画像のエラーオブジェクトです。`.jpeg`は`.jpg`の別名ではありません。

<a id="random-rectangle"></a>

### ランダムな矩形

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

レスポンスは`302 Found`です。`Location`は`/id/{id}/{width}/{height}.{ext}`です。拡張子を省くと、`{ext}`は`jpg`になります。

- `Cache-Control: no-store`
- `Picsum-ID`は、選ばれた写真を示します

`GET https://picsum.org/800/600`は、この形式の「標準」プリセットです。

<a id="random-square"></a>

### ランダムな正方形

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640`は、640×640のJPEGを要求します。レスポンスは`/id/{id}/{width}/{width}.jpg`への`302`で、`Cache-Control: no-store`と`Picsum-ID`ヘッダーが付きます。

<a id="seeded"></a>

### シードで指定する写真

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

レスポンスは`/id/{id}/{width}/{height}.{ext}`への`302`です。正方形のシードURLでは、幅と高さに同じ数値を使います。拡張子を省くと`jpg`です。

- `Cache-Control: public, max-age=3600`
- `Picsum-ID`は、選ばれた写真を示します
- 1つのシードは、サイズを変えても常に同じ元写真を選びます。`studio`が選ぶのは`1000561303`です。
- シードは検索語も兼ねます。`GET https://picsum.org/seed/cat/800/600`は、猫の写真を選びます。
- シードがどのタグにも一致しないときは、コレクションの中から決まっている1枚を返します。そのシードを再び使っても、返る写真は同じです。

<a id="pinned"></a>

### IDで固定した写真

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

レスポンスは`200 OK`と画像のバイト列で、`image/jpeg`または`image/webp`です。正方形のパスでは、1つの寸法を縦横の両方に使います。拡張子を省くとJPEGです。

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID`は`{id}`をそのまま返します

IDの撮影者と出典ページを読むには、[`/id/{id}/info`](#info-id)を呼び出します。未知のIDに対する`404`として仕様に書いてあるのは、画像のパスではなく、このメタデータのパスです。

<a id="query"></a>

### クエリパラメーター

| パラメーター | 適用箇所 | 規則 |
| --- | --- | --- |
| `tag` | ランダム画像、シード付き画像、`GET /v2/list` | 題材の文字列です。候補を絞ります。例: `?tag=forest`。 |
| `category` | ランダム画像、シード付き画像、`GET /v2/list` | 33個のカテゴリIDのいずれかです。例: `?category=woodlands`。 |
| `grayscale` | 画像URL | フラグ形式の`?grayscale`です。グレースケールは画像ファイル自体に適用されます。`/g/{width}/{height}`というパスはありません。 |
| `blur` | 画像URL | 1〜10の整数です。値のない`?blur`も受け付け、`blur=5`を意味します。`blur=0`と`blur=11`はHTTP 400を返します。 |

`tag`と`category`は、写真を選ぶときに使います。リダイレクトの`Location`にはコピーされません。

グレースケールとぼかしは、選ばれた画像に付いたままです。次のシード付きリクエスト

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

は`302`で、次を返します。

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

フラグ`grayscale`は、その固定URLでは`grayscale=1`と書かれます。`blur=4`はそのまま残ります。ファイル自体がグレースケールになり、ぼかしも入っています。これはCSSフィルターではありません。

<a id="presets"></a>

### ホームページのサイズプリセット

次の6サイズは、ホームページに出ているプリセットです。1〜2000のほかのサイズも、同じく無料です。

| プリセット | ピクセル | URL |
| --- | --- | --- |
| 標準 | 800×600 | `https://picsum.org/800/600` |
| 正方形 | 640×640 | `https://picsum.org/640` |
| 横長 | 1200×800 | `https://picsum.org/1200/800` |
| 縦長 | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| フルHD | 1920×1080 | `https://picsum.org/1920/1080` |

新しいサイズ、または新しいグレースケールやぼかしの組み合わせへの最初のリクエストは、少し時間がかかることがあります。その後は、固定したファイルがキャッシュされます。

<a id="json"></a>

## JSONメタデータ

`/list`のv1エンドポイントはありません。コレクションの一覧は`/v2/list`です。

`/v2/list`はJSON配列を返します。`/id/{id}/info`と`/seed/{seed}/info`は、JSONオブジェクトを1つ返します。3つとも`Cache-Control: public, max-age=300`と`Access-Control-Allow-Origin: *`を送ります。

<a id="list"></a>

### 写真の一覧

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| クエリ | 規則 |
| --- | --- |
| `page` | 1以上の整数です。既定値は`1`です。 |
| `limit` | 1〜100の整数です。既定値は`30`です。 |
| `tag` | 省略できる題材の文字列です。 |
| `category` | 省略できるカテゴリIDです。 |

レスポンスヘッダー:

- `Link`は`rel="next"`を使い、前のページがあるときは`rel="prev"`も使います。
- `Picsum-Total`は、一致した写真の数です。`tag`も`category`もないとき、値は`100000`です。
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

`limit=1`の1ページ目のリクエストは、次の`Link`ヘッダーと`Picsum-Total: 100000`を返しました。

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

本文は、[オブジェクトのフィールド](#fields)で説明するオブジェクトの配列です。各要素が写真1枚です。並び順は変わることがあるので、先頭の行を固定の写真とみなさないでください。

<a id="info-id"></a>

### IDで1枚取得する

```http
GET https://picsum.org/id/{id}/info
```

存在するIDは`200`とJSONオブジェクト1つを返します。未知のIDは`404`と、次の本文をそのまま返します。

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### シードで1枚取得する

```http
GET https://picsum.org/seed/{seed}/info
```

レスポンスは`200`とJSONオブジェクト1つ、それに`Picsum-ID`ヘッダーです。どのタグにも一致しないシードは、エラーにはなりません。シード付きの画像URLと同じく、決まっている1枚の写真を返します。

<a id="fields"></a>

### オブジェクトのフィールド

| フィールド | 意味 |
| --- | --- |
| `id` | 写真IDです。文字列です。 |
| `author` | 撮影者の名前です。空文字列になることがあります。 |
| `width` | 元の幅（ピクセル）です。出力に指定した幅ではありません。 |
| `height` | 元の高さ（ピクセル）です。出力に指定した高さではありません。 |
| `description` | 写真の短い説明です。 |
| `category` | カテゴリIDが1つ入ります。 |
| `tags` | 題材を表す文字列の配列です。 |
| `url` | 元の出典ページです。 |
| `license` | 文字列`"CC0 1.0"`そのものです。 |
| `license_url` | 文字列`"https://creativecommons.org/publicdomain/zero/1.0/"`そのものです。 |
| `download_url` | この写真の800×600 JPEGのURLです。 |

WebPやグレースケールのURLは、`id`から組み立てます。`download_url`は、常に800×600のJPEGです。

<a id="examples"></a>

### 例

`GET https://picsum.org/id/179363399/info`は、次を返します。

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

この写真は3840×2160で、撮影者はSyony、カテゴリは`landscapes`です。説明は「Colorful mountain slopes in Landmannalaugar」です。タグは`mountains`、`highlands`、`colorful`、`iceland`です。

`GET https://picsum.org/seed/studio/info`は、次を返します。

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

レスポンスヘッダーの`Picsum-ID`は`1000561303`です。元のフレームは2400×1800で、`author`は空、`category`は`food`です。

<a id="categories"></a>

## カテゴリ

`category`には、次のIDのいずれかを指定します。公開されたHTTPの`/categories`エンドポイントはありません。MCPツール`list_categories`が返すのも同じIDですが、表示名は英語で、グループも付きます。下の表の名前は、読者向けの訳です。リクエストでは、表示名ではなくIDを送ってください。

### 自然・風景

| ID | 名前 |
| --- | --- |
| `coasts` | 海岸・海 |
| `deserts` | 砂漠・砂丘 |
| `freshwater` | 湖・滝 |
| `gardens` | 庭園 |
| `landscapes` | 風景 |
| `macro` | マクロ写真 |
| `mountains` | 山 |
| `plants` | 植物・花 |
| `skies` | 空・天気 |
| `snow` | 雪・氷 |
| `woodlands` | 森林 |

### 動物

| ID | 名前 |
| --- | --- |
| `animals` | その他の動物 |
| `birds` | 鳥 |
| `insects` | 昆虫 |
| `marine` | 海の生き物 |
| `pets` | ペット |

### 場所・旅

| ID | 名前 |
| --- | --- |
| `aerial` | 空撮 |
| `architecture` | 建築 |
| `city` | 街並み・通り |
| `interiors` | インテリア |
| `landmarks` | 名所 |
| `night` | 夜景 |
| `transport` | 乗り物・交通 |

### 物・アクティビティ

| ID | 名前 |
| --- | --- |
| `agriculture` | 農業 |
| `food` | 食べ物・飲み物 |
| `industry` | 産業 |
| `music` | 音楽 |
| `objects` | 小物 |
| `sculpture` | 彫刻 |
| `sports` | スポーツ |
| `technology` | テクノロジー |
| `textures` | テクスチャ |
| `workspaces` | 作業スペース |

<a id="headers"></a>

## ヘッダー、キャッシュ、CORS

画像とJSONのレスポンスは、次を送ります。

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers`には`Picsum-ID`、`Picsum-Total`、`Link`が含まれます。そのため、別オリジンのページでも、`fetch`からこの3つのヘッダーを読めます。

| レスポンス | `Cache-Control` |
| --- | --- |
| ランダムなリダイレクト（`/{width}`または`/{width}/{height}`） | `no-store` |
| シード付きのリダイレクト（`/seed/{seed}/...`） | `public, max-age=3600` |
| 固定した画像（`/id/{id}/{width}/...`） | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`、`/id/{id}/info`、`/seed/{seed}/info` | `public, max-age=300` |

ランダムなリダイレクトは`no-store`なので、次のリクエストでは別の写真を選べます。`Location`にある`/id/...`のURLが、キャッシュできるファイルです。新しいサイズや効果への最初のリクエストは、そのファイルがキャッシュされるまで、少し時間がかかることがあります。

下で説明する400と404のJSONエラーも、`Cache-Control: no-store`と`Access-Control-Allow-Origin: *`を付けて送ります。

<a id="errors"></a>

## エラーとレート制限

エラー本文はJSONです。次の`error`文字列は、表記どおりに一致させてください。

画像の寸法が不正なとき、未対応の拡張子のとき、またはぼかしの値が1〜10の範囲外のとき（HTTP 400）:

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`/v2/list`の`page`または`limit`が不正なとき（HTTP 400）:

```json
{"error":"Invalid page or limit."}
```

`/id/{id}/info`の写真IDが未知のとき（HTTP 404）:

```json
{"error":"Unknown image ID."}
```

HTTP 429は、レート制限が適用されたことを意味します。レスポンスヘッダー`Retry-After`に従ってください。サービス品質を下げる自動アクセスは行わないでください。レート制限を回避しないでください。

<a id="code"></a>

## コード例

<a id="html"></a>

### HTML

`width`、`height`、`alt`を設定します。`alt`には、その写真の内容を書いてください。下の説明は、写真`179363399`の`description`です。

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

1つ目のコマンドは、シード付きリダイレクトのヘッダーを表示します。`Location`と`Picsum-ID`が含まれ、画像は保存しません。2つ目は、写真オブジェクトを1つ表示します。3つ目は、一覧のヘッダーとJSON配列を表示します。

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`Access-Control-Allow-Origin`が`*`なので、ブラウザーの`fetch`からJSONエンドポイントを呼び出せます。`Picsum-Total`はレスポンスから読めるので、`headers.get`で取得できます。

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

この例では、`requests`ライブラリを使います。

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

## ライセンスと商用利用

写真は[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)です。個人利用も商用利用も無料です。クレジット表記は任意です。写真にクレジットを入れるときは、JSONオブジェクトの`author`が撮影者、`url`が出典ページです。

人物を識別できる写真、商標、元の出典の記録については、配慮が必要な用途では利用する側が責任を負います。そのような用途の前に、`url`を確認してください。

このサービスを、自分の画像APIとして再販売したり再配布したりしないでください。

お問い合わせ: [hello@picsum.org](mailto:hello@picsum.org)。

利用規約: [利用規約](https://picsum.org/ja/terms)。

<a id="mcp"></a>

## MCPサーバー

Lorem PicsumがホストするMCPサーバーは、モデルコンテキストプロトコルに対応したクライアントが送る、読み取り専用の写真クエリに応答します。上の画像URLの代わりにはなりません。テキストのプロンプトから画像を生成することもしません。画像URLは`https://picsum.org/{...}`のままです。MCPのエンドポイントは別です。

| | |
| --- | --- |
| エンドポイント | `https://picsum.org/mcp` |
| トランスポート | Streamable HTTP |
| 認可 | PKCE必須のOAuth 2.1 |
| スコープ | `photos:read` |
| セットアップガイド | [AIアシスタントをPicsumに接続](https://picsum.org/ja/connect) |
| クライアント設定 | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

ツールは読み取り専用です。

| ツール | 動作 |
| --- | --- |
| `search_photos` | `tag`、`category`、またはその両方で検索します。 |
| `get_photo` | 写真ID 1件のメタデータです。 |
| `list_categories` | すべてのカテゴリIDと、英語の表示名、グループです。 |
| `build_image_url` | 選んだサイズ、形式、グレースケール、ぼかしに対する画像URLと、HTMLの`<img>`断片です。 |

ログインとクライアントの設定は、[AIアシスタントをPicsumに接続](https://picsum.org/ja/connect)に書いてあります。ほかの言語のページも、それぞれのロケール接頭辞の下で同じ`/connect`パスを使います。設定例は[https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp)にあります。
