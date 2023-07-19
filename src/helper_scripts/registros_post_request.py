import requests
import json
from random import choice

base_url = 'http://localhost:8000/api_V1/registro_new'


my_data ={
    "pothole_diameter":choice([i for i in range(3,15)]),
    "pothole_depth":choice([i for i in range(0,3)]),
    "pothole_quantity":choice([i for i in range(3,15)]),
    "material_type_road":choice([1,2,3]),
    "road_type":choice([1,2,3]),
    "type_of_traffic":choice([1,2,3]),
    "pothole_coordinates":"SRID=4326;POINT (-25.272316 -57.585773)",
    "registered_date":"2021-03-02T18:43:21.147461Z",
    "user":1
    }


for i in range(0,10):
    requests.post(base_url, data = json.loads(json.dumps(my_data)))
    print('\n'*5)
    print('Guardado el N° -> {0}'.format(i))
    print('\n'*5)



# print('\n'*5)
# print(my_data)
# print('\n'*5)
# print(json.loads(json.dumps(my_data)))
# print('\n'*5)
# 