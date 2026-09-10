import pandas as pd

dataset = r"data/raw/acidentes2026_todas_causas_tipos.csv"

df = pd.read_csv(
    dataset,
    sep=";",
    encoding="latin1"
)

# -------------------------
# DUPLICADOS
# -------------------------

print("Duplicados:", df.duplicated().sum())

df = df.drop_duplicates()


# -------------------------
# DATA
# -------------------------

df["data_inversa"] = pd.to_datetime(
    df["data_inversa"],
    dayfirst=True,
    errors="coerce"
)

df["ano"] = df["data_inversa"].dt.year
df["mes"] = df["data_inversa"].dt.month
df["dia"] = df["data_inversa"].dt.day


# -------------------------
# HORÁRIO
# -------------------------

horario_convertido = pd.to_datetime(
    df["horario"],
    format="%H:%M:%S",
    errors="coerce"
)

df["hora"] = horario_convertido.dt.hour


# -------------------------
# FIM DE SEMANA
# -------------------------

df["fim_semana"] = df["dia_semana"].isin(
    ["sábado", "domingo"]
).astype(int)


# -------------------------
# IDADE
# -------------------------

# A PRF pode usar valores inválidos como -1
df.loc[df["idade"] < 0, "idade"] = pd.NA


# -------------------------
# COLUNAS NUMÉRICAS
# -------------------------

colunas_numericas = [
    "br",
    "km",
    "idade",
    "latitude",
    "longitude",
    "ano_fabricacao_veiculo"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )


# -------------------------
# SALVANDO
# -------------------------

df.to_csv(
     "data/processed/acidentes2026_tratados.csv",
     index=False,
     encoding="utf-8"
)