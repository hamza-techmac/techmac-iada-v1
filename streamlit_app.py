import os
import pandas as pd
import plotly.express as px
import streamlit as st
import extra_streamlit_components as stx
from services.api_client import (
    get_branches, get_channels,
    create_sale, branch_map, channel_map, login,
    get_gl_report, get_expense_categories,
    get_franchises, get_cities, create_branch, create_channel, create_city, create_franchise,
    update_branch, delete_branch, update_franchise, delete_franchise, create_expense,
    get_channel_monthly, get_weekly_segmented, get_monthly_expenses, get_chart_of_accounts,
    get_expenses, get_branch_performance, get_branch_analytics, get_branch_monthly_performance
)

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="IADA Executive Dashboard")

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

# --- 1. Cookie Manager (persistent sessions) ---
cookie_manager = stx.CookieManager(key="iada_cookie_manager")

# --- 2. Restore session from cookies on page load ---
# --- 2. RESTORE FROM COOKIE (DISABLED Temporarily) ---
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

# if st.session_state["authentication_status"] is not True:
#     # Try to restore from cookies
#     saved_key  = cookie_manager.get("iada_auth_key")
#     saved_user = cookie_manager.get("iada_username")
#     saved_name = cookie_manager.get("iada_name")
#     saved_role = cookie_manager.get("iada_role_id")
#     if saved_key and saved_user:
#         st.session_state["authentication_status"] = True
#         st.session_state["auth_key"]  = saved_key
#         st.session_state["username"]  = saved_user
#         st.session_state["name"]      = saved_name or saved_user.title()
#         st.session_state["role_id"]   = int(saved_role) if saved_role else 0

def show_login_ui():
    """Renders a premium 100vh style split login interface."""
    
    # Custom CSS for the 100vh Split Layout
    st.markdown("""
        <style>
            /* Hide the standard Streamlit header and footer area decorations if possible */
            [data-testid="stHeader"], [data-testid="stFooter"] {
                display: none;
            }
            .login-container {
                display: flex;
                height: 100vh;
                width: 100%;
            }
            .login-left {
                flex: 1;
                background-color: #fdfdfd;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                border-right: 1px solid #ecf0f1;
            }
            .login-right {
                flex: 1;
                background-color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Streamlit layout: Two Side-by-Side columns
    col_l, col_r = st.columns([1, 1], gap="large")
    
    with col_l:
        # Centering smaller logo and text
        st.write("") 
        st.write("") 
        
        # Internal sub-columns to make the image smaller
        col_img_1, col_img_2, col_img_3 = st.columns([1.5, 1, 1.5])
        with col_img_2:
             st.image("assets/media__1775071056203.png", use_container_width=True)
             
        st.markdown("<h1 style='text-align: center; color: #2c3e50; font-family: Outfit; margin-top: 20px;'>IADA Intelligence</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 1.1rem;'>The core of your branch analytics</p>", unsafe_allow_html=True)

    with col_r:
        st.write("") 
        st.write("") 
        with st.form("login_form", clear_on_submit=False):
            st.markdown("""
                <div style="text-align: left; margin-bottom: 25px;">
                    <h1 style="color: #2c3e50; margin: 0;">Sign In</h1>
                    <p style="color: #95a5a6; margin-top: 5px;">Welcome back! Access your dashboard below.</p>
                </div>
            """, unsafe_allow_html=True)
            
            user = st.text_input("Username", placeholder="e.g. admin", key="login_val_user")
            pw   = st.text_input("Password", type="password", placeholder="Password", key="login_val_pw")
            
            st.write("")
            submit = st.form_submit_button("LOGIN TO DASHBOARD", use_container_width=True)

            if submit:
                if not user or not pw:
                    st.error("Missing Username or Password.")
                else:
                    with st.spinner("Authenticating..."):
                        res = login(user, pw)
                        if res and res.get("status") == "success":
                            data = res.get("data", {})
                            auth_key = data.get("auth_key") or data.get("access_token") or data.get("token")
                            if not auth_key:
                                st.error("❌ Auth Token Error.")
                            else:
                                st.session_state["authentication_status"] = True
                                st.session_state["username"] = data.get("username")
                                st.session_state["name"]     = data.get("name") or str(data.get("username")).title()
                                st.session_state["auth_key"] = auth_key
                                st.session_state["role_id"]  = data.get("role_id", 0)
                                st.session_state["franchise_id"] = data.get("franchise_id")
                                
                                # SET COOKIES
                                cookie_manager.set("iada_auth_key", auth_key, max_age=30*24*3600, key="auth_set")
                                
                                # Diagnostics: Clear cache first if possible
                                try: get_branches.clear()
                                except: pass
                                
                                st.rerun()
                        else:
                            st.session_state["authentication_status"] = False
                            msg = res.get("message") if res else "Connection failed"
                            st.error(f"❌ Login Failed: {msg or 'Invalid credentials'}")

# --- 3. Check Authentication Status ---
if st.session_state["authentication_status"] is not True:
    show_login_ui()
    st.stop()

# --- ROLE PERMISSIONS ---
# role_id == 1: Admin
# role_id == 2: Manager (Franchise Owner)
# role_id == 3: Data Analyst
user_role = st.session_state.get("role_id", 0)

def get_allowed_branches(all_branches: list) -> list:
    """Filters branches based on the user's role."""
    # Admins and Data Analysts can view all branches
    if user_role in [1, 3]:  
        return all_branches
    # Franchise users can only view their own branches
    elif user_role == 2:
        franchise_id = st.session_state.get("franchise_id")
        if franchise_id:
            return [b for b in all_branches if b.get("franchise_id") == franchise_id]
        else:
            return [b for b in all_branches]
    return all_branches

# --- 3. Logged In Content Header ---
st.image("assets/media__1775072322438.png", use_container_width=True)

# --- DIAGNOSTIC HELP ---
with st.expander("🛠️ Diagnostics (Session & API Status)"):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("**Session State:**")
        st.write(f"Logged In: {st.session_state.get('authentication_status')}")
        st.write(f"Role: {st.session_state.get('role_id')}")
        st.write(f"Auth Key Start: {str(st.session_state.get('auth_key'))[:10]}...")
    with col_d2:
        st.write("**API Status:**")
        raw_branches = get_branches()
        raw_franchises = get_franchises()
        raw_cities = get_cities()
        
        st.write(f"Branches: {len(raw_branches) if raw_branches else 0}")
        st.write(f"Franchises: {len(raw_franchises) if raw_franchises else 0}")
        st.write(f"Cities: {len(raw_cities) if raw_cities else 0}")
        
        if not raw_branches:
            st.info("No branches returned from API. Check if your database is empty or connection is correct.")
        
        with st.expander("Show Raw JSON Responses"):
            st.write("Branches:")
            st.json(raw_branches if raw_branches else {"info": "Empty or None"})
            st.write("Franchises:")
            st.json(raw_franchises if raw_franchises else {"info": "Empty or None"})
            st.write("Cities:")
            st.json(raw_cities if raw_cities else {"info": "Empty or None"})

col_title, col_selector, col_profile = st.columns([6, 3, 1])
with col_title:
    st.title("Branch Dashboard")
with col_selector:
    st.write("") # Spacer
    # We fetch allowed branches globally here to use across the dashboard
    all_allowed_branches = get_allowed_branches(get_branches())
    branch_names = [b["branch_name"] for b in all_allowed_branches]
    if branch_names:
        selected_dashboard_branch = st.selectbox("Filter Branch", options=["All Branches"] + branch_names, key="global_branch_filter")
    else:
        st.warning("No branches accessible")
        selected_dashboard_branch = "None"
with col_profile:
    st.write("")
    st.write("")
    with st.popover("👤 User Profile"):
        role_map = {1: "🛡️ Administrator", 2: "🏢 Manager", 3: "📊 Data Analyst"}
        current_role = role_map.get(st.session_state.get("role_id"), "👤 User")
        
        st.write(f"**Name:** {st.session_state.get('name')}")
        st.write(f"**Role:** {current_role}")
        st.write(f"**Username:** @{st.session_state.get('username')}")
        
        with st.expander("🔍 Auth Details"):
            st.code(f"Key: {st.session_state.get('auth_key')[:10]}...")
            if "last_login_response" in st.session_state:
                st.write("Last Login API Response:")
                st.json(st.session_state["last_login_response"])

        st.divider()
        if st.button("Logout", use_container_width=True):
            # Clear all browser cookies
            for c in ["iada_auth_key", "iada_username", "iada_name", "iada_role_id", "iada_franchise_id"]:
                cookie_manager.delete(c, key=f"{c}_delete")
            # Clear all session state
            st.session_state.clear()
            st.rerun()

# --- Sidebar Branding ---
with st.sidebar:
    st.image("assets/media__1775071056203.png", use_container_width=True)
    st.divider()
    st.info(f"Session Active\nWelcome, {st.session_state.get('name')}")
    st.write("TechMAC Branch Intelligence v1.2")

st.divider()

st.divider()

tab_dashboard, tab_monthly, tab_weekly, tab_entry, tab_accounts, tab_franchise, tab_admin, tab_flow1 = st.tabs([
    "Dashboard", "Monthly Analysis", "Weekly Analysis", "Data Entry", "Accounts", "Franchise & Branches", "Admin Management", "Flow 1"
])

with tab_franchise:
    st.header("🏢 Franchise & Branch Management")
    st.write("View and manage your business entities here.")

    # -- Section: Franchise Management --
    st.subheader("Manage Franchises")
    
    f_list = get_franchises()
    if f_list:
        f_df = pd.DataFrame(f_list)
        # Reorder/rename for display
        f_display = f_df.copy()
        col_map = {"id": "ID", "franchise_name": "Franchise Name", "owner_name": "Owner Name", "contact_email": "Contact Email"}
        f_display.rename(columns={k: v for k, v in col_map.items() if k in f_display.columns}, inplace=True)
        
        # Display as a table with actions
        for i, row in f_df.iterrows():
            with st.expander(f"Franchise: {row['franchise_name']} (ID: {row['id']})"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Owner:** {row.get('owner_name', 'N/A')}")
                    st.write(f"**Email:** {row.get('contact_email', 'N/A')}")
                with c2:
                    # Edit Popover
                    with st.popover("✏️ Edit Franchise", use_container_width=True):
                        with st.form(f"edit_franchise_{row['id']}"):
                            new_name = st.text_input("Name", value=row["franchise_name"])
                            new_owner = st.text_input("Owner", value=row.get("owner_name", ""))
                            new_email = st.text_input("Email", value=row.get("contact_email", ""))
                            if st.form_submit_button("Save Changes"):
                                update_body = {
                                    "franchise_name": new_name,
                                    "owner_name": new_owner,
                                    "contact_email": new_email
                                }
                                if update_franchise(row["id"], update_body):
                                    st.success("Franchise updated!")
                                    st.rerun()
                    
                    # Delete Popover
                    with st.popover("🗑️ Delete Franchise", use_container_width=True):
                        st.warning(f"Are you sure you want to delete **{row['franchise_name']}**?")
                        st.info("Deleting a franchise may affect associated branches and data.")
                        if st.button(f"Confirm Delete {row['id']}", type="primary"):
                            if delete_franchise(row["id"]):
                                st.success("Franchise deleted!")
                                st.rerun()

        # Table view for quick reference
        st.write("---")
        st.write("**Quick Glance Table:**")
        st.dataframe(f_display, hide_index=True, use_container_width=True)
    else:
        st.info("No franchises found. Create one below.")

    st.write("---")
    with st.expander("➕ Add New Franchise"):
        with st.form("add_franchise_form"):
            f_name = st.text_input("Franchise Name")
            f_owner = st.text_input("Owner Name")
            f_email = st.text_input("Contact Email")
            if st.form_submit_button("Create Franchise", use_container_width=True):
                if f_name:
                    if create_franchise(f_name, f_owner, f_email):
                        st.success(f"Franchise '{f_name}' created!")
                        st.rerun()
                else:
                    st.error("Franchise name is required.")

    # -- Section: Branch Management (Optional but relevant) --
    st.divider()
    st.subheader("Manage Branches")
    
    b_list = get_branches()
    cities = get_cities()
    
    if b_list:
        b_df = pd.DataFrame(b_list)
        for _, b_row in b_df.iterrows():
            with st.expander(f"Branch: {b_row['branch_name']} (ID: {b_row['id']})"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Franchise ID:** {b_row.get('franchise_id')}")
                    st.write(f"**City ID:** {b_row.get('city_id')}")
                    st.write(f"**Postcode:** {b_row.get('postcode', 'N/A')}")
                with c2:
                    # Edit Branch
                    with st.popover("✏️ Edit Branch", use_container_width=True):
                        with st.form(f"edit_branch_{b_row['id']}"):
                            eb_name = st.text_input("Branch Name", value=b_row["branch_name"])
                            eb_post = st.text_input("Postcode", value=b_row.get("postcode", ""))
                            eb_area = st.text_input("Area", value=b_row.get("area_name", ""))
                            # Simplified selection for franchise/city in edit
                            if st.form_submit_button("Update Branch"):
                                b_update = {
                                    "branch_name": eb_name,
                                    "postcode": eb_post,
                                    "area_name": eb_area
                                }
                                if update_branch(b_row["id"], b_update):
                                    st.success("Branch updated!")
                                    st.rerun()
                    
                    with st.popover("🗑️ Delete Branch", use_container_width=True):
                        st.warning(f"Delete **{b_row['branch_name']}**?")
                        if st.button(f"Confirm Delete Branch {b_row['id']}", type="primary"):
                            if delete_branch(b_row["id"]):
                                st.success("Branch deleted!")
                                st.rerun()

    with st.expander("➕ Add New Branch"):
        if f_list and cities:
            with st.form("add_branch_form"):
                nb_name = st.text_input("Branch Name")
                nb_fran = st.selectbox("Assign to Franchise", options=[f["id"] for f in f_list], format_func=lambda x: next(f["franchise_name"] for f in f_list if f["id"] == x))
                nb_city = st.selectbox("City", options=[c["id"] for c in cities], format_func=lambda x: next(c["city_name"] for c in cities if c["id"] == x))
                nb_area = st.text_input("Area Name")
                nb_post = st.text_input("Postcode")
                if st.form_submit_button("Create Branch", use_container_width=True):
                    if nb_name:
                        if create_branch(nb_fran, nb_name, nb_city, nb_area, nb_post):
                            st.success(f"Branch '{nb_name}' created!")
                            st.rerun()
                    else:
                        st.error("Branch name is required.")
        else:
            st.warning("Please ensure at least one Franchise and one City exist before adding branches.")

with tab_admin:
    if user_role == 1:
        st.header("⚙️ Infrastructure Configuration")
        st.write("Manage system-wide settings including operational cities and sales channels.")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.subheader("🏙️ Manage Cities")
            with st.form("create_city_form", clear_on_submit=True):
                c_name = st.text_input("City Name", placeholder="e.g. London")
                c_region = st.text_input("Region (Optional)", placeholder="e.g. Greater London")
                if st.form_submit_button("➕ Add City", use_container_width=True):
                    if c_name:
                        if create_city(c_name, c_region): 
                            st.success(f"✅ {c_name} added!")
                            st.rerun()
                    else: st.warning("City name is required.")
        
        with col_c2:
            st.subheader("🔗 Manage Sales Channels")
            with st.form("create_channel_form", clear_on_submit=True):
                ch_name = st.text_input("Channel Name", placeholder="e.g. Deliveroo")
                ch_desc = st.text_input("Description (Optional)")
                if st.form_submit_button("➕ Add Channel", use_container_width=True):
                    if ch_name:
                        if create_channel(ch_name, ch_desc): 
                            st.success(f"✅ {ch_name} added!")
                            st.rerun()
                    else: st.warning("Channel name is required.")
    else:
        st.error("🔒 Access Denied. Admin role required.")
with tab_dashboard:
    all_allowed_branches = get_allowed_branches(get_branches())
    if not all_allowed_branches:
        st.warning("No branches accessible")
        st.stop()
    
    selected_dashboard_branch = st.session_state.get("global_branch_filter", "All Branches")

    # ---------------------------------------------------------------------------
    # BRANCH ANALYTICS TILES (Official /reports/branch-analytics Endpoint)
    # ---------------------------------------------------------------------------
    
    # Currency Formatting Utility
    def format_currency(value):
        try:
            return f"£{float(value or 0):,.2f}"
        except:
            return "£0.00"

    analytics_data = None
    if selected_dashboard_branch != "All Branches":
        # Find the ID for the selected branch
        selected_b_id = next((b["id"] for b in all_allowed_branches if b["branch_name"] == selected_dashboard_branch), None)
        if selected_b_id:
            with st.spinner("Fetching analytical data..."):
                analytics_raw = get_branch_analytics(selected_b_id)
                if analytics_raw and isinstance(analytics_raw, list) and len(analytics_raw) > 0:
                    analytics_data = analytics_raw[0]

            if analytics_data:
                st.subheader(f"🚀 {selected_dashboard_branch} Insights")
                
                # Sample Fields: Lifetime_sales, Lifetime_expense, Lifetime_profit, Last_month_profit, Last_week_profit, Average_Weekly_Profit, Average_Monthly_Profit
                
                # Row 1: Consolidated Lifetime Overview
                col_main, col_date = st.columns([3, 1])
                with col_main:
                    st.markdown(f'''
                        <div class="metric-tile" style="border-left: 5px solid #27ae60;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h6 style="color: #7f8c8d; margin-bottom: 5px;">LIFETIME OPERATIONAL OVERVIEW</h6>
                                    <h2 style="margin: 0; color: #2c3e50;">{format_currency(analytics_data.get("Lifetime_sales"))}</h2>
                                    <p style="font-size: 0.9rem; color: #95a5a6; margin-top: 5px;">Total Gross Revenue</p>
                                </div>
                                <div style="text-align: right; border-left: 1px solid #ecf0f1; padding-left: 20px;">
                                    <div style="margin-bottom: 15px;">
                                        <h4 style="margin: 0; color: #e74c3c;">{format_currency(analytics_data.get("Lifetime_expense"))}</h4>
                                        <h6 style="margin: 0; color: #bdc3c7; font-weight: normal;">Total Expenses</h6>
                                    </div>
                                    <div>
                                        <h4 style="margin: 0; color: #27ae60;">{format_currency(analytics_data.get("Lifetime_profit"))}</h4>
                                        <h6 style="margin: 0; color: #bdc3c7; font-weight: normal;">Net Profit</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                with col_date:
                    st.markdown(f'<div class="metric-tile"><h3>{analytics_data.get("Date", "N/A")}</h3><h6>Report Last Sync Date</h6></div>', unsafe_allow_html=True)

                # Row 2: Monthly & Weekly Performance (Similar Style)
                st.write("")
                col_monthly, col_weekly = st.columns(2)
                
                # Performance Calculation Helper
                def calc_perf_pct(current, average):
                    try:
                        curr = float(current or 0)
                        avg = float(average or 1) # avoid div by zero
                        if avg == 0: return 0.0
                        return ((curr - avg) / abs(avg)) * 100
                    except:
                        return 0.0

                with col_monthly:
                    mo_perf = calc_perf_pct(analytics_data.get("Last_month_profit"), analytics_data.get("Average_Monthly_Profit"))
                    mo_color = "#27ae60" if mo_perf >= 0 else "#e74c3c"
                    mo_icon = "&uarr;" if mo_perf >= 0 else "&darr;"
                    
                    st.markdown(f'''
                        <div class="metric-tile" style="border-left: 5px solid #3498db;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h6 style="color: #7f8c8d; margin-bottom: 5px;">LAST MONTH SUMMARY</h6>
                                    <h3 style="margin: 0; color: #2c3e50;">{format_currency(analytics_data.get("Last_month_sales"))}</h3>
                                    <p style="font-size: 0.8rem; color: #95a5a6; margin-top: 5px;">Monthly Sales</p>
                                </div>
                                <div style="text-align: right; border-left: 1px solid #ecf0f1; padding-left: 15px;">
                                    <div style="margin-bottom: 8px;">
                                        <h5 style="margin: 0; color: #e74c3c;">{format_currency(analytics_data.get("Last_month_expense"))}</h5>
                                        <h6 style="margin: 0; color: #bdc3c7; font-size: 0.7rem; font-weight: normal;">Expenses</h6>
                                    </div>
                                    <div>
                                        <h5 style="margin: 0; color: #27ae60;">{format_currency(analytics_data.get("Last_month_profit"))}</h5>
                                        <h6 style="margin: 0; color: #bdc3c7; font-size: 0.7rem; font-weight: normal;">Net Profit</h6>
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top: 10px; border-top: 1px dashed #ecf0f1; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 0.75rem; color: #7f8c8d;">Avg Profit: <b>{format_currency(analytics_data.get("Average_Monthly_Profit"))}</b></span>
                                <span style="font-size: 1.1rem; color: {mo_color}; font-weight: bold;">{mo_icon} <span style="font-size: 0.85rem;">{abs(mo_perf):.1f}% Performance</span></span>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

                with col_weekly:
                    wk_perf = calc_perf_pct(analytics_data.get("Last_week_profit"), analytics_data.get("Average_Weekly_Profit"))
                    wk_color = "#27ae60" if wk_perf >= 0 else "#e74c3c"
                    wk_icon = "&uarr;" if wk_perf >= 0 else "&darr;"
                    
                    st.markdown(f'''
                        <div class="metric-tile" style="border-left: 5px solid #f1c40f;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h6 style="color: #7f8c8d; margin-bottom: 5px;">LAST WEEK SUMMARY</h6>
                                    <h3 style="margin: 0; color: #2c3e50;">{format_currency(analytics_data.get("Last_week_sales"))}</h3>
                                    <p style="font-size: 0.8rem; color: #95a5a6; margin-top: 5px;">Weekly Sales</p>
                                </div>
                                <div style="text-align: right; border-left: 1px solid #ecf0f1; padding-left: 15px;">
                                    <div style="margin-bottom: 8px;">
                                        <h5 style="margin: 0; color: #e74c3c;">{format_currency(analytics_data.get("Last_week_expense"))}</h5>
                                        <h6 style="margin: 0; color: #bdc3c7; font-size: 0.7rem; font-weight: normal;">Expenses</h6>
                                    </div>
                                    <div>
                                        <h5 style="margin: 0; color: #27ae60;">{format_currency(analytics_data.get("Last_week_profit"))}</h5>
                                        <h6 style="margin: 0; color: #bdc3c7; font-size: 0.7rem; font-weight: normal;">Net Profit</h6>
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top: 10px; border-top: 1px dashed #ecf0f1; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 0.75rem; color: #7f8c8d;">Avg Profit: <b>{format_currency(analytics_data.get("Average_Weekly_Profit"))}</b></span>
                                <span style="font-size: 1.1rem; color: {wk_color}; font-weight: bold;">{wk_icon} <span style="font-size: 0.85rem;">{abs(wk_perf):.1f}% Performance</span></span>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                # --- Weekday vs Weekend Sales Comparison ---
                
                # --- Weekday vs Weekend Sales Comparison ---
                st.write("")
                st.subheader("📅 Sales Distribution: Weekdays vs. Weekends")
                
                dist_col1, dist_col2 = st.columns(2)
                
                with dist_col1:
                    # Last Week Distribution
                    wk_labels = ["Weekdays", "Weekend"]
                    wk_values = [analytics_data.get("Last_week_sales_weekdays", 0), analytics_data.get("Last_week_sales_weekend", 0)]
                    
                    fig_wk_dist = px.pie(
                        names=wk_labels,
                        values=wk_values,
                        title="Last Week Sales Split",
                        color_discrete_sequence=["#34495e", "#f39c12"],
                        hole=0.5
                    )
                    fig_wk_dist.update_layout(height=350, margin=dict(t=40, b=40, l=10, r=10))
                    st.plotly_chart(fig_wk_dist, use_container_width=True)

                with dist_col2:
                    # Last Month Distribution
                    mo_labels = ["Weekdays", "Weekend"]
                    mo_values = [analytics_data.get("Last_month_sales_weekdays", 0), analytics_data.get("Last_month_sales_weekend", 0)]
                    
                    fig_mo_dist = px.pie(
                        names=mo_labels,
                        values=mo_values,
                        title="Last Month Sales Split",
                        color_discrete_sequence=["#2c3e50", "#e67e22"],
                        hole=0.5
                    )
                    fig_mo_dist.update_layout(height=350, margin=dict(t=40, b=40, l=10, r=10))
                    st.plotly_chart(fig_mo_dist, use_container_width=True)

                st.divider()
            else:
                st.warning("⚠️ Could not load official analytical KPIs for this branch. Please check selection.")

    # Show list of all branches for high-level overview if "All Branches" selected
    if selected_dashboard_branch == "All Branches" and all_allowed_branches:
        st.subheader("🏦 All Branches Summary")
        # Since we removed day-wise fallback, we can show a list of branch names with quick links
        for b in all_allowed_branches:
            st.write(f"- **{b['branch_name']}** ({b.get('area_name', 'N/A')})")

with tab_monthly:
    st.header("📅 Monthly Performance Analysis")
    live_branches = get_allowed_branches(get_branches())
    if not live_branches:
        st.warning("No branches available.")
    else:
        # Use Global Branch selection
        global_sel = st.session_state.get("global_branch_filter", "All Branches")
        if global_sel == "All Branches":
            st.info("ℹ️ Analyzing **first available branch** (Global filter set to All Branches)")
            sel_b_name = live_branches[0]["branch_name"]
            sel_b_id = live_branches[0]["id"]
        else:
            sel_b_name = global_sel
            sel_b_id = next((b["id"] for b in live_branches if b["branch_name"] == global_sel), live_branches[0]["id"])
            
        st.subheader(f"📊 Market Trend & Profitability: {sel_b_name}")

        # --- Sales API Logic ---
        # --- Branch Monthly Performance API Logic ---
        api_sales_data = get_branch_monthly_performance(sel_b_id)
        # --- Fetch Data ---
        api_data = get_branch_monthly_performance(sel_b_id)
        if not api_data or not isinstance(api_data, list):
            st.warning("⚠️ No monthly performance data found for this branch.")
            st.stop()

        raw_df = pd.DataFrame(api_data)
        
        # --- 1. Mapping & Normalization ---
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }
        
        if "Month" in raw_df.columns:
            if pd.api.types.is_numeric_dtype(raw_df["Month"]):
                raw_df["month_text"] = raw_df["Month"].map(month_names)
            else:
                raw_df["month_text"] = raw_df["Month"]
        
        if "Year" in raw_df.columns and "Month" in raw_df.columns:
            to_num = {v: k for k, v in month_names.items()}
            m_num = raw_df["Month"] if pd.api.types.is_numeric_dtype(raw_df["Month"]) else raw_df["Month"].map(to_num)
            raw_df["month_label"] = raw_df["Year"].astype(str) + " - " + raw_df["month_text"]
            raw_df["sort_key"] = raw_df["Year"] * 100 + m_num.fillna(0).astype(int)
            raw_df = raw_df.sort_values("sort_key")

        # Dynamic Display Mapping as requested
        display_map = {
            "Sales_Collection": "Direct Sales", "Sales_JustEat": "Just Eat",
            "Sales_Deliveroo": "Deliveroo", "Sales_Uber": "Uber Eat",
            "Exp_COS": "Cost of Sale", "Exp_COL": "Cost of Labour",
            "Exp_Admin": "Admin Cost", "Exp_Marketing": "Marketing Cost",
            "Exp_Commissions": "Sales Platform Cost",
            "Total_Sales": "Revenue", "Total_Expense": "Expenses", "Net_Profit": "Net Profit"
        }
        
        available_sales = [k for k in ["Sales_Collection", "Sales_JustEat", "Sales_Deliveroo", "Sales_Uber"] if k in raw_df.columns]
        available_exp   = [k for k in ["Exp_COS", "Exp_COL", "Exp_Admin", "Exp_Marketing", "Exp_Commissions"] if k in raw_df.columns]
        
        # --- Filters ---
        st.markdown("#### Analytical Filters")
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            sel_months = st.multiselect("Toggle Months", options=raw_df["month_label"].unique(), default=raw_df["month_label"].unique())
        with f_col2:
            sel_channels = st.multiselect("Toggle Channels", options=[display_map[k] for k in available_sales], default=[display_map[k] for k in available_sales])
        with f_col3:
            sel_expenses = st.multiselect("Toggle Expenses", options=[display_map[k] for k in available_exp], default=[display_map[k] for k in available_exp])

        rev_map = {v: k for k, v in display_map.items()}
        filt_sales_keys = [rev_map[c] for c in sel_channels if c in rev_map]
        filt_exp_keys   = [rev_map[e] for e in sel_expenses if e in rev_map]
        
        df = raw_df[raw_df["month_label"].isin(sel_months)].copy()

        st.divider()
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            st.subheader("1️⃣ Monthly Sales vs. Expenses Distribution")
            import plotly.graph_objects as go
            fig_compare = go.Figure()
            for i, sk in enumerate(filt_sales_keys):
                fig_compare.add_trace(go.Bar(name=display_map[sk], x=df["month_label"], y=df[sk], offsetgroup=0, marker_color=px.colors.qualitative.Plotly[i % 10]))
            for i, ek in enumerate(filt_exp_keys):
                fig_compare.add_trace(go.Bar(name=display_map[ek], x=df["month_label"], y=df[ek], offsetgroup=1, marker_opacity=0.7, marker_color=px.colors.qualitative.Pastel[i % 10]))
            fig_compare.update_layout(barmode='stack', title="Sales (Left) vs. Expenses (Right)", legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5))
            st.plotly_chart(fig_compare, use_container_width=True)

        with r1_c2:
            st.subheader("2️⃣ Performance Overview (MoM)")
            # Sanitize columns for Sales, Cost, Profit
            # Map potential duplicates to ensure we find what's there
            line_map = {
                "Total_Sales": "Sales", "Total_Revenue": "Sales",
                "Total_Expense": "Cost", "Total_Expenses": "Cost",
                "Net_Profit": "Profit", "Monthly_Net_Profit": "Profit"
            }
            # Add to local display_map for chart labels
            display_map.update(line_map)
            
            # Find which keys exist in df from the line_map
            valid_line_keys = [k for k in line_map.keys() if k in df.columns]
            
            if valid_line_keys:
                fig_line = px.line(
                    df, x="month_label", y=valid_line_keys,
                    title="Revenue, Cost & Profit Trend", markers=True,
                    labels={k: display_map[k] for k in valid_line_keys},
                    color_discrete_map={"Total_Sales": "#3498db", "Total_Revenue": "#3498db", 
                                        "Total_Expense": "#e74c3c", "Total_Expenses": "#e74c3c", 
                                        "Net_Profit": "#27ae60", "Monthly_Net_Profit": "#27ae60"}
                )
                fig_line.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5))
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Performance trend data pending for this branch.")

        # Bottom Row: Pies (Share) - 3 Columns
        st.divider()
        st.subheader("📊 Profitability & Cost Structures")
        r2_c1, r2_c2, r2_c3 = st.columns(3)
        
        with r2_c1:
            st.markdown("#### 3️⃣ Expense Share")
            exp_sums = df[filt_exp_keys].sum().reset_index()
            exp_sums.columns = ["Category", "Amount"]; exp_sums["Label"] = exp_sums["Category"].map(display_map)
            fig_p_exp = px.pie(exp_sums, values="Amount", names="Label", hole=0.5, title="Expense Distribution")
            fig_p_exp.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), legend_title_text="")
            st.plotly_chart(fig_p_exp, use_container_width=True)
            
        with r2_c2:
            st.markdown("#### 4️⃣ Sales Share")
            sale_sums = df[filt_sales_keys].sum().reset_index()
            sale_sums.columns = ["Channel", "Amount"]; sale_sums["Label"] = sale_sums["Channel"].map(display_map)
            fig_p_sale = px.pie(sale_sums, values="Amount", names="Label", hole=0.5, title="Sales Split")
            fig_p_sale.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), legend_title_text="")
            st.plotly_chart(fig_p_sale, use_container_width=True)

        with r2_c3:
            st.markdown("#### 5️⃣ Platform Fee (Est. 21%)")
            platform_channels = ["Sales_JustEat", "Sales_Deliveroo", "Sales_Uber"]
            avail_platform = [k for k in platform_channels if k in df.columns]
            if avail_platform:
                # Calculate fee per channel
                plat_data = []
                for ch in avail_platform:
                    fee = df[ch].sum() * 0.21
                    plat_data.append({"Channel": display_map.get(ch, ch), "Estimated Fee": fee})
                
                fee_df = pd.DataFrame(plat_data)
                fig_p_fee = px.pie(fee_df, values="Estimated Fee", names="Channel", hole=0.5, title="Platform Fee Share")
                fig_p_fee.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), legend_title_text="")
                st.plotly_chart(fig_p_fee, use_container_width=True)
            else:
                st.info("No online channel data found for platform analysis.")
                
        # --- Tabular Report View ---
        st.divider()
        st.subheader("📋 Monthly Performance Data (Tabular)")
        
        # 1. Prepare display dataframe with Renaming
        report_df = df.copy()
        report_df.rename(columns={k: v for k, v in display_map.items() if k in report_df.columns}, inplace=True)
        
        # 2. Add New Calculation: Profit Margin %
        # (Ensure columns exist before calculation)
        if "Sales" in report_df.columns and "Profit" in report_df.columns:
            report_df["Profit Margin %"] = (report_df["Profit"] / report_df["Sales"].replace(0, 1)) * 100
        else:
            report_df["Profit Margin %"] = 0.0

        # 3. Clean and Reorder
        # Drop columns explicitly not needed
        bad_cols = ["Branch id", "Branch ID", "branch_id", "Branch Name", "branch_name", "Year", "year", "Month", "month", "sort_key", "month_text", "Agg_Platform_Sales", "Est_21_Platform_Fee"]
        report_df.drop(columns=[c for c in bad_cols if c in report_df.columns], inplace=True, errors='ignore')

        # Precise Column Order: Label first, then core metrics
        core_order = ["month_label", "Sales", "Cost", "Profit", "Profit Margin %"]
        other_cols = [c for c in report_df.columns if c not in core_order]
        final_order = [c for c in core_order if c in report_df.columns] + other_cols
        report_df = report_df[final_order]

        # 4. Styling Logic (Green > 5%, Amber 0-5%, Red < 0%)
        def style_profitability(row):
            margin = row.get("Profit Margin %", 0)
            color = ""
            if margin > 5: color = "background-color: #d4edda; color: #155724;" # Green
            elif margin >= 0: color = "background-color: #fff3cd; color: #856404;" # Amber
            else: color = "background-color: #f8d7da; color: #721c24;" # Red
            
            styles = ['' for _ in row.index]
            if "Profit" in row.index:
                styles[row.index.get_loc("Profit")] = color
            if "Profit Margin %" in row.index:
                styles[row.index.get_loc("Profit Margin %")] = color
            return styles

        # 5. Display Styled DataFrame
        st.dataframe(
            report_df.style.apply(style_profitability, axis=1).format({
                "Profit Margin %": "{:.2f}%", 
                "Sales": "£{:,.2f}", "Cost": "£{:,.2f}", "Profit": "£{:,.2f}",
                **{c: "£{:,.2f}" for c in other_cols if any(m in c for m in ["Direct", "Eat", "Deliveroo", "Sale", "Cost", "Fee"])}
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Download Button
        csv_data = report_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Monthly Audit (CSV)",
            data=csv_data,
            file_name=f"audit_{sel_b_name.replace(' ', '_')}.csv",
            mime='text/csv'
        )


with tab_weekly:
    st.header("📅 Weekly Performance Analysis")
    live_branches = get_allowed_branches(get_branches())
    if not live_branches:
        st.warning("No branches available.")
    else:
        # Use Global Branch selection
        global_sel = st.session_state.get("global_branch_filter", "All Branches")
        if global_sel == "All Branches":
            st.info("ℹ️ Analyzing **first available branch** (Global filter set to All Branches)")
            sel_b_name = live_branches[0]["branch_name"]
            sel_b_id = live_branches[0]["id"]
        else:
            sel_b_name = global_sel
            sel_b_id = next((b["id"] for b in live_branches if b["branch_name"] == global_sel), live_branches[0]["id"])
            
        st.subheader(f"📊 Weekly Market Trend: {sel_b_name}")

        # --- Fetch Data ---
        from services.api_client import get_branch_weekly_performance
        weekly_api_data = get_branch_weekly_performance(sel_b_id)
        
        if not weekly_api_data or not isinstance(weekly_api_data, list):
            st.warning("⚠️ No weekly performance data found for this branch.")
            st.stop()

        df_w = pd.DataFrame(weekly_api_data)
        # --- Weekly Performance Logic ---
        # Mapping for human-readable labels
        w_map = {
            "Sales_Collection": "Direct Sales", 
            "Sales_JustEat": "Just Eat", 
            "Sales_Deliveroo": "Deliveroo", 
            "Sales_Uber": "Uber Eat",
            "Exp_COS": "Cost of Sale", 
            "Exp_COL": "Cost of Labour", 
            "Exp_Admin": "Admin Cost", 
            "Exp_Marketing": "Marketing Cost", 
            "Exp_Commissions": "Sales Platform Cost",
            "Total_Revenue": "Sales", 
            "Total_Expenses": "Cost", 
            "Weekly_Net_Profit": "Profit"
        }

        # Normalize data (Year-Week combination)
        if "Year" in df_w.columns and "Week" in df_w.columns:
            # Display format: "Week 01 (2026)" or simply "Week 01" if single year
            df_w["week_label"] = "Week " + df_w["Week"].astype(str).str.zfill(2)
            if df_w["Year"].nunique() > 1:
                df_w["week_label"] += " (" + df_w["Year"].astype(str) + ")"
            
            df_w["sort_key"] = df_w["Year"] * 100 + df_w["Week"].astype(int)
            df_w = df_w.sort_values("sort_key")

        available_s = [k for k in ["Sales_Collection", "Sales_JustEat", "Sales_Deliveroo", "Sales_Uber"] if k in df_w.columns]
        available_e = [k for k in ["Exp_COS", "Exp_COL", "Exp_Admin", "Exp_Marketing", "Exp_Commissions"] if k in df_w.columns]

        # Analytical Filters
        st.markdown("#### Operational Filters")
        wf1, wf2, wf3 = st.columns(3)
        with wf1: sw_weeks = st.multiselect("Select Weeks", options=df_w["week_label"].unique(), default=df_w["week_label"].unique(), key="w_weeks")
        with wf2: sw_chans = st.multiselect("Toggle Channels", options=[w_map[k] for k in available_s], default=[w_map[k] for k in available_s], key="w_chans")
        with wf3: sw_exps = st.multiselect("Toggle Expenses", options=[w_map[k] for k in available_e], default=[w_map[k] for k in available_e], key="w_exps")

        rev_w = {v: k for k, v in w_map.items()}
        filt_s = [rev_w[c] for c in sw_chans if c in rev_w]
        filt_e = [rev_w[e] for e in sw_exps if e in rev_w]
        curr_w = df_w[df_w["week_label"].isin(sw_weeks)].copy()

        # Analytics Views
        st.divider()
        st.subheader("1️⃣ Weekly Sales vs. Expenses")
        import plotly.graph_objects as go
        fig = go.Figure()
        for i, sk in enumerate(filt_s):
            fig.add_trace(go.Bar(name=w_map[sk], x=curr_w["week_label"], y=curr_w[sk], offsetgroup=0, marker_color=px.colors.qualitative.Plotly[i % 10]))
        for i, ek in enumerate(filt_e):
            fig.add_trace(go.Bar(name=w_map[ek], x=curr_w["week_label"], y=curr_w[ek], offsetgroup=1, marker_opacity=0.7, marker_color=px.colors.qualitative.Pastel[i % 10]))
        fig.update_layout(
            barmode='stack', 
            title="Weekly Cashflow Comparison", 
            height=500,
            xaxis_title="Weeks",
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("") # Spacer
        st.subheader("2️⃣ Performance Index (WoW)")
        lk = [k for k in ["Total_Revenue", "Total_Expenses", "Weekly_Net_Profit"] if k in curr_w.columns]
        if lk:
            fig_l = px.line(curr_w, x="week_label", y=lk, markers=True, 
                            labels={k: w_map[k] for k in lk}, 
                            color_discrete_map={"Total_Revenue": "#3498db", "Total_Expenses": "#e74c3c", "Weekly_Net_Profit": "#27ae60"})
            fig_l.update_layout(
                height=500,
                xaxis_title="Weeks",
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
            )
            st.plotly_chart(fig_l, use_container_width=True)

        st.divider()
        st.subheader("📊 Profitability Diagnostics")
        p1, p2, p3 = st.columns(3)
        with p1:
            es = curr_w[filt_e].sum().reset_index(); es.columns=["K","V"]; es["L"]=es["K"].map(w_map)
            fig_we = px.pie(es, values="V", names="L", hole=0.5, title="Expense Dist.")
            fig_we.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), legend_title_text="")
            st.plotly_chart(fig_we, use_container_width=True)
        with p2:
            ss = curr_w[filt_s].sum().reset_index(); ss.columns=["K","V"]; ss["L"]=ss["K"].map(w_map)
            fig_ws = px.pie(ss, values="V", names="L", hole=0.5, title="Sales Dist.")
            fig_ws.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), legend_title_text="")
            st.plotly_chart(fig_ws, use_container_width=True)
        with p3:
            pc = [k for k in ["Sales_JustEat", "Sales_Deliveroo", "Sales_Uber"] if k in curr_w.columns]
            if pc:
                p_est = pd.DataFrame([{"CH": w_map[ch], "Fee": curr_w[ch].sum()*0.21} for ch in pc])
                fig_wf = px.pie(p_est, values="Fee", names="CH", hole=0.5, title="Platform Cost (21%)")
                fig_wf.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), legend_title_text="")
                st.plotly_chart(fig_wf, use_container_width=True)
            else: st.info("No online channel data found.")

        # Detailed Audit Table
        st.divider()
        st.subheader("📋 Weekly Audit Summary")
        table_df = curr_w.copy()
        table_df.rename(columns={k: v for k, v in w_map.items() if k in table_df.columns}, inplace=True)
        if "Sales" in table_df.columns and "Profit" in table_df.columns:
            table_df["Profit Margin %"] = (table_df["Profit"] / table_df["Sales"].replace(0,1)) * 100
        else: table_df["Profit Margin %"] = 0.0
        
        table_df.drop(columns=[c for c in ["Branch_id", "Branch id", "Branch ID", "branch_id", "Year", "Week", "sort_key", "Start_Date", "End_Date", "month_text"] if c in table_df.columns], inplace=True, errors='ignore')
        t_core = ["week_label", "Sales", "Cost", "Profit", "Profit Margin %"]
        t_final = [c for c in t_core if c in table_df.columns] + [c for c in table_df.columns if c not in t_core]
        table_df = table_df[t_final]

        def sw(row):
            m = row.get("Profit Margin %", 0)
            c = "background-color: #d4edda; color: #155724;" if m > 5 else ("background-color: #fff3cd; color: #856404;" if m >= 0 else "background-color: #f8d7da; color: #721c24;")
            s = ['' for _ in row.index]
            for tg in ["Profit", "Profit Margin %"]:
                if tg in row.index: s[row.index.get_loc(tg)] = c
            return s

        st.dataframe(table_df.style.apply(sw, axis=1).format({"Profit Margin %": "{:.2f}%", "Sales": "£{:,.2f}", "Cost": "£{:,.2f}", "Profit": "£{:,.2f}", **{c: "£{:,.2f}" for c in table_df.columns if any(m in c for m in ["Direct", "Eat", "Deliveroo", "Sale", "Cost", "Fee"])}}), use_container_width=True, hide_index=True)
        st.download_button("📥 Export Weekly Report", table_df.to_csv(index=False).encode('utf-8'), f"weekly_audit_{sel_b_name}.csv", "text/csv")


with tab_entry:
    if user_role in [1, 2]:
        sub_sales, sub_expenses = st.tabs(["💰 Daily Sales & Upload", "💸 Record Expenses"])
        
        with sub_sales:
            st.header("📝 Add Sales Data")
            st.write("Enter daily sales for each channel below.")
            
            # -- Load live reference data from API ------------------------------
            v_branches = get_allowed_branches(get_branches())
            v_channels = get_channels()

            if not v_branches or not v_channels:
                st.error("⚠️ Could not load branch/channel data from API. Please check connectivity.")
            else:
                branch_options = {b["branch_name"]: b["id"] for b in v_branches}
                ch_lookup = {c["id"]: c["channel_name"] for c in v_channels}

                with st.form("sales_data_form", clear_on_submit=True):
                    col_top1, col_top2 = st.columns(2)
                    with col_top1:
                        sales_date = st.date_input("📅 Sales Date")
                    with col_top2:
                        selected_branch_name = st.selectbox("🏬 Branch", options=list(branch_options.keys()), key="sale_branch")

                    st.divider()
                    st.markdown("**Sales Amounts by Channel**")

                    col1, col2 = st.columns(2)
                    channel_amounts = {}
                    all_ch_ids = sorted(ch_lookup.keys())
                    mid = (len(all_ch_ids) + 1) // 2

                    for i, ch_id in enumerate(all_ch_ids):
                        ch_label = ch_lookup.get(ch_id, f"Channel {ch_id}")
                        if ch_id == 1: ch_label = "Own (Card)"
                        elif ch_id == 2: ch_label = "Own (Cash)"
                        elif ch_id == 5: ch_label = "JustEat (Card)"
                        elif ch_id == 6: ch_label = "JustEat (Cash)"

                        col = col1 if i < mid else col2
                        with col:
                            channel_amounts[ch_id] = st.number_input(f"{ch_label}", min_value=0.0, step=0.01, format="%.2f", key=f"ch_{ch_id}")

                    st.divider()
                    if st.form_submit_button("✅ Submit Sales", use_container_width=True):
                        branch_idx = branch_options[selected_branch_name]
                        date_str = str(sales_date)
                        success_list = []
                        
                        for c_id, amt in channel_amounts.items():
                            if amt > 0:
                                res = create_sale(date_str, branch_idx, c_id, amt)
                                if res: success_list.append(ch_lookup.get(c_id, f"ch_{c_id}"))
                        
                        if success_list:
                            st.success(f"✔️ Saved sales for: {', '.join(success_list)}")
                            get_daywise_sales.clear()

            # -- Bulk Sales Data Upload ------------------------------------------
            st.divider()
            st.subheader("🚀 Bulk Sales Data Upload")
            with st.expander("📝 View Required CSV Format Template"):
                template_df = pd.DataFrame([["2026-04-01", "Crown Street", "Own (Cash)", 450.00]], columns=["Date", "Branch", "Channel", "Amount"])
                st.dataframe(template_df, hide_index=True)

            bulk_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
            if bulk_file:
                df_bulk = pd.read_csv(bulk_file)
                if st.button("🚀 Process & Upload CSV", use_container_width=True):
                    b_map_rev = {b["branch_name"].strip().lower(): b["id"] for b in v_branches}
                    c_map_rev = {c["channel_name"].strip().lower(): c["id"] for c in v_channels}
                    c_map_rev.update({"own (card)": 1, "own (cash)": 2, "justeat (card)": 5, "justeat (cash)": 6})
                    
                    s_count = 0
                    for _, row in df_bulk.iterrows():
                        try:
                            b_i = b_map_rev.get(str(row["Branch"]).strip().lower())
                            c_i = c_map_rev.get(str(row["Channel"]).strip().lower())
                            if b_i and c_i:
                                res = create_sale(str(pd.to_datetime(row["Date"]).date()), b_i, c_i, float(row["Amount"]))
                                if res: s_count += 1
                        except: pass
                    if s_count: st.success(f"✔️ Uploaded {s_count} records!"); get_daywise_sales.clear()

        with sub_expenses:
            st.header("💸 Record Expenses")
            st.write("Input operational expenses manually.")
            
            # Fresh lookups for expenses
            live_branches = get_allowed_branches(get_branches())
            live_exp_types = get_expense_categories()
            
            if not live_branches or not live_exp_types:
                st.error("⚠️ Could not load expense categories or branches. Please ensure backend is alive.")
            else:
                with st.form("manual_expense_form", clear_on_submit=True):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        exp_date = st.date_input("📅 Expense Date")
                        exp_branch_id = st.selectbox("🏬 Branch", options=[b["id"] for b in live_branches], format_func=lambda x: next(b["branch_name"] for b in live_branches if b["id"] == x), key="exp_branch")
                    with col_e2:
                        exp_type_id = st.selectbox("≡ƒôé Category", options=[t["id"] for t in live_exp_types], format_func=lambda x: f"{next(t['expense_type'] for t in live_exp_types if t['id'] == x)} ({next(t['category'] for t in live_exp_types if t['id'] == x)})", key="exp_cat")
                        exp_amt = st.number_input("💰 Amount (£)", min_value=0.0, step=0.01, format="%.2f")
                    
                    exp_desc = st.text_area("📝 Description (Optional)")
                    
                    if st.form_submit_button("🚀 Log Expense", use_container_width=True):
                        if exp_amt > 0:
                            res = create_expense(str(exp_date), exp_branch_id, exp_type_id, exp_amt, exp_desc)
                            if res: 
                                st.success(f"✅ Expense of £{exp_amt:,.2f} logged and deducted from net profit projections.")
                                get_daywise_sales.clear() # Refresh dashboard
                            else: st.error("❌ Failed to log expense.")
                        else: st.warning("Please enter an amount > £0.00")
    else:
        st.error("🔒 Access Denied. Manager role required for data entry.")

with tab_accounts:
    st.subheader("Chart of Accounts")
    st.write("This tab displays the system Chart of Accounts across Revenue and Expense categories.")

    # -- API: Live Chart of Accounts -------------------------------
    live_branches = get_allowed_branches(get_branches())
    api_coa = get_chart_of_accounts()
    
    if api_coa and isinstance(api_coa, list) and len(api_coa) > 0:
        accounts_df = pd.DataFrame(api_coa)
        # Handle naming discrepancies defensively
        rename_map = {
            "account_code": "Account_Code", 
            "account_name": "Account_Name", 
            "account_type": "Account_Type",
            "description": "Description"
        }
        accounts_df.rename(columns={k: v for k, v in rename_map.items() if k in accounts_df.columns}, inplace=True)
        st.success("✅ Showing live Chart of Accounts from API")
    else:
        # Fallback manual build if endpoint fails
        st.info("Falling back to manual Chart of Accounts building...")
        live_channels = get_channels()
        revenue_rows = []
        if live_channels:
            for c in live_channels:
                label = c["channel_name"]
                if c["id"] == 1: label = "Own (Card)"
                elif c["id"] == 2: label = "Own (Cash)"
                elif c["id"] == 5: label = "JustEat (Card)"
                elif c["id"] == 6: label = "JustEat (Cash)"
                revenue_rows.append(["Revenue", c["id"], label, "Income from sales"])

        live_expense_types = get_expense_categories()
        expense_rows = []
        if live_expense_types:
            for et in live_expense_types:
                acc_type = et.get("category_type", "Expense")
                acc_code = et.get("id", 0)
                acc_name = et.get("type_name", "Unknown Expense")
                acc_desc = et.get("description", "")
                expense_rows.append([acc_type, acc_code, acc_name, acc_desc])
        
        accounts_data = revenue_rows + expense_rows
        accounts_df = pd.DataFrame(accounts_data, columns=["Account_Type", "Account_Code", "Account_Name", "Description"])

    # Live branch info banner
    if live_branches:
        branch_info = " | ".join([f"**{b['branch_name']}** (id={b['id']}), {b['area_name']}, {b['postcode']}" for b in live_branches])
        st.info(f"🏬 **Active Branches:** {branch_info}")

    st.dataframe(accounts_df, use_container_width=True, hide_index=True)

    # --- GL Report (Consolidated) ---
    st.divider()
    st.header("🗄️ Branch General Ledger")
    st.write("Detailed audit trail of all transactions for the selected branch.")
    
    if not live_branches:
        st.warning("No branches available.")
    else:
        col_gl1, col_gl2 = st.columns([2, 1])
        with col_gl1:
            # Branch Selector for GL
            b_map = {b["branch_name"]: b["id"] for b in live_branches}
            sel_b_name = st.selectbox("🎯 Select Branch to View Ledger", options=list(b_map.keys()), key="gl_branch_selector")
            sel_b_id = b_map[sel_b_name]
        with col_gl2:
            uploaded_gl = st.file_uploader("Upload GL Data CSV/Override", type=["csv", "tsv", "txt"], label_visibility="collapsed")
            if st.button("🚀 Fetch Ledger from API", use_container_width=True):
                st.session_state["trigger_gl"] = True
                
        gl_df = None
        
        # 1. Manual Upload Override
        if uploaded_gl is not None:
            try:
                gl_df = pd.read_csv(uploaded_gl, sep=None, engine="python")
                st.success("✅ Showing GL from uploaded file")
            except Exception as e:
                st.error(f"Failed to read uploaded file: {e}")
        # 2. API Fetch
        elif st.session_state.get("trigger_gl", False) or sel_b_id:
            api_gl = get_gl_report(sel_b_id)
            if api_gl:
                gl_df = pd.DataFrame(api_gl)
                st.success(f"✅ Showing live GL report for {sel_b_name}")
            else:
                st.info("No ledger entries found for this branch.")
                
        if gl_df is not None and not gl_df.empty:
            # Normalize column names (API might return snake_case)
            rename_map = {
                "transaction_date": "Transaction_Date",
                "date_key": "Transaction_Date", # API returns date_key
                "account_code": "Account_Code",
                "account_name": "Account_Name",
                "debit": "Debit",
                "credit": "Credit",
                "description": "Description",
                "entry_type": "Entry_Type"
            }
            gl_df = gl_df.rename(columns=rename_map)

            # Convert 20240315 numeric date to proper datetime if needed
            if "Transaction_Date" in gl_df.columns:
                gl_df["Transaction_Date"] = pd.to_datetime(gl_df["Transaction_Date"].astype(str), format='%Y%m%d', errors='coerce').fillna(pd.to_datetime(gl_df["Transaction_Date"], errors='coerce')).dt.date
            
            # Formatter for null/NaN values
            if "Debit" in gl_df.columns: gl_df["Debit"] = gl_df["Debit"].fillna(0.0)
            if "Credit" in gl_df.columns: gl_df["Credit"] = gl_df["Credit"].fillna(0.0)

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

with tab_flow1:
    st.header("🏢 Flow 1: Branch Insights")
    
    # 1. Fetch live branches for dropdown
    all_branches_flow = get_branches()
    if not all_branches_flow:
        st.warning("No branches available to display in Flow 1.")
    else:
        branch_map_flow = {b["branch_name"]: b["id"] for b in all_branches_flow}
        selected_name_flow = st.selectbox("🎯 Select Branch", options=list(branch_map_flow.keys()), key="flow1_branch_selector")
        selected_id_flow = branch_map_flow[selected_name_flow]
        
        st.divider()
        
        # 2. Fetch Data
        col_kpi, col_exp = st.columns([1, 1])
        
        with col_kpi:
            st.subheader("📊 Performance KPIs")
            kpi_data = get_branch_performance(selected_id_flow)
            if kpi_data:
                # Display metrics if key-value pairs exist
                if isinstance(kpi_data, dict):
                    c1, c2 = st.columns(2)
                    for i, (k, v) in enumerate(kpi_data.items()):
                        # Clean up keys for display
                        display_label = k.replace('_', ' ').title()
                        if i % 2 == 0:
                            c1.metric(label=display_label, value=v)
                        else:
                            c2.metric(label=display_label, value=v)
                else:
                    st.json(kpi_data)
            else:
                st.info("No performance KPI data returned from API for this branch.")

        with col_exp:
            st.subheader("💸 Expenses")
            exp_list = get_expenses(selected_id_flow)
            if exp_list and isinstance(exp_list, list):
                exp_df = pd.DataFrame(exp_list)
                if not exp_df.empty:
                    st.dataframe(
                        exp_df,
                        use_container_width=True,
                        column_config={
                            "amount": st.column_config.NumberColumn(format="£%.2f"),
                            "date_key": "Date Code",
                            "id": None
                        }
                    )
                    total_exp = exp_df["amount"].sum() if "amount" in exp_df.columns else 0
                    st.write(f"**Total Expenses Found:** £{total_exp:,.2f}")
                else:
                    st.info("Expense list is empty for this branch.")
            else:
                st.info("No expense records found from API.")

# --- GLOBAL FOOTER ---
st.markdown("""
<div class="footer">
© 2026 TechMAC. All rights reserved. V1.2.0-API
</div>
""", unsafe_allow_html=True)
