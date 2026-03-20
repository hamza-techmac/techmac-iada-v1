import os

filepath = r"d:\IADA\V1\Streamlet\techmac-iada-v1\streamlit_app.py"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_dashboard_tab = False
in_monthly_tab = False
in_weekly_tab = False
in_upload_tab = False

def push_indented(line, indent_level=1):
    if line.strip() == "":
        new_lines.append("\n")
    else:
        new_lines.append(("    " * indent_level) + line)

for index, line in enumerate(lines):
    # CSS hidden sidebar rule
    if "st.set_page_config(layout=\"wide\")" in line:
        line = line.replace("st.set_page_config(layout=\"wide\")", "st.set_page_config(layout=\"wide\", initial_sidebar_state=\"collapsed\")")
    
    if "<style>" in line:
        new_lines.append(line)
        new_lines.append("[data-testid=\"collapsedControl\"] { display: none; }\n")
        continue

    # Logout and Header modification
    if "authenticator.logout(\"Logout\", \"sidebar\")" in line:
        continue # skip
    if "st.title(\"Branch Dashboard\")" in line:
        continue # skip
    if "st.write(f\"Welcome back, **{st.session_state.get('name')}**!\")" in line:
        continue # skip
    
    if "st.divider()" in line and index in [60, 61, 62, 432, 433]:
        # we will handle dividers explicitly
        continue

    if "    # Branch Dashboard Data" in line and not in_dashboard_tab:
        new_lines.append("    # --- LOGGED IN CONTENT ---\n")
        new_lines.append("    col_title, col_profile = st.columns([9, 1])\n")
        new_lines.append("    with col_title:\n")
        new_lines.append("        st.title(\"Branch Dashboard\")\n")
        new_lines.append("    with col_profile:\n")
        new_lines.append("        st.write(\"\")\n")
        new_lines.append("        st.write(\"\")\n")
        new_lines.append("        with st.popover(\"👤 Profile\"):\n")
        new_lines.append("            st.write(f\"**{st.session_state.get('name')}**\")\n")
        new_lines.append("            st.button(\"⚙️ Settings\")\n")
        new_lines.append("            authenticator.logout(\"Logout\", \"main\")\n")
        new_lines.append("\n")
        new_lines.append("    st.divider()\n")
        new_lines.append("\n")
        new_lines.append("    tab_dashboard, tab_monthly, tab_weekly, tab_upload = st.tabs([\n")
        new_lines.append("        \"Dashboard\", \"Monthly Analysis\", \"Weekly Analysis\", \"Add Sales Stats\"\n")
        new_lines.append("    ])\n")
        new_lines.append("\n")
        new_lines.append("    with tab_dashboard:\n")
        in_dashboard_tab = True

    if "    # --- Timeline Stacked Bar Chart ---" in line and not in_monthly_tab:
        in_dashboard_tab = False
        in_monthly_tab = True
        new_lines.append("\n    with tab_monthly:\n")

    if "    # --- Weekly Analysis ---" in line and not in_weekly_tab:
        in_monthly_tab = False
        in_weekly_tab = True
        new_lines.append("\n    with tab_weekly:\n")
        continue # skip the comment line

    if "    st.header(\"Weekly Analysis\")" in line and index < 280:
        continue # skip this as we rename the section
        
    if "    st.header(\"Upload Data\")" in line and not in_upload_tab:
        in_weekly_tab = False
        in_upload_tab = True
        new_lines.append("\n    with tab_upload:\n")

    if in_dashboard_tab or in_monthly_tab or in_weekly_tab or in_upload_tab:
        # Increase indent by setting indent=2
        # Except the lines are already indented by 1 at baseline ("    ") due to else statement
        # So we add 4 spaces.
        if line.startswith("    "):
            new_lines.append("    " + line)
        else:
            if line.strip() != "":
                new_lines.append("        " + line)
            else:
                new_lines.append("\n")
    else:
        new_lines.append(line)

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Done")
