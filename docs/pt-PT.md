[English](../README.md) · [العربية](./ar.md) · [Čeština](./cs.md) · [Deutsch](./de.md) · [Español](./es.md) · [Eesti](./et.md) · [हिन्दी](./hi.md) · [Bahasa Indonesia](./id.md) · [日本語](./ja.md) · [한국어](./ko.md) · [Lietuvių](./lt.md) · [Nederlands](./nl.md) · [Polski](./pl.md) · **Português (Portugal)** · [Ikinyarwanda](./rw.md) · [Svenska](./sv.md) · [Türkçe](./tr.md) · [Українська](./uk.md) · [اردو](./ur.md) · [Tiếng Việt](./vi.md) · [繁體中文](./zh-TW.md)

# Lorem Picsum API

[Lorem Picsum](https://picsum.org/pt-pt) é um gerador de imagens aleatórias gratuito: uma API de fotografias de substituição. Fornece **100 000 fotografias** CC0 ao abrigo de [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), em **33 categorias**. Os URL de imagem, os tamanhos personalizados, JPEG e WebP, a escala de cinzentos, a desfocagem e os pontos finais de metadados JSON não exigem conta nem chave de API.

O Lorem Picsum (`picsum.org`) é um serviço independente, inspirado no projeto de código aberto Picsum Photos. Não está associado a `picsum.photos`. Tem o seu próprio catálogo e os seus próprios identificadores de fotografia. Os caminhos desse outro projeto, incluindo um caminho de escala de cinzentos como `/g/{width}/{height}`, não fazem parte desta API.

O URL de base da API é `https://picsum.org`. Não anteponha um prefixo de idioma do site a um caminho da API. `https://picsum.org/de/800/600` é uma rota do site, não um URL de imagem. Os prefixos de idioma (`/de`, `/ja`, `/zh-tw` e os restantes) pertencem a páginas como a página inicial, o guia de configuração do MCP e os termos de utilização.

## Conteúdo

- [Visão geral](#overview)
- [Início rápido](#quick-start)
- [URL de imagens](#image-urls)
- [Metadados JSON](#json)
- [Categorias](#categories)
- [Cabeçalhos, cache e CORS](#headers)
- [Erros e limites de pedidos](#errors)
- [Exemplos de código](#code)
- [Licença e utilização comercial](#license)
- [Servidor MCP](#mcp)

<a id="overview"></a>

## Visão geral

Peça um URL de imagem quando a composição precisar de uma fotografia. Peça JSON quando precisar do autor, da descrição, da categoria, das etiquetas, das dimensões originais, da página de origem ou da licença.

Um URL aleatório pode selecionar uma fotografia diferente em cada pedido. Uma semente, ou um identificador de fotografia, mantém a mesma fotografia de origem. A largura e a altura são números inteiros de **1 a 2000** píxeis. Qualquer tamanho personalizado nesse intervalo é gratuito, tal como a escala de cinzentos e a desfocagem. Os seis tamanhos da página inicial são predefinições práticas, não um limite máximo.

<a id="quick-start"></a>

## Início rápido

Esta imagem aleatória de 800×600 redireciona para uma fotografia concreta. O redirecionamento não fica em cache, e a resposta traz o ID escolhido em `Picsum-ID`:

```html
<img
  src="https://picsum.org/800/600"
  width="800"
  height="600"
  alt=""
>
```

Use um URL fixo quando a fotografia tiver de permanecer:

```text
https://picsum.org/id/179363399/800/600.jpg
```

Use uma semente quando a fotografia tiver de ser repetível. A mesma semente corresponde à mesma fotografia de origem em qualquer tamanho. A semente `studio` corresponde a `1000561303`. Este exemplo pede WebP, escala de cinzentos e desfocagem:

```text
https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

<a id="image-urls"></a>

## URL de imagens

<a id="dimensions"></a>

### Dimensões e recorte

`width` e `height` são segmentos do caminho. Cada um é um número inteiro de 1 a 2000, inclusive. O serviço redimensiona a fotografia e recorta-a a partir do centro, para preencher o retângulo pedido. A fotografia não fica esticada.

<a id="formats"></a>

### Formatos

| Extensão | O que obtém |
| --- | --- |
| *(nenhuma)* | JPEG, `image/jpeg` |
| `.jpg` | JPEG, `image/jpeg` |
| `.webp` | WebP, `image/webp` |

`.png`, `.jpeg`, `.gif` e `.avif` não são aceites. A resposta é HTTP 400 e o objeto de erro de imagem indicado abaixo. `.jpeg` não é sinónimo de `.jpg`.

<a id="random-rectangle"></a>

### Retângulo aleatório

```http
GET https://picsum.org/{width}/{height}
GET https://picsum.org/{width}/{height}.jpg
GET https://picsum.org/{width}/{height}.webp
```

A resposta é `302 Found`. `Location` é `/id/{id}/{width}/{height}.{ext}`. Quando a extensão é omitida, `{ext}` é `jpg`.

- `Cache-Control: no-store`
- `Picsum-ID` é a fotografia que foi selecionada

`GET https://picsum.org/800/600` é a predefinição padrão desta forma.

<a id="random-square"></a>

### Quadrado aleatório

```http
GET https://picsum.org/{width}
```

`GET https://picsum.org/640` pede um JPEG de 640×640. A resposta é `302` para `/id/{id}/{width}/{width}.jpg`, com `Cache-Control: no-store` e um cabeçalho `Picsum-ID`.

<a id="seeded"></a>

### Fotografia com semente

```http
GET https://picsum.org/seed/{seed}/{width}/{height}
GET https://picsum.org/seed/{seed}/{width}/{height}.jpg
GET https://picsum.org/seed/{seed}/{width}/{height}.webp
GET https://picsum.org/seed/{seed}/{width}
GET https://picsum.org/seed/{seed}/{width}.webp
```

A resposta é `302` para `/id/{id}/{width}/{height}.{ext}`. Um URL de semente quadrado usa o mesmo número na largura e na altura. Uma extensão omitida corresponde a `jpg`.

- `Cache-Control: public, max-age=3600`
- `Picsum-ID` é a fotografia selecionada
- A mesma semente seleciona sempre a mesma fotografia de origem, mesmo que o tamanho mude. `studio` seleciona `1000561303`.
- A semente serve também de termo de pesquisa. `GET https://picsum.org/seed/cat/800/600` seleciona uma fotografia de gato.
- Se a semente não corresponder a nenhuma etiqueta, o serviço recorre a uma fotografia estável da coleção. A mesma semente desconhecida devolve sempre essa fotografia.

<a id="pinned"></a>

### Fotografia fixa

```http
GET https://picsum.org/id/{id}/{width}/{height}
GET https://picsum.org/id/{id}/{width}/{height}.jpg
GET https://picsum.org/id/{id}/{width}/{height}.webp
GET https://picsum.org/id/{id}/{width}
GET https://picsum.org/id/{id}/{width}.jpg
GET https://picsum.org/id/{id}/{width}.webp
```

A resposta é `200 OK` e o corpo binário da imagem, `image/jpeg` ou `image/webp`. Um caminho quadrado usa uma só dimensão para os dois lados. Uma extensão omitida corresponde a JPEG.

- `Cache-Control: public, max-age=86400, s-maxage=604800`
- `Picsum-ID` repete `{id}`

Para consultar o autor e a página de origem de um ID, chame [`/id/{id}/info`](#info-id). É essa rota de metadados, e não a rota da imagem, que documenta o `404` para um ID desconhecido.

<a id="query"></a>

### Parâmetros de consulta

| Parâmetro | Onde se aplica | Regra |
| --- | --- | --- |
| `tag` | Imagens aleatórias, imagens com semente e `GET /v2/list` | Texto do tema. Restringe o conjunto de fotografias. Exemplo: `?tag=forest`. |
| `category` | Imagens aleatórias, imagens com semente e `GET /v2/list` | Um dos 33 identificadores de categoria. Exemplo: `?category=woodlands`. |
| `grayscale` | URL de imagens | Forma de sinalizador `?grayscale`. A escala de cinzentos fica incorporada no ficheiro de imagem. Não existe o caminho `/g/{width}/{height}`. |
| `blur` | URL de imagens | Número inteiro de 1 a 10. Um `?blur` sem valor é aceite e significa `blur=5`. `blur=0` e `blur=11` devolvem HTTP 400. |

`tag` e `category` usam-se enquanto a fotografia está a ser escolhida. Não são copiados para o `Location` do redirecionamento.

A escala de cinzentos e a desfocagem acompanham a imagem. Este pedido com semente:

```text
GET https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4
```

responde `302` com:

```text
Location: /id/1000561303/800/600.webp?grayscale=1&blur=4
Cache-Control: public, max-age=3600
Picsum-ID: 1000561303
```

O sinalizador `grayscale` fica escrito como `grayscale=1` nesse URL fixo. `blur=4` mantém-se. O próprio ficheiro está em escala de cinzentos e desfocado; não se trata de um filtro CSS.

<a id="presets"></a>

### Tamanhos predefinidos da página inicial

Estes seis tamanhos são as predefinições mostradas na página inicial. Qualquer outro tamanho de 1 a 2000 também é gratuito.

| Predefinição | Píxeis | URL |
| --- | --- | --- |
| Padrão | 800×600 | `https://picsum.org/800/600` |
| Quadrado | 640×640 | `https://picsum.org/640` |
| Horizontal | 1200×800 | `https://picsum.org/1200/800` |
| Vertical | 600×800 | `https://picsum.org/600/800` |
| HD | 1280×720 | `https://picsum.org/1280/720` |
| Full HD | 1920×1080 | `https://picsum.org/1920/1080` |

O primeiro pedido de um tamanho novo, ou de uma combinação nova de escala de cinzentos ou de desfocagem, pode demorar um pouco mais. Em seguida, o ficheiro fixo fica em cache.

<a id="json"></a>

## Metadados JSON

Não existe o ponto final `/list` da v1. A coleção está listada em `/v2/list`.

`/v2/list` devolve uma lista JSON. `/id/{id}/info` e `/seed/{seed}/info` devolvem um objeto JSON. Os três enviam `Cache-Control: public, max-age=300` e `Access-Control-Allow-Origin: *`.

<a id="list"></a>

### Listar fotografias

```http
GET https://picsum.org/v2/list
GET https://picsum.org/v2/list?page=1&limit=30
GET https://picsum.org/v2/list?page=1&limit=30&tag=forest
GET https://picsum.org/v2/list?page=1&limit=30&category=woodlands
```

| Parâmetro | Regra |
| --- | --- |
| `page` | Número inteiro igual ou superior a 1. Predefinição: `1`. |
| `limit` | Número inteiro de 1 a 100. Predefinição: `30`. |
| `tag` | Texto do tema, opcional. |
| `category` | Identificador de categoria, opcional. |

Cabeçalhos da resposta:

- `Link` indica as ligações de paginação, com `rel="next"` e, quando existe uma página anterior, `rel="prev"`.
- `Picsum-Total`, o número de fotografias que correspondem. Sem `tag` nem `category`, o valor é `100000`.
- `Cache-Control: public, max-age=300`
- `Access-Control-Allow-Origin: *`

Um pedido à página 1 com `limit=1` devolveu este cabeçalho `Link` e `Picsum-Total: 100000`:

```http
Link: <https://picsum.org/v2/list?page=2&limit=1>; rel="next"
Picsum-Total: 100000
Cache-Control: public, max-age=300
Access-Control-Allow-Origin: *
```

O corpo é uma lista do objeto descrito em [Campos do objeto](#fields). Cada elemento é uma fotografia. A ordem pode mudar; não tome a primeira linha por uma fotografia fixa.

<a id="info-id"></a>

### Uma fotografia por ID

```http
GET https://picsum.org/id/{id}/info
```

Um ID conhecido devolve `200` e um objeto JSON. Um ID desconhecido devolve `404` e exatamente este corpo:

```json
{"error":"Unknown image ID."}
```

<a id="info-seed"></a>

### Uma fotografia por semente

```http
GET https://picsum.org/seed/{seed}/info
```

A resposta é `200` e um objeto JSON, além de um cabeçalho `Picsum-ID`. Uma semente que não corresponda a nenhuma etiqueta não devolve um erro. Devolve a mesma fotografia estável de reserva que o URL de imagem com semente.

<a id="fields"></a>

### Campos do objeto

| Campo | Significado |
| --- | --- |
| `id` | Identificador da fotografia, como cadeia de caracteres. |
| `author` | Nome do autor. A cadeia de caracteres pode estar vazia. |
| `width` | Largura original, em píxeis. Não é a largura pedida para a apresentação. |
| `height` | Altura original, em píxeis. Não é a altura pedida para a apresentação. |
| `description` | Descrição curta da fotografia. |
| `category` | Um identificador de categoria. |
| `tags` | Lista de termos do tema. |
| `url` | Página da fonte original. |
| `license` | A cadeia exata `"CC0 1.0"`. |
| `license_url` | A cadeia exata `"https://creativecommons.org/publicdomain/zero/1.0/"`. |
| `download_url` | URL JPEG para descarregar esta fotografia em 800×600. |

Para obter WebP ou escala de cinzentos, construa o URL a partir de `id`. `download_url` é sempre o JPEG de 800×600.

<a id="examples"></a>

### Exemplos

`GET https://picsum.org/id/179363399/info` devolve:

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

A fotografia tem 3840×2160, é de Syony, está na categoria `landscapes` e a descrição é «Colorful mountain slopes in Landmannalaugar». As etiquetas são `mountains`, `highlands`, `colorful` e `iceland`.

`GET https://picsum.org/seed/studio/info` devolve:

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

O cabeçalho de resposta `Picsum-ID` é `1000561303`. As dimensões originais são 2400×1800, `author` está vazio e `category` é `food`.

<a id="categories"></a>

## Categorias

Passe um destes identificadores em `category`. Não existe um ponto final HTTP público `/categories`. Os nomes destas tabelas são traduções para quem lê. A ferramenta MCP `list_categories` devolve os mesmos identificadores, cada um com o nome de apresentação em inglês e o grupo. No pedido tem de ir o identificador, não o nome de apresentação.

### Natureza e paisagens

| ID | Nome |
| --- | --- |
| `coasts` | Costas e oceanos |
| `deserts` | Desertos e dunas |
| `freshwater` | Lagos e cascatas |
| `gardens` | Jardins |
| `landscapes` | Paisagens |
| `macro` | Macro |
| `mountains` | Montanhas |
| `plants` | Plantas e flores |
| `skies` | Céus e meteorologia |
| `snow` | Neve e gelo |
| `woodlands` | Bosques |

### Animais

| ID | Nome |
| --- | --- |
| `animals` | Outros animais |
| `birds` | Aves |
| `insects` | Insetos |
| `marine` | Vida marinha |
| `pets` | Animais de estimação |

### Lugares e viagens

| ID | Nome |
| --- | --- |
| `aerial` | Vista aérea |
| `architecture` | Arquitetura |
| `city` | Cidades e ruas |
| `interiors` | Interiores |
| `landmarks` | Pontos de referência |
| `night` | Noite |
| `transport` | Transportes |

### Objetos e atividades

| ID | Nome |
| --- | --- |
| `agriculture` | Agricultura |
| `food` | Comida e bebida |
| `industry` | Indústria |
| `music` | Música |
| `objects` | Objetos |
| `sculpture` | Escultura |
| `sports` | Desporto |
| `technology` | Tecnologia |
| `textures` | Texturas |
| `workspaces` | Espaços de trabalho |

<a id="headers"></a>

## Cabeçalhos, cache e CORS

As respostas de imagem e de JSON enviam:

- `Access-Control-Allow-Origin: *`
- `Cross-Origin-Resource-Policy: cross-origin`

`Access-Control-Expose-Headers` inclui `Picsum-ID`, `Picsum-Total` e `Link`, para uma página noutra origem poder ler esses três cabeçalhos a partir de `fetch`.

| Resposta | `Cache-Control` |
| --- | --- |
| Redirecionamento aleatório, `/{width}` ou `/{width}/{height}` | `no-store` |
| Redirecionamento com semente, `/seed/{seed}/...` | `public, max-age=3600` |
| Imagem fixa, `/id/{id}/{width}/...` | `public, max-age=86400, s-maxage=604800` |
| `/v2/list`, `/id/{id}/info`, `/seed/{seed}/info` | `public, max-age=300` |

Um redirecionamento aleatório é `no-store`, por isso o pedido seguinte pode selecionar outra fotografia. O URL `/id/...` em `Location` é o ficheiro que pode ficar em cache. O primeiro pedido de um tamanho ou efeito novo pode demorar um pouco mais, antes de esse ficheiro ficar em cache.

Os erros JSON 400 e 404 documentados abaixo são também enviados com `Cache-Control: no-store` e `Access-Control-Allow-Origin: *`.

<a id="errors"></a>

## Erros e limites de pedidos

Os corpos de erro são JSON. As cadeias de `error` têm de coincidir exatamente.

Dimensões de imagem inválidas, extensão não suportada ou valor de desfocagem fora do intervalo de 1 a 10 (HTTP 400):

```json
{"error":"Use dimensions from 1 to 2000, JPG or WebP, grayscale, and blur from 1 to 10."}
```

`page` ou `limit` inválidos em `/v2/list` (HTTP 400):

```json
{"error":"Invalid page or limit."}
```

Identificador de fotografia desconhecido em `/id/{id}/info` (HTTP 404):

```json
{"error":"Unknown image ID."}
```

HTTP 429 significa que o limite de pedidos foi aplicado. Respeite o cabeçalho de resposta `Retry-After`. Não envie tráfego automatizado que prejudique o serviço e não contorne os limites de pedidos.

<a id="code"></a>

## Exemplos de código

<a id="html"></a>

### HTML

Defina `width`, `height` e `alt`. O `alt` deve descrever a fotografia. A descrição abaixo é o campo `description` da fotografia `179363399`.

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

O primeiro comando imprime os cabeçalhos do redirecionamento com semente, incluindo `Location` e `Picsum-ID`, e não guarda a imagem. O segundo imprime um objeto de fotografia. O terceiro imprime os cabeçalhos da listagem e uma lista JSON.

```bash
curl -sD - -o /dev/null "https://picsum.org/seed/studio/800/600.webp?grayscale&blur=4"
curl -s "https://picsum.org/id/179363399/info"
curl -sD - "https://picsum.org/v2/list?page=1&limit=10&category=landscapes"
```

<a id="javascript"></a>

### JavaScript

`fetch` pode chamar os pontos finais JSON a partir de um navegador, porque `Access-Control-Allow-Origin` é `*`. `Picsum-Total` está exposto, por isso `headers.get` consegue lê-lo.

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

Este exemplo usa a biblioteca `requests`.

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

## Licença e utilização comercial

As fotografias estão ao abrigo de [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). A utilização pessoal e a comercial são gratuitas. A menção de autoria é facultativa. Para creditar uma fotografia, `author` é o autor e `url` é a página de origem, ambos no objeto JSON.

Quando a utilização for sensível, cabe-lhe ter em conta as pessoas reconhecíveis, as marcas e o registo da fonte original. Consulte `url` antes desse tipo de utilização.

Não revenda nem redistribua este serviço como se fosse a sua própria API de imagens.

Dúvidas: [hello@picsum.org](mailto:hello@picsum.org).

Termos de utilização: [Termos de utilização](https://picsum.org/pt-pt/terms).

<a id="mcp"></a>

## Servidor MCP

Um servidor MCP alojado responde a consultas só de leitura sobre fotografias, para clientes que usam o Model Context Protocol. Não substitui os URL de imagem acima nem gera fotografias a partir de uma descrição em texto. Os URL de imagem mantêm-se em `https://picsum.org/{...}`. O ponto final MCP é separado.

| | |
| --- | --- |
| Ponto final | `https://picsum.org/mcp` |
| Transporte | Streamable HTTP |
| Autorização | OAuth 2.1 com PKCE |
| Âmbito | `photos:read` |
| Guia de configuração | [Ligue o seu assistente de IA ao Picsum](https://picsum.org/pt-pt/connect) |
| Configuração do cliente | [picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp) |

As ferramentas são só de leitura:

| Ferramenta | O que faz |
| --- | --- |
| `search_photos` | Pesquisa por `tag`, por `category` ou por ambos. |
| `get_photo` | Metadados de um identificador de fotografia. |
| `list_categories` | Todos os identificadores de categoria, com o nome de apresentação em inglês e o grupo. |
| `build_image_url` | Um URL de imagem e um fragmento HTML `<img>`, para o tamanho, o formato, a escala de cinzentos e a desfocagem escolhidos. |

O início de sessão e a configuração do cliente estão descritos em [Ligue o seu assistente de IA ao Picsum](https://picsum.org/pt-pt/connect). Nas outras línguas usa-se o mesmo caminho `/connect`, sob o prefixo de idioma correspondente. Os pedidos de imagem da API não levam esse prefixo. Os exemplos de configuração estão em [https://github.com/picsumorg/picsum-mcp](https://github.com/picsumorg/picsum-mcp).
