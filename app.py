import pandas as pd
import streamlit as st


dt = pd.read_csv("./dataset/BTCUSDT-15m.csv")


st.table(dt)