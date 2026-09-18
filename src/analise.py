import pandas as pd
import plotly.express as px
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

#print(acidentes_hora)


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
# Causas Principais de acidentes
# -------------------------

causas_principais = (
    df[df["causa_principal"] == "Sim"]
    .groupby("causa_acidente")["id"]
    .nunique()
    .reset_index(name="quantidade")
    .sort_values("quantidade", ascending=False)
    .reset_index(drop=True)
)

print("\nTotal de acidentes:", df["id"].nunique())
print(causas_principais)


# -------------------------
# Graficos de Classificação de acidentes 
# -------------------------

df_principal = df[df["causa_principal"] == "Sim"]

top_causas = (
    df_principal.groupby("causa_acidente")["id"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .index
)

comparacao = (
    df_principal[
        df_principal["causa_acidente"].isin(top_causas)
    ]
    .groupby(
        ["causa_acidente", "classificacao_acidente"]
    )["id"]
    .nunique()
    .reset_index(name="quantidade")
)

fig = px.bar(
    comparacao,
    x="causa_acidente",
    y="quantidade",
    color="classificacao_acidente",
    barmode="group",
    title="Principais Causas x Classificação dos Acidentes",
    labels={
        "causa_acidente": "Causa principal",
        "classificacao_acidente": "Classificação",
        "quantidade": "Quantidade de acidentes"
    }
)

fig.update_layout(
    title_x=0.5,
    xaxis_tickangle=-45
)

fig.show()

# Seguindo nas 10 maiores causas principais
# Podemos ver que as maiores causas principais são de reação tardia 
# ou algo relacionado a atenção do condutor
# Também essas que estão com maiores causas de acidentes fatais

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



#print("Acidentes sem classificação:", ids_sem_classificacao)
#print("Quantidade:", len(ids_sem_classificacao))

#print(maior_hora)
#print(maior_horario)

