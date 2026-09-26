import streamlit as st
import json
import requests


# ============================================================
# CONFIGURAÇÕES DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Pokédex",
    page_icon="🔴",
    layout="wide"
)


# ============================================================
# ESTILO DA PÁGINA
# ============================================================

st.markdown("""
<style>

    .titulo {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    .subtitulo {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .pokemon-nome {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
    }

    .tipo {
        text-align: center;
        font-size: 18px;
        margin-bottom: 15px;
    }

    .caixa {
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES
# ============================================================

@st.cache_data
def buscar_pokemon(nome):
    """
    Busca os dados principais do Pokémon na PokéAPI.
    """

    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"

    try:

        resposta = requests.get(
            url,
            timeout=10
        )

        if resposta.status_code == 200:
            return resposta.json()

        return None

    except requests.exceptions.RequestException:
        return None


@st.cache_data
def buscar_dados_url(url):
    """
    Busca informações usando uma URL fornecida pela própria API.
    """

    try:

        resposta = requests.get(
            url,
            timeout=10
        )

        if resposta.status_code == 200:
            return resposta.json()

        return None

    except requests.exceptions.RequestException:
        return None


# ============================================================
# LENDO O JSON DOS POKÉMON
# ============================================================

try:

    with open(
        "pokemon_index.json",
        "r",
        encoding="utf-8"
    ) as arquivo:

        nomes_pokemons = json.load(arquivo)

except FileNotFoundError:

    st.error(
        "❌ O arquivo pokemon_index.json não foi encontrado."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🔴 Pokédex")

    st.write(
        "Escolha um Pokémon para consultar suas informações."
    )

    nome = st.selectbox(
        "Escolha o seu Pokémon:",
        nomes_pokemons.values()
    )

    st.divider()

    st.info(
        "Os dados são obtidos através da PokéAPI."
    )


# ============================================================
# BUSCAR POKÉMON
# ============================================================

dados_pokemon = buscar_pokemon(nome)


if dados_pokemon is None:

    st.error(
        "❌ Não foi possível encontrar esse Pokémon."
    )

    st.stop()


# ============================================================
# DADOS PRINCIPAIS
# ============================================================

id_pokemon = dados_pokemon["id"]

nome_pokemon = dados_pokemon["name"].title()

altura = dados_pokemon["height"] / 10

peso = dados_pokemon["weight"] / 10

experiencia = dados_pokemon["base_experience"]


# ============================================================
# TIPOS
# ============================================================

tipos = []

for tipo in dados_pokemon["types"]:

    nome_tipo = (
        tipo["type"]["name"]
        .replace("-", " ")
        .title()
    )

    tipos.append(nome_tipo)


# ============================================================
# HABILIDADES
# ============================================================

habilidades = []

for habilidade in dados_pokemon["abilities"]:

    nome_habilidade = (
        habilidade["ability"]["name"]
        .replace("-", " ")
        .title()
    )

    habilidades.append(nome_habilidade)


# ============================================================
# IMAGENS
# ============================================================

imagem_normal = (
    dados_pokemon["sprites"]["front_default"]
)

imagem_shiny = (
    dados_pokemon["sprites"]["front_shiny"]
)


# ============================================================
# GIF NORMAL
# ============================================================

gif_normal = (
    dados_pokemon["sprites"]
    .get("versions", {})
    .get("generation-v", {})
    .get("black-white", {})
    .get("animated", {})
    .get("front_default")
)


# ============================================================
# GIF SHINY
# ============================================================

gif_shiny = (
    dados_pokemon["sprites"]
    .get("versions", {})
    .get("generation-v", {})
    .get("black-white", {})
    .get("animated", {})
    .get("front_shiny")
)


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo">🔴 Pokédex</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Explore informações sobre diferentes Pokémon'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    f'<div class="pokemon-nome">'
    f'#{id_pokemon:03d} — {nome_pokemon}'
    f'</div>',
    unsafe_allow_html=True
)


st.markdown(
    f'<div class="tipo">'
    f'{" / ".join(tipos)}'
    f'</div>',
    unsafe_allow_html=True
)


# ============================================================
# 3 COLUNAS PRINCIPAIS
# ============================================================

col1, col2, col3 = st.columns(3)


# ============================================================
# COLUNA 1 - NORMAL
# ============================================================

with col1:

    st.subheader("🟢 Normal")

    if imagem_normal:

        st.image(
            imagem_normal,
            width=300
        )

    else:

        st.warning(
            "Imagem normal não disponível."
        )

    st.caption(
        f"Pokémon #{id_pokemon:03d}"
    )


# ============================================================
# COLUNA 2 - ANIMAÇÃO + SOM
# ============================================================

with col2:

    st.subheader("🎞️ Animação")

    if gif_normal:

        st.image(
            gif_normal,
            width=300
        )

    else:

        st.info(
            "GIF animado não disponível para este Pokémon."
        )

    st.markdown("### 🔊 Sons")

    som_latest = (
        dados_pokemon["cries"]
        .get("latest")
    )

    som_legacy = (
        dados_pokemon["cries"]
        .get("legacy")
    )

    if som_latest:

        st.audio(
            som_latest
        )

    if som_legacy:

        st.audio(
            som_legacy
        )


# ============================================================
# COLUNA 3 - SHINY
# ============================================================

with col3:

    st.subheader("✨ Shiny")

    if gif_shiny:

        st.image(
            gif_shiny,
            width=300
        )

    elif imagem_shiny:

        st.image(
            imagem_shiny,
            width=300
        )

    else:

        st.info(
            "Imagem shiny não disponível."
        )


# ============================================================
# DIVISOR
# ============================================================

st.divider()


# ============================================================
# INFORMAÇÕES BÁSICAS
# ============================================================

st.header("📋 Informações básicas")


info1, info2, info3, info4 = st.columns(4)


with info1:

    st.metric(
        "🆔 ID",
        f"#{id_pokemon:03d}"
    )


with info2:

    st.metric(
        "📏 Altura",
        f"{altura} m"
    )


with info3:

    st.metric(
        "⚖️ Peso",
        f"{peso} kg"
    )


with info4:

    st.metric(
        "⭐ Experiência",
        experiencia
    )


# ============================================================
# HABILIDADES
# ============================================================

st.divider()

st.header("⚡ Habilidades")


col_hab1, col_hab2 = st.columns(2)


for indice, habilidade in enumerate(habilidades):

    if indice % 2 == 0:

        with col_hab1:

            st.write(
                f"⚡ **{habilidade}**"
            )

    else:

        with col_hab2:

            st.write(
                f"⚡ **{habilidade}**"
            )


# ============================================================
# STATUS
# ============================================================

st.divider()

st.header("📊 Status")


for stat in dados_pokemon["stats"]:

    nome_stat = (
        stat["stat"]["name"]
        .replace("-", " ")
        .title()
    )

    valor = stat["base_stat"]

    col_nome, col_barra = st.columns(
        [1, 4]
    )

    with col_nome:

        st.write(
            f"**{nome_stat}**"
        )

    with col_barra:

        st.progress(
            min(valor / 255, 1.0),
            text=str(valor)
        )


# ============================================================
# DADOS DA ESPÉCIE
# ============================================================

st.divider()

st.header("📖 Informações da espécie")


especie_url = (
    dados_pokemon["species"]["url"]
)

dados_especie = buscar_dados_url(
    especie_url
)


if dados_especie:

    especie1, especie2, especie3 = st.columns(3)


    with especie1:

        st.metric(
            "🎯 Taxa de captura",
            dados_especie["capture_rate"]
        )


    with especie2:

        st.metric(
            "😊 Felicidade base",
            dados_especie["base_happiness"]
        )


    with especie3:

        geracao = (
            dados_especie["generation"]["name"]
            .replace("-", " ")
            .title()
        )

        st.metric(
            "🌎 Geração",
            geracao
        )


    # ========================================================
    # STATUS ESPECIAL
    # ========================================================

    if dados_especie["is_legendary"]:

        st.success(
            "🌟 Este Pokémon é Lendário!"
        )

    elif dados_especie["is_mythical"]:

        st.success(
            "✨ Este Pokémon é Mítico!"
        )

    elif dados_especie["is_baby"]:

        st.info(
            "🥚 Este Pokémon é classificado como Pokémon Bebê."
        )


    # ========================================================
    # DESCRIÇÃO
    # ========================================================

    st.subheader("📜 Descrição")


    descricoes = (
        dados_especie
        .get("flavor_text_entries", [])
    )


    descricao = None


    for entrada in descricoes:

        if entrada["language"]["name"] == "en":

            descricao = (
                entrada["flavor_text"]
                .replace("\n", " ")
                .replace("\f", " ")
            )

            break


    if descricao:

        st.write(
            descricao
        )

    else:

        st.info(
            "Descrição não disponível."
        )


# ============================================================
# MOVIMENTOS
# ============================================================

st.divider()

st.header("🎮 Movimentos")


movimentos = dados_pokemon.get(
    "moves",
    []
)


if movimentos:

    nomes_movimentos = []


    for movimento in movimentos[:30]:

        nome_movimento = (
            movimento["move"]["name"]
            .replace("-", " ")
            .title()
        )

        nomes_movimentos.append(
            nome_movimento
        )


    # Divide os movimentos em duas colunas

    mov1, mov2 = st.columns(2)


    metade = len(nomes_movimentos) // 2


    for movimento in nomes_movimentos[:metade]:

        with mov1:

            st.write(
                f"🎮 {movimento}"
            )


    for movimento in nomes_movimentos[metade:]:

        with mov2:

            st.write(
                f"🎮 {movimento}"
            )


# ============================================================
# EVOLUÇÃO
# ============================================================

st.divider()

st.header("🔄 Cadeia de evolução")


if dados_especie:

    evolution_url = (
        dados_especie["evolution_chain"]["url"]
    )

    dados_evolucao = buscar_dados_url(
        evolution_url
    )


    if dados_evolucao:

        nomes_evolucao = []


        def encontrar_evolucoes(chain):

            nome = chain["species"]["name"]

            nomes_evolucao.append(
                nome
            )

            for proxima in chain["evolves_to"]:

                encontrar_evolucoes(
                    proxima
                )


        encontrar_evolucoes(
            dados_evolucao["chain"]
        )


        # ====================================================
        # MOSTRAR EVOLUÇÕES
        # ====================================================

        colunas_evolucao = st.columns(
            len(nomes_evolucao)
        )


        for indice, nome_evolucao in enumerate(
            nomes_evolucao
        ):

            dados_evo = buscar_pokemon(
                nome_evolucao
            )


            with colunas_evolucao[indice]:

                st.markdown(
                    f"### {nome_evolucao.title()}"
                )


                if dados_evo:

                    imagem_evo = (
                        dados_evo["sprites"]
                        ["front_default"]
                    )


                    if imagem_evo:

                        st.image(
                            imagem_evo,
                            width=180
                        )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🔴 Pokédex — Projeto desenvolvido em Python + Streamlit "
    "utilizando dados da PokéAPI."
)