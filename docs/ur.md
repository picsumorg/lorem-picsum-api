[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · **اردو** · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/ur) اصل CC0 فوٹو کا مفت API ہے، رینڈم تصاویر کا جنریٹر۔ یہ [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) کے تحت **33 زمروں** میں **100,000 تصاویر** دیتا ہے۔ تصویر کے لنک، حسبِ ضرورت سائز، JPEG اور WebP، گرے اسکیل، بلر، اور JSON میٹا ڈیٹا کے اینڈ پوائنٹس کے لیے اکاؤنٹ یا API کلید نہیں چاہیے۔

Lorem Picsum (`picsum.org`) ایک الگ سروس ہے، اوپن سورس پراجیکٹ Picsum Photos سے متاثر۔ یہ `picsum.photos` سے منسلک نہیں۔ اس کا اپنا مجموعہ ہے اور اپنی فوٹو IDs ہیں۔ اس دوسرے پراجیکٹ کے راستے، جیسے گرے اسکیل والا `/g/{width}/{height}`، اس API کا حصہ نہیں۔

API کا بنیادی URL `https://picsum.org` ہے۔ API کے راستے سے پہلے ویب سائٹ کا لوکیل نہ لگائیں۔ `https://picsum.org/de/800/600` ویب سائٹ کا راستہ ہے، تصویر کا URL نہیں۔ لوکیل کے سابقے (`/de`، `/ja`، `/zh-tw`، اور باقی) ہوم پیج، MCP کی ترتیب کی رہنمائی، اور استعمال کی شرائط جیسے صفحات کے ہوتے ہیں۔

## مشمولات

- [جائزہ](#overview)
- [فوری آغاز](#quick-start)
- [تصویر کے URL](#image-urls)
- [JSON میٹا ڈیٹا](#json)
- [زمرے](#categories)
- [ہیڈر، کیش، اور CORS](#headers)
- [خرابیاں اور ریٹ لمٹ](#errors)
- [کوڈ کی مثالیں](#code)
- [لائسنس اور تجارتی استعمال](#license)
- [MCP سرور](#mcp)

<a id="overview"></a>

## جائزہ

جب لے آؤٹ کو تصویر چاہیے تو تصویر کا URL مانگیں۔ جب فوٹوگرافر، تفصیل، زمرہ، ٹیگ، اصل پیمائش، ماخذ کا صفحہ، یا لائسنس چاہیے تو JSON مانگیں۔

رینڈم URL ہر درخواست پر کوئی اور فوٹو چن سکتا ہے۔ سیڈ یا فوٹو ID سے وہی اصل فوٹو ملتی رہتی ہے۔ چوڑائی اور اونچائی **1 سے 2000** پکسل تک کے صحیح اعداد ہیں۔ اس حد کا ہر حسبِ ضرورت سائز مفت ہے، گرے اسکیل اور بلر بھی۔ ہوم پیج کے چھ سائز سہولت کے تیار سائز ہیں، اوپری حد نہیں۔

<a id="quick-start"></a>

## فوری آغاز

یہ رینڈم 800×600 تصویر ایک مخصوص فوٹو کی طرف ری ڈائریکٹ ہوتی ہے۔ کیش یہ ری ڈائریکٹ محفوظ نہیں کرتا، اور منتخب ID جواب کے `Picsum-ID` ہیڈر میں آتی ہے:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

جب تصویر اپنی جگہ رہنی ہو تو پن شدہ URL استعمال کریں:

```text
https://picsum.org/id/179363399/800/600.jpg
```

جب تصویر بار بار وہی رہنی ہو تو سیڈ استعمال کریں۔ ایک ہی سیڈ ہر سائز پر وہی اصل فوٹو دیتا ہے۔ سیڈ `studio` فوٹو `1000561303` دیتا ہے۔ یہ مثال WebP، گرے اسکیل، اور بلر مانگتی ہے:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## تصویر کے URL

<a id="dimensions"></a>

### پیمائش اور کراپ

`width` اور `height` راستے کے حصے ہیں۔ ہر ایک 1 سے 2000 تک کا صحیح عدد ہے، اور 1 اور 2000 دونوں شامل ہیں۔ سروس فوٹو کو بڑا یا چھوٹا کرتی ہے اور بیچ سے کاٹتی ہے، تاکہ مانگا ہوا مستطیل بھر جائے۔ تصویر کھینچی نہیں جاتی۔

<a id="formats"></a>

### فارمیٹ

| ایکسٹینشن | کیا ملتا ہے |
| --- | --- |
| *(کوئی نہیں)* | JPEG، `image/jpeg` |
| `.jpg` | JPEG، `image/jpeg` |
| `.webp` | WebP، `image/webp` |

`.png`، `.jpeg`، `.gif`، اور `.avif` قبول نہیں۔ جواب HTTP 400 ہوتا ہے، اور نیچے تصویر کی خرابی کا آبجیکٹ ملتا ہے۔ `.jpeg` کو `.jpg` کا متبادل نام نہیں سمجھا جاتا۔

<a id="random-rectangle"></a>

### رینڈم مستطیل

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

جواب `302 Found` ہوتا ہے۔ `Location` کی قدر `/id/{id}/{width}/{height}.{ext}` ہوتی ہے۔ ایکسٹینشن چھوڑنے پر `{ext}` کی قدر `jpg` ہوتی ہے۔

- `Cache-Control: no-store`
- `Picsum-ID` وہ فوٹو ہے جو منتخب ہوئی

`GET https://picsum.org/800/600` اس شکل کا معیاری تیار سائز ہے۔

<a id="random-square"></a>

### رینڈم مربع

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` ایک 640×640 JPEG مانگتا ہے۔ جواب `/id/{id}/{width}/{width}.jpg` پر `302` ہوتا ہے، ساتھ `Cache-Control: no-store` اور `Picsum-ID` ہیڈر۔

<a id="seeded"></a>

### سیڈ والی فوٹو

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

جواب `/id/{id}/{width}/{height}.{ext}` پر `302` ہوتا ہے۔ مربع سیڈ URL چوڑائی اور اونچائی کے لیے ایک ہی عدد استعمال کرتا ہے۔ چھوڑی ہوئی ایکسٹینشن `jpg` ہے۔

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` منتخب فوٹو ہے
- ایک سیڈ ہمیشہ وہی اصل فوٹو چنتا ہے، سائز بدلنے پر بھی۔ `studio` فوٹو `1000561303` چنتا ہے۔
- سیڈ موضوع کا لفظ بھی ہے۔ `GET https://picsum.org/seed/cat/800/600` بلی کی فوٹو چنتا ہے۔
- سیڈ کسی ٹیگ سے نہ ملے تو سروس مجموعے کی ایک مستقل فوٹو پر آ جاتی ہے۔ وہی نامعلوم سیڈ بار بار وہی فوٹو دیتا ہے۔

<a id="pinned"></a>

### پن شدہ فوٹو

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

جواب `200 OK` ہوتا ہے اور تصویر کے بائٹس ملتے ہیں، `image/jpeg` یا `image/webp`۔ مربع راستہ دونوں طرف ایک ہی پیمائش استعمال کرتا ہے۔ چھوڑی ہوئی ایکسٹینشن JPEG ہے۔

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` وہی `{id}` دہراتا ہے

کسی ID کا فوٹوگرافر اور ماخذ کا صفحہ پڑھنے کے لیے [`/id/{id}/info`](#info-id) کال کریں۔ نامعلوم ID کے لیے دستاویز شدہ `404` میٹا ڈیٹا کے اس راستے پر ہے، تصویر کے راستے پر نہیں۔

<a id="query"></a>

### کوئری پیرامیٹرز

| پیرامیٹر | کہاں لگتا ہے | قاعدہ |
| --- | --- | --- |
| `tag` | رینڈم تصاویر، سیڈ والی تصاویر، اور `GET /v2/list` | موضوع کی سٹرنگ۔ اس سے انتخاب کا مجموعہ تنگ ہو جاتا ہے۔ مثال: `?tag=forest`۔ |
| `category` | رینڈم تصاویر، سیڈ والی تصاویر، اور `GET /v2/list` | 33 زمرہ IDs میں سے ایک۔ مثال: `?category=woodlands`۔ |
| `grayscale` | تصویر کے URL | فلیگ کی شکل `?grayscale`۔ گرے اسکیل تصویر کی فائل میں شامل ہو جاتا ہے۔ `/g/{width}/{height}` والا راستہ نہیں ہے۔ |
| `blur` | تصویر کے URL | 1 سے 10 تک کا صحیح عدد۔ بغیر عدد کے `?blur` قبول ہے، اور اس کا مطلب `blur=5` ہے۔ `blur=0` اور `blur=11` HTTP 400 دیتے ہیں۔ |

`tag` اور `category` فوٹو چنتے وقت استعمال ہوتے ہیں۔ وہ ری ڈائریکٹ کے `Location` پر نقل نہیں ہوتے۔

گرے اسکیل اور بلر تصویر کے ساتھ رہتے ہیں۔ یہ سیڈ والی درخواست:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

اس کا جواب `302` ہوتا ہے، ان ہیڈرز کے ساتھ:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

اس پن شدہ URL پر فلیگ `grayscale` کو `grayscale=1` لکھا جاتا ہے۔ `blur=4` برقرار رہتا ہے۔ فائل خود گرے اسکیل اور دھندلی ہوتی ہے۔ یہ CSS فلٹر نہیں۔

<a id="presets"></a>

### ہوم پیج کے تیار سائز

یہ چھ سائز ہوم پیج پر دکھائے گئے تیار سائز ہیں۔ 1 سے 2000 تک کوئی اور سائز بھی مفت ہے۔

| تیار سائز | پکسل | URL |
| --- | --- | --- |
| معیاری | 800×600 | `https://picsum.org/800/600` |
| مربع | 640×640 | `https://picsum.org/640` |
| افقی | 1200×800 | `https://picsum.org/1200/800` |
| عمودی | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

نئے سائز کی پہلی درخواست، یا گرے اسکیل اور بلر کے نئے جوڑ کی پہلی درخواست، تھوڑا زیادہ وقت لے سکتی ہے۔ اس کے بعد پن شدہ فائل کیش ہو جاتی ہے۔

<a id="json"></a>

## JSON میٹا ڈیٹا

`/list` نامی کوئی v1 اینڈ پوائنٹ نہیں۔ فہرست `/v2/list` پر ملتی ہے۔

`/v2/list` JSON ارے دیتا ہے۔ `/id/{id}/info` اور `/seed/{seed}/info` ایک JSON آبجیکٹ دیتے ہیں۔ تینوں `Cache-Control: public, max-age=300` اور `Access-Control-Allow-Origin: *` بھیجتے ہیں۔

<a id="list"></a>

### فوٹو کی فہرست

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| کوئری | قاعدہ |
| --- | --- |
| `page` | 1 یا اس سے بڑا صحیح عدد۔ طے شدہ `1`۔ |
| `limit` | 1 سے 100 تک کا صحیح عدد۔ طے شدہ `30`۔ |
| `tag` | اختیاری موضوع کی سٹرنگ۔ |
| `category` | اختیاری زمرہ ID۔ |

جواب کے ہیڈر:

- `Link`، `rel="next"` استعمال کرتا ہے، اور پچھلا صفحہ ہو تو `rel="prev"` بھی۔
- `Picsum-Total`، ملنے والی فوٹو کی تعداد۔ جب نہ `tag` ہو اور نہ `category`، قدر `100000` ہوتی ہے۔
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

`limit=1` کے ساتھ صفحہ 1 کی درخواست نے یہ `Link` ہیڈر اور `Picsum-Total: 100000` دیا:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

باڈی اس آبجیکٹ کا ارے ہے جو [آبجیکٹ کے فیلڈ](#fields) میں بیان ہوا ہے۔ ہر عنصر ایک فوٹو ہے۔ ترتیب بدل سکتی ہے؛ پہلی قطار کو مقرر فوٹو نہ مانیں۔

<a id="info-id"></a>

### ID سے ایک فوٹو

```http
GET https://picsum.org/id/{id}/info
```

جو ID موجود ہو اس پر `200` اور ایک JSON آبجیکٹ ملتا ہے۔ نامعلوم ID پر `404` ملتا ہے، اور باڈی بالکل یہ ہوتی ہے:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### سیڈ سے ایک فوٹو

```http
GET https://picsum.org/seed/{seed}/info
```

جواب `200` اور ایک JSON آبجیکٹ ہوتا ہے، اور `Picsum-ID` ہیڈر بھی آتا ہے۔ جو سیڈ کسی ٹیگ سے نہ ملے اس پر خرابی نہیں آتی۔ وہی مستقل متبادل فوٹو ملتی ہے جو سیڈ والی تصویر کے URL سے ملتی ہے۔

<a id="fields"></a>

### آبجیکٹ کے فیلڈ

| فیلڈ | معنی |
| --- | --- |
| `id` | فوٹو ID، سٹرنگ کی صورت میں۔ |
| `author` | فوٹوگرافر کا نام۔ سٹرنگ خالی ہو سکتی ہے۔ |
| `width` | اصل چوڑائی، پکسل میں۔ یہ وہ چوڑائی نہیں جو رینڈر کے لیے مانگی گئی۔ |
| `height` | اصل اونچائی، پکسل میں۔ یہ وہ اونچائی نہیں جو رینڈر کے لیے مانگی گئی۔ |
| `description` | فوٹو کی مختصر تفصیل۔ |
| `category` | ایک زمرہ ID۔ |
| `tags` | موضوع کی سٹرنگز کا ارے۔ |
| `url` | اصل ماخذ کا صفحہ۔ |
| `license` | بالکل یہ سٹرنگ `"CC0 1.0"`۔ |
| `license_url` | بالکل یہ سٹرنگ `"https://creativecommons.org/publicdomain/zero/1.0/"`۔ |
| `download_url` | اس فوٹو کا 800×600 JPEG URL۔ |

WebP یا گرے اسکیل کا URL `id` سے بنائیں۔ `download_url` ہمیشہ 800×600 JPEG ہوتا ہے۔

<a id="examples"></a>

### مثالیں

`GET https://picsum.org/id/179363399/info` یہ دیتا ہے:

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

یہ فوٹو 3840×2160 ہے، Syony کی، زمرہ `landscapes` میں۔ تفصیل: “Colorful mountain slopes in Landmannalaugar”۔ ٹیگ `mountains`، `highlands`، `colorful`، اور `iceland` ہیں۔

`GET https://picsum.org/seed/studio/info` یہ دیتا ہے:

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

جواب کے ہیڈر `Picsum-ID` کی قدر `1000561303` ہے۔ اصل فریم 2400×1800 ہے، `author` خالی ہے، اور `category` کی قدر `food` ہے۔

<a id="categories"></a>

## زمرے

`category` میں ان IDs میں سے ایک بھیجیں۔ عوامی HTTP اینڈ پوائنٹ `/categories` موجود نہیں۔ MCP ٹول `list_categories` وہی IDs واپس کرتا ہے، اور ہر ID کے ساتھ انگریزی نام اور گروپ دیتا ہے۔ نیچے درج نام قارئین کے لیے ترجمے ہیں؛ درخواست میں نام نہیں، ID بھیجیں۔

### فطرت اور مناظر

| ID | نام |
| --- | --- |
| `coasts` | ساحل اور سمندر |
| `deserts` | صحرا اور ریت کے ٹیلے |
| `freshwater` | جھیلیں اور آبشاریں |
| `gardens` | باغات |
| `landscapes` | مناظر |
| `macro` | میکرو |
| `mountains` | پہاڑ |
| `plants` | پودے اور پھول |
| `skies` | آسمان اور موسم |
| `snow` | برف اور یخ |
| `woodlands` | جنگلات |

### جانور

| ID | نام |
| --- | --- |
| `animals` | دیگر جانور |
| `birds` | پرندے |
| `insects` | کیڑے مکوڑے |
| `marine` | سمندری حیات |
| `pets` | پالتو جانور |

### مقامات اور سفر

| ID | نام |
| --- | --- |
| `aerial` | ہوائی منظر |
| `architecture` | فن تعمیر |
| `city` | شہر اور گلیاں |
| `interiors` | اندرونی حصے |
| `landmarks` | مشہور مقامات |
| `night` | رات |
| `transport` | نقل و حمل |

### اشیاء اور سرگرمیاں

| ID | نام |
| --- | --- |
| `agriculture` | زراعت |
| `food` | کھانا اور مشروبات |
| `industry` | صنعت |
| `music` | موسیقی |
| `objects` | اشیاء |
| `sculpture` | مجسمے |
| `sports` | کھیل |
| `technology` | ٹیکنالوجی |
| `textures` | بناوٹ |
| `workspaces` | کام کی جگہیں |

<a id="headers"></a>

## ہیڈر، کیش، اور CORS

تصویر اور JSON کے جوابات یہ بھیجتے ہیں:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` میں `Picsum-ID`، `Picsum-Total`، اور `Link` شامل ہیں، اس لیے دوسری اوریجن کا صفحہ `fetch` سے یہ تین ہیڈر پڑھ سکتا ہے۔

| جواب | `Cache-Control` |
| --- | --- |
| رینڈم ری ڈائریکٹ، `/{width}` یا `/{width}/{height}` | `no-store` |
| سیڈ والا ری ڈائریکٹ، `/seed/{seed}/...` | `public, max-age=3600` |
| پن شدہ تصویر، `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`، `/id/{id}/info`، `/seed/{seed}/info` | `public, max-age=300` |

رینڈم ری ڈائریکٹ `no-store` ہوتا ہے، اس لیے اگلی درخواست دوسری فوٹو چن سکتی ہے۔ `Location` میں جو `/id/...` URL ہے، وہی کیش ہونے والی فائل ہے۔ نئے سائز یا ایفیکٹ کی پہلی درخواست، اس فائل کے کیش ہونے سے پہلے، تھوڑا زیادہ وقت لے سکتی ہے۔

نیچے درج 400 اور 404 کی JSON خرابیاں بھی `Cache-Control: no-store` اور `Access-Control-Allow-Origin: *` کے ساتھ بھیجی جاتی ہیں۔

<a id="errors"></a>

## خرابیاں اور ریٹ لمٹ

خرابی کی باڈیز JSON ہیں۔ ان `error` سٹرنگز سے بالکل ملائیں۔

تصویر کی غلط پیمائش، ناقابلِ قبول ایکسٹینشن، یا 1 سے 10 کے باہر بلر کی قدر (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`/v2/list` پر غلط `page` یا `limit` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

`/id/{id}/info` پر نامعلوم فوٹو ID (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 کا مطلب ہے کہ ریٹ لمٹ لگ چکی ہے۔ `Retry-After` ہیڈر کو مانیں، اور اس میں دیے گئے وقت کے بعد دوبارہ کوشش کریں۔ ایسی خودکار ٹریفک نہ چلائیں جو سروس کو کمزور کرے، اور ریٹ لمٹ سے بچنے کی کوشش نہ کریں۔

<a id="code"></a>

## کوڈ کی مثالیں

<a id="html"></a>

### HTML

`width`، `height`، اور `alt` طے کریں۔ `alt` میں فوٹو کی وضاحت لکھیں۔ نیچے کی عبارت فوٹو `179363399` کی `description` ہے۔

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

پہلا حکم سیڈ والے ری ڈائریکٹ کے ہیڈر چھاپتا ہے، جن میں `Location` اور `Picsum-ID` شامل ہیں، اور تصویر محفوظ نہیں کرتا۔ دوسرا ایک فوٹو آبجیکٹ چھاپتا ہے۔ تیسرا فہرست کے ہیڈر اور JSON ارے چھاپتا ہے۔

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` براؤزر سے JSON اینڈ پوائنٹس کال کر سکتا ہے، کیونکہ `Access-Control-Allow-Origin` کی قدر `*` ہے۔ `Picsum-Total` ظاہر کیا گیا ہے، اس لیے `headers.get` اسے پڑھ سکتا ہے۔

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

یہ مثال `requests` لائبریری استعمال کرتی ہے۔

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

## لائسنس اور تجارتی استعمال

یہ فوٹو [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) کے تحت ہیں۔ ذاتی استعمال اور تجارتی استعمال مفت ہے۔ نام دینا اختیاری ہے۔ اگر نام دینا چاہیں تو JSON آبجیکٹ میں `author` تخلیق کار ہے اور `url` ماخذ کا صفحہ۔

استعمال حساس ہو تو شناخت کے قابل افراد، ٹریڈ مارک، اور اصل ماخذ کے ریکارڈ کی ذمہ داری آپ کی ہے۔ ایسے استعمال سے پہلے `url` دیکھ لیں۔

اس سروس کو اپنی تصویری API بنا کر نہ بیچیں اور نہ بانٹیں۔

سوالات: [hello@picsum.org](mailto:hello@picsum.org)۔

سروس کی شرائط: [استعمال کی شرائط](https://picsum.org/ur/terms)۔

<a id="mcp"></a>

## MCP سرور

ہوسٹ شدہ MCP سرور صرف پڑھنے والی فوٹو کی درخواستوں کا جواب دیتا ہے، ان کلائنٹس کے لیے جو Model Context Protocol استعمال کرتے ہیں۔ یہ اوپر والے تصویر کے URL کی جگہ نہیں لیتا، اور متن کے پرامپٹ سے تصویر نہیں بناتا۔ تصویر کے URL `https://picsum.org/{...}` پر رہتے ہیں۔ MCP کا اینڈ پوائنٹ الگ ہے۔

| | |
| --- | --- |
| اینڈ پوائنٹ | `https://picsum.org/mcp` |
| ٹرانسپورٹ | Streamable HTTP |
| اجازت | PKCE کے ساتھ OAuth 2.1 |
| اسکوپ | `photos:read` |
| ترتیب کی رہنمائی | [اپنے اے آئی اسسٹنٹ کو Picsum سے جوڑیں](https://picsum.org/ur/connect) |
| کلائنٹ کی ترتیب | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

یہ ٹولز صرف پڑھنے کے ہیں:

| ٹول | کیا کرتا ہے |
| --- | --- |
| `search_photos` | `tag` سے، `category` سے، یا دونوں سے تلاش۔ |
| `get_photo` | ایک فوٹو ID کا میٹا ڈیٹا۔ |
| `list_categories` | ہر زمرہ ID، انگریزی نام اور گروپ کے ساتھ۔ |
| `build_image_url` | چنے ہوئے سائز، فارمیٹ، گرے اسکیل، اور بلر کے لیے تصویر کا URL، اور HTML کا `<img>` ٹکڑا۔ |

سائن اِن اور کلائنٹ کی ترتیب [اپنے اے آئی اسسٹنٹ کو Picsum سے جوڑیں](https://picsum.org/ur/connect) پر لکھی ہے۔ دوسری زبانیں اپنے لوکیل کے سابقے کے نیچے وہی `/connect` راستہ استعمال کرتی ہیں۔ ترتیب کی مثالیں [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) میں ہیں۔
