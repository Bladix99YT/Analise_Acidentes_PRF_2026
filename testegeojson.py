import json
import pandas as pd


# -------------------------
# CAMINHOS
# -------------------------

caminho_geojson = (
    "data/GeoJson/br-geojson-main/dist/estados.geojson"
)

caminho_dataset = (
    "data/processed/acidentes2026_tratados.csv"
)


# -------------------------
# CARREGANDO O GEOJSON
# -------------------------

with open(caminho_geojson, "r", encoding="utf-8") as arquivo:
    geojson_brasil = json.load(arquivo)


# -------------------------
# CARREGANDO O DATASET
# -------------------------

df = pd.read_csv(
    caminho_dataset,
    low_memory=False
)


# -------------------------
# ACIDENTES POR UF
# -------------------------

acidentes_uf = (
    df.groupby("uf")["id"]
    .nunique()
    .reset_index(name="quantidade")
)

acidentes_uf["uf"] = acidentes_uf["uf"].str.upper()


# -------------------------
# TESTANDO CORRESPONDÊNCIA
# -------------------------

ufs_dados = set(acidentes_uf["uf"])

ufs_geojson = {
    estado["properties"]["sigla"]
    for estado in geojson_brasil["features"]
}

print("UFs no dataset:", len(ufs_dados))
print("UFs no GeoJSON:", len(ufs_geojson))

print("\nUFs sem correspondência:")
print(ufs_dados - ufs_geojson)

print("\nUFs extras no GeoJSON:")
print(ufs_geojson - ufs_dados)