[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · **Українська** · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/uk) — безплатний API фотографій-заповнювачів. Це генератор випадкових зображень: він віддає **100 000 фото CC0** на умовах [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) у **33 категоріях**. Для URL зображень, власних розмірів, JPEG і WebP, відтінків сірого, розмиття та кінцевих точок метаданих JSON не потрібні ні обліковий запис, ні ключ API.

Lorem Picsum (`picsum.org`) — незалежний сервіс, натхненний відкритим проєктом Picsum Photos. Він не пов’язаний із `picsum.photos`. У нього власний каталог і власні ідентифікатори фото. Шляхи з того проєкту, зокрема шлях відтінків сірого на кшталт `/g/{width}/{height}`, не входять до цього API.

Базова URL-адреса API — `https://picsum.org`. Не ставте локаль вебсайту перед шляхом API. `https://picsum.org/de/800/600` — це маршрут вебсайту, а не URL зображення. Префікси локалей (`/de`, `/ja`, `/zh-tw` та решта) належать сторінкам на кшталт головної, посібника з підключення MCP та умов користування.

## Зміст

- [Огляд](#overview)
- [Швидкий старт](#quick-start)
- [URL зображень](#image-urls)
- [Метадані JSON](#json)
- [Категорії](#categories)
- [Заголовки, кешування та CORS](#headers)
- [Помилки та обмеження частоти запитів](#errors)
- [Приклади коду](#code)
- [Ліцензія й комерційне використання](#license)
- [Сервер MCP](#mcp)

<a id="overview"></a>

## Огляд

Запитуйте посилання на зображення, коли макету потрібне фото. Запитуйте JSON, коли потрібні автор, опис, категорія, теги, вихідні розміри, сторінка джерела або ліцензія.

Випадкове посилання може вибрати інше фото на кожен запит. Початкове значення або ID фото зберігає те саме вихідне фото. Ширина й висота — цілі числа від **1 до 2000** пікселів. Кожен власний розмір у цьому діапазоні безплатний, як і відтінки сірого та розмиття. Шість розмірів на головній сторінці — зручні пресети, а не верхня межа.

<a id="quick-start"></a>

## Швидкий старт

Це випадкове зображення 800×600 перенаправляє на конкретне фото. Перенаправлення не зберігається в кеші, а відповідь передає вибраний ID у заголовку `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Використайте закріплене посилання, коли знімок має залишатися тим самим:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Використайте початкове значення, коли знімок має повторюватися. Те саме початкове значення дає те саме вихідне фото за будь-якого розміру. Початкове значення `studio` відповідає фото `1000561303`. Цей приклад запитує WebP, відтінки сірого й розмиття:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## URL зображень

<a id="dimensions"></a>

### Розміри та кадрування

`width` і `height` — сегменти шляху. Кожен із них є цілим числом від 1 до 2000 включно. Сервіс масштабує фотографію й обрізає її від центру, щоб заповнити запитаний прямокутник. Знімок не розтягується.

<a id="formats"></a>

### Формати

| Розширення | Що ви отримуєте |
| --- | --- |
| *(немає)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` і `.avif` не приймаються. Відповідь — HTTP 400 і об’єкт помилки зображення нижче. `.jpeg` не є псевдонімом `.jpg`.

<a id="random-rectangle"></a>

### Випадковий прямокутник

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

Відповідь — `302 Found`. `Location` має вигляд `/id/{id}/{width}/{height}.{ext}`. Якщо розширення опущено, `{ext}` дорівнює `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` — вибране фото

`GET https://picsum.org/800/600` — стандартний пресет у цій формі.

<a id="random-square"></a>

### Випадковий квадрат

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` запитує JPEG розміром 640×640. Відповідь — `302` на адресу `/id/{id}/{width}/{width}.jpg`, з `Cache-Control: no-store` і заголовком `Picsum-ID`.

<a id="seeded"></a>

### Фото за початковим значенням

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

Відповідь — `302` на адресу `/id/{id}/{width}/{height}.{ext}`. Квадратна URL-адреса з початковим значенням використовує те саме число для ширини й висоти. Опущене розширення — `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` — вибране фото
- Одне початкове значення завжди вибирає те саме вихідне фото, навіть якщо розмір змінюється. `studio` вибирає `1000561303`.
- Початкове значення також є тематичним словом. `GET https://picsum.org/seed/cat/800/600` вибирає фотографію кота.
- Якщо початкове значення не збігається з жодним тегом, сервіс натомість вибирає одну сталу фотографію з колекції. Те саме невідоме початкове значення й далі повертає цю фотографію.

<a id="pinned"></a>

### Закріплене фото

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

Відповідь — `200 OK` і байти зображення, `image/jpeg` або `image/webp`. Квадратний шлях використовує один розмір для обох сторін. Опущене розширення — JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` повторює `{id}`

Щоб дізнатися автора й сторінку джерела для ID, викличте [`/id/{id}/info`](#info-id). Задокументована відповідь `404` для невідомого ID стосується цього маршруту метаданих, а не маршруту зображення.

<a id="query"></a>

### Параметри запиту

| Параметр | Де застосовується | Правило |
| --- | --- | --- |
| `tag` | Випадкові зображення, зображення з початковим значенням і `GET /v2/list` | Тематичний рядок. Він звужує добірку. Приклад: `?tag=forest`. |
| `category` | Випадкові зображення, зображення з початковим значенням і `GET /v2/list` | Один із 33 ідентифікаторів категорій. Приклад: `?category=woodlands`. |
| `grayscale` | URL зображень | Прапорець у формі `?grayscale`. Відтінки сірого вбудовано у файл зображення. Шляху `/g/{width}/{height}` немає. |
| `blur` | URL зображень | Ціле число від 1 до 10. Запис `?blur` без значення приймається і означає `blur=5`. `blur=0` і `blur=11` повертають HTTP 400. |

`tag` і `category` застосовуються під час вибору фото. Їх не копіюють у заголовок `Location` перенаправлення.

Відтінки сірого й розмиття передаються разом із зображенням. Цей запит із початковим значенням:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

відповідає `302` з такими заголовками:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

Прапорець `grayscale` на цьому закріпленому URL записується як `grayscale=1`. Значення `blur=4` зберігається. Сам файл у відтінках сірого й розмитий; це не CSS-фільтр.

<a id="presets"></a>

### Готові розміри на головній сторінці

Ці шість розмірів — пресети, показані на головній сторінці. Будь-який інший розмір від 1 до 2000 також безплатний.

| Пресет | Пікселі | URL |
| --- | --- | --- |
| Стандартний | 800×600 | `https://picsum.org/800/600` |
| Квадрат | 640×640 | `https://picsum.org/640` |
| Горизонтальний | 1200×800 | `https://picsum.org/1200/800` |
| Вертикальний | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

Перший запит нового розміру або нової комбінації відтінків сірого чи розмиття може тривати трохи довше. Після цього закріплений файл потрапляє в кеш.

<a id="json"></a>

## Метадані JSON

Кінцевої точки `/list` версії v1 немає. Колекцію наведено за адресою `/v2/list`.

`/v2/list` повертає масив JSON. `/id/{id}/info` і `/seed/{seed}/info` повертають один об’єкт JSON. Усі три надсилають `Cache-Control: public, max-age=300` і `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Перелік фото

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Параметр | Правило |
| --- | --- |
| `page` | Ціле число не менше ніж 1. За замовчуванням — `1`. |
| `limit` | Ціле число від 1 до 100. За замовчуванням — `30`. |
| `tag` | Необов’язковий тематичний рядок. |
| `category` | Необов’язковий ідентифікатор категорії. |

Заголовки відповіді:

- `Link` із `rel="next"` і, якщо є попередня сторінка, з `rel="prev"`.
- `Picsum-Total` — кількість фото, які відповідають умовам. Без `tag` і без `category` значення дорівнює `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Запит першої сторінки з `limit=1` повернув цей заголовок `Link` і `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

Тіло — масив об’єктів, описаних у розділі [Поля об’єкта](#fields). Кожен елемент — одне фото. Порядок може змінюватися; не вважайте перший рядок фіксованим фото.

<a id="info-id"></a>

### Одне фото за ID

```http
GET https://picsum.org/id/{id}/info
```

Відомий ID повертає `200` і один об’єкт JSON. Невідомий ID повертає `404` і саме таке тіло:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Одне фото за початковим значенням

```http
GET https://picsum.org/seed/{seed}/info
```

Відповідь — `200` і один об’єкт JSON, а також заголовок `Picsum-ID`. Початкове значення, яке не збігається з жодним тегом, не повертає помилку. Воно повертає ту саму сталу запасну фотографію, що й URL зображення з початковим значенням.

<a id="fields"></a>

### Поля об’єкта

| Поле | Значення |
| --- | --- |
| `id` | ID фото у вигляді рядка. |
| `author` | Ім’я автора. Рядок може бути порожнім. |
| `width` | Вихідна ширина в пікселях. Це не запитана ширина зображення. |
| `height` | Вихідна висота в пікселях. Це не запитана висота зображення. |
| `description` | Короткий опис фотографії. |
| `category` | Один ідентифікатор категорії. |
| `tags` | Масив тематичних рядків. |
| `url` | Сторінка першоджерела. |
| `license` | Точний рядок `"CC0 1.0"`. |
| `license_url` | Точний рядок `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | URL JPEG цього фото розміром 800×600. |

URL для WebP або відтінків сірого складіть зі `id`. `download_url` завжди вказує на JPEG 800×600.

<a id="examples"></a>

### Приклади

`GET https://picsum.org/id/179363399/info` повертає:

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

Фотографія має розмір 3840×2160, автор — Syony, категорія — `landscapes`, опис — «Colorful mountain slopes in Landmannalaugar». Теги: `mountains`, `highlands`, `colorful` та `iceland`.

`GET https://picsum.org/seed/studio/info` повертає:

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

Заголовок відповіді `Picsum-ID` дорівнює `1000561303`. Вихідний кадр — 2400×1800, поле `author` порожнє, а `category` — `food`.

<a id="categories"></a>

## Категорії

Передавайте в `category` один із цих ID. Публічної HTTP-кінцевої точки `/categories` немає. Інструмент MCP `list_categories` повертає ті самі ID: кожен має англійську назву для показу та групу. У запитах надсилайте ID, а не назву. Назви в цій таблиці перекладено для читачів; `list_categories` повертає англійські назви.

### Природа й краєвиди

| ID | Назва |
| --- | --- |
| `coasts` | Узбережжя й океани |
| `deserts` | Пустелі й дюни |
| `freshwater` | Озера й водоспади |
| `gardens` | Сади |
| `landscapes` | Краєвиди |
| `macro` | Макрофотографія |
| `mountains` | Гори |
| `plants` | Рослини та квіти |
| `skies` | Небо й погода |
| `snow` | Сніг і лід |
| `woodlands` | Ліси |

### Тварини

| ID | Назва |
| --- | --- |
| `animals` | Інші тварини |
| `birds` | Птахи |
| `insects` | Комахи |
| `marine` | Морське життя |
| `pets` | Домашні улюбленці |

### Місця та подорожі

| ID | Назва |
| --- | --- |
| `aerial` | Аерозйомка |
| `architecture` | Архітектура |
| `city` | Міста та вулиці |
| `interiors` | Інтер’єри |
| `landmarks` | Пам’ятки |
| `night` | Нічна зйомка |
| `transport` | Транспорт |

### Предмети й заняття

| ID | Назва |
| --- | --- |
| `agriculture` | Сільське господарство |
| `food` | Їжа та напої |
| `industry` | Промисловість |
| `music` | Музика |
| `objects` | Предмети |
| `sculpture` | Скульптура |
| `sports` | Спорт |
| `technology` | Технології |
| `textures` | Текстури |
| `workspaces` | Робочі простори |

<a id="headers"></a>

## Заголовки, кешування та CORS

Відповіді зі зображенням і JSON надсилають:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` містить `Picsum-ID`, `Picsum-Total` і `Link`, тож сторінка з іншого походження може прочитати ці три заголовки через `fetch`.

| Відповідь | `Cache-Control` |
| --- | --- |
| Випадкове перенаправлення, `/{width}` або `/{width}/{height}` | `no-store` |
| Перенаправлення з початковим значенням, `/seed/{seed}/...` | `public, max-age=3600` |
| Закріплене зображення, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Випадкове перенаправлення надсилається з `no-store`, тож наступний запит може вибрати інше фото. URL `/id/...` у `Location` — це файл, який можна кешувати. Перший запит нового розміру або ефекту може тривати трохи довше, перш ніж цей файл потрапить у кеш.

Описані нижче помилки JSON з кодами 400 і 404 також надсилаються з `Cache-Control: no-store` і `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Помилки та обмеження частоти запитів

Тіла помилок — це JSON. Рядки `error` мають збігатися точно.

Неприпустимі розміри зображення, непідтримуване розширення або значення розмиття поза діапазоном 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

Неприпустимі `page` або `limit` на `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Невідомий ID фото на `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 означає, що застосовано обмеження частоти запитів. Дотримуйтеся заголовка відповіді `Retry-After`. Не створюйте автоматизований трафік, який погіршує роботу сервісу, і не обходьте обмеження частоти запитів.

<a id="code"></a>

## Приклади коду

<a id="html"></a>

### HTML

Задайте `width`, `height` і `alt`. Значення `alt` має описувати фотографію. Опис нижче — це поле `description` фото `179363399`.

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

Перша команда виводить заголовки перенаправлення з початковим значенням, зокрема `Location` і `Picsum-ID`, і не зберігає зображення. Друга виводить один об’єкт фото. Третя виводить заголовки переліку та масив JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` може викликати кінцеві точки JSON з браузера, оскільки `Access-Control-Allow-Origin` дорівнює `*`. Заголовок `Picsum-Total` відкритий для читання, тож `headers.get` може його прочитати.

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

У цьому прикладі використано бібліотеку `requests`.

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

## Ліцензія й комерційне використання

Фотографії надаються на умовах [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Особисте й комерційне використання безплатні. Зазначати автора необов’язково. Якщо хочете зазначити автора фото, візьміть ім’я з поля `author`, а сторінку джерела — з `url`. Обидва поля є в об’єкті JSON.

Якщо використання чутливе, ви відповідаєте за впізнаваних людей, торговельні марки та запис першоджерела. Перед таким використанням перевірте `url`.

Не перепродавайте й не поширюйте цей сервіс як власний API зображень.

Запитання: [hello@picsum.org](mailto:hello@picsum.org).

Умови користування: [Умови користування](https://picsum.org/uk/terms).

<a id="mcp"></a>

## Сервер MCP

Розміщений сервер MCP призначено для клієнтів, які підтримують Model Context Protocol. Він відповідає на запити про фото лише для читання. Він не замінює наведені вище URL зображень і не створює зображення з текстового запиту. URL зображень залишаються на `https://picsum.org/{...}`. Кінцева точка MCP окрема.

| | |
| --- | --- |
| Кінцева точка | `https://picsum.org/mcp` |
| Транспорт | Streamable HTTP |
| Авторизація | OAuth 2.1 з PKCE |
| Область доступу | `photos:read` |
| Посібник з налаштування | [Підключіть ШІ-асистента до Picsum](https://picsum.org/uk/connect) |
| Конфігурація клієнта | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Інструменти лише для читання:

| Інструмент | Що робить |
| --- | --- |
| `search_photos` | Шукає за `tag`, за `category` або за обома параметрами. |
| `get_photo` | Метадані одного ID фото. |
| `list_categories` | Усі ID категорій з англійською назвою для показу та групою. |
| `build_image_url` | URL зображення та фрагмент HTML `<img>` із вибраними розміром, форматом, відтінками сірого й розмиттям. |

Вхід і налаштування клієнта описані в посібнику [Підключіть ШІ-асистента до Picsum](https://picsum.org/uk/connect). Сторінки іншими мовами використовують той самий шлях `/connect` під префіксом своєї локалі. Приклади конфігурації зібрано в [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
