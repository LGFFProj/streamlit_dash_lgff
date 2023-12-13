import requests
from math import pi
import streamlit as st
import pandas as pd
from bokeh.plotting import figure, column

base_url = "https://api.exchange.coinbase.com"
product_id = "BTC-USD"
endpoint = f"/products/{product_id}/candles"

url = f"{base_url}{endpoint}"

params = {
    "granularity": 900,
    "start_time": "1699204964",
    "end_time": "1701796964",
}

# Making the GET request with parameters
response = requests.get(url, params=params)

if response.status_code == 200:
    # Extracting candlestick data from the response
    candlestick_data = response.json()

    columns = ["timestamp", "price_low", "price_high", "price_open", "price_close", "volume"]

    df = pd.DataFrame(candlestick_data, columns=columns)

    df["timestamp"] = pd.to_datetime(df['timestamp'], unit='s')


    

    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

    p = figure(x_axis_type="datetime", tools=TOOLS, width=1500, title="Candlestick Teste")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.timestamp, df.price_high, df.timestamp, df.price_low, color="black")

    st.bokeh_chart(p, use_container_width=True)

else:
    print(f"Error: {response.status_code} - {response.text}")
