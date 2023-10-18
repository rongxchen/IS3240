import requests
from utils.cipher import md5_encrypt

resp = requests.get("http://localhost:8000/api/favourites", headers={
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlci0wMTdiMjRlMy0xZWY5LTRlMWUtYjg0Ni1mODQ5MGRhMTE5MGEiLCJleHAiOjE3MDI4MjUwNjQzNTR9.XolXzjBJhpjMoT8yutYGIaPnbZd0E0ySBg1SvI3aTHg"
})
print(resp.json())