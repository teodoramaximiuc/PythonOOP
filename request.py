import requests

response = requests.post("http://127.0.0.1:8000/items", json={"item": "apple"})
print(response.json())
