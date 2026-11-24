[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · **Español** · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · [Português (Portugal)](./pt-PT.md) · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/es) es un generador de imágenes aleatorias gratuito. Sirve **100.000 fotos CC0** bajo la licencia [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) en **33 categorías**. Los enlaces de imagen, los tamaños personalizados, JPEG y WebP, la escala de grises, el desenfoque y los puntos de conexión de metadatos JSON no necesitan cuenta ni clave de API.

Lorem Picsum (`picsum.org`) es un servicio independiente inspirado en el proyecto de código abierto Picsum Photos. No está vinculado a `picsum.photos`. Tiene su propio catálogo y sus propios ID de foto. Las rutas de aquel otro proyecto, incluida una ruta de escala de grises como `/g/{width}/{height}`, no forman parte de esta API.

La URL base de la API es `https://picsum.org`. No antepongas un prefijo de idioma del sitio a una ruta de la API. `https://picsum.org/de/800/600` es una ruta del sitio web, no un enlace de imagen. Los prefijos de idioma (`/de`, `/ja`, `/zh-tw` y el resto) pertenecen a páginas como la de inicio, la guía de configuración de MCP y las condiciones de uso.

## Contenido

- [Descripción general](#overview)
- [Inicio rápido](#quick-start)
- [URL de imagen](#image-urls)
- [Metadatos JSON](#json)
- [Categorías](#categories)
- [Cabeceras, caché y CORS](#headers)
- [Errores y límites de solicitudes](#errors)
- [Ejemplos de código](#code)
- [Licencia y uso comercial](#license)
- [Servidor MCP](#mcp)

<a id="overview"></a>

## Descripción general

Pide un enlace de imagen cuando el diseño necesite una foto. Pide JSON cuando necesites el autor, la descripción, la categoría, las etiquetas, las dimensiones originales, la página de origen o la licencia.

Un enlace aleatorio puede elegir una foto distinta en cada petición. Una semilla, o un ID de foto, mantiene la misma fotografía de origen. El ancho y el alto son enteros de **1 a 2000** píxeles. Cualquier tamaño personalizado de ese intervalo es gratis, igual que la escala de grises y el desenfoque. Los seis tamaños de la página de inicio son predefinidos por comodidad y no marcan un máximo.

<a id="quick-start"></a>

## Inicio rápido

Esta imagen aleatoria de 800×600 redirige a una foto concreta. Las cachés no almacenan la redirección, y la respuesta lleva el ID elegido en `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Usa una URL fijada cuando la imagen no deba cambiar:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Usa una semilla cuando la imagen deba poder repetirse. La misma semilla corresponde a la misma foto de origen en todos los tamaños. La semilla `studio` corresponde a `1000561303`. Este ejemplo pide WebP, escala de grises y desenfoque:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## URL de imagen

<a id="dimensions"></a>

### Dimensiones y recorte

`width` y `height` son segmentos de la ruta. Cada uno es un entero de 1 a 2000, ambos inclusive. El servicio escala la fotografía y la recorta desde el centro para llenar el rectángulo pedido. La imagen no se estira.

<a id="formats"></a>

### Formatos

| Extensión | Qué obtienes |
| --- | --- |
| *(ninguna)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` y `.avif` no se aceptan. La respuesta es HTTP 400 y el objeto de error de imagen que aparece más abajo. `.jpeg` no es un alias de `.jpg`.

<a id="random-rectangle"></a>

### Rectángulo aleatorio

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

La respuesta es `302 Found`. `Location` es `/id/{id}/{width}/{height}.{ext}`. Si omites la extensión, `{ext}` es `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` es la foto seleccionada

`GET https://picsum.org/800/600` es el predefinido estándar de esta forma.

<a id="random-square"></a>

### Cuadrado aleatorio

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` pide un JPEG de 640×640. La respuesta es `302` a `/id/{id}/{width}/{width}.jpg`, con `Cache-Control: no-store` y una cabecera `Picsum-ID`.

<a id="seeded"></a>

### Foto con semilla

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

La respuesta es `302` a `/id/{id}/{width}/{height}.{ext}`. Una URL de semilla cuadrada usa el mismo número para el ancho y el alto. Si omites la extensión, es `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` es la foto seleccionada
- Una semilla elige siempre la misma foto de origen, también cuando cambia el tamaño. `studio` elige `1000561303`.
- La semilla también se usa como término de búsqueda. `GET https://picsum.org/seed/cat/800/600` elige una fotografía de un gato.
- Si la semilla no coincide con ninguna etiqueta, el servicio recurre a una fotografía estable de la colección. La misma semilla desconocida sigue devolviendo esa misma fotografía.

<a id="pinned"></a>

### Foto fijada

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

La respuesta es `200 OK` y los bytes de la imagen, `image/jpeg` o `image/webp`. Una ruta cuadrada usa una sola dimensión para los dos lados. Si omites la extensión, el formato es JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` repite `{id}`

Para leer el autor y la página de origen de un ID, consulta [`/id/{id}/info`](#info-id). Esa ruta de metadatos, y no la ruta de la imagen, es el `404` documentado para un ID desconocido.

<a id="query"></a>

### Parámetros de consulta

| Parámetro | Dónde se aplica | Regla |
| --- | --- | --- |
| `tag` | Imágenes aleatorias, imágenes con semilla y `GET /v2/list` | Texto de tema. Acota el conjunto. Ejemplo: `?tag=forest`. |
| `category` | Imágenes aleatorias, imágenes con semilla y `GET /v2/list` | Uno de los 33 ID de categoría. Ejemplo: `?category=woodlands`. |
| `grayscale` | URL de imagen | Indicador `?grayscale`. La escala de grises queda integrada en el archivo de imagen. No existe la ruta `/g/{width}/{height}`. |
| `blur` | URL de imagen | Entero de 1 a 10. Un `?blur` sin valor se acepta y significa `blur=5`. `blur=0` y `blur=11` devuelven HTTP 400. |

`tag` y `category` se usan al elegir la foto. No se copian en el `Location` de la redirección.

La escala de grises y el desenfoque se conservan en el enlace. Esta petición con semilla:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

responde `302` con:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

El indicador `grayscale` se escribe como `grayscale=1` en esa URL fijada. `blur=4` se mantiene. El archivo en sí está en escala de grises y desenfocado; no es un filtro CSS.

<a id="presets"></a>

### Tamaños predefinidos de la página de inicio

Estos seis tamaños son los predefinidos que muestra la página de inicio. Cualquier otro tamaño de 1 a 2000 también es gratis.

| Predefinido | Píxeles | URL |
| --- | --- | --- |
| Estándar | 800×600 | `https://picsum.org/800/600` |
| Cuadrado | 640×640 | `https://picsum.org/640` |
| Horizontal | 1200×800 | `https://picsum.org/1200/800` |
| Vertical | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

La primera petición de un tamaño nuevo, o de una combinación nueva de escala de grises o desenfoque, puede tardar un poco más. Después, el archivo fijado queda en caché.

<a id="json"></a>

## Metadatos JSON

No existe un punto de conexión `/list` de la v1. La colección se lista en `/v2/list`.

`/v2/list` devuelve una lista JSON. `/id/{id}/info` y `/seed/{seed}/info` devuelven un objeto JSON. Los tres envían `Cache-Control: public, max-age=300` y `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Listar fotos

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Parámetro | Regla |
| --- | --- |
| `page` | Entero mayor o igual que 1. Valor predeterminado `1`. |
| `limit` | Entero de 1 a 100. Valor predeterminado `30`. |
| `tag` | Texto de tema opcional. |
| `category` | ID de categoría opcional. |

Cabeceras de la respuesta:

- `Link`, con `rel="next"` y, si existe una página anterior, `rel="prev"`.
- `Picsum-Total`, el número de fotos que coinciden. Sin `tag` ni `category`, el valor es `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Una petición de la página 1 con `limit=1` devolvió esta cabecera `Link` y `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

El cuerpo es una lista de objetos como el descrito en [Campos del objeto](#fields). Cada elemento es una foto. El orden puede cambiar; no trates la primera fila como una foto fija.

<a id="info-id"></a>

### Una foto por ID

```http
GET https://picsum.org/id/{id}/info
```

Un ID conocido devuelve `200` y un objeto JSON. Un ID desconocido devuelve `404` y este cuerpo exacto:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Una foto por semilla

```http
GET https://picsum.org/seed/{seed}/info
```

La respuesta es `200` y un objeto JSON, más una cabecera `Picsum-ID`. Una semilla que no coincide con ninguna etiqueta no devuelve un error. Devuelve la misma foto estable de reserva que la URL de imagen con semilla.

<a id="fields"></a>

### Campos del objeto

| Campo | Significado |
| --- | --- |
| `id` | ID de la foto, como cadena. |
| `author` | Nombre de quien la creó. La cadena puede estar vacía. |
| `width` | Ancho original en píxeles. No es el ancho que pediste para la imagen. |
| `height` | Alto original en píxeles. No es el alto que pediste para la imagen. |
| `description` | Descripción breve de la fotografía. |
| `category` | Un ID de categoría. |
| `tags` | Lista de textos de tema. |
| `url` | Página de la fuente original. |
| `license` | La cadena exacta `"CC0 1.0"`. |
| `license_url` | La cadena exacta `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | URL JPEG de esta foto a 800×600. |

Crea una URL en WebP o en escala de grises a partir de `id`. `download_url` es siempre el JPEG de 800×600.

<a id="examples"></a>

### Ejemplos

`GET https://picsum.org/id/179363399/info` devuelve:

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

La fotografía mide 3840×2160, es de Syony, está en `landscapes` y se describe como «Colorful mountain slopes in Landmannalaugar». Las etiquetas son `mountains`, `highlands`, `colorful` y `iceland`.

`GET https://picsum.org/seed/studio/info` devuelve:

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

La cabecera de respuesta `Picsum-ID` es `1000561303`. El encuadre original es 2400×1800, `author` está vacío y `category` es `food`.

<a id="categories"></a>

## Categorías

Usa uno de estos ID en `category`. No hay un punto de conexión HTTP público `/categories`. Los nombres de esta tabla son traducciones para quien lee. La herramienta MCP `list_categories` devuelve los mismos ID, cada uno con el nombre en inglés y un grupo. Envía el ID, no el nombre.

### Naturaleza y paisajes

| ID | Nombre |
| --- | --- |
| `coasts` | Costas y océanos |
| `deserts` | Desiertos y dunas |
| `freshwater` | Lagos y cascadas |
| `gardens` | Jardines |
| `landscapes` | Paisajes |
| `macro` | Macro |
| `mountains` | Montañas |
| `plants` | Plantas y flores |
| `skies` | Cielos y meteorología |
| `snow` | Nieve y hielo |
| `woodlands` | Bosques |

### Animales

| ID | Nombre |
| --- | --- |
| `animals` | Otros animales |
| `birds` | Aves |
| `insects` | Insectos |
| `marine` | Vida marina |
| `pets` | Mascotas |

### Lugares y viajes

| ID | Nombre |
| --- | --- |
| `aerial` | Vista aérea |
| `architecture` | Arquitectura |
| `city` | Ciudades y calles |
| `interiors` | Interiores |
| `landmarks` | Lugares emblemáticos |
| `night` | Noche |
| `transport` | Transporte |

### Objetos y actividades

| ID | Nombre |
| --- | --- |
| `agriculture` | Agricultura |
| `food` | Comida y bebida |
| `industry` | Industria |
| `music` | Música |
| `objects` | Objetos |
| `sculpture` | Escultura |
| `sports` | Deportes |
| `technology` | Tecnología |
| `textures` | Texturas |
| `workspaces` | Espacios de trabajo |

<a id="headers"></a>

## Cabeceras, caché y CORS

Las respuestas de imagen y de JSON envían:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` incluye `Picsum-ID`, `Picsum-Total` y `Link`, así que una página de otro origen puede leer esas tres cabeceras desde `fetch`.

| Respuesta | `Cache-Control` |
| --- | --- |
| Redirección aleatoria, `/{width}` o `/{width}/{height}` | `no-store` |
| Redirección con semilla, `/seed/{seed}/...` | `public, max-age=3600` |
| Imagen fijada, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Una redirección aleatoria es `no-store`, así que la siguiente petición puede elegir otra foto. La URL `/id/...` de `Location` es el archivo que se puede guardar en caché. La primera petición de un tamaño o un efecto nuevo puede tardar un poco más, antes de que ese archivo quede en caché.

Los errores JSON 400 y 404 documentados más abajo también se envían con `Cache-Control: no-store` y `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Errores y límites de solicitudes

Los cuerpos de error son JSON. Haz coincidir estas cadenas `error` de forma exacta.

Dimensiones de imagen no válidas, una extensión no admitida o un valor de desenfoque fuera de 1–10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`page` o `limit` no válidos en `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

ID de foto desconocido en `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 significa que se aplicó el límite de solicitudes. Respeta la cabecera de respuesta `Retry-After`. No generes tráfico automatizado que degrade el servicio ni eludas los límites de solicitudes.

<a id="code"></a>

## Ejemplos de código

<a id="html"></a>

### HTML

Indica `width`, `height` y `alt`. `alt` debe describir la fotografía. La descripción de abajo es el `description` de la foto `179363399`.

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

El primer comando muestra las cabeceras de la redirección con semilla, incluidas `Location` y `Picsum-ID`, y no guarda la imagen. El segundo muestra un objeto de foto. El tercero muestra las cabeceras del listado y una lista JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` puede llamar a los puntos de conexión JSON desde un navegador porque `Access-Control-Allow-Origin` es `*`. `Picsum-Total` está expuesto, así que `headers.get` puede leerlo.

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

Este ejemplo usa la biblioteca `requests`.

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

## Licencia y uso comercial

Las fotografías son [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). El uso personal y el uso comercial son gratis. Mencionar al autor es opcional. Si quieres acreditar una foto, `author` es quien la creó y `url` es la página de origen, ambos en el objeto JSON.

Si el uso es delicado, respondes de las personas reconocibles, de las marcas y del registro de la fuente original. Revisa `url` antes de ese tipo de uso.

No revendas ni redistribuyas este servicio como si fuera tu propia API de imágenes.

Preguntas: [hello@picsum.org](mailto:hello@picsum.org).

Condiciones de uso: [Condiciones de uso](https://picsum.org/es/terms).

<a id="mcp"></a>

## Servidor MCP

Un servidor MCP alojado responde a consultas de fotos de solo lectura de los clientes que usan MCP. No sustituye los enlaces de imagen de arriba ni genera imágenes a partir de un texto. Los enlaces de imagen siguen en `https://picsum.org/{...}`. El punto de conexión MCP es independiente.

| | |
| --- | --- |
| Punto de conexión | `https://picsum.org/mcp` |
| Transporte | Streamable HTTP |
| Autorización | OAuth 2.1 con PKCE |
| Alcance | `photos:read` |
| Guía de configuración | [Conecta tu asistente de IA a Picsum](https://picsum.org/es/connect) |
| Configuración del cliente | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

Las herramientas son de solo lectura:

| Herramienta | Qué hace |
| --- | --- |
| `search_photos` | Busca por `tag`, por `category` o por ambos. |
| `get_photo` | Metadatos de un ID de foto. |
| `list_categories` | Cada ID de categoría, con su nombre visible en inglés y su grupo. |
| `build_image_url` | Un enlace de imagen y un fragmento HTML `<img>`, para el tamaño, el formato, la escala de grises y el desenfoque que elijas. |

El inicio de sesión y la configuración del cliente están documentados en [Conecta tu asistente de IA a Picsum](https://picsum.org/es/connect). En los demás idiomas se usa la misma ruta `/connect` bajo el prefijo de idioma. Los ejemplos de configuración están en [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
