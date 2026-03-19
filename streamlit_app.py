import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(layout="wide")

# Custom CSS for tiles
st.markdown("""
<style>
.metric-tile {
    border: 2px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 10px;
    margin: 5px auto;
    background-color: white;
    width: 260px;
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
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
    authenticator.logout("Logout", "sidebar")

    st.title("Branch Dashboard")
    st.write(f"Welcome back, **{st.session_state.get('name')}**!")
    
    st.divider()

    # Branch Dashboard Data (Static for now)
    branches = [
        {
            "branch_name": "Crown Fish Bar",
            "last_entry_date": "2026-03-11",
            "today_sales": 1318.00,
            "lifetime_daily_avg": 1154.09,
            "vs_lifetime_avg_pct": 14.20,
            "weekly_rolling_avg": 1244.29,
            "vs_weekly_avg_pct": 5.92,
            "monthly_rolling_avg": 1203.13,
            "vs_monthly_avg_pct": 9.55,
            "typical_day_type_avg": 1212.41,
            "vs_typical_day_avg_pct": 8.71,
            "month_on_month_growth": -5.72,
            "year_on_year_growth": 12.49
        }
    ]

    for branch in branches:
        st.subheader(branch["branch_name"])
        st.write(f"Last Entry Date: {branch['last_entry_date']}")
        
        # Row 1: Single values
        single_metrics = [
            ("Today Sales", f"£{branch['today_sales']:.2f}", None),
            ("Month on Month Growth", f"{branch['month_on_month_growth']:.2f}%", None),
            ("Year on Year Growth", f"{branch['year_on_year_growth']:.2f}%", None)
        ]
        
        cols = st.columns(4)
        for j in range(4):
            if j == 0:
                # Center the 3 tiles in 4 columns: leave first column empty
                continue
            idx = j - 1
            if idx < len(single_metrics):
                label, value, delta = single_metrics[idx]
                html = f"""
                <div class="metric-tile">
                    <div style="display: flex; justify-content: space-between;">
                        <h3>{value}</h3>
                    </div>
                    <h6 style="font-weight: normal;">{label}</h6>
                </div>
                """
                cols[j].markdown(html, unsafe_allow_html=True)
        
        # Row 2: Values with averages
        avg_metrics = [
            ("Lifetime Daily Avg", f"£{branch['lifetime_daily_avg']:.2f}", f"{branch['vs_lifetime_avg_pct']:.2f}%"),
            ("Weekly Rolling Avg", f"£{branch['weekly_rolling_avg']:.2f}", f"{branch['vs_weekly_avg_pct']:.2f}%"),
            ("Monthly Rolling Avg", f"£{branch['monthly_rolling_avg']:.2f}", f"{branch['vs_monthly_avg_pct']:.2f}%"),
            ("Typical Day Type Avg", f"£{branch['typical_day_type_avg']:.2f}", f"{branch['vs_typical_day_avg_pct']:.2f}%")
        ]
        
        cols = st.columns(4)
        for j, (label, value, delta) in enumerate(avg_metrics):
            color = "green" if delta and float(delta.rstrip('%')) > 0 else "red" if delta and float(delta.rstrip('%')) < 0 else "black"
            html = f"""
            <div class="metric-tile">
                <div style="display: flex; justify-content: space-between;">
                    <h3>{value}</h3>
                    <h4 style="color:{color};">{delta}</h4>
                </div>
                <h6 style="font-weight: normal;">{label}</h6>
            </div>
            """
            cols[j].markdown(html, unsafe_allow_html=True)
        
        st.divider()

    # --- Timeline Stacked Bar Chart ---
    import pandas as pd
    import plotly.express as px

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

    # Channel filter
    all_channels = sales_df["channel_name"].unique().tolist()
    selected_channels = st.multiselect(
        "Select Channels to Display:",
        options=all_channels,
        default=all_channels
    )

    # Month filter
    all_months = sorted(sales_df["month_label"].unique().tolist())
    selected_months = st.multiselect(
        "Select Months to Display:",
        options=all_months,
        default=all_months
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

    # Pie chart for total sales by channel
    channel_totals = filtered_df.groupby("channel_name")["monthly_sales"].sum().reset_index()
    fig_pie = px.pie(
        channel_totals,
        values="monthly_sales",
        names="channel_name",
        title="Total Sales by Channel",
        color_discrete_map=color_map
    )

    # Display charts side by side
    col1, col2 = st.columns([7, 3])
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)

    # Filters at the bottom
    st.subheader("Filters")
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_channels = st.multiselect(
            "Select Channels to Display:",
            options=all_channels,
            default=selected_channels,
            key="channels"
        )
    with col_filter2:
        selected_months = st.multiselect(
            "Select Months to Display:",
            options=all_months,
            default=selected_months,
            key="months"
        )

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