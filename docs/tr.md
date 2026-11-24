[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · **Türkçe** · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/tr), gerçek CC0 fotoğraflarla çalışan ücretsiz bir rastgele görsel oluşturucu API’sidir. [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) kapsamında **33 kategoride** **100.000 CC0 fotoğraf** sunar. Görsel bağlantıları, özel boyutlar, JPEG ve WebP, gri tonlama, bulanıklık ve JSON üst veri uç noktaları için hesap ya da API anahtarı gerekmez.

Lorem Picsum (`picsum.org`), açık kaynaklı Picsum Photos projesinden esinlenen bağımsız bir hizmettir. `picsum.photos` sitesine bağlı değildir. Kendi kataloğu ve kendi fotoğraf kimlikleri vardır. `/g/{width}/{height}` gibi gri tonlama yolu dahil, diğer projenin yolları bu API’de yoktur.

API taban URL’si `https://picsum.org` adresidir. API yolunun önüne sitenin dil önekini koymayın. `https://picsum.org/de/800/600` bir site rotasıdır; görsel URL’si olarak kullanılamaz. Dil önekleri (`/de`, `/ja`, `/zh-tw` ve diğerleri) ana sayfa, MCP kurulum kılavuzu ve kullanım koşulları gibi sayfalara aittir.

## İçindekiler

- [Genel bakış](#overview)
- [Hızlı başlangıç](#quick-start)
- [Görsel URL’ler](#image-urls)
- [JSON üst verisi](#json)
- [Kategoriler](#categories)
- [Başlıklar, önbellek ve CORS](#headers)
- [Hatalar ve hız sınırları](#errors)
- [Kod örnekleri](#code)
- [Lisans ve ticari kullanım](#license)
- [MCP sunucusu](#mcp)

<a id="overview"></a>

## Genel bakış

Sayfa düzeninde bir görsel gerektiğinde görsel URL’si isteyin. Fotoğrafçı, açıklama, kategori, etiketler, özgün boyutlar, kaynak sayfası veya lisans gerektiğinde JSON isteyin.

Rastgele bir URL her istekte farklı bir fotoğraf seçebilir. Başlangıç değeri veya fotoğraf kimliği aynı kaynak fotoğrafı korur. Genişlik ve yükseklik **1 ile 2000** piksel arasında tam sayılardır. Bu aralıktaki her özel boyut ücretsizdir; gri tonlama ve bulanıklık da ücretsizdir. Ana sayfadaki altı boyut kolaylık için verilmiş hazır boyutlardır. Bunlar izin verilen aralığın üst sınırı değildir.

<a id="quick-start"></a>

## Hızlı başlangıç

Bu rastgele 800×600 görsel, belirli bir fotoğrafa yönlendirir. Yönlendirme önbelleğe alınmaz; yanıt, seçilen kimliği `Picsum-ID` başlığında taşır:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Görselin yerinde kalması gerektiğinde sabitlenmiş bir URL kullanın:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Görsel her istekte aynı kalmalıysa başlangıç değeri kullanın. Aynı başlangıç değeri her boyutta aynı kaynak fotoğrafa karşılık gelir. `studio` başlangıç değeri `1000561303` kimliğine karşılık gelir. Bu örnek WebP, gri tonlama ve bulanıklık ister:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Görsel URL’ler

<a id="dimensions"></a>

### Boyutlar ve kırpma

`width` ve `height` yol parçalarıdır. Her biri 1 ile 2000 arasında, sınırlar dahil, bir tam sayıdır. Hizmet, fotoğrafı ölçekleyip istenen dikdörtgeni dolduracak şekilde ortadan kırpar. Görsel esnetilmez.

<a id="formats"></a>

### Biçimler

| Uzantı | Ne alırsınız |
| --- | --- |
| *(yok)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` ve `.avif` kabul edilmez. Yanıt HTTP 400’tür; gövde, aşağıdaki görsel hata nesnesidir. `.jpeg`, `.jpg` için bir takma ad değildir.

<a id="random-rectangle"></a>

### Rastgele dikdörtgen

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Yanıt `302 Found` olur. `Location` değeri `/id/{id}/{width}/{height}.{ext}` yoludur. Uzantı yazılmazsa `{ext}` değeri `jpg` olur.

- `Cache-Control: no-store`
- `Picsum-ID`, seçilen fotoğrafın kimliğidir

Bu biçimdeki standart hazır boyut `GET https://picsum.org/800/600` adresidir.

<a id="random-square"></a>

### Rastgele kare

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640`, 640×640 JPEG ister. Yanıt, `/id/{id}/{width}/{width}.jpg` adresine giden `302` yönlendirmesidir; yanında `Cache-Control: no-store` ve bir `Picsum-ID` başlığı bulunur.

<a id="seeded"></a>

### Başlangıç değerli fotoğraf

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Yanıt, `/id/{id}/{width}/{height}.{ext}` adresine giden `302` yönlendirmesidir. Kare bir başlangıç değeri URL’sinde genişlik ve yükseklik aynı sayıdır. Yazılmayan uzantı `jpg` olur.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID`, seçilen fotoğrafın kimliğidir
- Bir başlangıç değeri, boyut değişse bile her zaman aynı kaynak fotoğrafı seçer. `studio`, `1000561303` kimliğini seçer.
- Başlangıç değeri aynı zamanda bir arama sözcüğüdür. `GET https://picsum.org/seed/cat/800/600` bir kedi fotoğrafı seçer.
- Başlangıç değeri hiçbir etiketle eşleşmezse hizmet, koleksiyondaki sabit bir fotoğrafa geri düşer. Aynı bilinmeyen başlangıç değeri her seferinde o fotoğrafı verir.

<a id="pinned"></a>

### Sabitlenmiş fotoğraf

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Yanıt `200 OK` durumudur ve gövde görsel baytlarıdır: `image/jpeg` veya `image/webp`. Kare yolda tek boyut her iki kenara da uygulanır. Yazılmayan uzantı JPEG’dir.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID`, `{id}` değerini aynen döndürür

Bir kimliğin fotoğrafçısını ve kaynak sayfasını okumak için [`/id/{id}/info`](#info-id) yolunu çağırın. Bilinmeyen bir kimlik için belgelenen `404`, görsel yoluna değil, bu üst veri yoluna aittir.

<a id="query"></a>

### Sorgu parametreleri

| Parametre | Nerede geçerlidir | Kural |
| --- | --- | --- |
| `tag` | Rastgele görseller, başlangıç değerli görseller ve `GET /v2/list` | Konu dizesi. Havuzu daraltır. Örnek: `?tag=forest`. |
| `category` | Rastgele görseller, başlangıç değerli görseller ve `GET /v2/list` | 33 kategori kimliğinden biri. Örnek: `?category=woodlands`. |
| `grayscale` | Görsel URL’ler | `?grayscale` bayrağı. Gri tonlama görsel dosyasına işlenir. `/g/{width}/{height}` yolu yoktur. |
| `blur` | Görsel URL’ler | 1 ile 10 arasında tam sayı. Tek başına `?blur` kabul edilir ve `blur=5` anlamına gelir. `blur=0` ve `blur=11` HTTP 400 döndürür. |

`tag` ve `category`, fotoğraf seçilirken kullanılır. Yönlendirmedeki `Location` değerine kopyalanmazlar.

Gri tonlama ve bulanıklık görselle birlikte taşınır. Şu başlangıç değerli istek:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

`302` ile yanıt verir:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

`grayscale` bayrağı bu sabitlenmiş URL’de `grayscale=1` olarak yazılır. `blur=4` korunur. Dosyanın kendisi gri tonlamalı ve bulanıktır; bu bir CSS filtresi değildir.

<a id="presets"></a>

### Ana sayfadaki hazır boyutlar

Bu altı boyut, ana sayfada gösterilen hazır boyutlardır. 1 ile 2000 arasındaki diğer her boyut da ücretsizdir.

| Hazır boyut | Piksel | URL |
| --- | --- | --- |
| Standart | 800×600 | `https://picsum.org/800/600` |
| Kare | 640×640 | `https://picsum.org/640` |
| Yatay | 1200×800 | `https://picsum.org/1200/800` |
| Dikey | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Yeni bir boyutun veya yeni bir gri tonlama ya da bulanıklık birleşiminin ilk isteği biraz daha uzun sürebilir. Bundan sonra sabitlenmiş dosya önbelleğe alınır.

<a id="json"></a>

## JSON üst verisi

`/list` adında bir v1 uç noktası yoktur. Koleksiyon `/v2/list` adresinde listelenir.

`/v2/list` bir JSON dizisi döndürür. `/id/{id}/info` ve `/seed/{seed}/info` tek bir JSON nesnesi döndürür. Üçü de `Cache-Control: public, max-age=300` ve `Access-Control-Allow-Origin: *` gönderir.

<a id="list"></a>

### Fotoğrafları listeleme

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Sorgu | Kural |
| --- | --- |
| `page` | 1 veya daha büyük tam sayı. Varsayılan `1`. |
| `limit` | 1 ile 100 arasında tam sayı. Varsayılan `30`. |
| `tag` | İsteğe bağlı konu dizesi. |
| `category` | İsteğe bağlı kategori kimliği. |

Yanıt başlıkları:

- `Link`, `rel="next"` kullanır; önceki bir sayfa varsa `rel="prev"` de bulunur.
- `Picsum-Total`, eşleşen fotoğraf sayısıdır. `tag` ve `category` yoksa değer `100000` olur.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

`limit=1` ile yapılan birinci sayfa isteği şu `Link` başlığını ve `Picsum-Total: 100000` değerini döndürmüştür:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Gövde, [Nesne alanları](#fields) bölümünde anlatılan nesnenin bir dizisidir. Her öğe bir fotoğraftır. Sıra değişebilir; ilk satırı sabit bir fotoğraf saymayın.

<a id="info-id"></a>

### Kimliğe göre tek fotoğraf

```http
GET https://picsum.org/id/{id}/info
```

Bilinen bir kimlik `200` ve tek bir JSON nesnesi döndürür. Bilinmeyen bir kimlik `404` ve tam olarak şu gövdeyi döndürür:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Başlangıç değerine göre tek fotoğraf

```http
GET https://picsum.org/seed/{seed}/info
```

Yanıt `200`, tek bir JSON nesnesi ve bir `Picsum-ID` başlığıdır. Hiçbir etiketle eşleşmeyen bir başlangıç değeri hata döndürmez. Başlangıç değerli görsel URL’sinin verdiği sabit yedek fotoğrafı döndürür.

<a id="fields"></a>

### Nesne alanları

| Alan | Anlamı |
| --- | --- |
| `id` | Dize olarak fotoğraf kimliği. |
| `author` | Fotoğrafçının adı. Dize boş olabilir. |
| `width` | Piksel cinsinden özgün genişlik. İstekte belirttiğiniz çıktı genişliği değildir. |
| `height` | Piksel cinsinden özgün yükseklik. İstekte belirttiğiniz çıktı yüksekliği değildir. |
| `description` | Fotoğrafın kısa açıklaması. |
| `category` | Bir kategori kimliği. |
| `tags` | Konu dizelerinden oluşan dizi. |
| `url` | Özgün kaynağın sayfası. |
| `license` | Tam olarak `"CC0 1.0"` dizesi. |
| `license_url` | Tam olarak `"https://creativecommons.org/publicdomain/zero/1.0/"` dizesi. |
| `download_url` | Bu fotoğrafın 800×600 JPEG URL’si. |

WebP veya gri tonlama URL’sini `id` alanından oluşturun. `download_url` her zaman 800×600 JPEG’dir.

<a id="examples"></a>

### Örnekler

`GET https://picsum.org/id/179363399/info` şunu döndürür:

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

Fotoğraf 3840×2160 boyutundadır. Fotoğrafçı Syony olarak kayıtlıdır. Kategori `landscapes` değeridir. Açıklama “Colorful mountain slopes in Landmannalaugar” şeklindedir. Etiketler `mountains`, `highlands`, `colorful` ve `iceland` değerleridir.

`GET https://picsum.org/seed/studio/info` şunu döndürür:

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

Yanıt başlığındaki `Picsum-ID` değeri `1000561303` olur. Özgün kadraj 2400×1800 boyutundadır, `author` boştur ve `category` değeri `food` olur.

<a id="categories"></a>

## Kategoriler

`category` parametresine aşağıdaki kimliklerden birini verin. Herkese açık bir HTTP `/categories` uç noktası yoktur. MCP aracı `list_categories` aynı kimlikleri döndürür; her kimliğin yanında İngilizce görünen ad ve bir grup bulunur. Bu tablodaki adlar okurlar için yapılmış çevirilerdir. İsteklerde kimliği gönderin.

### Doğa ve manzaralar

| Kimlik | Ad |
| --- | --- |
| `coasts` | Kıyılar ve okyanuslar |
| `deserts` | Çöller ve kum tepeleri |
| `freshwater` | Göller ve şelaleler |
| `gardens` | Bahçeler |
| `landscapes` | Manzaralar |
| `macro` | Makro fotoğrafçılık |
| `mountains` | Dağlar |
| `plants` | Bitkiler ve çiçekler |
| `skies` | Gökyüzü ve hava durumu |
| `snow` | Kar ve buz |
| `woodlands` | Ormanlar |

### Hayvanlar

| Kimlik | Ad |
| --- | --- |
| `animals` | Diğer hayvanlar |
| `birds` | Kuşlar |
| `insects` | Böcekler |
| `marine` | Deniz yaşamı |
| `pets` | Evcil hayvanlar |

### Yerler ve seyahat

| Kimlik | Ad |
| --- | --- |
| `aerial` | Hava fotoğrafçılığı |
| `architecture` | Mimari |
| `city` | Şehirler ve sokaklar |
| `interiors` | İç mekânlar |
| `landmarks` | Görülecek yerler |
| `night` | Gece fotoğrafçılığı |
| `transport` | Ulaşım |

### Nesneler ve etkinlikler

| Kimlik | Ad |
| --- | --- |
| `agriculture` | Tarım |
| `food` | Yiyecek ve içecek |
| `industry` | Sanayi |
| `music` | Müzik |
| `objects` | Nesneler |
| `sculpture` | Heykel |
| `sports` | Spor |
| `technology` | Teknoloji |
| `textures` | Dokular |
| `workspaces` | Çalışma alanları |

<a id="headers"></a>

## Başlıklar, önbellek ve CORS

Görsel ve JSON yanıtları şunları gönderir:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` listesinde `Picsum-ID`, `Picsum-Total` ve `Link` vardır. Böylece başka bir kökendeki sayfa bu üç başlığı `fetch` ile okuyabilir.

| Yanıt | `Cache-Control` |
| --- | --- |
| Rastgele yönlendirme, `/{width}` veya `/{width}/{height}` | `no-store` |
| Başlangıç değerli yönlendirme, `/seed/{seed}/...` | `public, max-age=3600` |
| Sabitlenmiş görsel, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Rastgele yönlendirme `no-store` olduğu için sonraki istek başka bir fotoğraf seçebilir. `Location` içindeki `/id/...` URL’si önbelleğe alınabilen dosyadır. Yeni bir boyut veya efekt için ilk istek, dosya önbelleğe alınmadan önce biraz daha uzun sürebilir.

Aşağıda belgelenen 400 ve 404 JSON hataları da `Cache-Control: no-store` ve `Access-Control-Allow-Origin: *` ile gönderilir.

<a id="errors"></a>

## Hatalar ve hız sınırları

Hata gövdeleri JSON’dur. Bu `error` dizelerini aynen eşleştirin.

Geçersiz görsel boyutları, desteklenmeyen bir uzantı veya 1–10 aralığının dışındaki bir bulanıklık değeri (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`/v2/list` üzerinde geçersiz `page` veya `limit` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

`/id/{id}/info` üzerinde bilinmeyen fotoğraf kimliği (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429, hız sınırının uygulandığını gösterir. `Retry-After` yanıt başlığına uyun. Hizmetin kalitesini düşüren otomatik trafik çalıştırmayın ve hız sınırlarını dolanmayın.

<a id="code"></a>

## Kod örnekleri

<a id="html"></a>

### HTML

`width`, `height` ve `alt` değerlerini belirtin. `alt`, fotoğrafı anlatmalıdır. Aşağıdaki açıklama, `179363399` fotoğrafının `description` alanıdır.

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

İlk komut, görseli kaydetmeden başlangıç değerli yönlendirmenin başlıklarını yazar; `Location` ve `Picsum-ID` bu başlıklar arasındadır. İkinci komut tek bir fotoğraf nesnesini yazar. Üçüncü komut liste başlıklarını ve bir JSON dizisini yazar.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`Access-Control-Allow-Origin` değeri `*` olduğu için `fetch`, JSON uç noktalarını tarayıcıdan çağırabilir. `Picsum-Total` istemciye açıldığı için `headers.get` bu değeri okuyabilir.

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

Bu örnek `requests` kütüphanesini kullanır.

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

## Lisans ve ticari kullanım

Fotoğraflar [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) kapsamındadır. Kişisel kullanım ve ticari kullanım ücretsizdir. Atıf isteğe bağlıdır. Bir fotoğrafı kaynak göstermek istediğinizde JSON nesnesindeki `author` fotoğrafçıyı, `url` kaynak sayfasını gösterir.

Hassas bir kullanımda tanınabilir kişiler, ticari markalar ve özgün kaynak kaydı sizin sorumluluğunuzdadır. Böyle bir kullanımdan önce `url` alanını kontrol edin.

Bu hizmeti kendi görsel API’niz olarak yeniden satmayın veya yeniden dağıtmayın.

Sorular: [hello@picsum.org](mailto:hello@picsum.org).

Kullanım koşulları: [Kullanım koşulları](https://picsum.org/tr/terms).

<a id="mcp"></a>

## MCP sunucusu

Barındırılan bir MCP sunucusu, Model Context Protocol kullanan istemcilere salt okunur fotoğraf sorguları sunar. Yukarıdaki görsel URL’lerin yerini almaz ve metin isteminden görsel üretmez. Görsel URL’ler `https://picsum.org/{...}` adresinde kalır. MCP uç noktası ayrıdır.

| | |
| --- | --- |
| Uç nokta | `https://picsum.org/mcp` |
| Aktarım | Streamable HTTP |
| Yetkilendirme | PKCE ile OAuth 2.1 |
| Kapsam | `photos:read` |
| Kurulum kılavuzu | [Yapay zekâ asistanınızı Picsum’a bağlayın](https://picsum.org/tr/connect) |
| İstemci yapılandırması | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Araçlar salt okunurdur:

| Araç | Ne yapar |
| --- | --- |
| `search_photos` | `tag` ile, `category` ile veya ikisiyle birden arar. |
| `get_photo` | Tek bir fotoğraf kimliğinin üst verisini verir. |
| `list_categories` | Her kategori kimliğini, İngilizce görünen adını ve grubunu döndürür. |
| `build_image_url` | Seçilen boyut, biçim, gri tonlama ve bulanıklık için bir görsel URL’si ile bir HTML `<img>` parçası üretir. |

Oturum açma ve istemci kurulumu [Yapay zekâ asistanınızı Picsum’a bağlayın](https://picsum.org/tr/connect) kılavuzunda anlatılır. Diğer diller aynı `/connect` yolunu kendi dil öneklerinin altında kullanır. Görsel isteklerini bu önek üzerinden göndermeyin. Yapılandırma örnekleri [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) adresindedir.
