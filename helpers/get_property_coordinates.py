from fastapi import HTTPException
import urllib
from urllib.parse import urlencode
from typing import Union, List, Dict, Optional
import json
import asyncio
from aiohttp import ClientSession


def url_template(server_num: int, query_params: Optional[Dict[str, str]] = None):
    url = f"https://www.kadastrs.lv/di/proxy.ashx?AGS105/arcgis/rest/services/KK/CadasterIndex/MapServer/{server_num}/query"
    if query_params is not None:
        url += "?" + urlencode(query_params)
    return url


async def make_request(s: ClientSession, method: str, url: str, **kwargs):
    async with s.request(method, url, **kwargs) as response:
        if response.status == 200:
            return await response.text()
        else:
            raise HTTPException(status_code=503, detail=f"Status code: {response.status} from {url}")


async def get_property_coordinates(cadastre_code: str) -> List[List[str]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://www.kadastrs.lv/di/?appId=DI_PUB&lang=lv'
    }

    params = {
        'f': 'json',
        'where': f"LOWER(CODE)='{cadastre_code}'",
        'spatialRel': 'esriSpatialRelIntersects',
        'outSR': '3059',
        'isSpeedSearch': 'true'
    }

    lkm92tm_property_rings = []

    async with ClientSession(headers=headers) as session:
        tasks = []
        await session.get('https://www.kadastrs.lv')
        for server_num in [0, 2, 3, 4, 5]:
            tasks.append(make_request(session, 'get', url_template(server_num, query_params=params)))
        responses_text = await asyncio.gather(*tasks)
        for text in responses_text:
            try:
                response_body_obj = json.loads(text)
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

    return lkm92tm_property_rings
