import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import carregar_dados, carregar_geojson



# -------------------------
# FAZENDO A LEITURA INCIAL E CARREGANDO OS DADOS TRATADOS
# -------------------------

dataset = "data/processed/acidentes2026_tratados.csv"

df = carregar_dados(dataset)

geojson_brasil = carregar_geojson(
    "data/GeoJson/br-geojson-main/dist/estados.geojson"
)

geojson_brs = carregar_geojson(
    "data/GeoJson/rodovias_federais_brasil.json"
)

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

# Analise de acidente por hora padrão ex: 11:00
acidentes_hora = (
    df.groupby("hora")["id"]
    .nunique()
    .reset_index(name="quantidade")
)

fig_hora = px.line(
    acidentes_hora,
    x="hora",
    y="quantidade",
    markers=True,
    title="Quantidade de acidentes por hora exata"
)

fig_hora.update_layout(
    title_x=0.5,
    autosize=True,
    height=600,
    margin={
        "l": 60,
        "r": 30,
        "t": 70,
        "b": 60
    }
)

fig_hora.write_html(
    "site/graficos/acidentes_hora.html",
    include_plotlyjs="cdn",
    full_html=True,
    config={
        "responsive": True
    }
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

# -------------------------
# ACIDENTES POR UF
# -------------------------

acidentes_uf = (
    df.groupby("uf")["id"]
    .nunique()
    .reset_index(name="quantidade")
)

fig_mapa_uf = px.choropleth_map(
    acidentes_uf,
    geojson=geojson_brasil,
    locations="uf",
    featureidkey="properties.sigla",
    color="quantidade",

    hover_name="uf",

    color_continuous_scale="Blues",

    center={
        "lat": -14.2,
        "lon": -51.9
    },

    zoom=2.8,

    map_style="carto-positron",

    title="Quantidade de Acidentes por UF"
)

fig_mapa_uf.update_layout(
    title_x=0.5,
    margin={
        "r": 0,
        "t": 50,
        "l": 0,
        "b": 0
    }
)

# -------------------------
# ACIDENTES POR BR
# -------------------------

acidentes_br = (
    df.dropna(subset=["br"])
    .groupby("br")["id"]
    .nunique()
    .reset_index(name="quantidade")
    .sort_values("quantidade", ascending=False)
    .reset_index(drop=True)
)

# Padronizando o número da BR
acidentes_br["br"] = (
    acidentes_br["br"]
    .astype(int)
    .astype(str)
    .str.zfill(3)
)

# Criando nome formatado
acidentes_br["rodovia"] = "BR-" + acidentes_br["br"]


# -------------------------
# TOP 10 BRs COM MAIS ACIDENTES
# -------------------------

top_brs = acidentes_br.head(10)


fig_mapa_brs = go.Figure(fig_mapa_uf)


# Percorrendo as 10 BRs com mais acidentes
for _, linha in top_brs.iterrows():

    numero_br = linha["br"]
    quantidade = linha["quantidade"]

    longitude = []
    latitude = []

    # Procurando todos os trechos da BR no GeoJSON
    for trecho in geojson_brs["features"]:

        if trecho["properties"]["vl_br"] == numero_br:

            coordenadas = trecho["geometry"]["coordinates"]

            # Pegando longitude e latitude de cada ponto
            for coordenada in coordenadas:

                longitude.append(coordenada[0])
                latitude.append(coordenada[1])

            # Separando um trecho do próximo
            longitude.append(None)
            latitude.append(None)

    # Adicionando a BR no mapa
    fig_mapa_brs.add_trace(
        go.Scattermap(
            lon=longitude,
            lat=latitude,
            mode="lines",

            line={
                "width": 3
            },

            name=f"BR-{numero_br}",

            hovertemplate=(
                f"BR-{numero_br}<br>"
                f"Acidentes: {quantidade}"
                "<extra></extra>"
            )
        )
    )


# -------------------------
# CONFIGURAÇÃO DO MAPA
# -------------------------

fig_mapa_brs.update_layout(
    title="Acidentes por UF e Principais BRs",
    title_x=0.5,

    margin={
        "r": 20,
        "t": 50,
        "l": 20,
        "b": 100
    },

    legend={
        "orientation": "h",
        "yanchor": "top",
        "y": -0.08,
        "xanchor": "center",
        "x": 0.5
    },

    coloraxis_colorbar={
        "title": "Quantidade",
        "x": 1.02
    }
)


#Variavel para alternar entre gráficos para alternar 
# basta mudar o valor da variavel "grafico"
grafico = "hora"

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

elif(grafico == "uf"):
    fig_mapa_uf.show()

elif(grafico == "brs"):
    fig_mapa_brs.show()

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



