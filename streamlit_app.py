import streamlit as st
import streamlit_authenticator as stauth

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
    authenticator.logout("Logout", "sidebar")

    st.title("TECH MAC - IADA")
    st.write(f"Welcome back, **{st.session_state.get('name')}**!")
    
    st.divider()

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