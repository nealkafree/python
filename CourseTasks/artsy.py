import sys

import requests
import json

client_id = 'fd17e18f5836284e93ac'
client_secret = 'e8d262a33e7139fa5e4ac5346af114ae'

# инициируем запрос на получение токена
r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

# разбираем ответ сервера
j = json.loads(r.text)

# достаем токен
token = j["token"]

# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token": token}
artists = []
with open('dataset_24476_4.txt', encoding='UTF-8') as file:
    for line in file.readlines():
        # инициируем запрос с заголовком
        request = requests.get("https://api.artsy.net/api/artists/" + line.rstrip(), headers=headers)
        # разбираем ответ сервера
        answer = json.loads(request.text)
        artists.append((answer['sortable_name'], int(answer['birthday'])))
artists.sort(key=lambda i: i[0])
artists.sort(key=lambda i: i[1])
for artist, _ in artists:
    print(artist)


