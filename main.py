# from helpers.get_property_coordinates import get_property_coordinates
import pickle
import json


# cadastre_code = input("Cadastre number: ")

with open('config', 'rb') as dump_file:
    r2 = pickle.load(dump_file)

# with open('config', 'wb') as dump_file:
#     r2 = get_property_coordinates('0100001002001')
#     pickle.dump(r2, dump_file)

response_body_obj = json.loads(r2.content.decode(encoding='UTF-8'))

print(r2.status_code == 200)
