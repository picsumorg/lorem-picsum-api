[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · **Tiếng Việt** · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/vi) là trình tạo ảnh ngẫu nhiên miễn phí, dùng làm API ảnh giữ chỗ. Dịch vụ phục vụ **100.000 ảnh CC0** theo [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) trong **33 danh mục**. Đường dẫn ảnh, cỡ tùy chọn, JPEG và WebP, thang độ xám, làm mờ cùng các điểm cuối siêu dữ liệu JSON không cần tài khoản hay khóa API.

Lorem Picsum (`picsum.org`) là dịch vụ độc lập, lấy cảm hứng từ dự án mã nguồn mở Picsum Photos. Dịch vụ không liên kết với `picsum.photos`. Bộ sưu tập và mã ảnh là của riêng dịch vụ này. Các đường dẫn của dự án kia, kể cả đường dẫn thang độ xám như `/g/{width}/{height}`, không thuộc API này.

URL cơ sở của API là `https://picsum.org`. Bạn không đặt tiền tố ngôn ngữ của trang web phía trước đường dẫn API. `https://picsum.org/de/800/600` thuộc trang web, không phải đường dẫn ảnh. Tiền tố ngôn ngữ (`/de`, `/ja`, `/zh-tw` và các tiền tố còn lại) dành cho các trang như trang chủ, hướng dẫn thiết lập MCP và điều khoản sử dụng.

## Mục lục

- [Tổng quan](#overview)
- [Bắt đầu nhanh](#quick-start)
- [Đường dẫn ảnh](#image-urls)
- [Siêu dữ liệu JSON](#json)
- [Danh mục](#categories)
- [Tiêu đề, bộ nhớ đệm và CORS](#headers)
- [Lỗi và giới hạn tần suất](#errors)
- [Ví dụ mã](#code)
- [Giấy phép và sử dụng thương mại](#license)
- [Máy chủ MCP](#mcp)

<a id="overview"></a>

## Tổng quan

Khi bố cục cần một ảnh, bạn lấy một đường dẫn ảnh. Khi bạn cần tác giả, mô tả, danh mục, thẻ, kích thước gốc, trang nguồn hoặc giấy phép, bạn lấy JSON.

Một đường dẫn ngẫu nhiên có thể chọn ảnh khác ở mỗi yêu cầu. Một seed, hoặc một mã ảnh, giữ nguyên ảnh nguồn. Chiều rộng và chiều cao là số nguyên từ **1 đến 2000** pixel. Mọi cỡ tùy chọn trong khoảng đó đều miễn phí, thang độ xám và làm mờ cũng vậy. Sáu cỡ trên trang chủ là cỡ có sẵn cho tiện, không phải mức trần.

<a id="quick-start"></a>

## Bắt đầu nhanh

Ảnh ngẫu nhiên 800×600 này chuyển hướng tới một ảnh cụ thể. Bộ nhớ đệm không lưu chuyển hướng, và phản hồi đưa mã đã chọn vào `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Khi ảnh phải giữ nguyên, bạn dùng đường dẫn cố định:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Khi ảnh phải lặp lại được, bạn dùng seed. Cùng một seed luôn cho cùng ảnh nguồn ở mọi cỡ. Seed `studio` ứng với `1000561303`. Ví dụ này yêu cầu WebP, thang độ xám và làm mờ:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## Đường dẫn ảnh

<a id="dimensions"></a>

### Kích thước và cắt ảnh

`width` và `height` là hai đoạn của đường dẫn. Mỗi giá trị là số nguyên từ 1 đến 2000, tính cả hai đầu. Dịch vụ thu phóng bức ảnh rồi cắt từ tâm để lấp kín khung chữ nhật bạn yêu cầu. Ảnh không bị kéo giãn.

<a id="formats"></a>

### Định dạng

| Phần mở rộng | Nội dung nhận được |
| --- | --- |
| *(không có)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` và `.avif` không được chấp nhận. Phản hồi là HTTP 400, kèm đối tượng lỗi ảnh ở phần dưới. `.jpeg` không phải bí danh của `.jpg`.

<a id="random-rectangle"></a>

### Ảnh chữ nhật ngẫu nhiên

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Phản hồi là `302 Found`. `Location` là `/id/{id}/{width}/{height}.{ext}`. Khi không có phần mở rộng, `{ext}` là `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` là ảnh đã được chọn

`GET https://picsum.org/800/600` là cỡ tiêu chuẩn ở dạng này.

<a id="random-square"></a>

### Ảnh vuông ngẫu nhiên

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` yêu cầu một JPEG 640×640. Phản hồi là `302` tới `/id/{id}/{width}/{width}.jpg`, kèm `Cache-Control: no-store` và tiêu đề `Picsum-ID`.

<a id="seeded"></a>

### Ảnh theo seed

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Phản hồi là `302` tới `/id/{id}/{width}/{height}.{ext}`. URL seed dạng vuông dùng cùng một số cho chiều rộng và chiều cao. Khi bỏ phần mở rộng, giá trị đó là `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` là ảnh đã chọn
- Một seed luôn chọn cùng ảnh nguồn, kể cả khi đổi cỡ. `studio` chọn `1000561303`.
- Seed cũng được dùng làm từ khóa. `GET https://picsum.org/seed/cat/800/600` chọn một ảnh mèo.
- Nếu seed không khớp thẻ nào, dịch vụ chọn một ảnh cố định trong bộ sưu tập. Cùng seed đó luôn trả về đúng ảnh ấy.

<a id="pinned"></a>

### Ảnh cố định

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Phản hồi là `200 OK` và chuỗi byte của ảnh, `image/jpeg` hoặc `image/webp`. Đường dẫn vuông dùng một kích thước cho cả hai cạnh. Nếu bỏ phần mở rộng, ảnh là JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` trả về đúng `{id}`

Để đọc tác giả và trang nguồn của một mã, bạn gọi [`/id/{id}/info`](#info-id). Với mã không tồn tại, `404` được ghi cho đường dẫn siêu dữ liệu này, không phải cho đường dẫn ảnh.

<a id="query"></a>

### Tham số truy vấn

| Tham số | Phạm vi áp dụng | Quy tắc |
| --- | --- | --- |
| `tag` | Ảnh ngẫu nhiên, ảnh theo seed và `GET /v2/list` | Chuỗi chủ đề. Tham số này thu hẹp tập ảnh. Ví dụ: `?tag=forest`. |
| `category` | Ảnh ngẫu nhiên, ảnh theo seed và `GET /v2/list` | Một trong 33 mã danh mục. Ví dụ: `?category=woodlands`. |
| `grayscale` | Đường dẫn ảnh | Dạng cờ `?grayscale`. Thang độ xám được ghi vào tệp ảnh. Không có đường dẫn `/g/{width}/{height}`. |
| `blur` | Đường dẫn ảnh | Số nguyên từ 1 đến 10. `?blur` không kèm giá trị được chấp nhận và có nghĩa là `blur=5`. `blur=0` và `blur=11` trả về HTTP 400. |

`tag` và `category` được dùng khi chọn ảnh. Chúng không được sao chép vào `Location` của chuyển hướng.

Thang độ xám và làm mờ đi theo ảnh. Yêu cầu theo seed sau:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

trả về `302` với:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Cờ `grayscale` được ghi thành `grayscale=1` trên URL cố định đó. `blur=4` được giữ nguyên. Bản thân tệp đã ở thang độ xám và đã làm mờ. Đây không phải bộ lọc CSS.

<a id="presets"></a>

### Cỡ có sẵn trên trang chủ

Sáu cỡ này là cỡ có sẵn trên trang chủ. Mọi cỡ khác từ 1 đến 2000 cũng miễn phí.

| Cỡ có sẵn | Pixel | URL |
| --- | --- | --- |
| Tiêu chuẩn | 800×600 | `https://picsum.org/800/600` |
| Vuông | 640×640 | `https://picsum.org/640` |
| Ngang | 1200×800 | `https://picsum.org/1200/800` |
| Dọc | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Yêu cầu đầu tiên cho một cỡ mới, hoặc một tổ hợp thang độ xám hay làm mờ mới, có thể lâu hơn một chút. Sau đó, tệp cố định được lưu vào bộ nhớ đệm.

<a id="json"></a>

## Siêu dữ liệu JSON

Không tồn tại điểm cuối `/list` của v1. Bộ sưu tập được liệt kê tại `/v2/list`.

`/v2/list` trả về một mảng JSON. `/id/{id}/info` và `/seed/{seed}/info` trả về một đối tượng JSON. Cả ba đều gửi `Cache-Control: public, max-age=300` và `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Liệt kê ảnh

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Tham số | Quy tắc |
| --- | --- |
| `page` | Số nguyên lớn hơn hoặc bằng 1. Mặc định là `1`. |
| `limit` | Số nguyên từ 1 đến 100. Mặc định là `30`. |
| `tag` | Chuỗi chủ đề, không bắt buộc. |
| `category` | Mã danh mục, không bắt buộc. |

Tiêu đề phản hồi:

- `Link`, dùng `rel="next"` và, khi có trang trước, `rel="prev"`.
- `Picsum-Total`, số ảnh khớp. Khi không có `tag` và không có `category`, giá trị là `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Một yêu cầu trang 1 với `limit=1` đã trả về tiêu đề `Link` này và `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Phần thân là một mảng các đối tượng mô tả trong [Các trường của đối tượng](#fields). Mỗi phần tử là một ảnh. Thứ tự có thể thay đổi; bạn không nên lấy dòng đầu tiên làm một ảnh cố định.

<a id="info-id"></a>

### Một ảnh theo mã

```http
GET https://picsum.org/id/{id}/info
```

Mã tồn tại trả về `200` và một đối tượng JSON. Mã không tồn tại trả về `404` và đúng phần thân sau:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Một ảnh theo seed

```http
GET https://picsum.org/seed/{seed}/info
```

Phản hồi là `200` và một đối tượng JSON, kèm tiêu đề `Picsum-ID`. Seed không khớp thẻ nào không trả về lỗi. Kết quả là cùng ảnh cố định mà đường dẫn ảnh theo seed cũng trả về.

<a id="fields"></a>

### Các trường của đối tượng

| Trường | Ý nghĩa |
| --- | --- |
| `id` | Mã ảnh, dưới dạng chuỗi. |
| `author` | Tên người tạo. Chuỗi có thể rỗng. |
| `width` | Chiều rộng gốc, tính bằng pixel. Đây không phải chiều rộng bạn yêu cầu kết xuất. |
| `height` | Chiều cao gốc, tính bằng pixel. Đây không phải chiều cao bạn yêu cầu kết xuất. |
| `description` | Mô tả ngắn của bức ảnh. |
| `category` | Một mã danh mục. |
| `tags` | Mảng các chuỗi chủ đề. |
| `url` | Trang của nguồn gốc. |
| `license` | Đúng chuỗi `"CC0 1.0"`. |
| `license_url` | Đúng chuỗi `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | URL JPEG của ảnh này ở cỡ 800×600. |

Bạn tạo URL WebP hoặc URL thang độ xám từ `id`. `download_url` luôn là JPEG 800×600.

<a id="examples"></a>

### Ví dụ

`GET https://picsum.org/id/179363399/info` trả về:

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

Bức ảnh có kích thước 3840×2160, của Syony, thuộc `landscapes`, được mô tả là “Colorful mountain slopes in Landmannalaugar”. Các thẻ là `mountains`, `highlands`, `colorful` và `iceland`.

`GET https://picsum.org/seed/studio/info` trả về:

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

Tiêu đề phản hồi `Picsum-ID` là `1000561303`. Khung gốc là 2400×1800, `author` để trống và `category` là `food`.

<a id="categories"></a>

## Danh mục

Bạn truyền một trong các mã này vào `category`. Không có điểm cuối HTTP công khai `/categories`. Công cụ MCP `list_categories` trả về cùng các mã này, mỗi mã kèm tên hiển thị tiếng Anh và một nhóm. Tên trong bảng này là bản dịch cho người đọc; `list_categories` trả về tên tiếng Anh. Bạn gửi mã, không gửi tên hiển thị.

### Thiên nhiên và phong cảnh

| ID | Tên |
| --- | --- |
| `coasts` | Bờ biển và đại dương |
| `deserts` | Sa mạc và cồn cát |
| `freshwater` | Hồ và thác nước |
| `gardens` | Vườn |
| `landscapes` | Phong cảnh |
| `macro` | Macro |
| `mountains` | Núi |
| `plants` | Cây và hoa |
| `skies` | Bầu trời và thời tiết |
| `snow` | Tuyết và băng |
| `woodlands` | Rừng |

### Động vật

| ID | Tên |
| --- | --- |
| `animals` | Động vật khác |
| `birds` | Chim |
| `insects` | Côn trùng |
| `marine` | Sinh vật biển |
| `pets` | Thú cưng |

### Địa điểm và du lịch

| ID | Tên |
| --- | --- |
| `aerial` | Ảnh trên không |
| `architecture` | Kiến trúc |
| `city` | Thành phố và đường phố |
| `interiors` | Nội thất |
| `landmarks` | Địa danh |
| `night` | Đêm |
| `transport` | Giao thông |

### Đồ vật và hoạt động

| ID | Tên |
| --- | --- |
| `agriculture` | Nông nghiệp |
| `food` | Đồ ăn và đồ uống |
| `industry` | Công nghiệp |
| `music` | Âm nhạc |
| `objects` | Đồ vật |
| `sculpture` | Điêu khắc |
| `sports` | Thể thao |
| `technology` | Công nghệ |
| `textures` | Kết cấu |
| `workspaces` | Không gian làm việc |

<a id="headers"></a>

## Tiêu đề, bộ nhớ đệm và CORS

Phản hồi ảnh và phản hồi JSON đều gửi:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` gồm `Picsum-ID`, `Picsum-Total` và `Link`, nên một trang ở nguồn khác có thể đọc ba tiêu đề đó qua `fetch`.

| Phản hồi | `Cache-Control` |
| --- | --- |
| Chuyển hướng ngẫu nhiên, `/{width}` hoặc `/{width}/{height}` | `no-store` |
| Chuyển hướng theo seed, `/seed/{seed}/...` | `public, max-age=3600` |
| Ảnh cố định, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Chuyển hướng ngẫu nhiên dùng `no-store`, nên yêu cầu kế tiếp có thể chọn ảnh khác. URL `/id/...` trong `Location` là tệp được lưu đệm. Yêu cầu đầu tiên cho một cỡ hoặc hiệu ứng mới có thể lâu hơn một chút, trước khi tệp đó được lưu đệm.

Các lỗi JSON 400 và 404 nêu bên dưới cũng được gửi với `Cache-Control: no-store` và `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Lỗi và giới hạn tần suất

Phần thân lỗi là JSON. Bạn cần khớp đúng từng chuỗi `error`.

Kích thước ảnh không hợp lệ, phần mở rộng không được hỗ trợ, hoặc giá trị làm mờ nằm ngoài khoảng 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`page` hoặc `limit` không hợp lệ trên `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Mã ảnh không tồn tại trên `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 nghĩa là giới hạn tần suất đã áp dụng. Bạn tuân theo tiêu đề phản hồi `Retry-After`. Bạn không được gửi lưu lượng tự động làm suy giảm dịch vụ, và không được tìm cách vượt giới hạn tần suất.

<a id="code"></a>

## Ví dụ mã

<a id="html"></a>

### HTML

Bạn đặt `width`, `height` và `alt`. `alt` nên mô tả bức ảnh. Lời mô tả dưới đây chính là `description` của ảnh `179363399`.

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

Lệnh thứ nhất in các tiêu đề của chuyển hướng theo seed, gồm `Location` và `Picsum-ID`, và không lưu ảnh. Lệnh thứ hai in một đối tượng ảnh. Lệnh thứ ba in tiêu đề của danh sách cùng một mảng JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` gọi được các điểm cuối JSON từ trình duyệt vì `Access-Control-Allow-Origin` là `*`. `Picsum-Total` nằm trong các tiêu đề được phép đọc, nên `headers.get` lấy được giá trị này.

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

Ví dụ này dùng thư viện `requests`.

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

## Giấy phép và sử dụng thương mại

Các bức ảnh thuộc [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Mục đích cá nhân và mục đích thương mại đều miễn phí. Ghi tên tác giả là tùy chọn. Khi bạn muốn ghi công một ảnh, `author` là người tạo và `url` là trang nguồn; cả hai trường đều nằm trong đối tượng JSON.

Với cách dùng nhạy cảm, bạn chịu trách nhiệm về người nhận diện được, nhãn hiệu và bản ghi nguồn gốc. Bạn kiểm tra `url` trước khi dùng theo cách đó.

Bạn không được bán lại hoặc phân phối lại dịch vụ này như API ảnh của riêng bạn.

Câu hỏi: [hello@picsum.org](mailto:hello@picsum.org).

Điều khoản sử dụng: [Điều khoản sử dụng](https://picsum.org/vi/terms).

<a id="mcp"></a>

## Máy chủ MCP

Picsum chạy một máy chủ MCP để trả lời truy vấn ảnh chỉ đọc cho ứng dụng khách hỗ trợ giao thức MCP. Máy chủ không thay thế các đường dẫn ảnh ở trên, và không tạo ảnh từ lời nhắc bằng chữ. Đường dẫn ảnh vẫn nằm ở `https://picsum.org/{...}`. Điểm cuối MCP là một địa chỉ riêng.

| | |
| --- | --- |
| Điểm cuối | `https://picsum.org/mcp` |
| Cách truyền | Streamable HTTP |
| Ủy quyền | OAuth 2.1 với PKCE |
| Phạm vi | `photos:read` |
| Hướng dẫn thiết lập | [Kết nối trợ lý AI với Picsum](https://picsum.org/vi/connect) |
| Cấu hình ứng dụng khách | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Các công cụ này chỉ đọc:

| Công cụ | Chức năng |
| --- | --- |
| `search_photos` | Tìm theo `tag`, theo `category`, hoặc theo cả hai. |
| `get_photo` | Siêu dữ liệu của một mã ảnh. |
| `list_categories` | Mọi mã danh mục, kèm tên hiển thị tiếng Anh và nhóm. |
| `build_image_url` | Một đường dẫn ảnh và một đoạn HTML `<img>`, theo cỡ, định dạng, thang độ xám và làm mờ bạn chọn. |

Cách đăng nhập và thiết lập ứng dụng khách được ghi trong [Kết nối trợ lý AI với Picsum](https://picsum.org/vi/connect). Các ngôn ngữ khác dùng cùng đường dẫn `/connect` dưới tiền tố ngôn ngữ của trang đó. Ví dụ cấu hình nằm tại [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
