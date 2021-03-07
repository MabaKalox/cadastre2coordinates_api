from fastapi import HTTPException
import requests
from typing import Union
import json


def get_property_coordinates(cadastre_code: str) -> Union[list, None]:
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

    s.headers = headers

    params = {
        'f': 'json',
        'where': f"LOWER(CODE)={cadastre_code}",
        'isSpeedSearch': 'true'
    }

    url1 = 'https://www.kadastrs.lv'
    url2 = 'https://www.kadastrs.lv/di/proxy.ashx?AGS105/arcgis/rest/services/KK/CadasterIndex/MapServer/3/query?'

    r1 = s.get(url1)
    if r1.status_code == 200:
        print(s.cookies)
        r2 = s.get(url2, headers=headers, params=params)

        if r2.status_code == 200:
            try:
                response_body_obj = json.loads(r2.content.decode(encoding='UTF-8'))
                received_cadastre_code = response_body_obj.get('features')[0].get('attributes').get('CODE')
                if received_cadastre_code == cadastre_code:
                    return response_body_obj.get('features')[0].get('geometry').get('rings')
                else:
                    return []
            except json.decoder.JSONDecodeError:
                raise HTTPException(status_code=503, detail="Enable to parse JSON response from kadastrs.lv")
            except IndexError or KeyError:
                raise HTTPException(status_code=503, detail="Unexpected JSON response from kadastrs.lv")
        else:
            raise HTTPException(status_code=503, detail=f"Status code: {r2.status_code} from kadastrs.lv")
