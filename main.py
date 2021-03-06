import requests
import json


cadastre_number = int(input("Cadastre number: "))

s = requests.Session()

headers = {
    'Host': 'www.kadastrs.lv',
    'Connection': 'keep-alive',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.kadastrs.lv/di/?appId=DI_PUB&lang=lv',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8'
}

params = {
    'f': 'json',
    'where': f"LOWER(CODE)={cadastre_number}",
    'isSpeedSearch': 'true'
}

url1 = 'https://www.kadastrs.lv'
url2 = 'https://www.kadastrs.lv/di/proxy.ashx?AGS105/arcgis/rest/services/KK/CadasterIndex/MapServer/3/query?'

s.get(url1)
print(s.cookies)
r2 = s.get(url2, headers=headers, params=params)
data = json.loads(r2.content.decode(encoding='UTF-8'))
print(data['features'][0]['geometry']['rings'])
