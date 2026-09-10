import pandas as pd


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