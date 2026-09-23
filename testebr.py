import json


# -------------------------
# CARREGANDO O GEOJSON DAS RODOVIAS
# -------------------------

caminho = "data/GeoJson/rodovias_federais_brasil.json"

with open(caminho, "r", encoding="utf-8") as arquivo:
    geojson_brs = json.load(arquivo)


# -------------------------
# TESTANDO ESTRUTURA
# -------------------------

print("Tipo do arquivo:")
print(geojson_brs["type"])

print("\nQuantidade de trechos:")
print(len(geojson_brs["features"]))


# -------------------------
# PRIMEIRO TRECHO
# -------------------------

primeiro_trecho = geojson_brs["features"][0]

print("\nTipo da geometria:")
print(primeiro_trecho["geometry"]["type"])

print("\nPropriedades:")
print(primeiro_trecho["properties"])


# -------------------------
# BR DO PRIMEIRO TRECHO
# -------------------------

print("\nBR:")
print(primeiro_trecho["properties"]["vl_br"])

print("\nUF:")
print(primeiro_trecho["properties"]["sg_uf"])


# -------------------------
# QUANTIDADE DE BRs DIFERENTES
# -------------------------

brs = {
    trecho["properties"]["vl_br"]
    for trecho in geojson_brs["features"]
}

print("\nQuantidade de BRs diferentes:")
print(len(brs))


# -------------------------
# TESTANDO AS PRINCIPAIS BRs
# -------------------------

principais_brs = {
    "101",
    "116",
    "381",
    "040",
    "153",
    "364",
    "163",
    "277",
    "376",
    "262"
}

print("\nPrincipais BRs que não foram encontradas:")
print(principais_brs - brs)