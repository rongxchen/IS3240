import requests
from utils.cipher import md5_encrypt

resp = requests.post("http://localhost:8000/api/users", json={
    "username": "user1233",
    "password": "1233"
})
print(resp.text)
print(resp.json())