import streamlit as st

def load_theme():
    st.markdown("""
    <style>

    .main {
        background:#F5F7FB;
    }

    div[data-testid="stMetric"]{
        background:white;
        border-radius:15px;
        padding:15px;
        box-shadow:0 2px 10px rgba(0,0,0,.08);
    }

    h1{
        color:#1E3A8A;
        font-weight:700;
    }

    </style>
    """, unsafe_allow_html=True)
