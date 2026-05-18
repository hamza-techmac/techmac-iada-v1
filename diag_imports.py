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
    get_expenses, get_branch_performance, get_branch_analytics, get_branch_monthly_performance,
    process_weekly_expenses
)
print("All imports successful!")
