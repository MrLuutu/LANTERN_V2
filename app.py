import streamlit as st
from src.pages import home, explorer, risk

#Set page configuration
st.set_page_config(page_title="Lantern Air Lite", layout="wide")

#Set dict of page names to module names
PAGES = {
    "Home": home,
    "Air Quality Explorer": explorer,
    "Asthma Risk": risk,
}

#Create sidebar of pages
st.sidebar.title("Lantern Air Lite")
selection = st.sidebar.radio("Navigate", list(PAGES.keys()))

#Run the selected page
page = PAGES[selection]
page.app()
