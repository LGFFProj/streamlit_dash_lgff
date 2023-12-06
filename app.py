import pandas as pd
import streamlit as st


dt = pd.read_csv("https://raw.githubusercontent.com/LGFFProj/streamlit_dash_lgff/main/dataset/BTCUSDT-15m.csv")


st.table(dt)