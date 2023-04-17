#importando bibliotecas
import streamlit as st
import requests
import pandas as pd
from IPython.core.display import HTML


#classe link imagens para HTML
def link_imagem_html(url_imagem):
    return '<img src="'+ url_imagem + '" width="150" >'


st.sidebar.header('PREMIER LEAGUE')


#carregas os arquivos
clubes = pd.read_csv('backup/equipes_premier_league.csv')
atletas = pd.read_csv('backup/atletas_premier_league.csv')

#cria uma lista para listbox dos clubes
list_clubes = []
list_clubes = clubes['nome_clube'].values.tolist()
selected_clube = st.sidebar.selectbox('Selecione um clube abaixo:', list_clubes)


tab1, tab2, tab3 = st.tabs(['FICHA DO ATLETA', 'RESUMO POR POSIÇÃO DO ATLETA', 'RESUMO POR PAÍS DO ATLETA'])
with tab1:
    #cria uma dataframe do clube selecionado
    filtra_clube = clubes.loc[clubes['nome_clube'] == selected_clube]
    logo_clube = filtra_clube.iloc[0]['logo_clube'].replace("//", 'https://') #adiciona "https:" à url da imagem
    st.sidebar.image(logo_clube, width = 200, caption=selected_clube)

    #filtra os atletas pelo id do clube selecionado
    filtra_atleta = atletas.loc[atletas['id_clube'] == filtra_clube.iloc[0]['id_clube']]
    filtra_atleta = filtra_atleta[['numero_camisa', 'nome_atleta', 'posicao_atleta','img_atleta','pais_atleta']]

    #filtra_atleta = filtra_atleta.rename(columns={'img_atleta': 'img', 'bandeira_pais': 'img'})
    filtra_atleta = filtra_atleta.rename(columns={'numero_camisa': 'Nº', 'nome_atleta': 'NOME', 'posicao_atleta': 'POSIÇÃO', 
                                    'img_atleta': '_','pais_atleta': 'PAÍS'})#, inplace = True)

    col_posicao, col_2, col_3 = st.columns(3)
    with col_posicao:
        #cria uma lista para listbox dos atletas
        list_atletas_clube_selecionado = []
        list_atletas_clube_selecionado = filtra_atleta['NOME'].values.tolist()
        selected_atleta = st.selectbox('Selecione um atleta abaixo:', list_atletas_clube_selecionado)

    with col_2:
        st.text('')

    with col_3:
        st.text('')


    filtra_atleta_clube = filtra_atleta.loc[filtra_atleta['NOME'] == selected_atleta]

    numero = filtra_atleta_clube.iloc[0]['Nº']
    atleta = filtra_atleta_clube.iloc[0]['NOME']
    link_foto = filtra_atleta_clube.iloc[0]['_'].replace("//", 'https://') #adiciona "https:" à url da imagem
    posicao = filtra_atleta_clube.iloc[0]['POSIÇÃO']
    pais_atleta = filtra_atleta_clube.iloc[0]['PAÍS']

    col_foto_atleta, col_dados_atleta = st.columns(2)
    with col_foto_atleta:
        st.image(link_foto,
                    width = 200,
                    caption = atleta
                    )

    with col_dados_atleta:
        st.markdown('**Nº da Camisa**: ' + str(numero))
        st.markdown('**Posição do Atleta**: ' + posicao)
        st.markdown('**País do Atleta**: ' + pais_atleta)

with tab2:
    #cria uma lista para listbox de posições dos atletas
    list_posicao_atletas = []
    list_posicao_atletas = filtra_atleta['POSIÇÃO'].values.tolist()
    list_posicao_atletas = list(dict.fromkeys(list_posicao_atletas)) #remove duplicatas

    col_posicao, col_2, col_3 = st.columns(3)
    with col_posicao:
        selected_posicao = st.selectbox('Selecione a posição atleta abaixo:', list_posicao_atletas)

    with col_2:
        st.text('')
    
    with col_3:
        st.text('')

    filtra_posicao_atletas = filtra_atleta.loc[filtra_atleta['POSIÇÃO'] == selected_posicao]

    st.markdown(
        filtra_posicao_atletas.to_html(escape=False, formatters=dict(_=link_imagem_html)),
        unsafe_allow_html=True,
    )

with tab3:
    st.text('')
    #cria uma lista para listbox de posições dos atletas
    list_pais_atletas = []
    list_pais_atletas = filtra_atleta['PAÍS'].values.tolist()
    list_pais_atletas = list(dict.fromkeys(list_pais_atletas)) #remove duplicatas

    col_posicao, col_2, col_3 = st.columns(3)
    with col_posicao:
        selected_pais = st.selectbox('Selecione a posição atleta abaixo:', list_pais_atletas)

    with col_2:
        st.text('')
    
    with col_3:
        st.text('')

    filtra_pais_atletas = filtra_atleta.loc[filtra_atleta['PAÍS'] == selected_pais]

    st.markdown(
        filtra_pais_atletas.to_html(escape=False, formatters=dict(_=link_imagem_html)),
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.dataframe(filtra_atleta.groupby(by=['PAÍS']).size().reset_index())
