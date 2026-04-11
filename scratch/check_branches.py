import requests
import streamlit as st

# Since we don't have the session state here, this script will just help us understand the API structure.
BASE_URL = "https://iada.technologymac.co.uk"

def check_api():
    print("Checking /branches/ ...")
    try:
        resp = requests.get(f"{BASE_URL}/branches/", timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Content: {resp.json()[:3] if resp.status_code == 200 else resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_api()
