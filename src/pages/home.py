import streamlit as st


def app():
    st.title("Lantern Air Lite")
    st.header("Overview")
    st.write(
        "Lantern Air Lite is a minimal Streamlit dashboard for exploring air quality data."
    )
    st.markdown("- Navigate to 'Air Quality Explorer' to view charts and maps.")
    st.markdown("- Use 'Asthma Risk' for a simple rule-based risk summary.")
