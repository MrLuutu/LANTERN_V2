import streamlit as st

def app():

    st.set_page_config(layout="wide")

    # =========================
    # PREMIUM HERO SECTION
    # =========================
    HERO_URL = "https://images.unsplash.com/photo-1505751172876-fa1923c5c528"

    st.markdown(
        f"""
        <style>
            .hero {{
                position: relative;
                width: 100%;
                height: 380px;
                border-radius: 16px;
                overflow: hidden;
                margin-bottom: 30px;
            }}

            .hero img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                filter: brightness(60%);
            }}

            .hero-text {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                text-align: center;
                font-family: 'Helvetica Neue', sans-serif;
            }}

            .hero-title {{
                font-size: 48px;
                font-weight: 800;
                letter-spacing: -1px;
                margin-bottom: 10px;
            }}

            .hero-sub {{
                font-size: 20px;
                font-weight: 300;
                opacity: 0.9;
            }}

            /* Feature cards */
            .card {{
                padding: 25px;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 14px;
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                margin-bottom: 20px;
            }}

            .card-title {{
                font-size: 22px;
                font-weight: 600;
                margin-bottom: 8px;
            }}

            .cta-button {{
                display: inline-block;
                padding: 12px 28px;
                background: #2e7df6;
                color: white;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                margin-top: 18px;
            }}

            .cta-button:hover {{
                background: #1b57aa;
            }}

        </style>
        """,
        unsafe_allow_html=True,
    )

    # HERO IMAGE + TEXT
    st.markdown(
        f"""
        <div class="hero">
            <img src="{HERO_URL}">
            <div class="hero-text">
                <div class="hero-title">Lantern Air Lite</div>
                <div class="hero-sub">Real-time insights on air quality & asthma health analytics</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")  # spacing

    # =========================
    # FEATURE CARDS SECTION
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">🌍 Air Quality Explorer</div>
                Explore pollution trends, sensor data, and spatial maps for different cities.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">❤️ Asthma Risk Insights</div>
                Estimate environmental asthma triggers using local AQI & PM readings.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">📊 Health Analytics</div>
                Understand long-term pollution exposure patterns and health correlations.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =========================
    # CALL TO ACTION
    # =========================
    st.markdown(
        """
        <div style="text-align:center; margin-top:30px;">
            <a class="cta-button" href="?Air_Quality_Explorer">Launch Dashboard</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Description footer
    st.markdown(
        """
        <br><br>
        <div style="text-align:center; font-size:14px; opacity:0.6;">
            Built for environmental analytics, public health insights, and data-driven air monitoring.
        </div>
        """,
        unsafe_allow_html=True,
    )
