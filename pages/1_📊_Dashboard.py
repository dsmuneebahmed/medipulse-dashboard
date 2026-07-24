import streamlit as st
import plotly.express as px

from utils.data import load_data
from utils.theme import load_theme

load_theme()

df = load_data()

st.title("📊 Executive Dashboard")

revenue = df["Paid"].sum()
charges = df["Charge"].sum()
claims = len(df)
collection = revenue / charges * 100

c1,c2,c3,c4 = st.columns(4)

c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Claims", claims)
c3.metric("Charges", f"${charges:,.0f}")
c4.metric("Collection", f"{collection:.1f}%")

monthly = df.groupby("Month")["Paid"].sum().reset_index()

fig = px.line(
    monthly,
    x="Month",
    y="Paid",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig, use_container_width=True)
