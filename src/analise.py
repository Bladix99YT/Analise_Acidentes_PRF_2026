import pandas as pd
from utils.utils import carregar_dados


# -------------------------
# FAZENDO A LEITURA INCIAL E CARREGANDO OS DADOS TRATADOS
# -------------------------

dataset = "data/processed/acidentes2026_tratados.csv"

df = carregar_dados(dataset)

print(df["dia_semana"].nunique())