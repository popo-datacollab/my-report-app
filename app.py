import streamlit as st
import pandas as pd

st.title("Test App")
st.write("App is running correctly!")

file = st.file_uploader("Upload CSV", type=["csv"])
if file:
    df = pd.read_csv(file)
    st.write(df.head())
