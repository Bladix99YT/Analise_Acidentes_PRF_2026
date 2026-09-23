import pandas as pd
import json


def carregar_dados(dataset):
    df = pd.read_csv(
        dataset,
        parse_dates=["data_inversa"],
        dtype={
            "regional": "string",
            "delegacia": "string",
            "uop": "string"
        },
        low_memory=False
    )

    return df

def carregar_geojson(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)