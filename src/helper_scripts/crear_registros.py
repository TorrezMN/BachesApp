# Testing simlation of generating random points 
from __future__ import division
import numpy as np
from random import choice
import json
from faker import Faker
from faker.providers import geo
from app_db.models import Registro, User
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point #GeoDjango takes lat and lng values in Point object.


latitude1,longitude1 =-25.28646, -57.647


def create_random_point(x0,y0,distance):
    """
            Utility method for simulation of the points
    """   
    r = distance/ 111300
    u = np.random.uniform(0,1)
    v = np.random.uniform(0,1)
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t)
    x1 = x / np.cos(y0)
    y = w * np.sin(t)
    return (x0+x1, y0 +y)




# locations = [list(f.local_latlng(country_code='AR', coords_only=True)) for i in range(0,1000)]
# locations = [list(f.local_latlng(country_code='AR', coords_only=True)) for i in range(0,1000)]
locations = [create_random_point(latitude1,longitude1 ,1500 ) for i in range(0,300)]
coordenadas = []

for l in locations:
    coordenadas.append([float(l[0]),float(l[1])])


for coord in coordenadas:
   
    point = {
        "type": "Point",
        "coordinates":coord
    }
    # print(GEOSGeometry(json.dumps(point)))
    Registro.objects.create(                  
        user = choice(User.objects.all()),        
        # user = User.objects.get(id=103),        
        pothole_coordinates=GEOSGeometry(json.dumps(point)),
        pothole_diameter = choice([i for i in range(0,10)]),
        pothole_depth = choice([i for i in range(0,10)]),
        pothole_quantity = choice([i for i in range(0,10)]),
        material_type_road = choice([1,2,3]),
        road_type = choice([1,2,3]),
        type_of_traffic = choice([1,2,3]),
        
        )

    print("-> Se guardo uno...")



             

print('TERMINE!')
