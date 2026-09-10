import requests

url = "http://127.0.0.1:8000/"
town = input("enter town name : ")
data = {
    "town" : town
}

res = requests.post(url=url , json=data)
print(res.status_code)
print(res.json())