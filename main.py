import requests
import streamlit as st
from sentiment import AnalizeAppend
import pandas as pd
import config
import plotly.express as px
#import time

st.set_page_config(
    page_title="Analiza sentymentu w czasie rzeczywistym",
    layout="wide",
)


headers = {
    'Authorization': f'Bearer {config.API_SECRET}',
}

url = 'https://api.typeform.com/forms/VeYMzJ2A/responses'

def get_data(url):
    response = requests.get(url, headers=headers)
    response = response.json()
    return response

o = get_data(url)

def return_values(response):
    res_list = []
    for item in response['items']:
        if(item['answers'] is not None):
            for answer in item["answers"]:
                res_list.append(answer['text'])
    return res_list
res_list = return_values(o)
st.title("Poniżej wszystkie udzielone odpowiedzi:")
res_list

def return_sentences(res_lists):
  list_zmienne = []
  for i in range(len(res_lists)):
    zmienna = AnalizeAppend(res_lists[i])
    zmienne = zmienna.analyze_token_sentiment()
    list_zmienne.append(zmienne)
  return list_zmienne

wynik = return_sentences(res_list)
df = pd.DataFrame(wynik)

colnames = ['positives', 'negatives', 'neutral']

def bracket_delete(df):
    df['totalwords'] = df['sentence'].str.split().str.len()
    for colname in colnames:
        df[colname] = df[colname].str[0]
    return df
df = bracket_delete(df)
df['sentiment'] = df['positives'].fillna("") + df['negatives'].fillna("") + df['neutral'].fillna("")
df.drop(colnames, axis=1, inplace=True)

with st.expander("### Zobacz wyniki analizy sentymentu"):
    st.write("""
        Tabela poniżej przedstawia wszystkie udzielone odpowiedzi wraz z oceną ich sentymentu.
        Sentyment oceniany jest w trzech wymiarach: pozytywny, negatywny, neutralny.
    """)
    st.dataframe(df)

placeholder = st.empty()
positives = df[df.sentiment == 'positive'].shape[0]
negatives = df[df.sentiment == 'negative'].shape[0]
neutrals = df[df.sentiment == 'neutral'].shape[0]

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Positives 🙂",
        value=int(positives),
    )

    kpi2.metric(
        label="Negatives🙁",
        value=int(negatives),
    )

    kpi3.metric(
        label="Neutrals😐",
        value=int(neutrals),
    )

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Macierz sentymentu")
        fig = px.density_heatmap(
            data_frame=df, y="totalwords", x="sentiment"
            )
        st.write(fig)
    with fig_col2:
        st.markdown("### Liczba zliczeń słów")
        fig2 = px.histogram(data_frame=df, x="totalwords")
        st.write(fig2)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
