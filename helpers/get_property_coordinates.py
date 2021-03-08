from fastapi import HTTPException
import requests
from typing import Union, List
import json


def url_template(server_num: int):
    return f"https://www.kadastrs.lv/di/proxy.ashx?AGS105/arcgis/rest/services/KK/CadasterIndex/MapServer/{server_num}/query?"


def get_property_coordinates(cadastre_code: str) -> List[List[str]]:
    s = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://www.kadastrs.lv/di/?appId=DI_PUB&lang=lv',
    }

    s.headers = headers

    params = {
        'f': 'json',
        'where': f"LOWER(CODE)='{cadastre_code}'",
        'spatialRel': 'esriSpatialRelIntersects',
        'outSR': '3059'
        # 'isSpeedSearch': 'true'
    }

    r1 = s.get('https://www.kadastrs.lv')
    if r1.status_code == 200:
        print(s.cookies)
    lkm92tm_property_rings = []

    for server_num in [0, 2, 3, 4, 5]:
        r2 = s.get(url_template(server_num), headers=headers, params=params)
        if r2.status_code == 200:
            try:
                response_body_obj = json.loads(r2.content.decode(encoding='UTF-8'))
                if 'error' in response_body_obj:
                    code = response_body_obj['error']['code']
                    message = response_body_obj['error']['message']
                    raise HTTPException(status_code=503,
                                        detail=f"Error code: {code}, message: {message} from kadastrs.lv")
                response_features = response_body_obj.get('features')
                if len(response_features) > 0:
                    received_cadastre_code = response_features[0].get('attributes').get('CODE')
                    if received_cadastre_code == cadastre_code:
                        lkm92tm_property_rings.extend(response_features[0].get('geometry').get('rings'))
            except json.decoder.JSONDecodeError:
                raise HTTPException(status_code=503, detail="Enable to parse JSON response from kadastrs.lv")
            except (IndexError, KeyError, AttributeError, TypeError):
                raise HTTPException(status_code=503, detail="Unexpected JSON response from kadastrs.lv")
        else:
            raise HTTPException(status_code=503, detail=f"Status code: {r2.status_code} from kadastrs.lv")
    return lkm92tm_property_rings
