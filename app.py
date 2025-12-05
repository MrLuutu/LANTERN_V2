import streamlit as st
from src.pages import home, explorer, risk

st.set_page_config(page_title="Lantern Air Lite", layout="wide")

PAGES = {
    "Home": home,
    "Air Quality Explorer": explorer,
    "Asthma Risk": risk,
}

st.sidebar.title("Lantern Air Lite")
selection = st.sidebar.radio("Navigate", list(PAGES.keys()))

page = PAGES[selection]
page.app()
