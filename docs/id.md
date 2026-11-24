[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · **Bahasa Indonesia** · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/id) adalah API generator gambar acak yang gratis. Layanan ini menyajikan **100.000 foto CC0** berlisensi [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) dalam **33 kategori**. Tautan gambar, ukuran khusus, JPEG dan WebP, skala abu-abu, blur, serta endpoint metadata JSON tidak memerlukan akun maupun kunci API.

Lorem Picsum (`picsum.org`) adalah layanan independen yang terinspirasi oleh proyek sumber terbuka Picsum Photos. Layanan ini tidak berafiliasi dengan `picsum.photos`. Layanan ini memiliki katalog sendiri dan ID foto sendiri. Path dari proyek lain tersebut, termasuk path skala abu-abu seperti `/g/{width}/{height}`, bukan bagian dari API ini.

URL dasar API adalah `https://picsum.org`. Jangan menaruh prefiks locale situs web di depan path API. `https://picsum.org/de/800/600` adalah rute situs web, bukan tautan gambar. Prefiks locale (`/de`, `/ja`, `/zh-tw`, dan selebihnya) hanya untuk halaman seperti beranda, panduan penyiapan MCP, dan ketentuan.

## Daftar isi

- [Ikhtisar](#overview)
- [Mulai cepat](#quick-start)
- [Tautan gambar](#image-urls)
- [Metadata JSON](#json)
- [Kategori](#categories)
- [Header, cache, dan CORS](#headers)
- [Kesalahan dan batas laju](#errors)
- [Contoh kode](#code)
- [Lisensi dan penggunaan komersial](#license)
- [Server MCP](#mcp)

<a id="overview"></a>

## Ikhtisar

Minta tautan gambar ketika tata letak memerlukan foto. Minta JSON ketika Anda memerlukan penulis, deskripsi, kategori, tag, dimensi asli, halaman sumber, atau lisensi.

URL acak dapat memilih foto yang berbeda pada setiap permintaan. Seed, atau ID foto, mempertahankan foto sumber yang sama. Lebar dan tinggi adalah bilangan bulat dari **1 sampai 2000** piksel. Setiap ukuran khusus dalam rentang itu gratis, begitu pula skala abu-abu dan blur. Enam ukuran di beranda hanyalah preset praktis, bukan batas maksimum.

<a id="quick-start"></a>

## Mulai cepat

Gambar acak berukuran 800×600 ini dialihkan ke foto tertentu. Pengalihan tidak disimpan oleh cache, dan respons menyertakan ID yang dipilih pada `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Gunakan URL tersemat ketika gambar harus tetap sama:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Gunakan seed ketika gambar harus dapat diulang. Seed yang sama selalu dipetakan ke foto sumber yang sama pada setiap ukuran. Seed `studio` dipetakan ke `1000561303`. Contoh ini meminta WebP, skala abu-abu, dan blur:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Tautan gambar

<a id="dimensions"></a>

### Dimensi dan pemotongan

`width` dan `height` adalah segmen path. Masing-masing berupa bilangan bulat dari 1 sampai 2000 inklusif. Layanan menskalakan foto lalu memotongnya di tengah agar persegi panjang yang diminta terisi penuh. Gambar tidak diregangkan.

<a id="formats"></a>

### Format

| Ekstensi | Yang Anda peroleh |
| --- | --- |
| *(tidak ada)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif`, dan `.avif` tidak diterima. Responsnya HTTP 400 dan objek kesalahan gambar di bawah. `.jpeg` bukan alias dari `.jpg`.

<a id="random-rectangle"></a>

### Persegi panjang acak

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Responsnya `302 Found`. `Location` berisi `/id/{id}/{width}/{height}.{ext}`. Jika ekstensi dihilangkan, `{ext}` bernilai `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` adalah foto yang dipilih

`GET https://picsum.org/800/600` adalah preset standar dalam bentuk ini.

<a id="random-square"></a>

### Persegi acak

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` meminta JPEG berukuran 640×640. Responsnya `302` ke `/id/{id}/{width}/{width}.jpg`, dengan `Cache-Control: no-store` dan header `Picsum-ID`.

<a id="seeded"></a>

### Foto berdasarkan seed

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Responsnya `302` ke `/id/{id}/{width}/{height}.{ext}`. URL seed berbentuk persegi memakai angka yang sama untuk lebar dan tinggi. Ekstensi yang dihilangkan bernilai `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` adalah foto yang dipilih
- Satu seed selalu memilih foto sumber yang sama, termasuk ketika ukuran berubah. `studio` memilih `1000561303`.
- Seed juga dipakai sebagai kata subjek. `GET https://picsum.org/seed/cat/800/600` memilih foto kucing.
- Jika seed tidak cocok dengan tag mana pun, layanan memakai satu foto stabil dari koleksi sebagai cadangan. Seed tidak dikenal yang sama selalu mengembalikan foto yang sama.

<a id="pinned"></a>

### Foto tersemat

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Responsnya `200 OK` dan byte gambar, `image/jpeg` atau `image/webp`. Path persegi memakai satu dimensi untuk kedua sisi. Ekstensi yang dihilangkan berarti JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` berisi `{id}` yang sama

Untuk membaca penulis dan halaman sumber suatu ID, panggil [`/id/{id}/info`](#info-id). Rute metadata itu, bukan rute gambar, adalah `404` yang didokumentasikan untuk ID yang tidak dikenal.

<a id="query"></a>

### Parameter kueri

| Parameter | Berlaku untuk | Aturan |
| --- | --- | --- |
| `tag` | Gambar acak, gambar berdasarkan seed, dan `GET /v2/list` | String subjek. Mempersempit kumpulan foto. Contoh: `?tag=forest`. |
| `category` | Gambar acak, gambar berdasarkan seed, dan `GET /v2/list` | Salah satu dari 33 ID kategori. Contoh: `?category=woodlands`. |
| `grayscale` | Tautan gambar | Bentuk bendera `?grayscale`. Skala abu-abu tertanam di dalam berkas gambar. Tidak ada path `/g/{width}/{height}`. |
| `blur` | Tautan gambar | Bilangan bulat dari 1 sampai 10. `?blur` tanpa nilai diterima dan berarti `blur=5`. `blur=0` dan `blur=11` mengembalikan HTTP 400. |

`tag` dan `category` dipakai saat foto dipilih. Keduanya tidak disalin ke `Location` pada pengalihan.

Skala abu-abu dan blur menyertai gambar. Permintaan berdasarkan seed ini:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

merespons `302` dengan:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Bendera `grayscale` ditulis sebagai `grayscale=1` pada URL tersemat itu. `blur=4` dipertahankan. Berkasnya sendiri berskala abu-abu dan blur; ini bukan filter CSS.

<a id="presets"></a>

### Preset ukuran di beranda

Enam ukuran ini adalah preset yang ditampilkan di beranda. Ukuran lain dari 1 sampai 2000 juga gratis.

| Preset | Piksel | URL |
| --- | --- | --- |
| Standar | 800×600 | `https://picsum.org/800/600` |
| Persegi | 640×640 | `https://picsum.org/640` |
| Lanskap | 1200×800 | `https://picsum.org/1200/800` |
| Potret | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Permintaan pertama untuk ukuran baru, atau kombinasi skala abu-abu maupun blur yang baru, dapat sedikit lebih lama. Setelah itu, berkas tersemat tersimpan di cache.

<a id="json"></a>

## Metadata JSON

Tidak ada endpoint `/list` v1. Koleksi dicantumkan di `/v2/list`.

`/v2/list` mengembalikan array JSON. `/id/{id}/info` dan `/seed/{seed}/info` mengembalikan satu objek JSON. Ketiganya mengirim `Cache-Control: public, max-age=300` dan `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Daftar foto

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Kueri | Aturan |
| --- | --- |
| `page` | Bilangan bulat lebih besar atau sama dengan 1. Bawaan `1`. |
| `limit` | Bilangan bulat dari 1 sampai 100. Bawaan `30`. |
| `tag` | String subjek opsional. |
| `category` | ID kategori opsional. |

Header respons:

- `Link`, memakai `rel="next"` dan, jika ada halaman sebelumnya, `rel="prev"`.
- `Picsum-Total`, jumlah foto yang cocok. Tanpa `tag` dan tanpa `category`, nilainya `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Permintaan halaman 1 dengan `limit=1` mengembalikan header `Link` ini dan `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Isi respons berupa array objek yang dijelaskan di [Bidang objek](#fields). Setiap elemen adalah satu foto. Urutan dapat berubah; jangan anggap baris pertama sebagai foto tetap.

<a id="info-id"></a>

### Satu foto menurut ID

```http
GET https://picsum.org/id/{id}/info
```

ID yang dikenal mengembalikan `200` dan satu objek JSON. ID yang tidak dikenal mengembalikan `404` dan isi persis ini:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Satu foto menurut seed

```http
GET https://picsum.org/seed/{seed}/info
```

Responsnya `200` dan satu objek JSON, ditambah header `Picsum-ID`. Seed yang tidak cocok dengan tag mana pun tidak mengembalikan kesalahan. Seed itu mengembalikan foto cadangan stabil yang sama seperti tautan gambar berdasarkan seed.

<a id="fields"></a>

### Bidang objek

| Bidang | Arti |
| --- | --- |
| `id` | ID foto, sebagai string. |
| `author` | Nama pembuat. String dapat kosong. |
| `width` | Lebar asli dalam piksel. Ini bukan lebar yang Anda minta untuk ditampilkan. |
| `height` | Tinggi asli dalam piksel. Ini bukan tinggi yang Anda minta untuk ditampilkan. |
| `description` | Deskripsi singkat foto. |
| `category` | Satu ID kategori. |
| `tags` | Array string subjek. |
| `url` | Halaman sumber asli. |
| `license` | String persis `"CC0 1.0"`. |
| `license_url` | String persis `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | Tautan JPEG foto ini pada ukuran 800×600. |

Bangun tautan WebP atau skala abu-abu dari `id`. `download_url` selalu berupa JPEG 800×600.

<a id="examples"></a>

### Contoh

`GET https://picsum.org/id/179363399/info` mengembalikan:

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

Foto berukuran 3840×2160, karya Syony, dalam `landscapes`, dideskripsikan sebagai “Colorful mountain slopes in Landmannalaugar”. Tag-nya `mountains`, `highlands`, `colorful`, dan `iceland`.

`GET https://picsum.org/seed/studio/info` mengembalikan:

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

Header respons `Picsum-ID` bernilai `1000561303`. Bingkai asli berukuran 2400×1800, `author` kosong, dan `category` adalah `food`.

<a id="categories"></a>

## Kategori

Kirim salah satu ID berikut pada `category`. Tidak ada endpoint HTTP publik `/categories`. Nama pada tabel ini adalah terjemahan untuk pembaca. Alat MCP `list_categories` mengembalikan ID yang sama, masing-masing dengan nama tampilan bahasa Inggris dan grupnya. Permintaan harus mengirim ID, bukan nama tampilan.

### Alam dan bentang alam

| ID | Nama |
| --- | --- |
| `coasts` | Pesisir & samudra |
| `deserts` | Gurun & gumuk pasir |
| `freshwater` | Danau & air terjun |
| `gardens` | Taman |
| `landscapes` | Bentang alam |
| `macro` | Makro |
| `mountains` | Pegunungan |
| `plants` | Tumbuhan & bunga |
| `skies` | Langit & cuaca |
| `snow` | Salju & es |
| `woodlands` | Hutan |

### Hewan

| ID | Nama |
| --- | --- |
| `animals` | Hewan lain |
| `birds` | Burung |
| `insects` | Serangga |
| `marine` | Kehidupan laut |
| `pets` | Hewan peliharaan |

### Tempat dan perjalanan

| ID | Nama |
| --- | --- |
| `aerial` | Foto udara |
| `architecture` | Arsitektur |
| `city` | Kota & jalan |
| `interiors` | Interior |
| `landmarks` | Tengara |
| `night` | Malam |
| `transport` | Transportasi |

### Benda dan kegiatan

| ID | Nama |
| --- | --- |
| `agriculture` | Pertanian |
| `food` | Makanan & minuman |
| `industry` | Industri |
| `music` | Musik |
| `objects` | Benda |
| `sculpture` | Patung |
| `sports` | Olahraga |
| `technology` | Teknologi |
| `textures` | Tekstur |
| `workspaces` | Ruang kerja |

<a id="headers"></a>

## Header, cache, dan CORS

Respons gambar dan JSON mengirim:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` mencakup `Picsum-ID`, `Picsum-Total`, dan `Link`, sehingga halaman pada origin lain dapat membaca ketiga header itu dari `fetch`.

| Respons | `Cache-Control` |
| --- | --- |
| Pengalihan acak, `/{width}` atau `/{width}/{height}` | `no-store` |
| Pengalihan berdasarkan seed, `/seed/{seed}/...` | `public, max-age=3600` |
| Gambar tersemat, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Pengalihan acak bernilai `no-store`, sehingga permintaan berikutnya dapat memilih foto lain. URL `/id/...` pada `Location` adalah berkas yang dapat disimpan di cache. Permintaan pertama untuk ukuran atau efek baru dapat sedikit lebih lama, sebelum berkas itu masuk cache.

Kesalahan JSON 400 dan 404 yang didokumentasikan di bawah juga dikirim dengan `Cache-Control: no-store` dan `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Kesalahan dan batas laju

Isi kesalahan berupa JSON. Cocokkan string `error` ini secara persis.

Dimensi gambar tidak valid, ekstensi yang tidak didukung, atau nilai blur di luar 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`page` atau `limit` tidak valid pada `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

ID foto tidak dikenal pada `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 berarti batas laju berlaku. Patuhi header respons `Retry-After`. Jangan menjalankan lalu lintas otomatis yang menurunkan mutu layanan, dan jangan mengakali batas laju.

<a id="code"></a>

## Contoh kode

<a id="html"></a>

### HTML

Tetapkan `width`, `height`, dan `alt`. `alt` sebaiknya mendeskripsikan foto. Deskripsi di bawah adalah `description` foto `179363399`.

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

Perintah pertama mencetak header pengalihan berdasarkan seed, termasuk `Location` dan `Picsum-ID`, dan tidak menyimpan gambar. Perintah kedua mencetak satu objek foto. Perintah ketiga mencetak header daftar dan array JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` dapat memanggil endpoint JSON dari peramban karena `Access-Control-Allow-Origin` bernilai `*`. `Picsum-Total` diekspos, sehingga `headers.get` dapat membacanya.

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

Contoh ini memakai pustaka `requests`.

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

## Lisensi dan penggunaan komersial

Foto-foto ini berlisensi [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Penggunaan pribadi dan penggunaan komersial gratis. Atribusi bersifat opsional. Jika Anda ingin memberi kredit pada suatu foto, `author` adalah pembuatnya dan `url` adalah halaman sumber, keduanya terdapat pada objek JSON.

Anda bertanggung jawab atas orang yang dapat dikenali, merek dagang, dan catatan sumber asli ketika suatu penggunaan bersifat sensitif. Periksa `url` sebelum penggunaan semacam itu.

Jangan menjual kembali atau mendistribusikan ulang layanan ini sebagai API gambar milik Anda sendiri.

Pertanyaan: [hello@picsum.org](mailto:hello@picsum.org).

Ketentuan penggunaan: [Ketentuan penggunaan](https://picsum.org/id/terms).

<a id="mcp"></a>

## Server MCP

Server MCP yang dihosting menjawab kueri foto hanya-baca untuk klien yang menggunakan Model Context Protocol. Server ini tidak menggantikan tautan gambar di atas, dan tidak menghasilkan gambar dari perintah teks. Tautan gambar tetap berada di `https://picsum.org/{...}`. Endpoint MCP terpisah.

| | |
| --- | --- |
| Endpoint | `https://picsum.org/mcp` |
| Transpor | Streamable HTTP |
| Otorisasi | OAuth 2.1 dengan PKCE |
| Cakupan | `photos:read` |
| Panduan penyiapan | [Hubungkan asisten AI Anda ke Picsum](https://picsum.org/id/connect) |
| Konfigurasi klien | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Alat-alat ini hanya-baca:

| Alat | Fungsinya |
| --- | --- |
| `search_photos` | Mencari menurut `tag`, menurut `category`, atau keduanya. |
| `get_photo` | Metadata untuk satu ID foto. |
| `list_categories` | Setiap ID kategori, dengan nama tampilan bahasa Inggris dan grupnya. |
| `build_image_url` | Tautan gambar, serta cuplikan HTML `<img>`, untuk ukuran, format, skala abu-abu, dan blur yang dipilih. |

Masuk dan penyiapan klien didokumentasikan di [Hubungkan asisten AI Anda ke Picsum](https://picsum.org/id/connect). Bahasa lain memakai path `/connect` yang sama di bawah prefiks locale masing-masing. Contoh konfigurasi ada di [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
