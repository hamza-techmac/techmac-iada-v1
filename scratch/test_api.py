import requests

BASE_URL = "https://iada.technologymac.co.uk"

def test_branch(branch_id):
    print(f"Testing Branch ID: {branch_id}")
    # We don't have the auth key here, but let's see if the endpoint responds or 401s
    try:
        resp = requests.get(f"{BASE_URL}/reports/branch-analytics", params={"branch_id": branch_id}, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

test_branch(3)
test_branch(4)
