# br-geojson

GeoJSON pré-compilados dos estados e municípios brasileiros, enriquecidos com metadados do IBGE e prontos para uso via CDN.

## Diferencial

Diferente de outros datasets similares, cada feature já vem com as propriedades enriquecidas (`nome`, `sigla`, `cd_geocmu`, `hc-key`) prontas para uso — sem necessidade de joins em runtime.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `dist/estados.geojson` | Polígonos dos 27 estados + DF com metadados |
| `dist/municipios/{UF}.geojson` | Polígonos dos municípios por estado |
| `dist/municipios/all.geojson` | Todos os municípios em um único FeatureCollection |
| `dist/municipios-index.json` | Lookup `{ "cd_geocmu": índice }` para join em O(1) |

### Propriedades das features

**Estados:**
| Propriedade | Exemplo |
|---|---|
| `nome` | `"São Paulo"` |
| `sigla` | `"SP"` |
| `cd_geocuf` | `"35"` |
| `hc-key` | `"br-sp"` |

**Municípios:**
| Propriedade | Exemplo |
|---|---|
| `nome` | `"Campinas"` |
| `uf` | `"SP"` |
| `cd_geocmu` | `"3509502"` |
| `hc-key` | `"br-sp-3509502"` |

## CDN (jsDelivr)

```
https://cdn.jsdelivr.net/gh/henriquemalvar/br-geojson@main/dist/estados.geojson
https://cdn.jsdelivr.net/gh/henriquemalvar/br-geojson@main/dist/municipios/{UF}.geojson
https://cdn.jsdelivr.net/gh/henriquemalvar/br-geojson@main/dist/municipios/all.geojson
https://cdn.jsdelivr.net/gh/henriquemalvar/br-geojson@main/dist/municipios-index.json
```

## Regenerar os dados

Requer Python 3.8+, sem dependências externas.

```bash
python3 build_ibge_geojson.py
# Para forçar reprocessamento:
python3 build_ibge_geojson.py --force
```

## Fonte dos dados

[IBGE — Malhas Territoriais](https://servicodados.ibge.gov.br/api/docs/malhas) e [IBGE — Localidades](https://servicodados.ibge.gov.br/api/docs/localidades)

## Licença

Creative Commons [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) — Domínio Público. Faça o que quiser.

Os dados são de fonte pública do IBGE, sem restrições de uso.

## Projetos relacionados

- [tbrugz/geodata-br](https://github.com/tbrugz/geodata-br)
- [datasets/geo-countries](https://github.com/datasets/geo-countries)
- [johan/world.geo.json](https://github.com/johan/world.geo.json)
