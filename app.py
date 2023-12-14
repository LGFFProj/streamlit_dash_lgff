from candlestickData import get_data
from math import pi
import streamlit as st
import pandas as pd
from bokeh.plotting import figure, column, curdoc

#Configurar Pagina
st.set_page_config(
    page_title="Atividade Avaliativa - N2", 
    page_icon=":rocket:", 
    layout="centered", 
    initial_sidebar_state="auto", 
    menu_items=None
)

st.header(":money_with_wings: :chart: Grafico de Velas (Candlestick Chart) :candle:")

#Pegando candlestick data da API-CoinBase
data = get_data(product_id='BTC-USD', granularity='900')

if data.status_code == 200:
    
    #Organizando o DataFrame com Pandas
    candlestick_data = data.json()
    columns = ["timestamp", "price_low", "price_high", "price_open", "price_close", "volume"]
    df = pd.DataFrame(candlestick_data, columns=columns)
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')

    #Configurando o Bokeh para apresentar as Candles
    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"
    inc = df.price_close > df.price_open
    dec = df.price_open > df.price_close
    w = 12*60*60*10

    p = figure(x_axis_type="datetime", tools=TOOLS, width=1500, title='BTC-USD')
    p.xaxis.major_label_orientation = pi/5
    p.grid.grid_line_alpha=0.3

    p.segment(df.timestamp, df.price_high, df.timestamp, df.price_low, color="black")
    p.vbar(df.timestamp[inc], w, df.price_open[inc], df.price_close[inc], fill_color="green", line_color="black")
    p.vbar(df.timestamp[dec], w, df.price_open[dec], df.price_close[dec], fill_color="#F2583E", line_color="black")

    #Botão para mudar o Estilo do grafico
    cor_grafico = False

    col1, col2, col3 = st.columns([15, 15, 5])

    with col3:
        if st.button(":dark_sunglasses:"):
            
            cor_grafico = not cor_grafico

            if cor_grafico:
                doc = curdoc()
                doc.theme = 'dark_minimal'
                doc.add_root(p)

    st.bokeh_chart(p, use_container_width=True)

else:
    print(f"Error: {response.status_code} - {response.text}")
