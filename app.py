"""
Name: Andrew Luutu & Jacob LeMoine
Date: Fall 2025
URL: https://lanternv2-9bdzqdpxngocf7cfonpb8c.streamlit.app/

Description:
This open-source program is an interactive Streamlit application that visualizes
air-quality data from OpenAQ for Boston and Kampala. It includes data cleaning,
analytics, a line chart, summary metrics, and an interactive Folium map. Users
can explore pollution trends, filter parameters, and analyze exposure risks.
"""


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
