[English](../README.md) · **العربية** · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/ar) هو مولّد الصور العشوائية، وواجهة مجانية لصور مؤقتة. يقدّم **100,000 صورة فوتوغرافية** حقيقية بترخيص [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) في **33 تصنيفاً**. لا يلزم حساب ولا مفتاح API لرابط الصورة، ولا للمقاس المخصّص، ولا لصيغتي JPEG وWebP، ولا للتدرّج الرمادي، ولا للتمويه، ولا لمسارات بيانات JSON الوصفية.

Lorem Picsum (`picsum.org`) خدمة مستقلة مستوحاة من مشروع Picsum Photos المفتوح المصدر. ليست تابعة لـ `picsum.photos`. لها مجموعتها الخاصة ومعرّفات صورها الخاصة. مسارات ذلك المشروع الآخر، ومنها مسار التدرّج الرمادي `/g/{width}/{height}`، ليست جزءاً من هذه الواجهة.

عنوان الأساس للواجهة هو `https://picsum.org`. لا تضع بادئة لغة الموقع قبل مسار الواجهة. `https://picsum.org/de/800/600` مسار في الموقع وليس رابط صورة. بادئات اللغة (`/de` و`/ja` و`/zh-tw` وسواها) تخص صفحات مثل الصفحة الرئيسية ودليل إعداد MCP وشروط الاستخدام.

## المحتويات

- [نظرة عامة](#overview)
- [بداية سريعة](#quick-start)
- [روابط الصور](#image-urls)
- [بيانات JSON الوصفية](#json)
- [التصنيفات](#categories)
- [الترويسات والتخزين المؤقت وCORS](#headers)
- [الأخطاء وحدود المعدّل](#errors)
- [أمثلة الشيفرة](#code)
- [الترخيص والاستخدام التجاري](#license)
- [خادم MCP](#mcp)

<a id="overview"></a>

## نظرة عامة

اطلب رابط الصورة حين يحتاج التخطيط إلى صورة. اطلب JSON حين تحتاج إلى المصوّر أو الوصف أو التصنيف أو الوسوم أو الأبعاد الأصلية أو صفحة المصدر أو الترخيص.

قد يختار رابط الصورة العشوائي صورة مختلفة مع كل طلب. أما قيمة seed أو معرّف الصورة فيُبقي الصورة المصدر نفسها. العرض والارتفاع عددان صحيحان من **1 إلى 2000** بكسل. كل مقاس مخصّص في هذا المدى مجاني، ومثله التدرّج الرمادي والتمويه. المقاسات الستة في الصفحة الرئيسية مقاسات جاهزة للتيسير، وليست حداً أقصى.

<a id="quick-start"></a>

## بداية سريعة

يعيد هذا الرابط العشوائي بمقاس 800×600 التوجيه إلى صورة محدّدة. لا يُخزَّن التوجيه في ذاكرة التخزين المؤقّت، ويحمل الرد المعرّف المختار في `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

استخدم رابط صورة مثبّتاً إذا كان يجب أن تبقى الصورة كما هي:

```text
https://picsum.org/id/179363399/800/600.jpg
```

استخدم قيمة seed إذا كان يجب أن تتكرر الصورة. قيمة seed نفسها تختار الصورة المصدر نفسها في كل مقاس. تختار القيمة `studio` الصورة `1000561303`. يطلب هذا المثال صيغة WebP مع التدرّج الرمادي والتمويه:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## روابط الصور

<a id="dimensions"></a>

### الأبعاد والقص

`width` و`height` قطعتان في المسار. كل منهما عدد صحيح من 1 إلى 2000 ضمناً. تضبط الخدمة مقياس الصورة الفوتوغرافية وتقصّها من الوسط حتى يمتلئ المستطيل المطلوب. لا تُمدَّد الصورة.

<a id="formats"></a>

### الصيغ

| الامتداد | الناتج |
| --- | --- |
| *(من دون امتداد)* | JPEG، `image/jpeg` |
| `.jpg` | JPEG، `image/jpeg` |
| `.webp` | WebP، `image/webp` |

لا تُقبل `.png` ولا `.jpeg` ولا `.gif` ولا `.avif`. الرد هو HTTP 400 وكائن خطأ الصورة الوارد أدناه. `.jpeg` ليس مرادفاً لـ `.jpg`.

<a id="random-rectangle"></a>

### مستطيل عشوائي

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

الرد هو `302 Found`. قيمة `Location` هي `/id/{id}/{width}/{height}.{ext}`. إذا حُذف الامتداد، فقيمة `{ext}` هي `jpg`.

- `Cache-Control: no-store`
- يدل `Picsum-ID` على الصورة التي اختيرت

`GET https://picsum.org/800/600` هو المقاس القياسي الجاهز بهذا الشكل.

<a id="random-square"></a>

### مربّع عشوائي

```http
GET https://picsum.org/{width}
```

يطلب `GET https://picsum.org/640` صورة JPEG بمقاس 640×640. الرد هو `302` إلى `/id/{id}/{width}/{width}.jpg`، مع `Cache-Control: no-store` وترويسة `Picsum-ID`.

<a id="seeded"></a>

### صورة بقيمة seed

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

الرد هو `302` إلى `/id/{id}/{width}/{height}.{ext}`. يستخدم رابط seed المربّع الرقم نفسه للعرض والارتفاع. الامتداد المحذوف هو `jpg`.

- `Cache-Control: public, max-age=3600`
- يدل `Picsum-ID` على الصورة المختارة
- تختار قيمة seed الواحدة الصورة المصدر نفسها دائماً، حتى إذا تغيّر المقاس. تختار `studio` الصورة `1000561303`.
- قيمة seed كلمة موضوع أيضاً. يختار `GET https://picsum.org/seed/cat/800/600` صورة قط.
- إذا لم تطابق قيمة seed أي وسم، تعود الخدمة إلى صورة ثابتة واحدة من المجموعة. تعيد قيمة seed المجهولة نفسها تلك الصورة في كل مرة.

<a id="pinned"></a>

### صورة مثبّتة

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

الرد `200 OK` وبايتات الصورة، ونوع المحتوى `image/jpeg` أو `image/webp`. يستخدم المسار المربّع بعداً واحداً للضلعين. إذا حُذف الامتداد فالصيغة JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- يعيد `Picsum-ID` قيمة `{id}`

لقراءة المصوّر وصفحة المصدر لمعرّف ما، استدعِ [`/id/{id}/info`](#info-id). مسار البيانات الوصفية هذا، لا مسار الصورة، هو المسار الموثّق الذي يعيد `404` لمعرّف مجهول.

<a id="query"></a>

### معاملات الاستعلام

| المعامل | موضع الاستخدام | القاعدة |
| --- | --- | --- |
| `tag` | الصور العشوائية، والصور ذات قيمة seed، و`GET /v2/list` | سلسلة الموضوع. تضيّق مجموعة الصور. مثال: `?tag=forest`. |
| `category` | الصور العشوائية، والصور ذات قيمة seed، و`GET /v2/list` | أحد معرّفات التصنيف، وعددها 33. مثال: `?category=woodlands`. |
| `grayscale` | روابط الصور | بصيغة العلم `?grayscale`. يُحفظ التدرّج الرمادي داخل ملف الصورة. لا يوجد مسار `/g/{width}/{height}`. |
| `blur` | روابط الصور | عدد صحيح من 1 إلى 10. يُقبل `?blur` من دون قيمة ويعني `blur=5`. يعيد `blur=0` و`blur=11` حالة HTTP 400. |

تُراعى قيمتا `tag` و`category` أثناء اختيار الصورة، ولا تُنسخان إلى `Location` في رد التوجيه.

ينتقل التدرّج الرمادي والتمويه مع الصورة. هذا الطلب بقيمة seed:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

ويكون الرد `302` ومعه:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

يُكتب العلم `grayscale` على شكل `grayscale=1` في ذلك الرابط المثبّت. تبقى قيمة `blur=4`. الملف نفسه رمادي ومموّه، وهذا ليس مرشّح CSS.

<a id="presets"></a>

### المقاسات الجاهزة في الصفحة الرئيسية

هذه المقاسات الستة هي المقاسات الجاهزة المعروضة في الصفحة الرئيسية. أي مقاس آخر من 1 إلى 2000 مجاني أيضاً.

| المقاس الجاهز | البكسل | الرابط |
| --- | --- | --- |
| قياسي | 800×600 | `https://picsum.org/800/600` |
| مربّع | 640×640 | `https://picsum.org/640` |
| أفقي | 1200×800 | `https://picsum.org/1200/800` |
| عمودي | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

قد يستغرق الطلب الأول لمقاس جديد، أو لتركيبة جديدة من التدرّج الرمادي أو التمويه، وقتاً أطول قليلاً. بعد ذلك يُحفظ الملف المثبّت في ذاكرة التخزين المؤقّت.

<a id="json"></a>

## بيانات JSON الوصفية

لا يوجد مسار `/list` للإصدار `v1`. تُعرض المجموعة على `/v2/list`.

يعيد `/v2/list` مصفوفة JSON. يعيد كل من `/id/{id}/info` و`/seed/{seed}/info` كائناً واحداً بصيغة JSON. ترسل المسارات الثلاثة `Cache-Control: public, max-age=300` و`Access-Control-Allow-Origin: *`.

<a id="list"></a>

### قائمة الصور

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| الاستعلام | القاعدة |
| --- | --- |
| `page` | عدد صحيح أكبر من أو يساوي 1. القيمة الافتراضية `1`. |
| `limit` | عدد صحيح من 1 إلى 100. القيمة الافتراضية `30`. |
| `tag` | سلسلة موضوع اختيارية. |
| `category` | معرّف تصنيف اختياري. |

ترويسات الرد:

- `Link`، باستخدام `rel="next"`، وباستخدام `rel="prev"` إذا وُجدت صفحة سابقة.
- `Picsum-Total`، وهو عدد الصور المطابقة. من دون `tag` ومن دون `category` تكون القيمة `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

أعاد طلب الصفحة 1 مع `limit=1` ترويسة `Link` هذه والقيمة `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

الجسم مصفوفة من الكائن الموضّح في [حقول الكائن](#fields). كل عنصر صورة واحدة. قد يتغيّر الترتيب، فلا تعامل الصف الأول على أنه صورة ثابتة.

<a id="info-id"></a>

### صورة واحدة بالمعرّف

```http
GET https://picsum.org/id/{id}/info
```

يعيد المعرّف المعروف حالة `200` وكائناً واحداً بصيغة JSON. يعيد المعرّف المجهول حالة `404` وهذا الجسم كما هو:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### صورة واحدة بقيمة seed

```http
GET https://picsum.org/seed/{seed}/info
```

الرد حالة `200` وكائن واحد بصيغة JSON، إضافة إلى ترويسة `Picsum-ID`. قيمة seed التي لا تطابق أي وسم لا تعيد خطأ، بل تعيد الصورة البديلة الثابتة نفسها التي يعيدها رابط الصورة بقيمة seed.

<a id="fields"></a>

### حقول الكائن

| الحقل | المعنى |
| --- | --- |
| `id` | معرّف الصورة، على شكل سلسلة. |
| `author` | اسم المصوّر. قد تكون السلسلة فارغة. |
| `width` | العرض الأصلي بالبكسل. ليس هذا العرض الذي طلبت إخراج الصورة به. |
| `height` | الارتفاع الأصلي بالبكسل. ليس هذا الارتفاع الذي طلبت إخراج الصورة به. |
| `description` | وصف قصير للصورة الفوتوغرافية. |
| `category` | معرّف تصنيف واحد. |
| `tags` | مصفوفة من سلاسل الموضوع. |
| `url` | صفحة المصدر الأصلي. |
| `license` | السلسلة كما هي `"CC0 1.0"`. |
| `license_url` | السلسلة كما هي `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | رابط JPEG لهذه الصورة بمقاس 800×600. |

ابنِ رابط WebP أو رابط تدرّج رمادي انطلاقاً من `id`. قيمة `download_url` دائماً صورة JPEG بمقاس 800×600.

<a id="examples"></a>

### أمثلة

يعيد `GET https://picsum.org/id/179363399/info` ما يلي:

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

الصورة بمقاس 3840×2160، من تصوير Syony، وتصنيفها `landscapes`، ووصفها “Colorful mountain slopes in Landmannalaugar”. الوسوم هي `mountains` و`highlands` و`colorful` و`iceland`.

يعيد `GET https://picsum.org/seed/studio/info` ما يلي:

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

ترويسة الرد `Picsum-ID` قيمتها `1000561303`. الأبعاد الأصلية 2400×1800، وحقل `author` فارغ، وقيمة `category` هي `food`.

<a id="categories"></a>

## التصنيفات

مرّر أحد هذه المعرّفات في `category`. لا يوجد مسار HTTP عام باسم `/categories`. تعيد أداة MCP `list_categories` المعرّفات نفسها، ومع كل معرّف الاسم الإنجليزي والمجموعة. أسماء الجدول أدناه مترجمة للقارئ، وعلى الطلب أن يرسل المعرّف لا اسم العرض.

### الطبيعة والمناظر الطبيعية

| ID | الاسم |
| --- | --- |
| `coasts` | السواحل والمحيطات |
| `deserts` | الصحاري والكثبان |
| `freshwater` | البحيرات والشلالات |
| `gardens` | الحدائق |
| `landscapes` | المناظر الطبيعية |
| `macro` | تصوير عن قرب |
| `mountains` | الجبال |
| `plants` | النباتات والزهور |
| `skies` | السماء والطقس |
| `snow` | الثلج والجليد |
| `woodlands` | الغابات |

### الحيوانات

| ID | الاسم |
| --- | --- |
| `animals` | حيوانات أخرى |
| `birds` | الطيور |
| `insects` | الحشرات |
| `marine` | الحياة البحرية |
| `pets` | الحيوانات الأليفة |

### الأماكن والسفر

| ID | الاسم |
| --- | --- |
| `aerial` | التصوير الجوي |
| `architecture` | العمارة |
| `city` | المدن والشوارع |
| `interiors` | المساحات الداخلية |
| `landmarks` | المعالم |
| `night` | التصوير الليلي |
| `transport` | وسائل النقل |

### الأشياء والأنشطة

| ID | الاسم |
| --- | --- |
| `agriculture` | الزراعة |
| `food` | الأطعمة والمشروبات |
| `industry` | الصناعة |
| `music` | الموسيقى |
| `objects` | الأشياء |
| `sculpture` | المنحوتات |
| `sports` | الرياضة |
| `technology` | التكنولوجيا |
| `textures` | الخامات والملمس |
| `workspaces` | أماكن العمل |

<a id="headers"></a>

## الترويسات والتخزين المؤقت وCORS

ترسل ردود الصور وردود JSON ما يلي:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

تشمل `Access-Control-Expose-Headers` كلاً من `Picsum-ID` و`Picsum-Total` و`Link`، فتستطيع صفحة على أصل آخر قراءة هذه الترويسات الثلاث من `fetch`.

| الرد | `Cache-Control` |
| --- | --- |
| توجيه عشوائي، `/{width}` أو `/{width}/{height}` | `no-store` |
| توجيه بقيمة seed، `/seed/{seed}/...` | `public, max-age=3600` |
| صورة مثبّتة، `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list` و`/id/{id}/info` و`/seed/{seed}/info` | `public, max-age=300` |

التوجيه العشوائي بقيمة `no-store`، فيستطيع الطلب التالي اختيار صورة أخرى. رابط `/id/...` داخل `Location` هو الملف القابل للتخزين المؤقّت. قد يستغرق الطلب الأول لمقاس جديد أو لتأثير جديد وقتاً أطول قليلاً، قبل أن يُحفظ ذلك الملف في ذاكرة التخزين المؤقّت.

تُرسل أخطاء JSON ذات الحالتين 400 و404 الموثّقة أدناه أيضاً مع `Cache-Control: no-store` و`Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## الأخطاء وحدود المعدّل

أجسام الأخطاء بصيغة JSON. طابق سلاسل `error` هذه كما هي.

أبعاد صورة غير صالحة، أو امتداد غير مدعوم، أو قيمة `blur` خارج المدى من 1 إلى 10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

قيمة `page` أو `limit` غير صالحة في `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

معرّف صورة مجهول في `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

تعني HTTP 429 أن حد المعدّل قد طُبّق. التزم بترويسة الرد `Retry-After`. لا ترسل حركة آلية تضعف الخدمة، ولا تتحايل على حدود المعدّل.

<a id="code"></a>

## أمثلة الشيفرة

<a id="html"></a>

### HTML

عيّن `width` و`height` و`alt`. ينبغي أن يصف `alt` الصورة. النص أدناه هو قيمة `description` للصورة `179363399`.

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

يطبع الأمر الأول ترويسات توجيه seed، ومنها `Location` و`Picsum-ID`، ولا يحفظ الصورة. يطبع الأمر الثاني كائناً لصورة واحدة. يطبع الأمر الثالث ترويسات القائمة ومصفوفة JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

يستطيع `fetch` استدعاء مسارات JSON من المتصفح لأن قيمة `Access-Control-Allow-Origin` هي `*`. ترويسة `Picsum-Total` مكشوفة، فيمكن قراءتها عبر `headers.get`.

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

يستخدم هذا المثال مكتبة `requests`.

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

## الترخيص والاستخدام التجاري

الصور بترخيص [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). الاستخدام الشخصي والاستخدام التجاري مجانيان. ذكر المصوّر اختياري. إذا أردت نسبة الصورة إلى صاحبها، فحقل `author` هو المصوّر وحقل `url` هو صفحة المصدر، وكلاهما في كائن JSON.

تبقى مسؤولاً عن الأشخاص الذين يمكن التعرّف عليهم، وعن العلامات التجارية، وعن سجل المصدر الأصلي، حين يكون الاستخدام حسّاساً. راجع `url` قبل هذا النوع من الاستخدام.

يُحظر إعادة بيع هذه الخدمة أو إعادة توزيعها على أنها واجهة صور خاصة بك.

للاستفسار: [hello@picsum.org](mailto:hello@picsum.org).

شروط الاستخدام: [شروط الاستخدام](https://picsum.org/ar/terms).

<a id="mcp"></a>

## خادم MCP

خادم MCP مستضاف يجيب عن استعلامات الصور للقراءة فقط، للعملاء الذين يعتمدون بروتوكول سياق النموذج. لا يغني عن روابط الصور أعلاه، ولا يولّد صوراً من وصف نصي. تبقى روابط الصور على `https://picsum.org/{...}`. نقطة نهاية MCP منفصلة.

| | |
| --- | --- |
| نقطة النهاية | `https://picsum.org/mcp` |
| النقل | HTTP المتدفّق (`Streamable HTTP`) |
| التفويض | OAuth 2.1 مع PKCE |
| النطاق | `photos:read` |
| دليل الإعداد | [ربط Picsum بمساعدك الذكي](https://picsum.org/ar/connect) |
| إعداد العميل | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

الأدوات للقراءة فقط:

| الأداة | ما تفعله |
| --- | --- |
| `search_photos` | البحث بـ `tag` أو بـ `category` أو بهما معاً. |
| `get_photo` | البيانات الوصفية لمعرّف صورة واحد. |
| `list_categories` | كل معرّفات التصنيف، مع اسم العرض الإنجليزي والمجموعة. |
| `build_image_url` | رابط صورة، ومقتطف HTML للعنصر `<img>`، بحسب المقاس والصيغة والتدرّج الرمادي والتمويه الذي تختاره. |

تسجيل الدخول وإعداد العميل موثّقان في [ربط Picsum بمساعدك الذكي](https://picsum.org/ar/connect). تستخدم اللغات الأخرى مسار `/connect` نفسه تحت بادئة لغتها. أمثلة الإعداد في [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
