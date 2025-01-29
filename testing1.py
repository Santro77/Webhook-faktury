import requests

url = "http://127.0.0.1:5000/add_page"
payload = {
    "Numer konta": "403-6 Usługi na potrzeby biura",
    "calkowitaWartoscNetto": "1292,66",
    "Waluta": "PLN",
    "opis": "Lekcje Języka Angielskiego"
}
response = requests.post(url, json=payload)
print(response.text)