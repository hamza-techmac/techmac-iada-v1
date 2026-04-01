import os
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for tiles
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none; }
.metric-tile {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    padding: 15px;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 90px;
    margin-bottom: 10px;
}
.metric-tile h3 {
    margin: 0;
    font-size: 1.5rem;
    color: #1f1f1f;
}
.metric-tile h4 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
}
.metric-tile h6 {
    margin: 5px 0 0 0;
    font-size: 0.9rem;
    color: #666;
    font-weight: 500;
}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #ffffff;
    color: #555;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #ddd;
    z-index: 100;
}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 1. User Authentication Setup ---
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin User",
            "password": "$2b$12$Pp9vsL3blfjaOsJHdQsFsOWau0vvctlsHSKANv9ujKwr4n7kw.dm6"  # <--- Paste the hash here!
        }
    }
}

# --- 2. Initialize Authenticator ---
authenticator = stauth.Authenticate(
    credentials,
    "techmac_iada_auth_cookie", 
    "techmac_iada_auth_key",
    cookie_expiry_days=1
)

# --- 3. Login Logic ---
# In v0.3.0+, .login() handles state internally and returns nothing.
authenticator.login(location='main')

# Check authentication status via session_state
if st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password")
else:
    # --- LOGGED IN CONTENT ---
    # Header Banner
    st.image("assets/media__1775072322438.png", use_container_width=True)

    col_title, col_profile = st.columns([9, 1])
    with col_title:
        st.title("Branch Dashboard")
    with col_profile:
        st.write("")
        st.write("")
        with st.popover("👤"):
            st.write(f"**{st.session_state.get('name')}**")
            st.button("⚙️ Settings")
            authenticator.logout("Logout", "main")

    # Sidebar Branding
    with st.sidebar:
        st.image("assets/media__1775071056203.png", use_container_width=True)
        st.divider()
        st.write(f"Logged in as: **{st.session_state.get('name')}**")

    st.divider()

    tab_dashboard, tab_monthly, tab_weekly, tab_upload, tab_accounts = st.tabs([
        "Dashboard", "Monthly Analysis", "Weekly Analysis", "Add Sales Stats", "Accounts"
    ])

    with tab_dashboard:
        # --- Profit & Loss Data ---
        raw_pnl_data = [
            ["Crown Fish Bar", "2025-08-12", 33, 690.00, 0.00, 690.00],
            ["Crown Fish Bar", "2025-08-13", 33, 660.00, 0.00, 660.00],
            ["Crown Fish Bar", "2025-08-14", 33, 990.00, 0.00, 990.00],
            ["Crown Fish Bar", "2025-08-15", 33, 1290.00, 0.00, 1290.00],
            ["Crown Fish Bar", "2025-08-16", 33, 1000.00, 0.00, 1000.00],
            ["Crown Fish Bar", "2025-08-17", 33, 0.00, 0.00, 0.00],
            ["Crown Fish Bar", "2025-08-18", 34, 810.00, 2490.52, -1680.52],
            ["Crown Fish Bar", "2025-08-19", 34, 818.00, 0.00, 818.00],
            ["Crown Fish Bar", "2025-08-20", 34, 934.00, 0.00, 934.00],
            ["Crown Fish Bar", "2025-08-21", 34, 930.00, 0.00, 930.00],
            ["Crown Fish Bar", "2025-08-22", 34, 1240.00, 0.00, 1240.00],
            ["Crown Fish Bar", "2025-08-23", 34, 800.00, 0.00, 800.00],
            ["Crown Fish Bar", "2025-08-24", 34, 0.00, 0.00, 0.00],
            ["Crown Fish Bar", "2025-08-25", 35, 960.00, 2943.78, -1983.78],
            ["Crown Fish Bar", "2025-08-26", 35, 1002.00, 0.00, 1002.00],
            ["Crown Fish Bar", "2025-08-27", 35, 1230.00, 0.00, 1230.00],
            ["Crown Fish Bar", "2025-08-28", 35, 1016.00, 0.00, 1016.00],
            ["Crown Fish Bar", "2025-08-29", 35, 1460.00, 0.00, 1460.00],
            ["Crown Fish Bar", "2025-08-30", 35, 1190.00, 0.00, 1190.00],
            ["Crown Fish Bar", "2025-08-31", 35, 0.00, 0.00, 0.00],
            ["Crown Fish Bar", "2025-09-01", 36, 920.00, 3698.08, -2778.08],
            ["Crown Fish Bar", "2025-09-02", 36, 802.00, 0.00, 802.00],
            ["Crown Fish Bar", "2025-09-03", 36, 656.00, 0.00, 656.00],
            ["Crown Fish Bar", "2025-09-04", 36, 798.00, 0.00, 798.00],
            ["Crown Fish Bar", "2025-09-05", 36, 1340.00, 0.00, 1340.00],
            ["Crown Fish Bar", "2025-09-06", 36, 910.00, 0.00, 910.00],
            ["Crown Fish Bar", "2025-09-07", 36, 0.00, 0.00, 0.00],
            ["Crown Fish Bar", "2025-09-08", 37, 918.00, 4098.50, -3180.50],
            ["Crown Fish Bar", "2025-09-09", 37, 1226.00, 0.00, 1226.00],
            ["Crown Fish Bar", "2025-09-10", 37, 836.00, 0.00, 836.00],
            ["Crown Fish Bar", "2025-09-11", 37, 1300.00, 0.00, 1300.00],
            ["Crown Fish Bar", "2025-09-12", 37, 1632.00, 0.00, 1632.00],
            ["Crown Fish Bar", "2025-09-13", 37, 1470.00, 0.00, 1470.00],
            ["Crown Fish Bar", "2025-09-14", 37, 580.00, 0.00, 580.00],
            ["Crown Fish Bar", "2025-09-15", 38, 960.00, 4148.82, -3188.82],
            ["Crown Fish Bar", "2025-09-16", 38, 1380.00, 0.00, 1380.00],
            ["Crown Fish Bar", "2025-09-17", 38, 1070.00, 0.00, 1070.00],
            ["Crown Fish Bar", "2025-09-18", 38, 1150.00, 0.00, 1150.00],
            ["Crown Fish Bar", "2025-09-19", 38, 1820.00, 0.00, 1820.00],
            ["Crown Fish Bar", "2025-09-20", 38, 1370.00, 0.00, 1370.00],
            ["Crown Fish Bar", "2025-09-21", 38, 840.00, 0.00, 840.00],
            ["Crown Fish Bar", "2025-09-22", 39, 1120.00, 4309.30, -3189.30],
            ["Crown Fish Bar", "2025-09-23", 39, 1198.00, 0.00, 1198.00],
            ["Crown Fish Bar", "2025-09-24", 39, 1370.00, 0.00, 1370.00],
            ["Crown Fish Bar", "2025-09-25", 39, 1400.00, 0.00, 1400.00],
            ["Crown Fish Bar", "2025-09-26", 39, 1750.00, 0.00, 1750.00],
            ["Crown Fish Bar", "2025-09-27", 39, 1520.00, 0.00, 1520.00],
            ["Crown Fish Bar", "2025-09-28", 39, 820.00, 0.00, 820.00],
            ["Crown Fish Bar", "2025-09-29", 40, 1180.00, 4337.82, -3157.82],
            ["Crown Fish Bar", "2025-09-30", 40, 1440.00, 0.00, 1440.00],
            ["Crown Fish Bar", "2025-10-01", 40, 1280.00, 0.00, 1280.00],
            ["Crown Fish Bar", "2025-10-02", 40, 1260.00, 0.00, 1260.00],
            ["Crown Fish Bar", "2025-10-03", 40, 2160.00, 0.00, 2160.00],
            ["Crown Fish Bar", "2025-10-04", 40, 1070.00, 0.00, 1070.00],
            ["Crown Fish Bar", "2025-10-05", 40, 720.00, 0.00, 720.00],
            ["Crown Fish Bar", "2025-10-06", 41, 1572.00, 4241.22, -2669.22],
            ["Crown Fish Bar", "2025-10-07", 41, 1030.00, 0.00, 1030.00],
            ["Crown Fish Bar", "2025-10-08", 41, 1110.00, 0.00, 1110.00],
            ["Crown Fish Bar", "2025-10-09", 41, 1510.00, 0.00, 1510.00],
            ["Crown Fish Bar", "2025-10-10", 41, 1850.00, 0.00, 1850.00],
            ["Crown Fish Bar", "2025-10-11", 41, 1230.00, 0.00, 1230.00],
            ["Crown Fish Bar", "2025-10-12", 41, 600.00, 0.00, 600.00],
            ["Crown Fish Bar", "2025-10-13", 42, 1180.00, 4412.42, -3232.42],
            ["Crown Fish Bar", "2025-10-14", 42, 1420.00, 0.00, 1420.00],
            ["Crown Fish Bar", "2025-10-15", 42, 1640.00, 0.00, 1640.00],
            ["Crown Fish Bar", "2025-10-16", 42, 1070.00, 0.00, 1070.00],
            ["Crown Fish Bar", "2025-10-17", 42, 1820.00, 0.00, 1820.00],
            ["Crown Fish Bar", "2025-10-18", 42, 1430.00, 0.00, 1430.00],
            ["Crown Fish Bar", "2025-10-19", 42, 530.00, 0.00, 530.00],
            ["Crown Fish Bar", "2025-10-20", 43, 800.00, 4678.62, -3878.62],
            ["Crown Fish Bar", "2025-10-21", 43, 800.00, 0.00, 800.00],
            ["Crown Fish Bar", "2025-10-22", 43, 1200.00, 0.00, 1200.00],
            ["Crown Fish Bar", "2025-10-23", 43, 920.00, 0.00, 920.00],
            ["Crown Fish Bar", "2025-10-24", 43, 2120.00, 0.00, 2120.00],
            ["Crown Fish Bar", "2025-10-25", 43, 1620.00, 0.00, 1620.00],
            ["Crown Fish Bar", "2025-10-26", 43, 1040.00, 0.00, 1040.00],
            ["Crown Fish Bar", "2025-10-27", 44, 1110.00, 961.80, 148.20],
            ["Crown Fish Bar", "2025-10-28", 44, 1110.00, 0.00, 1110.00],
            ["Crown Fish Bar", "2025-10-29", 44, 1160.00, 0.00, 1160.00],
            ["Crown Fish Bar", "2025-10-30", 44, 1380.00, 0.00, 1380.00],
            ["Crown Fish Bar", "2025-10-31", 44, 1920.00, 0.00, 1920.00],
            ["Crown Fish Bar", "2025-11-01", 44, 1460.00, 0.00, 1460.00],
            ["Crown Fish Bar", "2025-11-02", 44, 660.00, 0.00, 660.00],
            ["Crown Fish Bar", "2025-11-03", 45, 1090.00, 4628.52, -3538.52],
            ["Crown Fish Bar", "2025-11-04", 45, 1260.00, 0.00, 1260.00],
            ["Crown Fish Bar", "2025-11-05", 45, 1420.00, 0.00, 1420.00],
            ["Crown Fish Bar", "2025-11-06", 45, 1380.00, 0.00, 1380.00],
            ["Crown Fish Bar", "2025-11-07", 45, 1790.00, 0.00, 1790.00],
            ["Crown Fish Bar", "2025-11-08", 45, 1750.00, 0.00, 1750.00],
            ["Crown Fish Bar", "2025-11-09", 45, 920.00, 0.00, 920.00],
            ["Crown Fish Bar", "2025-11-10", 46, 1400.00, 995.40, 404.60],
            ["Crown Fish Bar", "2025-11-11", 46, 1290.00, 0.00, 1290.00],
            ["Crown Fish Bar", "2025-11-12", 46, 1180.00, 0.00, 1180.00],
            ["Crown Fish Bar", "2025-11-13", 46, 1370.00, 0.00, 1370.00],
            ["Crown Fish Bar", "2025-11-14", 46, 1800.00, 0.00, 1800.00],
            ["Crown Fish Bar", "2025-11-15", 46, 1280.00, 0.00, 1280.00],
            ["Crown Fish Bar", "2025-11-16", 46, 900.00, 0.00, 900.00],
            ["Crown Fish Bar", "2025-11-17", 47, 1400.00, 4595.44, -3195.44],
            ["Crown Fish Bar", "2025-11-18", 47, 880.00, 0.00, 880.00],
            ["Crown Fish Bar", "2025-11-19", 47, 1160.00, 0.00, 1160.00],
            ["Crown Fish Bar", "2025-11-20", 47, 1460.00, 0.00, 1460.00],
            ["Crown Fish Bar", "2025-11-21", 47, 1760.00, 0.00, 1760.00],
            ["Crown Fish Bar", "2025-11-22", 47, 1442.00, 0.00, 1442.00],
            ["Crown Fish Bar", "2025-11-23", 47, 900.00, 0.00, 900.00],
            ["Crown Fish Bar", "2025-11-24", 48, 1130.00, 1073.73, 56.27],
            ["Crown Fish Bar", "2025-11-25", 48, 1240.00, 0.00, 1240.00],
            ["Crown Fish Bar", "2025-11-26", 48, 1050.00, 0.00, 1050.00],
            ["Crown Fish Bar", "2025-11-27", 48, 1240.00, 0.00, 1240.00],
            ["Crown Fish Bar", "2025-11-28", 48, 2020.00, 0.00, 2020.00],
            ["Crown Fish Bar", "2025-11-29", 48, 1750.00, 0.00, 1750.00],
            ["Crown Fish Bar", "2025-11-30", 48, 1170.00, 0.00, 1170.00],
            ["Crown Fish Bar", "2025-12-01", 49, 1536.00, 4303.25, -2767.25],
            ["Crown Fish Bar", "2025-12-02", 49, 1726.00, 0.00, 1726.00],
            ["Crown Fish Bar", "2025-12-03", 49, 1086.00, 0.00, 1086.00],
            ["Crown Fish Bar", "2025-12-04", 49, 1426.00, 0.00, 1426.00],
            ["Crown Fish Bar", "2025-12-05", 49, 1726.00, 0.00, 1726.00],
            ["Crown Fish Bar", "2025-12-06", 49, 1646.00, 0.00, 1646.00],
            ["Crown Fish Bar", "2025-12-07", 49, 896.00, 0.00, 896.00],
            ["Crown Fish Bar", "2025-12-08", 50, 1026.00, 990.57, 35.43],
            ["Crown Fish Bar", "2025-12-09", 50, 966.00, 0.00, 966.00],
            ["Crown Fish Bar", "2025-12-10", 50, 1166.00, 0.00, 1166.00],
            ["Crown Fish Bar", "2025-12-11", 50, 1206.00, 0.00, 1206.00],
            ["Crown Fish Bar", "2025-12-12", 50, 1926.00, 0.00, 1926.00],
            ["Crown Fish Bar", "2025-12-13", 50, 1586.00, 0.00, 1586.00],
            ["Crown Fish Bar", "2025-12-14", 50, 816.00, 0.00, 816.00],
            ["Crown Fish Bar", "2025-12-15", 51, 1196.00, 4545.39, -3349.39],
            ["Crown Fish Bar", "2025-12-16", 51, 986.00, 0.00, 986.00],
            ["Crown Fish Bar", "2025-12-17", 51, 1016.00, 0.00, 1016.00],
            ["Crown Fish Bar", "2025-12-18", 51, 1168.00, 0.00, 1168.00],
            ["Crown Fish Bar", "2025-12-19", 51, 1856.00, 0.00, 1856.00],
            ["Crown Fish Bar", "2025-12-20", 51, 1716.00, 0.00, 1716.00],
            ["Crown Fish Bar", "2025-12-21", 51, 866.00, 0.00, 866.00],
            ["Crown Fish Bar", "2025-12-22", 52, 1608.00, 3774.16, -2166.16],
            ["Crown Fish Bar", "2025-12-23", 52, 1328.00, 0.00, 1328.00],
            ["Crown Fish Bar", "2025-12-24", 52, 1338.00, 0.00, 1338.00],
            ["Crown Fish Bar", "2025-12-25", 52, 26.00, 0.00, 26.00],
            ["Crown Fish Bar", "2025-12-26", 52, 26.00, 0.00, 26.00],
            ["Crown Fish Bar", "2025-12-27", 52, 1664.00, 0.00, 1664.00],
            ["Crown Fish Bar", "2025-12-28", 52, 866.00, 0.00, 866.00],
            ["Crown Fish Bar", "2025-12-29", 1, 1340.00, 3855.50, -2515.50],
            ["Crown Fish Bar", "2025-12-30", 1, 1420.00, 0.00, 1420.00],
            ["Crown Fish Bar", "2025-12-31", 1, 1510.00, 0.00, 1510.00],
            ["Crown Fish Bar", "2026-01-01", 1, 1510.00, 264.60, 1245.40],
            ["Crown Fish Bar", "2026-01-02", 1, 1620.00, 0.00, 1620.00],
            ["Crown Fish Bar", "2026-01-03", 1, 1390.00, 0.00, 1390.00],
            ["Crown Fish Bar", "2026-01-04", 1, 768.00, 0.00, 768.00],
            ["Crown Fish Bar", "2026-01-05", 2, 1000.00, 4260.10, -3260.10],
            ["Crown Fish Bar", "2026-01-06", 2, 1020.00, 0.00, 1020.00],
            ["Crown Fish Bar", "2026-01-07", 2, 1300.00, 0.00, 1300.00],
            ["Crown Fish Bar", "2026-01-08", 2, 1380.00, 0.00, 1380.00],
            ["Crown Fish Bar", "2026-01-09", 2, 1860.00, 0.00, 1860.00],
            ["Crown Fish Bar", "2026-01-10", 2, 1160.00, 0.00, 1160.00],
            ["Crown Fish Bar", "2026-01-11", 2, 866.00, 0.00, 866.00],
            ["Crown Fish Bar", "2026-01-12", 3, 0.00, 4297.90, -4297.90],
            ["Crown Fish Bar", "2026-01-13", 3, 1100.00, 0.00, 1100.00],
            ["Crown Fish Bar", "2026-01-14", 3, 1070.00, 0.00, 1070.00],
            ["Crown Fish Bar", "2026-01-15", 3, 1300.00, 0.00, 1300.00],
            ["Crown Fish Bar", "2026-01-16", 3, 1200.00, 0.00, 1200.00],
            ["Crown Fish Bar", "2026-01-17", 3, 1160.00, 0.00, 1160.00],
            ["Crown Fish Bar", "2026-01-18", 3, 720.00, 0.00, 720.00],
            ["Crown Fish Bar", "2026-01-19", 4, 980.00, 4232.80, -3252.80],
            ["Crown Fish Bar", "2026-01-20", 4, 1430.00, 0.00, 1430.00],
            ["Crown Fish Bar", "2026-01-21", 4, 1000.00, 0.00, 1000.00],
            ["Crown Fish Bar", "2026-01-22", 4, 1310.00, 0.00, 1310.00],
            ["Crown Fish Bar", "2026-01-23", 4, 1540.00, 0.00, 1540.00],
            ["Crown Fish Bar", "2026-01-24", 4, 1390.00, 0.00, 1390.00],
            ["Crown Fish Bar", "2026-01-25", 4, 760.00, 0.00, 760.00],
            ["Crown Fish Bar", "2026-01-26", 5, 1006.00, 4291.20, -3285.20],
            ["Crown Fish Bar", "2026-01-27", 5, 1106.00, 0.00, 1106.00],
            ["Crown Fish Bar", "2026-01-28", 5, 840.00, 0.00, 840.00],
            ["Crown Fish Bar", "2026-01-29", 5, 860.00, 0.00, 860.00],
            ["Crown Fish Bar", "2026-01-30", 5, 1690.00, 0.00, 1690.00],
            ["Crown Fish Bar", "2026-01-31", 5, 896.00, 0.00, 896.00],
            ["Crown Fish Bar", "2026-02-01", 5, 880.00, 0.00, 880.00],
            ["Crown Fish Bar", "2026-02-02", 6, 1110.00, 4383.10, -3273.10],
            ["Crown Fish Bar", "2026-02-03", 6, 996.00, 0.00, 996.00],
            ["Crown Fish Bar", "2026-02-04", 6, 1210.00, 0.00, 1210.00],
            ["Crown Fish Bar", "2026-02-05", 6, 1330.00, 0.00, 1330.00],
            ["Crown Fish Bar", "2026-02-06", 6, 1430.00, 0.00, 1430.00],
            ["Crown Fish Bar", "2026-02-07", 6, 1370.00, 0.00, 1370.00],
            ["Crown Fish Bar", "2026-02-08", 6, 1080.00, 0.00, 1080.00],
            ["Crown Fish Bar", "2026-02-09", 7, 1220.00, 4307.50, -3087.50],
            ["Crown Fish Bar", "2026-02-10", 7, 1030.00, 0.00, 1030.00],
            ["Crown Fish Bar", "2026-02-11", 7, 960.00, 0.00, 960.00],
            ["Crown Fish Bar", "2026-02-12", 7, 1060.00, 0.00, 1060.00],
            ["Crown Fish Bar", "2026-02-13", 7, 1580.00, 0.00, 1580.00],
            ["Crown Fish Bar", "2026-02-14", 7, 1250.00, 0.00, 1250.00],
            ["Crown Fish Bar", "2026-02-15", 7, 800.00, 0.00, 800.00],
            ["Crown Fish Bar", "2026-02-16", 8, 980.00, 4441.90, -3461.90],
            ["Crown Fish Bar", "2026-02-17", 8, 1220.00, 0.00, 1220.00],
            ["Crown Fish Bar", "2026-02-18", 8, 1320.00, 0.00, 1320.00],
            ["Crown Fish Bar", "2026-02-19", 8, 1090.00, 0.00, 1090.00],
            ["Crown Fish Bar", "2026-02-20", 8, 1650.00, 0.00, 1650.00],
            ["Crown Fish Bar", "2026-02-21", 8, 1270.00, 0.00, 1270.00],
            ["Crown Fish Bar", "2026-02-22", 8, 940.00, 0.00, 940.00],
            ["Crown Fish Bar", "2026-02-23", 9, 1936.00, 4213.00, -2277.00],
            ["Crown Fish Bar", "2026-02-24", 9, 1130.00, 0.00, 1130.00],
            ["Crown Fish Bar", "2026-02-25", 9, 960.00, 0.00, 960.00],
            ["Crown Fish Bar", "2026-02-26", 9, 1220.00, 0.00, 1220.00],
            ["Crown Fish Bar", "2026-02-27", 9, 2000.00, 0.00, 2000.00],
            ["Crown Fish Bar", "2026-02-28", 9, 1290.00, 0.00, 1290.00],
            ["Crown Fish Bar", "2026-03-01", 9, 540.00, 0.00, 540.00],
            ["Crown Fish Bar", "2026-03-02", 10, 1150.00, 4060.40, -2910.40],
            ["Crown Fish Bar", "2026-03-03", 10, 1140.00, 0.00, 1140.00],
            ["Crown Fish Bar", "2026-03-04", 10, 868.00, 0.00, 868.00],
            ["Crown Fish Bar", "2026-03-05", 10, 868.00, 0.00, 868.00],
            ["Crown Fish Bar", "2026-03-06", 10, 1640.00, 0.00, 1640.00],
            ["Crown Fish Bar", "2026-03-07", 10, 1506.00, 0.00, 1506.00],
            ["Crown Fish Bar", "2026-03-08", 10, 920.00, 0.00, 920.00],
            ["Crown Fish Bar", "2026-03-09", 11, 1268.00, 3550.94, -2282.94],
            ["Crown Fish Bar", "2026-03-10", 11, 1190.00, 0.00, 1190.00],
            ["Crown Fish Bar", "2026-03-11", 11, 1318.00, 0.00, 1318.00],
            ["Crown Fish Bar", "2025-08-04", 32, 503.00, 3321.99, -2818.99],
            ["Crown Fish Bar", "2025-08-05", 32, 455.00, 0.00, 455.00],
            ["Crown Fish Bar", "2025-08-06", 32, 365.00, 0.00, 365.00],
            ["Crown Fish Bar", "2025-08-07", 32, 601.00, 0.00, 601.00],
            ["Crown Fish Bar", "2025-08-08", 32, 530.00, 0.00, 530.00],
            ["Crown Fish Bar", "2025-08-09", 32, 354.00, 0.00, 354.00],
            ["Crown Fish Bar", "2025-08-10", 32, 0.00, 0.00, 0.00],
            ["Crown Fish Bar", "2025-08-11", 33, 465.00, 2866.50, -2401.50],
        ]
        pnl_df = pd.DataFrame(raw_pnl_data, columns=["branch_name", "sales_date", "week_number", "gross_revenue", "total_expenses", "net_profit"])
        pnl_df["sales_date"] = pd.to_datetime(pnl_df["sales_date"])
        pnl_df = pnl_df.sort_values("sales_date")

        # Metrics Calculations
        today_expense = pnl_df.iloc[-1]["total_expenses"]
        lifetime_expense = pnl_df["total_expenses"].sum()
        lifetime_profit = pnl_df["net_profit"].sum()
        lifetime_profit_avg = pnl_df["net_profit"].mean()
        
        # Last Week Profit
        last_week_num = pnl_df["week_number"].iloc[-1]
        last_week_profit = pnl_df[pnl_df["week_number"] == last_week_num]["net_profit"].sum()
        
        # Last Month Profit
        last_month = pnl_df["sales_date"].iloc[-1].month
        last_year = pnl_df["sales_date"].iloc[-1].year
        last_month_profit = pnl_df[(pnl_df["sales_date"].dt.month == last_month) & (pnl_df["sales_date"].dt.year == last_year)]["net_profit"].sum()

        # Dashboard Logic
        branches = [{
            "branch_name": "Crown Fish Bar",
            "last_entry_date": pnl_df["sales_date"].iloc[-1].strftime("%Y-%m-%d"),
            "today_sales": pnl_df["gross_revenue"].iloc[-1],
            "today_expense": today_expense,
            "lifetime_expense": lifetime_expense,
            "lifetime_profit": lifetime_profit,
            "last_week_profit": last_week_profit,
            "last_month_profit": last_month_profit,
            "lifetime_profit_avg": lifetime_profit_avg
        }]

        for branch in branches:
            st.subheader(branch["branch_name"])
            st.write(f"Last Entry Date: {branch['last_entry_date']}")
            
            # Currency Formatting Utility (BBB,MMM,TTT.HHH)
            def format_currency(value):
                return f"£{value:,.2f}"

            # Row 1: Sales & Expenses
            lifetime_sales = pnl_df["gross_revenue"].sum()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["today_sales"])}</h3><h6 style="font-weight:normal;">Today Sales</h6></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["today_expense"])}</h3><h6 style="font-weight:normal;">Today Expense</h6></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["lifetime_expense"])}</h3><h6 style="font-weight:normal;">Lifetime Expense</h6></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(lifetime_sales)}</h3><h6 style="font-weight:normal;">Lifetime Sales</h6></div>', unsafe_allow_html=True)

            # Row 2: Sales Trends (Averages)
            st.write("")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="metric-tile"><div style="display:flex;justify-content:space-between;"><h3>{format_currency(1154.09)}</h3><h4 style="color:green;">14.20%</h4></div><h6 style="font-weight:normal;">Lifetime Daily Avg</h6></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-tile"><div style="display:flex;justify-content:space-between;"><h3>{format_currency(1244.29)}</h3><h4 style="color:green;">5.92%</h4></div><h6 style="font-weight:normal;">Weekly Rolling Avg</h6></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-tile"><div style="display:flex;justify-content:space-between;"><h3>{format_currency(1203.13)}</h3><h4 style="color:green;">9.55%</h4></div><h6 style="font-weight:normal;">Monthly Rolling Avg</h6></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-tile"><div style="display:flex;justify-content:space-between;"><h3>{format_currency(1212.41)}</h3><h4 style="color:green;">8.71%</h4></div><h6 style="font-weight:normal;">Typical Day Type Avg</h6></div>', unsafe_allow_html=True)

            # Row 3: Profit Metrics
            st.write("")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["lifetime_profit_avg"])}</h3><h6 style="font-weight:normal;">Lifetime Profit Avg</h6></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["last_week_profit"])}</h3><h6 style="font-weight:normal;">Profit Last Week</h6></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["last_month_profit"])}</h3><h6 style="font-weight:normal;">Profit Last Month</h6></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-tile"><h3>{format_currency(branch["lifetime_profit"])}</h3><h6 style="font-weight:normal;">Lifetime Profit</h6></div>', unsafe_allow_html=True)

            st.divider()
            
            # Profit vs Expense Chart
            fig_pnl = px.line(
                pnl_df,
                x="sales_date",
                y=["gross_revenue", "net_profit"],
                title="Gross Revenue vs. Net Profit Trend",
                labels={"value": "Amount (£)", "sales_date": "Date"},
                color_discrete_map={"gross_revenue": "#3498db", "net_profit": "#2ecc71"}
            )
            fig_pnl.update_layout(margin=dict(t=60, b=100, l=40, r=40), legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5), legend_title_text="")
            st.plotly_chart(fig_pnl, use_container_width=True)

    with tab_monthly:
        # --- Timeline Stacked Bar Chart ---
        # Static sales data
        sales_data = [
            # sales_year, sales_month, month_name, branch_id, branch_name, channel_name, provider_name, monthly_sales
            [2025,8,"August",3,"Crown Fish Bar","Deliveroo","Deliveroo",1093.00],
            [2025,9,"September",3,"Crown Fish Bar","Deliveroo","Deliveroo",1928.00],
            [2025,10,"October",3,"Crown Fish Bar","Deliveroo","Deliveroo",2680.00],
            [2025,11,"November",3,"Crown Fish Bar","Deliveroo","Deliveroo",2332.00],
            [2025,12,"December",3,"Crown Fish Bar","Deliveroo","Deliveroo",3366.00],
            [2026,1,"January",3,"Crown Fish Bar","Deliveroo","Deliveroo",1790.00],
            [2026,2,"February",3,"Crown Fish Bar","Deliveroo","Deliveroo",2290.00],
            [2026,3,"March",3,"Crown Fish Bar","Deliveroo","Deliveroo",782.00],
            [2025,8,"August",3,"Crown Fish Bar","JustEat","Just Eat",3259.00],
            [2025,9,"September",3,"Crown Fish Bar","JustEat","Just Eat",7556.00],
            [2025,10,"October",3,"Crown Fish Bar","JustEat","Just Eat",11190.00],
            [2025,11,"November",3,"Crown Fish Bar","JustEat","Just Eat",11920.00],
            [2025,12,"December",3,"Crown Fish Bar","JustEat","Just Eat",11830.00],
            [2026,1,"January",3,"Crown Fish Bar","JustEat","Just Eat",10830.00],
            [2026,2,"February",3,"Crown Fish Bar","JustEat","Just Eat",10750.00],
            [2026,3,"March",3,"Crown Fish Bar","JustEat","Just Eat",4552.00],
            [2025,8,"August",3,"Crown Fish Bar","Own","Own",14045.00],
            [2025,9,"September",3,"Crown Fish Bar","Own","Own",19740.00],
            [2025,10,"October",3,"Crown Fish Bar","Own","Own",19570.00],
            [2025,11,"November",3,"Crown Fish Bar","Own","Own",17160.00],
            [2025,12,"December",3,"Crown Fish Bar","Own","Own",15470.00],
            [2025,12,"December",3,"Crown Fish Bar","Own","Own",15470.00],
            [2026,1,"January",3,"Crown Fish Bar","Own","Own",15566.00],
            [2026,2,"February",3,"Crown Fish Bar","Own","Own",14912.00],
            [2026,3,"March",3,"Crown Fish Bar","Own","Own",5860.00],
            [2025,8,"August",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2025,9,"September",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2025,10,"October",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2025,11,"November",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2025,12,"December",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2026,1,"January",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2026,2,"February",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2026,3,"March",3,"Crown Fish Bar","Telephone","Telephone",0.00],
            [2025,8,"August",3,"Crown Fish Bar","Uber","Uber",1896.00],
            [2025,9,"September",3,"Crown Fish Bar","Uber","Uber",4238.00],
            [2025,10,"October",3,"Crown Fish Bar","Uber","Uber",5170.00],
            [2025,11,"November",3,"Crown Fish Bar","Uber","Uber",7520.00],
            [2025,12,"December",3,"Crown Fish Bar","Uber","Uber",7270.00],
            [2026,1,"January",3,"Crown Fish Bar","Uber","Uber",6940.00],
            [2026,2,"February",3,"Crown Fish Bar","Uber","Uber",6360.00],
            [2026,3,"March",3,"Crown Fish Bar","Uber","Uber",1214.00],
            [2025,8,"August",3,"Crown Fish Bar","Web","Web",0.00],
            [2025,9,"September",3,"Crown Fish Bar","Web","Web",314.00],
            [2025,10,"October",3,"Crown Fish Bar","Web","Web",1052.00],
            [2025,11,"November",3,"Crown Fish Bar","Web","Web",620.00],
            [2025,12,"December",3,"Crown Fish Bar","Web","Web",728.00],
            [2026,1,"January",3,"Crown Fish Bar","Web","Web",106.00],
            [2026,2,"February",3,"Crown Fish Bar","Web","Web",0.00],
            [2026,3,"March",3,"Crown Fish Bar","Web","Web",0.00],
        ]
        sales_df = pd.DataFrame(sales_data, columns=[
            "sales_year", "sales_month", "month_name", "branch_id", "branch_name", "channel_name", "provider_name", "monthly_sales"
        ])

        # Create a month label for x-axis
        sales_df["month_label"] = sales_df["sales_year"].astype(str) + "-" + sales_df["sales_month"].astype(str).str.zfill(2)

        # Define color map for channels
        color_map = {
            "Deliveroo": "#1f77b4",
            "JustEat": "#ff7f0e",
            "Own": "#2ca02c",
            "Telephone": "#d62728",
            "Uber": "#9467bd",
            "Web": "#8c564b"
        }

        # Chart Filters
        all_channels = sales_df["channel_name"].unique().tolist()
        all_months = sorted(sales_df["month_label"].unique().tolist())
        
        st.subheader("Chart Filters")
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            selected_months = st.multiselect(
                "Select Months to Display:",
                options=all_months,
                default=all_months,
                key="months"
            )
        with col_filter2:
            selected_channels = st.multiselect(
                "Select Channels (Sales Only):",
                options=all_channels,
                default=all_channels,
                key="channels"
            )
        
        # --- Expense Filter Prep ---
        # We define these here so the filter can see them
        expense_category_names = ["COS", "COL", "Admin_Exp", "Marketing_Ads", "Channel_Commissions"]
        
        with col_filter3:
            selected_expense_types = st.multiselect(
                "Select Expense Categories:",
                options=expense_category_names,
                default=expense_category_names,
                key="expense_types"
            )

        # Filter data
        filtered_df = sales_df[
            (sales_df["channel_name"].isin(selected_channels)) &
            (sales_df["month_label"].isin(selected_months))
        ]

        # Pivot for stacked bar
        pivot_df = filtered_df.pivot_table(
            index="month_label",
            columns="channel_name",
            values="monthly_sales",
            aggfunc="sum",
            fill_value=0
        ).reset_index()

        # Sort months
        pivot_df = pivot_df.sort_values("month_label")

        # Plotly stacked bar chart
        fig_bar = px.bar(
            pivot_df,
            x="month_label",
            y=selected_channels,  # Use selected channels for y
            labels={"value": "Sales", "month_label": "Month"},
            title="Monthly Channel-wise Sales (Stacked)",
            barmode="stack",
            color_discrete_map=color_map
        )
        fig_bar.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), legend_title_text="")

        # Pie chart for total sales by channel
        channel_totals = filtered_df.groupby("channel_name")["monthly_sales"].sum().reset_index()
        fig_pie = px.pie(
            channel_totals,
            values="monthly_sales",
            names="channel_name",
            title="Total Sales by Channel",
            color_discrete_map=color_map
        )
        fig_pie.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), legend_title_text="")

        # Display charts side by side
        col1, col2 = st.columns([7, 3])
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- Updated Monthly Expense Data ---
        raw_expense_data = [
            [2026, "March", "Crown Fish Bar", 6500.00, 7000.00, 2875.00, 210.00, 977.34],
            [2026, "February", "Crown Fish Bar", 5200.00, 5600.00, 2300.00, 140.00, 4105.50],
            [2026, "January", "Crown Fish Bar", 5200.00, 5600.00, 2300.00, 391.00, 3855.60],
            [2025, "December", "Crown Fish Bar", 4900.00, 5200.00, 2300.00, 565.00, 4503.87],
            [2025, "November", "Crown Fish Bar", 2600.00, 2800.00, 1150.00, 546.24, 4196.85],
            [2025, "October", "Crown Fish Bar", 4050.00, 4200.00, 1725.00, 702.86, 3616.20],
            [2025, "September", "Crown Fish Bar", 6350.00, 7000.00, 2875.00, 818.10, 3549.42],
            [2025, "August", "Crown Fish Bar", 3800.00, 3360.00, 2300.00, 0.00, 2162.79],
        ]
        
        raw_expense_df = pd.DataFrame(raw_expense_data, columns=[
            "Year", "Month", "Branch", "COS", "COL", "Admin_Exp", "Marketing_Ads", "Channel_Commissions_21pct"
        ])

        expense_category_names = ["COS", "COL", "Admin_Exp", "Marketing_Ads", "Channel_Commissions_21pct"]
        
        # Melt to get Category and Amount per row
        expense_df = pd.melt(
            raw_expense_df,
            id_vars=["Year", "Month", "Branch"],
            value_vars=expense_category_names,
            var_name="category",
            value_name="amount"
        )
        
        # Map Month names to numbers for label sorting consistency
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        expense_df["month_num"] = expense_df["Month"].map(month_map)
        expense_df["month_label"] = expense_df["Year"].astype(str) + "-" + expense_df["month_num"].astype(str).str.zfill(2)
        
        # Group by month_label and category
        monthly_expense_df = expense_df.groupby(["month_label", "category"])["amount"].sum().reset_index()
        
        # Filter expenses by selected months AND selected expense categories
        filtered_expense_df = monthly_expense_df[
            (monthly_expense_df["month_label"].isin(selected_months)) &
            (monthly_expense_df["category"].isin(selected_expense_types))
        ]

        st.divider()
        st.subheader("Monthly Expense Analysis")

        # 1. Stacked Bar Chart for Expenses
        expense_categories = filtered_expense_df["category"].unique().tolist()
        pivot_expense_df = filtered_expense_df.pivot_table(
            index="month_label",
            columns="category",
            values="amount",
            aggfunc="sum",
            fill_value=0
        ).reset_index()

        fig_expense_bar = px.bar(
            pivot_expense_df,
            x="month_label",
            y=expense_categories,
            labels={"value": "Amount (£)", "month_label": "Month"},
            title="Monthly Expenses (Stacked)",
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_expense_bar.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), legend_title_text="")

        # 2. Pie Chart for Expense Split
        expense_totals = filtered_expense_df.groupby("category")["amount"].sum().reset_index()
        fig_expense_pie = px.pie(
            expense_totals,
            values="amount",
            names="category",
            title="Total Expense Split",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_expense_pie.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), legend_title_text="")

        # Display expense charts side by side
        col_exp1, col_exp2 = st.columns([7, 3])
        with col_exp1:
            st.plotly_chart(fig_expense_bar, use_container_width=True)
        with col_exp2:
            st.plotly_chart(fig_expense_pie, use_container_width=True)


    with tab_weekly:
        st.divider()

        weekly_data_raw = [
            # 2026 Weekday
            ["2026 Week 14", "Weekday", 1300.00, 0.00], # Note: User provided 1300 for 14, 13, 12 in the tabular data earlier, but this specific request has 3776 for 11 etc. I will stick to the latest requested list.
            ["2026 Week 11", "Weekday", 3776.00, -33.36],
            ["2026 Week 10", "Weekday", 5666.00, -21.81],
            ["2026 Week 09", "Weekday", 7246.00, 15.75],
            ["2026 Week 08", "Weekday", 6260.00, 7.01],
            ["2026 Week 07", "Weekday", 5850.00, -3.72],
            ["2026 Week 06", "Weekday", 6076.00, 10.43],
            ["2026 Week 05", "Weekday", 5502.00, -12.11],
            ["2026 Week 04", "Weekday", 6260.00, 34.05],
            ["2026 Week 03", "Weekday", 4670.00, -28.81],
            ["2026 Week 02", "Weekday", 6560.00, 109.58],
            ["2026 Week 01", "Weekday", 3130.00, -26.70],
            # 2025 Weekday
            ["2025 Week 53", "Weekday", 4270.00, -1.29],
            ["2025 Week 52", "Weekday", 4326.00, -30.47],
            ["2025 Week 51", "Weekday", 6222.00, -1.08],
            ["2025 Week 50", "Weekday", 6290.00, -16.13],
            ["2025 Week 49", "Weekday", 7500.00, 12.28],
            ["2025 Week 48", "Weekday", 6680.00, 0.30],
            ["2025 Week 47", "Weekday", 6660.00, -5.40],
            ["2025 Week 46", "Weekday", 7040.00, 1.44],
            ["2025 Week 45", "Weekday", 6940.00, 3.89],
            ["2025 Week 44", "Weekday", 6680.00, 14.38],
            ["2025 Week 43", "Weekday", 5840.00, -18.09],
            ["2025 Week 42", "Weekday", 7130.00, 0.82],
            ["2025 Week 41", "Weekday", 7072.00, -3.39],
            ["2025 Week 40", "Weekday", 7320.00, 7.05],
            ["2025 Week 39", "Weekday", 6838.00, 7.18],
            ["2025 Week 38", "Weekday", 6380.00, 7.92],
            ["2025 Week 37", "Weekday", 5912.00, 30.91],
            ["2025 Week 36", "Weekday", 4516.00, -20.32],
            ["2025 Week 35", "Weekday", 5668.00, 19.78],
            ["2025 Week 34", "Weekday", 4732.00, 15.56],
            ["2025 Week 33", "Weekday", 4095.00, 66.87],
            ["2025 Week 32", "Weekday", 2454.00, None],
            # 2026 Weekend
            ["2026 Week 10", "Weekend", 2426.00, 32.57],
            ["2026 Week 09", "Weekend", 1830.00, -17.19],
            ["2026 Week 08", "Weekend", 2210.00, 7.80],
            ["2026 Week 07", "Weekend", 2050.00, -16.33],
            ["2026 Week 06", "Weekend", 2450.00, 37.95],
            ["2026 Week 05", "Weekend", 1776.00, -17.40],
            ["2026 Week 04", "Weekend", 2150.00, 14.36],
            ["2026 Week 03", "Weekend", 1880.00, -7.21],
            ["2026 Week 02", "Weekend", 2026.00, -6.12],
            ["2026 Week 01", "Weekend", 2158.00, -14.70],
            # 2025 Weekend
            ["2025 Week 52", "Weekend", 2530.00, -2.01],
            ["2025 Week 51", "Weekend", 2582.00, 7.49],
            ["2025 Week 50", "Weekend", 2402.00, -5.51],
            ["2025 Week 49", "Weekend", 2542.00, -12.95],
            ["2025 Week 48", "Weekend", 2920.00, 24.68],
            ["2025 Week 47", "Weekend", 2342.00, 7.43],
            ["2025 Week 46", "Weekend", 2180.00, -18.35],
            ["2025 Week 45", "Weekend", 2670.00, 25.94],
            ["2025 Week 44", "Weekend", 2120.00, -20.30],
            ["2025 Week 43", "Weekend", 2660.00, 35.71],
            ["2025 Week 42", "Weekend", 1960.00, 7.10],
            ["2025 Week 41", "Weekend", 1830.00, 2.23],
            ["2025 Week 40", "Weekend", 1790.00, -23.50],
            ["2025 Week 39", "Weekend", 2340.00, 5.88],
            ["2025 Week 38", "Weekend", 2210.00, 7.80],
            ["2025 Week 37", "Weekend", 2050.00, 125.27],
            ["2025 Week 36", "Weekend", 910.00, -23.53],
            ["2025 Week 35", "Weekend", 1190.00, 48.75],
            ["2025 Week 34", "Weekend", 800.00, -20.00],
            ["2025 Week 33", "Weekend", 1000.00, 182.49],
            ["2025 Week 32", "Weekend", 354.00, None]
        ]

        weekly_df = pd.DataFrame(weekly_data_raw, columns=["week_timeline", "day_label", "segment_total", "wow_segment_growth_pct"])

        # Explicitly calculate numeric Year and Week for absolute chronological sorting
        weekly_df["year"] = weekly_df["week_timeline"].str[:4].astype(int)
        weekly_df["week"] = weekly_df["week_timeline"].str[-2:].astype(int)

        # Order by year, then week
        weekly_df = weekly_df.sort_values(by=["year", "week"])
        
        # Timeline Filter
        unique_weeks = weekly_df["week_timeline"].drop_duplicates().tolist()
        if len(unique_weeks) > 0:
            start_week, end_week = st.select_slider(
                "Select Timeline Range:",
                options=unique_weeks,
                value=(unique_weeks[0], unique_weeks[-1])
            )
            
            # Helper to get the Start Date for a specific 'YYYY Week XX' string
            # We look it up from the raw_weekly_expense_data which contains the mapping
            def get_week_start_date(week_str):
                y = int(week_str[:4])
                w = int(week_str[-2:])
                # Search in raw_weekly_expense_data (Year=idx0, WK=idx1, Date=idx2)
                for row in [
                    [2026, 14, "2026-03-30"], [2026, 13, "2026-03-23"], [2026, 12, "2026-03-16"],
                    [2026, 11, "2026-03-09"], [2026, 10, "2026-03-02"], [2026, 9, "2026-02-23"],
                    [2026, 8, "2026-02-16"], [2026, 7, "2026-02-09"], [2026, 6, "2026-02-02"],
                    [2026, 5, "2026-01-26"], [2026, 4, "2026-01-19"], [2026, 3, "2026-01-12"],
                    [2026, 2, "2026-01-05"], [2026, 1, "2026-01-01"], [2025, 52, "2025-12-22"],
                    [2025, 51, "2025-12-15"], [2025, 50, "2025-12-08"], [2025, 49, "2025-12-01"],
                    [2025, 48, "2025-11-24"], [2025, 47, "2025-11-17"], [2025, 46, "2025-11-10"],
                    [2025, 45, "2025-11-03"], [2025, 44, "2025-10-27"], [2025, 43, "2025-10-20"],
                    [2025, 42, "2025-10-13"], [2025, 41, "2025-10-06"], [2025, 40, "2025-09-29"],
                    [2025, 39, "2025-09-22"], [2025, 38, "2025-09-15"], [2025, 37, "2025-09-08"],
                    [2025, 36, "2025-09-01"], [2025, 35, "2025-08-25"], [2025, 34, "2025-08-18"],
                    [2025, 33, "2025-08-11"], [2025, 32, "2025-08-04"], [2025, 1, "2025-12-29"]
                ]:
                    if row[0] == y and row[1] == w:
                        return row[2]
                return "N/A"

            sel_start_date = get_week_start_date(start_week)
            sel_end_date = get_week_start_date(end_week)
            
            st.info(f"📅 **Selected Range:** {sel_start_date} (Start of {start_week}) to {sel_end_date} (Start of {end_week})")

            start_idx = unique_weeks.index(start_week)
            end_idx = unique_weeks.index(end_week)
            valid_weeks = unique_weeks[start_idx:end_idx+1]
            
            # Filter the dataframe for the selected range
            weekly_df = weekly_df[weekly_df["week_timeline"].isin(valid_weeks)]

        # Update category orders in the plotly figures just in case Plotly tries to resort them
        category_order = weekly_df["week_timeline"].unique().tolist()
        
        # --- Weekly Expense Data ---
        raw_weekly_expense_data = [
            [2026, 14, "2026-03-30", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 42.00, 0.00],
            [2026, 13, "2026-03-23", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 42.00, 0.00],
            [2026, 12, "2026-03-16", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 42.00, 0.00],
            [2026, 11, "2026-03-09", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 42.00, 233.94],
            [2026, 10, "2026-03-02", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 42.00, 743.40],
            [2026, 9, "2026-02-23", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 35.00, 903.00],
            [2026, 8, "2026-02-16", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 35.00, 1131.90],
            [2026, 7, "2026-02-09", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 35.00, 997.50],
            [2026, 6, "2026-02-02", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 35.00, 1073.10],
            [2026, 5, "2026-01-26", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 88.00, 928.20],
            [2026, 4, "2026-01-19", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 101.00, 856.80],
            [2026, 3, "2026-01-12", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 101.00, 921.90],
            [2026, 2, "2026-01-05", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 101.00, 884.10],
            [2026, 1, "2026-01-01", "Crown Fish Bar", 0.00, 0.00, 0.00, 0.00, 264.60],
            [2025, 52, "2025-12-22", "Crown Fish Bar", 1000.00, 1000.00, 575.00, 276.00, 923.16],
            [2025, 51, "2025-12-15", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 103.00, 1167.39],
            [2025, 50, "2025-12-08", "Crown Fish Bar", 0.00, 0.00, 0.00, 0.00, 990.57],
            [2025, 49, "2025-12-01", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 120.00, 908.25],
            [2025, 48, "2025-11-24", "Crown Fish Bar", 0.00, 0.00, 0.00, 0.00, 1073.73],
            [2025, 47, "2025-11-17", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 240.62, 1079.82],
            [2025, 46, "2025-11-10", "Crown Fish Bar", 0.00, 0.00, 0.00, 0.00, 995.40],
            [2025, 45, "2025-11-03", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 305.62, 1047.90],
            [2025, 44, "2025-10-27", "Crown Fish Bar", 0.00, 0.00, 0.00, 0.00, 961.80],
            [2025, 43, "2025-10-20", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 374.62, 1029.00],
            [2025, 42, "2025-10-13", "Crown Fish Bar", 1450.00, 1400.00, 575.00, 193.62, 793.80],
            [2025, 41, "2025-10-06", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 134.62, 831.60],
            [2025, 40, "2025-09-29", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 134.62, 928.20],
            [2025, 39, "2025-09-22", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 234.62, 799.68],
            [2025, 38, "2025-09-15", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 134.62, 739.20],
            [2025, 37, "2025-09-08", "Crown Fish Bar", 1250.00, 1400.00, 575.00, 174.62, 698.88],
            [2025, 36, "2025-09-01", "Crown Fish Bar", 1200.00, 1400.00, 575.00, 139.62, 383.46],
            [2025, 35, "2025-08-25", "Crown Fish Bar", 1000.00, 840.00, 575.00, 0.00, 528.78],
            [2025, 34, "2025-08-18", "Crown Fish Bar", 800.00, 840.00, 575.00, 0.00, 275.52],
            [2025, 33, "2025-08-11", "Crown Fish Bar", 1000.00, 840.00, 575.00, 0.00, 451.50],
            [2025, 32, "2025-08-04", "Crown Fish Bar", 1000.00, 840.00, 575.00, 0.00, 906.99],
            [2025, 1, "2025-12-29", "Crown Fish Bar", 1300.00, 1400.00, 575.00, 66.00, 514.50],
        ]
        
        raw_weekly_expense_df = pd.DataFrame(raw_weekly_expense_data, columns=[
            "Year", "WK", "Week_Start", "Branch", 
            "COS", "COL", "Admin_Exp", "Marketing_Ads", "Channel_Commissions"
        ])

        # Add Filter for Weekly Expense categories
        weekly_exp_categories = ["COS", "COL", "Admin_Exp", "Marketing_Ads", "Channel_Commissions"]
        selected_weekly_exp_types = st.multiselect(
            "Select Weekly Expense Categories:",
            options=weekly_exp_categories,
            default=weekly_exp_categories,
            key="weekly_expense_types"
        )
        
        # Melt and process
        weekly_expense_df = pd.melt(
            raw_weekly_expense_df,
            id_vars=["Year", "WK", "Week_Start", "Branch"],
            value_vars=weekly_exp_categories,
            var_name="category",
            value_name="amount"
        )
        
        # Filter by selected timeline AND categories
        # Week_Start in expense data should correspond roughly to the slider's 'YYYY Week XX' format
        # For simplicity, we'll extract matching weeks or just show based on categories if date filtering is complex
        # But we can try to match them:
        weekly_expense_df["week_match"] = weekly_expense_df["Year"].astype(str) + " Week " + weekly_expense_df["WK"].astype(str).str.zfill(2)
        
        filtered_weekly_exp_df = weekly_expense_df[
            (weekly_expense_df["week_match"].isin(valid_weeks)) &
            (weekly_expense_df["category"].isin(selected_weekly_exp_types))
        ]

        # 1. Weekly Expense Bar Chart
        pivot_weekly_exp = filtered_weekly_exp_df.pivot_table(
            index="week_match",
            columns="category",
            values="amount",
            aggfunc="sum",
            fill_value=0
        ).reset_index()

        fig_weekly_exp_bar = px.bar(
            pivot_weekly_exp,
            x="week_match",
            y=selected_weekly_exp_types,
            labels={"value": "Amount (£)", "week_match": "Week"},
            title="Weekly Expenses (Stacked)",
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_weekly_exp_bar.update_layout(
            margin=dict(t=60, b=100, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5), 
            legend_title_text="",
            xaxis=dict(categoryorder='array', categoryarray=category_order)
        )

        # 2. Weekly Expense Pie Chart
        weekly_exp_totals = filtered_weekly_exp_df.groupby("category")["amount"].sum().reset_index()
        fig_weekly_exp_pie = px.pie(
            weekly_exp_totals,
            values="amount",
            names="category",
            title="Total Weekly Expense Split",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_weekly_exp_pie.update_layout(
            margin=dict(t=60, b=100, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5), 
            legend_title_text=""
        )

        # Line chart for segment total
        fig_weekly_sales = px.line(
            weekly_df,
            x="week_timeline",
            y="segment_total",
            color="day_label",
            markers=True,
            title="Weekly Sales Trend (Segment Total)",
            labels={"segment_total": "Total Sales", "week_timeline": "Week"},
            color_discrete_map={"Weekday": "#1f77b4", "Weekend": "#ff7f0e"}
        )
        fig_weekly_sales.update_layout(
            margin=dict(t=60, b=100, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5), 
            legend_title_text="",
            xaxis=dict(categoryorder='array', categoryarray=category_order)
        )

        # Stacked bar chart for segment total
        fig_weekly_stacked = px.bar(
            weekly_df,
            x="week_timeline",
            y="segment_total",
            color="day_label",
            barmode="stack",
            title="Weekly Sales Composition (Stacked)",
            labels={"segment_total": "Total Sales", "week_timeline": "Week"},
            color_discrete_map={"Weekday": "#1f77b4", "Weekend": "#ff7f0e"}
        )
        fig_weekly_stacked.update_layout(
            margin=dict(t=60, b=100, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5), 
            legend_title_text="",
            xaxis=dict(categoryorder='array', categoryarray=category_order)
        )

        # Bar chart for wow growth
        # We can calculate a color column for positive/negative growth
        weekly_df["growth_color"] = weekly_df["wow_segment_growth_pct"].apply(lambda x: "Growth" if x >= 0 else "Decline")
        
        fig_wow_growth = px.bar(
            weekly_df,
            x="week_timeline",
            y="wow_segment_growth_pct",
            color="growth_color",
            text=weekly_df["wow_segment_growth_pct"].apply(lambda x: f"{x:.1f}%" if x is not None else ""),
            barmode="group",
            title="Week-over-Week Segment Growth (%)",
            labels={"wow_segment_growth_pct": "Growth (%)", "week_timeline": "Week", "growth_color": "Status"},
            color_discrete_map={"Growth": "#2ecc71", "Decline": "#e74c3c"}
        )
        fig_wow_growth.update_traces(textposition='outside')
        fig_wow_growth.update_layout(
            margin=dict(t=60, b=100, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5), 
            legend_title_text="",
            xaxis=dict(categoryorder='array', categoryarray=category_order),
            uniformtext_minsize=8, 
            uniformtext_mode='hide'
        )

        with st.container():
            st.plotly_chart(fig_weekly_sales, use_container_width=True)
            st.plotly_chart(fig_weekly_stacked, use_container_width=True)
            st.plotly_chart(fig_wow_growth, use_container_width=True)
        
        st.divider()
        st.subheader("Weekly Expense Analysis")
        col_exp_w1, col_exp_w2 = st.columns([7, 3])
        with col_exp_w1:
            st.plotly_chart(fig_weekly_exp_bar, use_container_width=True)
        with col_exp_w2:
            st.plotly_chart(fig_weekly_exp_pie, use_container_width=True)

        # --- Sales vs Expenses Comparison ---
        # Aggregate Sales by week
        sales_agg = weekly_df.groupby("week_timeline")["segment_total"].sum().reset_index()
        sales_agg.columns = ["week", "Total Sales"]
        
        # Aggregate Expenses by week
        exp_agg = filtered_weekly_exp_df.groupby("week_match")["amount"].sum().reset_index()
        exp_agg.columns = ["week", "Total Expenses"]
        
        # Merge
        comparison_df = pd.merge(sales_agg, exp_agg, on="week", how="outer").fillna(0)
        comparison_df = comparison_df.sort_values("week")
        
        # Melt for plotting
        vs_df = comparison_df.melt(id_vars="week", value_vars=["Total Sales", "Total Expenses"], var_name="Type", value_name="Amount")
        
        fig_vs = px.line(
            vs_df,
            x="week",
            y="Amount",
            color="Type",
            markers=True,
            title="Weekly Sales vs. Total Expenses",
            labels={"Amount": "Amount (£)", "week": "Week"},
            color_discrete_map={"Total Sales": "#2ecc71", "Total Expenses": "#e74c3c"}
        )
        fig_vs.update_layout(
            margin=dict(t=60, b=100, l=40, r=40),
            legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5),
            legend_title_text=""
        )
        
        st.divider()
        st.subheader("Sales vs. Expenses Comparison")
        st.plotly_chart(fig_vs, use_container_width=True)
        
        # Optional: Display dataframe table
        with st.expander("View Weekly Data"):
            # Display the table, dropping the synthetic year/week fields to keep it clean
            display_df = weekly_df.sort_values(by=["year", "week"], ascending=[False, False])
            display_df = display_df.drop(columns=["year", "week"])
            st.dataframe(display_df, use_container_width=True, hide_index=True)


    with tab_upload:
        st.header("Upload Data")
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

        st.header("Insert Sales Data")
        with st.form("sales_data_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                sales_date = st.date_input("Sales Date")
                year = st.number_input("Year", min_value=1900, max_value=2100, value=2026)
                week = st.number_input("Week", min_value=1, max_value=53)
                day_name = st.selectbox("Day Name", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                own_card = st.number_input("Own Card", min_value=0.0)
                own_cash = st.number_input("Own Cash", min_value=0.0)
            with col2:
                telephone_card = st.number_input("Telephone Card", min_value=0.0)
                web_card = st.number_input("Web Card", min_value=0.0)
                je_card = st.number_input("JE Card", min_value=0.0)
                je_cash = st.number_input("JE Cash", min_value=0.0)
                deliveroo_card = st.number_input("Deliveroo Card", min_value=0.0)
                uber_card = st.number_input("Uber Card", min_value=0.0)
            
            total_sales = st.number_input("Total Sales", min_value=0.0)
            submitted = st.form_submit_button("Submit Data")
            
            if submitted:
                st.success("Data submitted successfully!")
                st.json({
                    "sales_date": str(sales_date),
                    "total_sales": total_sales,
                    "user": st.session_state.get("username")
                })

    with tab_accounts:
        st.subheader("Chart of Accounts")
        st.write("This tab displays the system Chart of Accounts across Revenue and Expense categories.")
        
        accounts_data = [
            ["Revenue", 1, "Own", "Income from sales"],
            ["Revenue", 2, "Own", "Income from sales"],
            ["Revenue", 3, "Telephone", "Income from sales"],
            ["Revenue", 4, "Web", "Income from sales"],
            ["Revenue", 5, "JustEat", "Income from sales"],
            ["Revenue", 6, "JustEat", "Income from sales"],
            ["Revenue", 7, "Deliveroo", "Income from sales"],
            ["Revenue", 8, "Uber", "Income from sales"],
            ["Direct Expense", 101, "Cost of Sales", "COS"],
            ["Direct Expense", 102, "Cost of Labour", "COL"],
            ["Operating Expense", 103, "Admin Exp", "Admin"],
            ["Operating Expense", 104, "AD - Deliveroo", "Marketing"],
            ["Operating Expense", 105, "AD - Uber", "Marketing"],
            ["Operating Expense", 106, "AD - JE", "Marketing"],
            ["Operating Expense", 107, "AD - Google", "Marketing"],
            ["Operating Expense", 108, "AD - Fb/Tiktok", "Marketing"],
            ["Direct Expense", 109, "Sale - Deliveroo", "Sale"],
            ["Direct Expense", 110, "Sale - Uber", "Sale"],
            ["Direct Expense", 111, "Sale - JE", "Sale"],
        ]
        
        accounts_df = pd.DataFrame(accounts_data, columns=["Account_Type", "Account_Code", "Account_Name", "Description"])
        st.dataframe(accounts_df, use_container_width=True, hide_index=True)

        # --- GL Report (Consolidated) ---
        st.divider()
        st.subheader("General Ledger (GL) Report")
        
        gl_file_path = "Crown_GL_Report.csv"
        
        col_gl1, col_gl2 = st.columns([2, 1])
        with col_gl1:
            st.info(f"Upload a new GL CSV export, or the system will automatically read from:\n`{gl_file_path}`")
        with col_gl2:
            uploaded_gl = st.file_uploader("Upload GL Data", type=["csv", "tsv", "txt"], label_visibility="collapsed")
            
        gl_df = None
        
        if uploaded_gl is not None:
            try:
                gl_df = pd.read_csv(uploaded_gl, sep=None, engine="python")
            except Exception as e:
                st.error(f"Failed to read uploaded file: {e}")
        elif os.path.exists(gl_file_path):
            try:
                gl_df = pd.read_csv(gl_file_path, sep=None, engine="python")
            except Exception as e:
                st.error(f"Failed to read local file '{gl_file_path}': {e}")
                
        if gl_df is not None and not gl_df.empty:
            if "Transaction_Date" in gl_df.columns:
                gl_df["Transaction_Date"] = pd.to_datetime(gl_df["Transaction_Date"]).dt.date
            
            # Filters
            st.write("### Filters")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                start_date = st.date_input("Start Date", value=gl_df["Transaction_Date"].min() if "Transaction_Date" in gl_df.columns else pd.to_datetime("today"))
            with col_f2:
                end_date = st.date_input(
                    "End Date", 
                    value=gl_df["Transaction_Date"].max() if "Transaction_Date" in gl_df.columns else pd.to_datetime("today")
                )
            
            filtered_gl = gl_df
            if "Transaction_Date" in gl_df.columns:
                filtered_gl = gl_df[
                    (gl_df["Transaction_Date"] >= start_date) & 
                    (gl_df["Transaction_Date"] <= end_date)
                ]
            
            st.dataframe(
                filtered_gl, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Credit": st.column_config.NumberColumn(format="£%,.2f"),
                    "Debit": st.column_config.NumberColumn(format="£%,.2f")
                }
            )
        else:
            st.warning("No GL Data available. Please upload a structured file to view transactions.")

# --- GLOBAL FOOTER ---
st.markdown("""
<div class="footer">
    © 2026 TechMAC. All rights reserved.
</div>
""", unsafe_allow_html=True)
