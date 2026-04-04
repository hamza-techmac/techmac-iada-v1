"""
IADA API Client
Centralized service layer for all communication with the FastAPI backend.
Base URL: https://iada.technologymac.co.uk
"""

import requests
import streamlit as st

BASE_URL = "https://iada.technologymac.co.uk"

# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _get_headers(branch_id: int = None) -> dict:
    """Helper to get headers with X-Auth-Key, Authorization, and optional branch_id."""
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    # Use 'auth_key' which might represent a JWT token or a traditional API key
    auth_key = st.session_state.get("auth_key")
    if auth_key:
        headers["X-Auth-Key"] = str(auth_key)
        # Add standard Bearer token header for JWT-based backends
        headers["Authorization"] = f"Bearer {auth_key}"
    if branch_id:
        # Some endpoints use 'branch_id' (underscore) and others use 'branch-id' (hyphen)
        headers["branch_id"] = str(branch_id)
        headers["branch-id"] = str(branch_id)
    return headers


def _get(path: str, branch_id: int = None, params: dict = None) -> list | dict | None:
    """Perform a GET request with optional branch_id in header and params."""
    if params is None:
        params = {}
    if branch_id:
        params["branch_id"] = branch_id
    
    try:
        resp = requests.get(
            f"{BASE_URL}{path}",
            headers=_get_headers(branch_id),
            params=params,
            timeout=10
        )
        resp.raise_for_status()
        payload = resp.json()
        if isinstance(payload, dict) and payload.get("status") == "success":
            return payload.get("data", [])
        # Some endpoints return the data directly (e.g. root)
        return payload
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.session_state["authentication_status"] = False
        elif e.response.status_code == 422:
            try:
                err_detail = e.response.json().get("detail", "Validation Error")
                st.error(f"❌ API Validation Error (422) for `{path}`: {err_detail}")
            except:
                st.error(f"❌ API Validation Error (422) for `{path}`: {e}")
        elif st.session_state.get("authentication_status"):
            st.warning(f"⚠️ API call failed for `{path}`: {e}")
        return None
    except Exception as e:
        if st.session_state.get("authentication_status"):
            st.warning(f"⚠️ API call failed for `{path}`: {e}")
        return None


def _post(path: str, body: dict, branch_id: int = None) -> dict | None:
    """Perform a POST request with optional branch_id header."""
    try:
        resp = requests.post(
            f"{BASE_URL}{path}",
            json=body,
            headers=_get_headers(branch_id),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.session_state["authentication_status"] = False
        else:
            st.error(f"❌ API POST failed for `{path}`: {e}")
        return None
    except Exception as e:
        st.error(f"❌ API POST failed for `{path}`: {e}")
        return None


def _put(path: str, body: dict) -> dict | None:
    """Perform a PUT request and return the response dict, or None on error."""
    try:
        resp = requests.put(f"{BASE_URL}{path}", json=body, headers=_get_headers(), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.session_state["authentication_status"] = False
        else:
            st.error(f"❌ API PUT failed for `{path}`: {e}")
        return None
    except Exception as e:
        st.error(f"❌ API PUT failed for `{path}`: {e}")
        return None


def _delete(path: str) -> dict | None:
    """Perform a DELETE request and return the response dict, or None on error."""
    try:
        resp = requests.delete(f"{BASE_URL}{path}", headers=_get_headers(), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.session_state["authentication_status"] = False
        else:
            st.error(f"❌ API DELETE failed for `{path}`: {e}")
        return None
    except Exception as e:
        st.error(f"❌ API DELETE failed for `{path}`: {e}")
        return None


# ---------------------------------------------------------------------------
# Auth endpoint
# ---------------------------------------------------------------------------

def login(username, password) -> dict | None:
    """Perform login against the /auth/login endpoint."""
    return _post("/auth/login", {"username": username, "password": password})


# ---------------------------------------------------------------------------
# READ endpoints  (cached for 5 minutes to reduce API calls on reruns)
# ---------------------------------------------------------------------------

# @st.cache_data(ttl=1, show_spinner=False)
def get_branches() -> list[dict]:
    """Return list of active branches from /branches/"""
    # Debug: Check headers being sent
    # headers = _get_headers()
    # st.sidebar.write(f"DEBUG: Headers keys: {list(headers.keys())}")
    data = _get("/branches/")
    return data if data else []


# @st.cache_data(ttl=300, show_spinner=False)
def get_channels() -> list[dict]:
    """Return list of channels from /channels/"""
    data = _get("/channels/")
    return data if data else []


# @st.cache_data(ttl=300, show_spinner=False)
def get_franchises() -> list[dict]:
    """Return list of franchises from /franchises/"""
    data = _get("/franchises/")
    return data if data else []


# @st.cache_data(ttl=300, show_spinner=False)
def get_cities() -> list[dict]:
    """Return list of cities from /cities/"""
    data = _get("/cities/")
    return data if data else []


# @st.cache_data(ttl=60, show_spinner=False)
def get_gl_report(branch_id: int = None) -> list[dict]:
    """
    Return general ledger data for a specific branch.
    """
    if not branch_id: return []
    data = _get("/financials/general-ledger", branch_id=branch_id)
    return data if data else []

# @st.cache_data(ttl=60, show_spinner=False)
def get_channel_monthly(branch_id: int) -> list[dict]:
    """Monthly sales aggregated by channel."""
    if not branch_id: return []
    data = _get("/reports/channel-monthly", branch_id=branch_id)
    return data if data else []

# @st.cache_data(ttl=60, show_spinner=False)
def get_monthly_expenses(branch_id: int) -> list[dict]:
    """Expense breakdown by category for each month."""
    if not branch_id: return []
    data = _get("/financials/monthly-expenses", branch_id=branch_id)
    return data if data else []

# @st.cache_data(ttl=60, show_spinner=False)
def get_weekly_segmented(branch_id: int) -> list[dict]:
    """Weekly sales breakdown by segment."""
    if not branch_id: return []
    data = _get("/reports/weekly-segmented", branch_id=branch_id)
    return data if data else []

# @st.cache_data(ttl=300, show_spinner=False)
def get_chart_of_accounts() -> list[dict]:
    """Returns all account codes, names, and types."""
    data = _get("/financials/chart-of-accounts")
    return data if data else []


# @st.cache_data(ttl=300, show_spinner=False)
def get_expense_categories() -> list[dict]:
    """
    Return list of expense types/categories from /expenses/types.
    """
    data = _get("/expenses/types")
    return data if data else []


# @st.cache_data(ttl=60, show_spinner=False)
def get_expenses(branch_id: int = None) -> list[dict]:
    """
    Return list of expenses for a specific branch.
    """
    data = _get("/expenses/", branch_id=branch_id)
    return data if data else []


# @st.cache_data(ttl=60, show_spinner=False)
def get_branch_performance(branch_id: int = None) -> dict | None:
    """
    Return KPIs for a specific branch from /reports/branch-performance.
    """
    if not branch_id: return None
    data = _get("/reports/branch-performance", branch_id=branch_id)
    return data


# @st.cache_data(ttl=60, show_spinner=False)
def get_branch_analytics(branch_id: int = None) -> list[dict] | None:
    """
    Return detailed analytics for a specific branch from /reports/branch-analytics.
    """
    if not branch_id: return None
    data = _get("/reports/branch-analytics", branch_id=branch_id)
    return data

# @st.cache_data(ttl=60, show_spinner=False)
def get_branch_monthly_performance(branch_id: int = None) -> list[dict]:
    """
    Detailed monthly P&L trend from /reports/branch-monthly-performance/{branch_id}.
    """
    if not branch_id: return []
    data = _get(f"/reports/branch-monthly-performance/{branch_id}", branch_id=branch_id)
    return data if data else []

# @st.cache_data(ttl=60, show_spinner=False)
def get_branch_weekly_performance(branch_id: int = None) -> list[dict]:
    """
    Detailed weekly P&L trend from /reports/branch-weekly-performance/{branch_id}.
    """
    if not branch_id: return []
    data = _get(f"/reports/branch-weekly-performance/{branch_id}", branch_id=branch_id)
    return data if data else []


# ---------------------------------------------------------------------------
# WRITE endpoints (POST, PUT, DELETE) - No caching
# ---------------------------------------------------------------------------

# --- Branch CRUD ---
def create_branch(franchise_id: int, branch_name: str, city_id: int,
                  area_name: str = None, postcode: str = None) -> dict | None:
    """POST a new branch to /branches/"""
    res = _post("/branches/", {
        "franchise_id": franchise_id,
        "branch_name": branch_name,
        "city_id": city_id,
        "area_name": area_name,
        "postcode": postcode,
        "is_active": 1,
    })
    if res:
        try: get_branches.clear()
        except: pass
    return res

def update_branch(branch_id: int, body: dict) -> dict | None:
    """PUT update a branch to /branches/{id}"""
    res = _put(f"/branches/{branch_id}", body)
    if res:
        try: get_branches.clear()
        except: pass
    return res

def delete_branch(branch_id: int) -> dict | None:
    """DELETE a branch at /branches/{id}"""
    res = _delete(f"/branches/{branch_id}")
    if res:
        try: get_branches.clear()
        except: pass
    return res


# --- Franchise CRUD ---
def create_franchise(franchise_name: str, owner_name: str, contact_email: str) -> dict | None:
    """POST a new franchise to /franchises/"""
    res = _post("/franchises/", {
        "franchise_name": franchise_name,
        "owner_name": owner_name,
        "contact_email": contact_email,
    })
    if res:
        try: get_franchises.clear()
        except: pass
    return res

def update_franchise(franchise_id: int, body: dict) -> dict | None:
    """PUT update a franchise to /franchises/{id}"""
    res = _put(f"/franchises/{franchise_id}", body)
    if res:
        try: get_franchises.clear()
        except: pass
    return res

def delete_franchise(franchise_id: int) -> dict | None:
    """DELETE a franchise at /franchises/{id}"""
    res = _delete(f"/franchises/{franchise_id}")
    if res:
        try: get_franchises.clear()
        except: pass
    return res


# --- Financial Entry (Sales & Expenses) ---
def create_sale(sales_date: str, branch_id: int, channel_id: int, amount: float) -> dict | None:
    """POST a single sale record to /sales/"""
    res = _post("/sales/", {
        "sales_date": sales_date,
        "branch_id": branch_id,
        "channel_id": channel_id,
        "amount": round(float(amount), 2),
    })
    if res:
        try: get_branch_analytics.clear()
        except: pass
    return res

def create_expense(sales_date: str, branch_id: int, expense_type_id: int, amount: float, description: str = None) -> dict | None:
    """POST a new expense record to /expenses/"""
    # Backend expects date_key (int YYYYMMDD)
    date_key = int(sales_date.replace("-", ""))
    res = _post("/expenses/", {
        "date_key": date_key,
        "branch_id": branch_id,
        "expense_type_id": expense_type_id,
        "amount": round(float(amount), 2),
        "description": description
    })
    if res:
        try: get_branch_analytics.clear()
        except: pass
    return res


# --- Infrastructure (City & Channel) ---
def create_city(city_name: str, region: str = None) -> dict | None:
    res = _post("/cities/", {"city_name": city_name, "region": region})
    if res:
        try: get_cities.clear()
        except: pass
    return res

def create_channel(channel_name: str, description: str = None) -> dict | None:
    res = _post("/channels/", {"channel_name": channel_name, "description": description, "is_active": 1})
    if res:
        try: get_channels.clear()
        except: pass
    return res


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------
def branch_map() -> dict[int, str]:
    return {b["id"]: b["branch_name"] for b in get_branches()}

def channel_map() -> dict[int, str]:
    return {c["id"]: c["channel_name"] for c in get_channels()}
