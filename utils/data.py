import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("medical_billing.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df
