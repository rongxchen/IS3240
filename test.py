import requests

resp = requests.get("http://localhost:8000/api/news/1/20?keyword=market", headers={
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlci0wMTdiMjRlMy0xZWY5LTRlMWUtYjg0Ni1mODQ5MGRhMTE5MGEiLCJleHAiOjE3MDI4MjUwNjQzNTR9.XolXzjBJhpjMoT8yutYGIaPnbZd0E0ySBg1SvI3aTHg"
})
print(resp.text)
