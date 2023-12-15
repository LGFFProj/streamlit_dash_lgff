from candlestickData import get_data
from math import pi
from productData import get_products
import streamlit as st
import pandas as pd
import math
from bokeh.plotting import figure, column, curdoc, ColumnDataSource, output_file
from bokeh.models import HoverTool, WheelZoomTool

#Configurar Pagina
st.set_page_config(
    page_title="Atividade Avaliativa - N2", 
    page_icon=":rocket:", 
    layout="wide",
    initial_sidebar_state="auto", 
    menu_items=None
)


st.header(" :chart: Grafico de Velas (Candlestick Chart) :candle:")

#Granularidade
tempos = [60, 300, 900, 3600, 21600, 86400]

#Barra Lateral
produtos = get_products()

def formatarTempo(option):
    if option <= 900:
        return f'{math.trunc(option / 60)}  Min'
    if option > 900:
        return f'{math.trunc(option / 60 / 60)} Hr'

#barra lateral
with st.sidebar:
    with st.form("form"):
        option = st.selectbox("Escolha seu Ativo:", produtos, help="Quotagem do Par de Cripto-Moedas, O primero Item, antes do 'Hífen' é o qual está sendo Comprado/Vendido enquanto o segundo é o que será comprado/vendido contra, Imagine que você está Vendendo o primeiro para Comprar o segundo, pra ai esperar a variação do preço e depois obter o lucro.  ")
        tempo_vela = st.selectbox("Escolha o tempo da Candle: ", tempos, format_func=formatarTempo ,help="Cada Barra/Candle representa uma quantidade de tempo no Grafico, seja ela de 5min ou 24 horas.")
        st.form_submit_button("Vai!!")


#Pegando candlestick data da API-CoinBase
data = get_data(product_id=option, granularity=tempo_vela)

if data.status_code == 200:
    
    
    #Organizando o DataFrame com Pandas
    candlestick_data = data.json()
    columns = ["timestamp", "price_low", "price_high", "price_open", "price_close", "volume"]
    df = pd.DataFrame(candlestick_data, columns=columns)
    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')

    df['timestamp_str'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Formatar as Unidades para Preços
    df['price_low_usd'] = df['price_low'].apply(lambda x: f"${x:.5f}")
    df['price_high_usd'] = df['price_high'].apply(lambda x: f"${x:.5f}")
    df['price_open_usd'] = df['price_open'].apply(lambda x: f"${x:.5f}")
    df['price_close_usd'] = df['price_close'].apply(lambda x: f"${x:.5f}")

    #Hover nas Candles
    output_file("toolbar.html")

    source = ColumnDataSource(data=df)

    TOOLTIPS = [
        ("Tempo", "@timestamp_str"),
        ("Low", "@price_low_usd"),
        ("High", "@price_high_usd"),
        ("Open", "@price_open_usd"),
        ("Close", "@price_close_usd"),
    ]

    #Configurando o Bokeh para apresentar as Candles
    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"
    inc = df.price_close > df.price_open
    dec = df.price_open > df.price_close

    df_inc = df[inc]
    df_dec = df[dec]

    w = tempo_vela * 900

    p = figure(x_axis_type="datetime", tools=TOOLS ,width=1500, height=380, title=option, x_range=(df['timestamp'].min(), df['timestamp'].max()))
    p.xaxis.major_label_orientation = pi/5
    p.grid.grid_line_alpha=0.3

    seg = p.segment(df.timestamp, df.price_high, df.timestamp, df.price_low, color="black")
    vbar_inc = p.vbar( x='timestamp', width=w, top='price_open', bottom='price_close', fill_color="green", line_color="green", source=ColumnDataSource(data=df_inc))
    vbar_dec = p.vbar( x='timestamp', width=w, top='price_open', bottom='price_close', fill_color="#F2583E", line_color="red", source=ColumnDataSource(data=df_dec))

    hover = HoverTool(renderers=[vbar_inc, vbar_dec], tooltips=TOOLTIPS, formatters={'@timestamp_str': 'datetime'})
    p.add_tools(hover)

    p.toolbar.active_scroll = p.select_one(WheelZoomTool)

    #Botão para mudar o Estilo do grafico
    col1, col2, col3, col4 = st.columns([30,1,1.7,1])

    with col2:
        st.write(":sunny:")

    with col3:
        cegueira = st.toggle(':new_moon:')

    if cegueira:
        doc = curdoc()
        doc.theme = 'dark_minimal'
        doc.add_root(p)
    else:
        doc = curdoc()
        doc.theme = 'caliber'
        doc.add_root(p)

    p.xaxis.axis_label="Data"
    p.yaxis.axis_label="Preço ($)"


    #Apresentar o Grafico Final
    st.bokeh_chart(p, use_container_width=True)

else:
    print(f"Error: {response.status_code} - {response.text}")
