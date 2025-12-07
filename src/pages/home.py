import streamlit as st


def app():
    st.title("Lantern Air Lite - V2 prototype")
    st.header("Overview")
    st.write(
        "Lantern Air Lite is a minimal Streamlit dashboard for exploring air quality data."
    )
    info = st.selectbox("Select an option to learn more about it:", ["Website Overview", "What is Asthma?", "What is AQI?", "The Importance of Air Quality"])
    
    if info == "Website Overview":
        st.markdown("**Home** describes the functionality of the pagse of the website and provides background information on asthma and AQI:")
        st.markdown("**Air Quality Explorer** shows charts and maps of air quality data for different cities and parameters.")
        st.markdown("**Asthma Risk** offers an estimation of general and personal risk  based on air quality readings.")
    elif info == "What is Asthma?":
        st.write("Asthma is a long-term condition that makes the airways in your lungs extra sensitive. When something triggers them—like allergies, exercise, or cold air—the airways can tighten, swell, and produce extra mucus. This can cause symptoms such as coughing, wheezing, chest tightness, and shortness of breath. Asthma varies from person to person, but with proper management and treatment, most people can keep their symptoms under good control and live active, healthy lives.")
    elif info == "What is AQI?":
        st.write("The Air Quality Index (AQI) is a simple rating system that tells you how clean or polluted the air is and how that pollution might affect your health. It uses a scale—usually from 0 to 500—where lower numbers mean cleaner air and higher numbers mean more pollution. The AQI is often color-coded (like green for good air and red or purple for unhealthy air) so you can quickly understand whether it’s safe to be outdoors or if you should limit activities, especially if you have conditions like asthma.")
    elif info == "The Importance of Air Quality":
        st.write("Air quality matters because the air you breathe directly affects your health and overall well-being. When the air is clean, your lungs and heart don’t have to work as hard, and it’s easier to stay active and healthy. But when the air contains pollutants—like smoke, vehicle exhaust, or allergens—it can irritate your lungs, trigger breathing problems, worsen conditions like asthma, and even affect long-term health. Good air quality also supports healthy communities, protects children and older adults, and helps the environment stay balanced. In short, cleaner air means a healthier life for everyone.")
    