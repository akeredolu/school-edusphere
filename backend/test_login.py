import requests
from pprint import pprint

# ============================
# 1️⃣ LOGIN
# ============================

login_url = "http://127.0.0.1:8000/api/auth/login/"
login_data = {
    "username": "akeredolu.waheed@gmail.com",  # your login
    "password": "admin123"                      # your password
}

res = requests.post(login_url, json=login_data)
print("LOGIN STATUS:", res.status_code)
data = res.json()
pprint(data)

if res.status_code != 200:
    print("Login failed! Check credentials or backend.")
    exit()

access_token = data.get("access")
refresh_token = data.get("refresh")

print("\nACCESS TOKEN:", access_token)
print("REFRESH TOKEN:", refresh_token)

# ============================
# 2️⃣ TEST /users/me/ WITH TOKEN
# ============================

me_url = "http://127.0.0.1:8000/api/v1/users/me/"
headers = {
    "Authorization": f"Bearer {access_token}"
}

res = requests.get(me_url, headers=headers)
print("\n/users/me/ STATUS:", res.status_code)
try:
    pprint(res.json())
except:
    print(res.text)

# ============================
# 3️⃣ TEST /users/me/ WITHOUT TOKEN (should fail 401)
# ============================

res = requests.get(me_url)
print("\n/users/me/ WITHOUT TOKEN STATUS:", res.status_code)

