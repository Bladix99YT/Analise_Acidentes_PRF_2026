import pandas as pd
from utils.utils import carregar_dados


# -------------------------
# FAZENDO A LEITURA INCIAL E CARREGANDO OS DADOS TRATADOS
# -------------------------

dataset = "data/processed/acidentes2026_tratados.csv"

df = carregar_dados(dataset)

#print(df.info())



# -------------------------
# ANALISE DE CAUSA/TIPO E HORA/HORÁRIO
# -------------------------


# Criando a variavel contagem para contar acidentes unicos com causa e tipo
contagem = (
    df.groupby(["causa_acidente", "tipo_acidente"])["id"]
    .nunique()
    .reset_index(name="quantidade")
)


# Analise de acidente por hora padrão ex: 11:00
acidentes_hora = (
    df.groupby("hora")["id"]
    .nunique()
    .reset_index(name="quantidade")
)

print(acidentes_hora)


# Analise de acidente por horario exato ex: "11:32"
# Criei essas duas ramificações pois pode ser que tenha varios acidentes nesse mesmo horario
# Como o mesmo acidente pode aparecer em várias linhas no dataset,
# contamos apenas IDs únicos para evitar duplicar acidentes na análise.
acidentes_horario = (
    df.groupby("horario")["id"]
    .nunique()
    .reset_index(name="quantidade")
)

# -------------------------
# CLASSIFICAÇÃO DOS ACIDENTES
# -------------------------

classificacao = (
    df.groupby("classificacao_acidente")["id"]
    .nunique()
    .reset_index(name="quantidade")
)

print(classificacao)

print("\nTotal de acidentes:", df["id"].nunique())
print("Soma das classificações:", classificacao["quantidade"].sum())

# -------------------------
# MAIORES ACIDENTES UNICOS POR HORA/HORARIO
# -------------------------


maior_hora = acidentes_hora.loc[acidentes_hora["quantidade"].idxmax()]


maior_horario = acidentes_horario.loc[
    acidentes_horario["quantidade"].idxmax()
]


# -------------------------
# IDENTIFICANDO ACIDENTES SEM CLASSIFICAÇÃO
# -------------------------

ids_totais = set(df["id"].dropna().unique())

ids_classificados = set(
    df.loc[
        df["classificacao_acidente"].notna(),
        "id"
    ].unique()
)

ids_sem_classificacao = ids_totais - ids_classificados



print("Acidentes sem classificação:", ids_sem_classificacao)
print("Quantidade:", len(ids_sem_classificacao))

print(maior_hora)
#print(maior_horario)

