

# import json
# from django.contrib.gis.geos import GEOSGeometry

# data_coordinates = [
# [36.66678428649903, -1.5474249907643578], 
# [36.670904159545906, -1.542620219636788], 
# [36.66635513305665,-1.5353272427374922],
# [36.662406921386726, -1.5403894293513378]
# ]

# for coordinate in data_coordinates:
#     point = {
#         "type": "Point",
#         "coordinates": coordinate 
#     }

#     LogsUpload.objects.create(name="your location name", geom=GEOSGeometry(json.dumps(point)))











# E:\Milton\PROYECTO_TESIS\thesis_web>python manage.py shell < helper_scripts/crear_registros.py
from random import choice
import json
from faker import Faker
from faker.providers import geo
from app_db.models import Registro, User
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point #GeoDjango takes lat and lng values in Point object.


f = Faker()

f.add_provider(geo)
# aria-label="-25.272949, -57.585480"
# -25.272949,-57.572276
# longitud = f.coordinate(center = "-57.585480", radius=0.001)
# latitud = f.coordinate(center = "-25.272949", radius=0.001)

# print(f.coordinate(center = [36.662406921386726, -1.5403894293513378], radius=0.001))


# locations = [list(f.coordinate(center=None, radius=0.001)) for i in range(0,1000)]
# # locations = [list(f.local_latlng(country_code='AR', coords_only=True)) for i in range(0,1000)]
# coordenadas = []

# for l in locations:
#     coordenadas.append([float(l[0]),float(l[1])])

locations = [[f.coordinate(center = "-25.272949", radius=0.001),f.coordinate(center = "-57.585480", radius=0.001) ] for i in range(0,500)]
# locations = [[f.coordinate(center = "-25.272949", radius=0.001),f.coordinate(center = "-57.585480", radius=0.001) ] for i in range(0,100)]
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
        # user = User.objects.get(id=103),        
        user = choice(User.objects.all()),        
        pothole_coordinates=GEOSGeometry(json.dumps(point)),
        pothole_diameter = choice([i for i in range(0,10)]),
        pothole_depth = choice([i for i in range(0,10)]),
        pothole_quantity = choice([i for i in range(0,10)]),
        material_type_road = choice([1,2,3]),
        road_type = choice([1,2,3]),
        type_of_traffic = choice([1,2,3]),

        )
    print('------------------------------')
    print("-> Se guardo uno...")
    print('------------------------------')
    print('\n'*3)

print('TERMINE!')
