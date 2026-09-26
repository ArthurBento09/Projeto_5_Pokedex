import streamlit as st
import json
import requests

# Ajustando o size da pagina
st.set_page_config(layout="wide")

# Lendo o Arquivo
with open('pokemon_index.json', 'r', encoding='utf-8') as arquivo:
    nomes_pokemons = json.load(arquivo)

nome = st.selectbox('Escolha o seu Pokemon: ', nomes_pokemons.values())

# Link da API
url = f'https://pokeapi.co/api/v2/pokemon/{nome}'

# Usando Todas as informações da API
dados_pokemon = requests.get(url).json()

# criar colunas para dividir o site em 3 partes
col1,col2,col3 = st.columns(3)

#pegando as informações dos pokemons
peso = dados_pokemon ['weight'] /10
altura = dados_pokemon ['height'] /10
imc = round(peso / (altura ** 2))

with col1:
    st.image(dados_pokemon['sprites']['front_default'], width=500)
    st.write('Normal4c')

with col2:
    st.audio(dados_pokemon['cries']['latest'])
    st.audio(dados_pokemon['cries']['legacy'])

with col3:
    st.image(dados_pokemon['sprites']['front_shiny'], width=550 )
    st.write('Shiny')

#Recriando as colunas para informação de Peso, Altura e IMC
col1,col2,col3 = st.columns(3)
with col1:
    st.metric(f"O Peso do Pokemon é:", peso)

with col2:
    st.metric(f"A Altura do Pokemon é:", altura)

with col3:
    st.metric(f"O IMC é:", imc)

# Criando as partes de guias no site
status,tipos,habilidades,locais = st.tabs(['Status', 'Tipos', 'Habilidades', 'Locais'])

with tipos:
    for i in dados_pokemon['types']:
        st.markdown(f'- {i['type']['name']}')

with status:
    hp, ataque, defesa, ataque_esp, defesa_esp, velocidade = st.columns(6)
    with hp:
        st.metric('HP', dados_pokemon['stats'][0]['base_stat'])
    with ataque:
        st.metric('Ataque', dados_pokemon['stats'][1]['base_stat'])
    with defesa:
        st.metric('Defesa', dados_pokemon['stats'][2]['base_stat'])
    with ataque_esp:
        st.metric('Ataque Especial', dados_pokemon['stats'][3]['base_stat'])
    with defesa_esp:
        st.metric('Defesa Especial', dados_pokemon['stats'][4]['base_stat'])
    with velocidade:
        st.metric('Velocidade', dados_pokemon['stats'][5]['base_stat'])


with locais:
    locais = requests.get(dados_pokemon['location_area_encounters']).json()
    for local in locais:
        st.markdown(f'- {local['location_area']['name']}')


with habilidades:
    for abilidade in dados_pokemon['abilities']:
        st.markdown(f'- {abilidade['ability']['name']}')


