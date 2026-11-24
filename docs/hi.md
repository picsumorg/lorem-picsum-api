[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · **हिन्दी** · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/hi) असली CC0 फ़ोटो का मुफ़्त प्लेसहोल्डर API और रैंडम इमेज जनरेटर है। यह [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) के तहत **33 श्रेणियों** की **1,00,000 फ़ोटो** देता है। इमेज URL, मनचाहा साइज़, JPEG और WebP, ग्रेस्केल, ब्लर और JSON मेटाडेटा के एंडपॉइंट के लिए खाते या API कुंजी की ज़रूरत नहीं है।

Lorem Picsum (`picsum.org`) एक स्वतंत्र सेवा है। यह ओपन सोर्स प्रोजेक्ट Picsum Photos की प्रेरणा से बनी है, पर `picsum.photos` से इसका औपचारिक संबंध नहीं है। संग्रह इसका अपना है, और फ़ोटो की आईडी भी इसकी अपनी हैं। उस प्रोजेक्ट के पथ इस API का हिस्सा नहीं हैं, जैसे ग्रेस्केल वाला `/g/{width}/{height}`।

API का बेस URL `https://picsum.org` है। API पथ से पहले वेबसाइट की लोकेल न लगाएँ। `https://picsum.org/de/800/600` वेबसाइट का मार्ग है, इमेज URL नहीं। लोकेल के उपसर्ग (`/de`, `/ja`, `/zh-tw` और बाकी) होमपेज, MCP सेटअप गाइड और शर्तों जैसे पेजों पर लगते हैं।

## विषय-सूची

- [अवलोकन](#overview)
- [जल्दी शुरू करें](#quick-start)
- [इमेज URL](#image-urls)
- [JSON मेटाडेटा](#json)
- [श्रेणियाँ](#categories)
- [हेडर, कैश और CORS](#headers)
- [त्रुटियाँ और दर-सीमा](#errors)
- [कोड के उदाहरण](#code)
- [लाइसेंस और व्यावसायिक इस्तेमाल](#license)
- [MCP सर्वर](#mcp)

<a id="overview"></a>

## अवलोकन

लेआउट में फ़ोटो चाहिए, तो इमेज का लिंक माँगें। फ़ोटोग्राफ़र, विवरण, श्रेणी, टैग, मूल आयाम, स्रोत पेज या लाइसेंस चाहिए, तो JSON माँगें।

रैंडम URL हर अनुरोध पर अलग फ़ोटो चुन सकता है। सीड या फ़ोटो आईडी लगाने पर मूल फ़ोटो वही रहती है। चौड़ाई और ऊँचाई **1 से 2000** पिक्सेल तक की पूरी संख्याएँ हैं। इस सीमा में हर मनचाहा साइज़ मुफ़्त है। ग्रेस्केल और ब्लर भी मुफ़्त हैं। होमपेज के छह साइज़ सुविधा के प्रीसेट हैं। वे चुने जा सकने वाले साइज़ की पूरी सूची नहीं हैं।

<a id="quick-start"></a>

## जल्दी शुरू करें

यह रैंडम 800×600 इमेज एक तय फ़ोटो पर रीडायरेक्ट होती है। रीडायरेक्ट कैश में नहीं रखा जाता, और चुनी हुई आईडी जवाब के `Picsum-ID` में आती है:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

फ़ोटो टिकी रहनी चाहिए, तो पिन किया हुआ URL लगाएँ:

```text
https://picsum.org/id/179363399/800/600.jpg
```

फ़ोटो हर बार वही आनी चाहिए, तो सीड लगाएँ। एक ही सीड हर साइज़ पर वही मूल फ़ोटो देता है। सीड `studio` फ़ोटो `1000561303` चुनता है। इस उदाहरण में WebP, ग्रेस्केल और ब्लर माँगे गए हैं:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## इमेज URL

<a id="dimensions"></a>

### आयाम और क्रॉप

`width` और `height` पथ के खंड हैं। हर खंड 1 से 2000 तक की पूरी संख्या है, और 1 तथा 2000 भी मान्य हैं। सेवा फ़ोटो को बड़ा या छोटा करके बीच से क्रॉप करती है, ताकि माँगा गया आयत भर जाए। फ़ोटो खींची नहीं जाती।

<a id="formats"></a>

### फ़ॉर्मैट

| एक्सटेंशन | क्या मिलता है |
| --- | --- |
| *(कोई नहीं)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` और `.avif` स्वीकार नहीं होते। जवाब HTTP 400 होता है, और नीचे वाला इमेज त्रुटि ऑब्जेक्ट मिलता है। `.jpeg`, `.jpg` का दूसरा नाम नहीं है।

<a id="random-rectangle"></a>

### रैंडम आयत

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

जवाब `302 Found` होता है। `Location` का मान `/id/{id}/{width}/{height}.{ext}` होता है। एक्सटेंशन न दिया हो, तो `{ext}` `jpg` होता है।

- `Cache-Control: no-store`
- `Picsum-ID` चुनी हुई फ़ोटो की आईडी है।

`GET https://picsum.org/800/600` इसी रूप का मानक प्रीसेट है।

<a id="random-square"></a>

### रैंडम वर्ग

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` 640×640 का JPEG माँगता है। जवाब `302` होता है और `/id/{id}/{width}/{width}.jpg` पर रीडायरेक्ट करता है। साथ में `Cache-Control: no-store` तथा `Picsum-ID` हेडर आते हैं।

<a id="seeded"></a>

### सीड वाली फ़ोटो

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

जवाब `302` होता है और `/id/{id}/{width}/{height}.{ext}` पर रीडायरेक्ट करता है। वर्गाकार सीड URL में चौड़ाई और ऊँचाई दोनों के लिए एक ही संख्या होती है। एक्सटेंशन न दिया हो, तो वह `jpg` होता है।

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` चुनी हुई फ़ोटो की आईडी है।
- साइज़ बदलने पर भी एक सीड वही मूल फ़ोटो चुनता है। `studio` फ़ोटो `1000561303` चुनता है।
- सीड को खोज शब्द भी माना जाता है। `GET https://picsum.org/seed/cat/800/600` बिल्ली की फ़ोटो चुनता है।
- सीड किसी टैग से न मिले, तो सेवा संग्रह में से एक स्थिर फ़ोटो दे देती है। वही अनजाना सीड हर बार वही फ़ोटो लौटाता है।

<a id="pinned"></a>

### पिन की गई फ़ोटो

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

जवाब `200 OK` होता है, और बॉडी में इमेज के बाइट आते हैं: `image/jpeg` या `image/webp`। वर्गाकार पथ दोनों भुजाओं पर एक ही माप लगाता है। एक्सटेंशन न हो, तो फ़ॉर्मैट JPEG होता है।

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` `{id}` को ज्यों का त्यों लौटाता है।

किसी आईडी का फ़ोटोग्राफ़र और स्रोत पेज पढ़ने के लिए [`/id/{id}/info`](#info-id) कॉल करें। अज्ञात आईडी के लिए दस्तावेज़ में जो `404` है, वह इमेज वाले रूट पर नहीं, इसी मेटाडेटा रूट पर मिलता है।

<a id="query"></a>

### क्वेरी पैरामीटर

| पैरामीटर | कहाँ लगता है | नियम |
| --- | --- | --- |
| `tag` | रैंडम इमेज, सीड वाली इमेज, और `GET /v2/list` | विषय की स्ट्रिंग। इससे फ़ोटो का दायरा घटता है। उदाहरण: `?tag=forest`। |
| `category` | रैंडम इमेज, सीड वाली इमेज, और `GET /v2/list` | 33 श्रेणी आईडी में से कोई एक। उदाहरण: `?category=woodlands`। |
| `grayscale` | इमेज URL | फ़्लैग का रूप `?grayscale`। ग्रेस्केल इमेज फ़ाइल के अंदर ही बन जाता है। कोई `/g/{width}/{height}` पथ नहीं है। |
| `blur` | इमेज URL | 1 से 10 तक की पूरी संख्या। अकेला `?blur` मान्य है, और उसका मतलब `blur=5` है। `blur=0` और `blur=11` पर HTTP 400 आता है। |

`tag` और `category` उसी समय लगते हैं जब फ़ोटो चुनी जा रही हो। रीडायरेक्ट के `Location` पर वे नहीं आते।

ग्रेस्केल और ब्लर इमेज के साथ ही जाते हैं। यह सीड वाला अनुरोध:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

`302` लौटाता है, और जवाब में ये आते हैं:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

उस पिन किए हुए URL पर फ़्लैग `grayscale` को `grayscale=1` लिख दिया जाता है। `blur=4` वैसा ही रहता है। फ़ाइल खुद ग्रेस्केल और धुंधली होती है। यह CSS का फ़िल्टर नहीं है।

<a id="presets"></a>

### होमपेज के साइज़ प्रीसेट

ये छह साइज़ होमपेज पर दिखते प्रीसेट हैं। 1 से 2000 तक का कोई और साइज़ भी मुफ़्त है।

| प्रीसेट | पिक्सेल | URL |
| --- | --- | --- |
| मानक | 800×600 | `https://picsum.org/800/600` |
| चौकोर | 640×640 | `https://picsum.org/640` |
| लैंडस्केप | 1200×800 | `https://picsum.org/1200/800` |
| पोर्ट्रेट | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

नया साइज़, या ग्रेस्केल और ब्लर का नया संयोजन, पहली बार अनुरोध करने पर थोड़ा ज़्यादा समय ले सकता है। उसके बाद पिन की गई फ़ाइल कैश में रहती है।

<a id="json"></a>

## JSON मेटाडेटा

`/list` का कोई v1 एंडपॉइंट नहीं है। संग्रह की सूची `/v2/list` पर है।

`/v2/list` JSON ऐरे देता है। `/id/{id}/info` और `/seed/{seed}/info` एक JSON ऑब्जेक्ट देते हैं। तीनों जवाब `Cache-Control: public, max-age=300` और `Access-Control-Allow-Origin: *` भेजते हैं।

<a id="list"></a>

### फ़ोटो की सूची

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| क्वेरी | नियम |
| --- | --- |
| `page` | 1 या उससे बड़ी पूरी संख्या। डिफ़ॉल्ट `1`। |
| `limit` | 1 से 100 तक की पूरी संख्या। डिफ़ॉल्ट `30`। |
| `tag` | वैकल्पिक विषय स्ट्रिंग। |
| `category` | वैकल्पिक श्रेणी आईडी। |

जवाब के हेडर:

- `Link`: इसमें `rel="next"` होता है, और पिछला पेज हो तो `rel="prev"` भी।
- `Picsum-Total`: जितनी फ़ोटो मेल खाती हैं। `tag` और `category` दोनों न हों, तो मान `100000` होता है।
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

`limit=1` वाले पेज 1 के अनुरोध ने यह `Link` हेडर लौटाया, और साथ में `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

बॉडी उस ऑब्जेक्ट का ऐरे है, जिसका वर्णन [ऑब्जेक्ट के फ़ील्ड](#fields) में है। हर तत्व एक फ़ोटो है। क्रम बदल सकता है, इसलिए पहली पंक्ति को तय फ़ोटो न मानें।

<a id="info-id"></a>

### आईडी से एक फ़ोटो

```http
GET https://picsum.org/id/{id}/info
```

ज्ञात आईडी `200` के साथ एक JSON ऑब्जेक्ट लौटाती है। अज्ञात आईडी `404` और ठीक यही बॉडी लौटाती है:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### सीड से एक फ़ोटो

```http
GET https://picsum.org/seed/{seed}/info
```

जवाब `200` होता है। बॉडी में एक JSON ऑब्जेक्ट होता है, और हेडर में `Picsum-ID` आता है। जो सीड किसी टैग से नहीं मिलता, वह त्रुटि नहीं देता। सीड वाले इमेज URL की तरह वही स्थिर फ़ोटो मिलती है।

<a id="fields"></a>

### ऑब्जेक्ट के फ़ील्ड

| फ़ील्ड | अर्थ |
| --- | --- |
| `id` | फ़ोटो आईडी, स्ट्रिंग के रूप में। |
| `author` | रचनाकार का नाम। स्ट्रिंग खाली हो सकती है। |
| `width` | मूल चौड़ाई, पिक्सेल में। यह वह चौड़ाई नहीं जिसे इमेज में माँगा गया। |
| `height` | मूल ऊँचाई, पिक्सेल में। यह वह ऊँचाई नहीं जिसे इमेज में माँगा गया। |
| `description` | फ़ोटो का छोटा विवरण। |
| `category` | एक श्रेणी आईडी। |
| `tags` | विषय की स्ट्रिंग का ऐरे। |
| `url` | मूल स्रोत का पेज। |
| `license` | ठीक यही स्ट्रिंग: `"CC0 1.0"`। |
| `license_url` | ठीक यही स्ट्रिंग: `"https://creativecommons.org/publicdomain/zero/1.0/"`। |
| `download_url` | इस फ़ोटो का 800×600 JPEG URL। |

WebP या ग्रेस्केल का URL `id` से बनाएँ। `download_url` हमेशा 800×600 का JPEG होता है।

<a id="examples"></a>

### उदाहरण

`GET https://picsum.org/id/179363399/info` यह देता है:

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

यह 3840×2160 की फ़ोटो है। रचनाकार Syony हैं, श्रेणी `landscapes` है, और विवरण “Colorful mountain slopes in Landmannalaugar” है। टैग `mountains`, `highlands`, `colorful` और `iceland` हैं।

`GET https://picsum.org/seed/studio/info` यह देता है:

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

जवाब के हेडर `Picsum-ID` का मान `1000561303` है। मूल फ़्रेम 2400×1800 है, `author` खाली है, और `category` `food` है।

<a id="categories"></a>

## श्रेणियाँ

`category` में इनमें से एक आईडी भेजें। कोई सार्वजनिक HTTP `/categories` एंडपॉइंट नहीं है। MCP टूल `list_categories` वही आईडी लौटाता है, और हर आईडी के साथ अंग्रेज़ी प्रदर्शन नाम तथा समूह देता है। इस तालिका के नाम पाठकों के लिए अनुवाद हैं। `list_categories` अंग्रेज़ी नाम लौटाता है। अनुरोध में नाम नहीं, आईडी भेजें।

### प्रकृति और भूदृश्य

| आईडी | नाम |
| --- | --- |
| `coasts` | तट और महासागर |
| `deserts` | रेगिस्तान और टीले |
| `freshwater` | झीलें और झरने |
| `gardens` | बगीचे |
| `landscapes` | भूदृश्य |
| `macro` | मैक्रो |
| `mountains` | पहाड़ |
| `plants` | पौधे और फूल |
| `skies` | आकाश और मौसम |
| `snow` | बर्फ़ और हिम |
| `woodlands` | जंगल |

### जानवर

| आईडी | नाम |
| --- | --- |
| `animals` | अन्य जानवर |
| `birds` | पक्षी |
| `insects` | कीड़े |
| `marine` | समुद्री जीव |
| `pets` | पालतू जानवर |

### जगहें और यात्रा

| आईडी | नाम |
| --- | --- |
| `aerial` | हवाई दृश्य |
| `architecture` | वास्तुकला |
| `city` | शहर और सड़कें |
| `interiors` | अंदरूनी जगहें |
| `landmarks` | प्रसिद्ध स्थल |
| `night` | रात |
| `transport` | परिवहन |

### वस्तुएँ और गतिविधियाँ

| आईडी | नाम |
| --- | --- |
| `agriculture` | कृषि |
| `food` | खाना और पेय |
| `industry` | उद्योग |
| `music` | संगीत |
| `objects` | वस्तुएँ |
| `sculpture` | मूर्तियाँ |
| `sports` | खेल |
| `technology` | तकनीक |
| `textures` | बनावट |
| `workspaces` | कार्यस्थल |

<a id="headers"></a>

## हेडर, कैश और CORS

इमेज और JSON के जवाब ये भेजते हैं:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` में `Picsum-ID`, `Picsum-Total` और `Link` शामिल हैं, इसलिए किसी दूसरी ऑरिजिन का पेज `fetch` से ये तीन हेडर पढ़ सकता है।

| जवाब | `Cache-Control` |
| --- | --- |
| रैंडम रीडायरेक्ट, `/{width}` या `/{width}/{height}` | `no-store` |
| सीड वाला रीडायरेक्ट, `/seed/{seed}/...` | `public, max-age=3600` |
| पिन की गई इमेज, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

रैंडम रीडायरेक्ट `no-store` होता है, ताकि अगला अनुरोध दूसरी फ़ोटो चुन सके। `Location` में जो `/id/...` URL है, वही कैश हो सकने वाली फ़ाइल है। नया साइज़ या नया इफ़ेक्ट पहली बार अनुरोध करने पर थोड़ा ज़्यादा समय लग सकता है, जब तक वह फ़ाइल कैश न हो जाए।

नीचे दर्ज 400 और 404 की JSON त्रुटियाँ भी `Cache-Control: no-store` और `Access-Control-Allow-Origin: *` के साथ भेजी जाती हैं।

<a id="errors"></a>

## त्रुटियाँ और दर-सीमा

त्रुटि की बॉडी JSON होती है। `error` की स्ट्रिंग हूबहू वही होनी चाहिए।

इमेज के आयाम गलत हों, एक्सटेंशन समर्थित न हो, या ब्लर का मान 1–10 के बाहर हो (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`/v2/list` पर `page` या `limit` गलत हो (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

`/id/{id}/info` पर फ़ोटो की आईडी अज्ञात हो (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 का मतलब है कि दर-सीमा लग गई है। `Retry-After` हेडर के मुताबिक दोबारा कोशिश करें। ऐसा स्वचालित ट्रैफ़िक न चलाएँ जिससे सेवा बाधित हो, और दर-सीमा से बचने की कोशिश न करें।

<a id="code"></a>

## कोड के उदाहरण

<a id="html"></a>

### HTML

`width`, `height` और `alt` दें। `alt` में फ़ोटो का वर्णन हो। नीचे लिखा वर्णन फ़ोटो `179363399` का `description` है।

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

पहला कमांड सीड वाले रीडायरेक्ट के हेडर छापता है, जिनमें `Location` और `Picsum-ID` शामिल हैं, और इमेज सहेजता नहीं। दूसरा एक फ़ोटो ऑब्जेक्ट छापता है। तीसरा सूची के हेडर और एक JSON ऐरे छापता है।

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` ब्राउज़र से JSON एंडपॉइंट कॉल कर सकता है, क्योंकि `Access-Control-Allow-Origin` का मान `*` है। `Picsum-Total` पढ़ने के लिए खुला है, इसलिए `headers.get` उसे पढ़ लेता है।

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

यह उदाहरण `requests` लाइब्रेरी का इस्तेमाल करता है।

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

## लाइसेंस और व्यावसायिक इस्तेमाल

ये फ़ोटो [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) के तहत हैं। निजी और व्यावसायिक, दोनों इस्तेमाल मुफ़्त हैं। फ़ोटोग्राफ़र का नाम देना वैकल्पिक है। श्रेय देना हो, तो JSON ऑब्जेक्ट में `author` रचनाकार है और `url` स्रोत का पेज है।

संवेदनशील इस्तेमाल में पहचानने योग्य लोगों, ट्रेडमार्क और मूल स्रोत के रिकॉर्ड की ज़िम्मेदारी आपकी है। ऐसा इस्तेमाल करने से पहले `url` जाँच लें।

इस सेवा को अपनी इमेज API बताकर दोबारा न बेचें, और न बाँटें।

सवाल: [hello@picsum.org](mailto:hello@picsum.org)।

सेवा की शर्तें: [इस्तेमाल की शर्तें](https://picsum.org/hi/terms)।

<a id="mcp"></a>

## MCP सर्वर

होस्ट किया गया MCP सर्वर उन्हीं क्लाइंट के लिए केवल पढ़ने वाली फ़ोटो क्वेरी का जवाब देता है जो Model Context Protocol का इस्तेमाल करते हैं। यह ऊपर दिए इमेज URL की जगह नहीं लेता, और टेक्स्ट प्रॉम्प्ट से फ़ोटो नहीं बनाता। इमेज URL `https://picsum.org/{...}` पर ही रहते हैं। MCP का एंडपॉइंट अलग है।

| | |
| --- | --- |
| एंडपॉइंट | `https://picsum.org/mcp` |
| ट्रांसपोर्ट | Streamable HTTP |
| अनुमति | PKCE के साथ OAuth 2.1 |
| स्कोप | `photos:read` |
| सेटअप गाइड | [अपने एआई असिस्टेंट को Picsum से जोड़ें](https://picsum.org/hi/connect) |
| क्लाइंट कॉन्फ़िगरेशन | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

टूल केवल पढ़ने के हैं:

| टूल | क्या करता है |
| --- | --- |
| `search_photos` | `tag` से, `category` से, या दोनों से फ़ोटो खोजता है। |
| `get_photo` | एक फ़ोटो आईडी का मेटाडेटा। |
| `list_categories` | हर श्रेणी आईडी, उसके अंग्रेज़ी प्रदर्शन नाम और समूह के साथ। |
| `build_image_url` | चुने साइज़, फ़ॉर्मैट, ग्रेस्केल और ब्लर के लिए एक इमेज URL, और HTML `<img>` का छोटा कोड। |

साइन-इन और क्लाइंट सेटअप [अपने एआई असिस्टेंट को Picsum से जोड़ें](https://picsum.org/hi/connect) पर लिखे हैं। दूसरी भाषाओं के पेज भी अपनी लोकेल के उपसर्ग के साथ वही `/connect` पथ रखते हैं। इमेज वाले अनुरोध लोकेल के उपसर्ग पर न भेजें। कॉन्फ़िगरेशन के उदाहरण [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) में हैं।
