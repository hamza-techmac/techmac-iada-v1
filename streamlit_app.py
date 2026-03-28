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

    st.divider()

    tab_dashboard, tab_monthly, tab_weekly, tab_upload = st.tabs([
        "Dashboard", "Monthly Analysis", "Weekly Analysis", "Add Sales Stats"
    ])

    with tab_dashboard:
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
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            selected_channels = st.multiselect(
                "Select Channels to Display:",
                options=all_channels,
                default=all_channels,
                key="channels"
            )
        with col_filter2:
            selected_months = st.multiselect(
                "Select Months to Display:",
                options=all_months,
                default=all_months,
                key="months"
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


    with tab_weekly:
        st.divider()

        weekly_data_raw = [
            ["2026 Week 11", "Weekday", 3776.00, -33.36],
            ["2026 Week 10", "Weekday", 5666.00, -21.81],
            ["2026 Week 10", "Weekend", 2426.00, 32.57],
            ["2026 Week 09", "Weekday", 7246.00, 15.75],
            ["2026 Week 09", "Weekend", 1830.00, -17.19],
            ["2026 Week 08", "Weekday", 6260.00, 7.01],
            ["2026 Week 08", "Weekend", 2210.00, 7.80],
            ["2026 Week 07", "Weekday", 5850.00, -3.72],
            ["2026 Week 07", "Weekend", 2050.00, -16.33],
            ["2026 Week 06", "Weekday", 6076.00, 10.43],
            ["2026 Week 06", "Weekend", 2450.00, 37.95],
            ["2026 Week 05", "Weekday", 5502.00, -12.11],
            ["2026 Week 05", "Weekend", 1776.00, -17.40],
            ["2026 Week 04", "Weekday", 6260.00, 34.05],
            ["2026 Week 04", "Weekend", 2150.00, 14.36],
            ["2026 Week 03", "Weekday", 4670.00, -28.81],
            ["2026 Week 03", "Weekend", 1880.00, -7.21],
            ["2026 Week 02", "Weekday", 6560.00, 109.58],
            ["2026 Week 02", "Weekend", 2026.00, -6.12],
            ["2026 Week 01", "Weekday", 3130.00, -26.70],
            ["2026 Week 01", "Weekend", 2158.00, -14.70],
            ["2025 Week 53", "Weekday", 4270.00, -1.29],
            ["2025 Week 52", "Weekday", 4326.00, -30.47],
            ["2025 Week 52", "Weekend", 2530.00, -2.01],
            ["2025 Week 51", "Weekday", 6222.00, -1.08],
            ["2025 Week 51", "Weekend", 2582.00, 7.49],
            ["2025 Week 50", "Weekday", 6290.00, -16.13],
            ["2025 Week 50", "Weekend", 2402.00, -5.51],
            ["2025 Week 49", "Weekday", 7500.00, 12.28],
            ["2025 Week 49", "Weekend", 2542.00, -12.95],
            ["2025 Week 48", "Weekday", 6680.00, 0.30],
            ["2025 Week 48", "Weekend", 2920.00, 24.68],
            ["2025 Week 47", "Weekday", 6660.00, -5.40],
            ["2025 Week 47", "Weekend", 2342.00, 7.43],
            ["2025 Week 46", "Weekday", 7040.00, 1.44],
            ["2025 Week 46", "Weekend", 2180.00, -18.35],
            ["2025 Week 45", "Weekday", 6940.00, 3.89],
            ["2025 Week 45", "Weekend", 2670.00, 25.94],
            ["2025 Week 44", "Weekday", 6680.00, 14.38],
            ["2025 Week 44", "Weekend", 2120.00, -20.30],
            ["2025 Week 43", "Weekday", 5840.00, -18.09],
            ["2025 Week 43", "Weekend", 2660.00, 35.71],
            ["2025 Week 42", "Weekday", 7130.00, 0.82],
            ["2025 Week 42", "Weekend", 1960.00, 7.10],
            ["2025 Week 41", "Weekday", 7072.00, -3.39],
            ["2025 Week 41", "Weekend", 1830.00, 2.23],
            ["2025 Week 40", "Weekday", 7320.00, 7.05],
            ["2025 Week 40", "Weekend", 1790.00, -23.50],
            ["2025 Week 39", "Weekday", 6838.00, 7.18],
            ["2025 Week 39", "Weekend", 2340.00, 5.88],
            ["2025 Week 38", "Weekday", 6380.00, 7.92],
            ["2025 Week 38", "Weekend", 2210.00, 7.80],
            ["2025 Week 37", "Weekday", 5912.00, 30.91],
            ["2025 Week 37", "Weekend", 2050.00, 125.27],
            ["2025 Week 36", "Weekday", 4516.00, -20.32],
            ["2025 Week 36", "Weekend", 910.00, -23.53],
            ["2025 Week 35", "Weekday", 5668.00, 19.78],
            ["2025 Week 35", "Weekend", 1190.00, 48.75],
            ["2025 Week 34", "Weekday", 4732.00, 15.56],
            ["2025 Week 34", "Weekend", 800.00, -20.00],
            ["2025 Week 33", "Weekday", 4095.00, 66.87],
            ["2025 Week 33", "Weekend", 1000.00, 182.49],
            ["2025 Week 32", "Weekday", 2454.00, None],
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
            
            start_idx = unique_weeks.index(start_week)
            end_idx = unique_weeks.index(end_week)
            valid_weeks = unique_weeks[start_idx:end_idx+1]
            
            # Filter the dataframe for the selected range
            weekly_df = weekly_df[weekly_df["week_timeline"].isin(valid_weeks)]

        # Update category orders in the plotly figures just in case Plotly tries to resort them
        category_order = weekly_df["week_timeline"].unique().tolist()

        # Line chart for segment total
        fig_weekly_sales = px.line(
            weekly_df,
            x="week_timeline",
            y="segment_total",
            color="day_label",
            markers=True,
            title="Weekly Sales Trend (Segment Total)",
            labels={"segment_total": "Total Sales", "week_timeline": "Week"}
        )
        fig_weekly_sales.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), 
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
            labels={"segment_total": "Total Sales", "week_timeline": "Week"}
        )
        fig_weekly_stacked.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), 
            legend_title_text="",
            xaxis=dict(categoryorder='array', categoryarray=category_order)
        )

        # Bar chart for wow growth
        fig_wow_growth = px.bar(
            weekly_df,
            x="week_timeline",
            y="wow_segment_growth_pct",
            color="day_label",
            barmode="group",
            title="Week-over-Week Segment Growth (%)",
            labels={"wow_segment_growth_pct": "Growth (%)", "week_timeline": "Week"}
        )
        fig_wow_growth.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), 
            legend_title_text="",
            xaxis=dict(categoryorder='array', categoryarray=category_order)
        )

        st.plotly_chart(fig_weekly_sales, use_container_width=True)
        st.plotly_chart(fig_weekly_stacked, use_container_width=True)
        st.plotly_chart(fig_wow_growth, use_container_width=True)
        
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
