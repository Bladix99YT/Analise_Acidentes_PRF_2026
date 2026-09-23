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

# print(classificacao)

# print("\nTotal de acidentes:", df["id"].nunique())
# print("Soma das classificações:", classificacao["quantidade"].sum())



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

# print("\nTotal de acidentes:", df["id"].nunique())
# print(causas_principais)


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


# -------------------------
# CAUSA DE ACIDENTES
# -------------------------

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

fig_comparacao = px.bar(
    comparacao,
    x= "causa_acidente",
    y= "quantidade",
    color="classificacao_acidente",
    barmode="group",
    title="Principais Causas x Classificação dos Acidentes",
    labels={
        "causa_acidente": "Causa principal",
        "classificacao_acidente": "Classificação",
        "quantidade": "Quantidade de acidentes"
    }
)

fig_comparacao.update_layout(
    title_x=0.5,
    xaxis_tickangle=-45
)

# -------------------------
# TIPO X CAUSA DE ACIDENTE
# -------------------------

tipo_causa = (
    df[
        (df["causa_principal"] == "Sim")
        & (df["ordem_tipo_acidente"] == 1)
    ]
    .groupby(["tipo_acidente", "causa_acidente"])["id"]
    .nunique()
    .reset_index(name="quantidade")
    .sort_values("quantidade", ascending=False)
)

fig_causa_tipo = px.bar(
    tipo_causa,
    x="quantidade",
    y="tipo_acidente",
    color="causa_acidente",
    orientation="h",
    title="Causa x Tipo Acidente",
    labels={
        "tipo_acidente": "Tipo_acidente",
        "causa_acidente": "Causa_acidente",
        "quantidade": "Quantidade de acidentes"
    },
    text="quantidade"  
)

fig_causa_tipo.update_layout(
    title_x=0.5,
    yaxis={"categoryorder": "total ascending"}
)

# -------------------------
# HORARIO ACIDENTES
# -------------------------

fig_horario = px.line(
    acidentes_horario,
    x="horario",
    y="quantidade",
    markers=True,
    title= "Quantidade de acidentes por faixa horária"

)

# -------------------------
# HORA ACIDENTES
# -------------------------

fig_hora = px.line(
    acidentes_hora,
    x="hora",
    y="quantidade",
    markers=True,
    title="Quantidade de acidentes por hora exata"
)

# -------------------------
# ACIDENTES DIA DA SEMANA
# -------------------------

acidentes_dia = (
    df.groupby("dia_semana")["id"]
    .nunique()
    .reset_index(name="quantidade")
)
ordem_dias = [
    "segunda",
    "terça",
    "quarta",
    "quinta",
    "sexta",
    "sábado",
    "domingo"
]

fig_dia = px.bar(
    acidentes_dia,
    x="dia_semana",
    y="quantidade",
    title="Quantidade de Acidentes por Dia da Semana",
    labels={
        "dia_semana": "Dia da semana",
        "quantidade": "Quantidade de acidentes"
    },
    text="quantidade",
    category_orders={
        "dia_semana": ordem_dias
    }
)

fig_dia.update_layout(
    title_x=0.5
)


#Variavel para alternar entre gráficos para alternar 
# basta mudar o valor da variavel "grafico"
grafico = "dia"

if (grafico == "comparacao"):
    fig_comparacao.show()

elif(grafico == "causa_tipo"):
    fig_causa_tipo.show()

elif(grafico == "horario"):
    fig_horario.show()

elif(grafico == "hora"):
    fig_hora.show()

elif(grafico == "dia"):
    fig_dia.show()

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

#print(maior_hora)
#print(maior_horario)

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



