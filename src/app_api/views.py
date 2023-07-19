from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from app_db.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



from django.views.generic import TemplateView
import json
# Folium
import folium
from numpy import interp
from app_db.models import Registro
from rest_framework import status
import pandas as pd
from datetime import datetime
from django.conf import settings
# Importing Models
from app_db.models import User_Profile
from app_db.models import User
from app_db.models import Caracteristicas
from app_db.models import Registro
# SERIALIZERS
from .serializers import User_Serializer
from .serializers import test_data
from .serializers import Caracteristicas_Serializer
from .serializers import Registro_Serializer
from .serializers import CreateUserSerializer
"""
    Available Models
    - User
    - User_Profile
    - Contact_Request
    - Registro
    - Caracteristicas
"""
 
def get_caracteristicas_stats(request):
    """ Returns Caracteristicas statistics. 
        Caracteristicas
            usuario_solicitante
            caracteristica_estado
            descripcion
            caracteristica_registered_date
    """
    super_user = User.objects.get(email='torrez.mn@gmail.com')
    data = list(Caracteristicas.objects.all().values())
    df = pd.DataFrame(data)
    if(len(data) > 0):
        return({
            'about': {
                'title': 'Caracteristicas Statistics',
                'description': 'Small summary of statistics on the <Features> requested by the users of the system.'
            },
            'caracteristicas_estado': {
                'recibido': len(df[df.caracteristica_estado == 0]),
                'visto': len(df[df.caracteristica_estado == 1]),
                'confirmado': len(df[df.caracteristica_estado == 2]),
                'en_desarrollo': len(df[df.caracteristica_estado == 3]),
                'en_produccion': len(df[df.caracteristica_estado == 4]),
                'rechazado': len(df[df.caracteristica_estado == 5]),
            },
        })
    else:
        return(None)


def get_user_stats(request):
    """ Returns user statistics. 
        User_Profile:
            profile_user
            names
            last_name
            education_level
            age
            interest
    """
    super_user = User.objects.get(email='torrez.mn@gmail.com')
    data = list(User_Profile.objects.exclude(
        profile_user=super_user.id).values())
    df = pd.DataFrame(data)
    if(len(data) > 0):
        return({
            'about': {
                'title': 'User Statistics',
                'description': 'Small summary of statistics related to users of the system.'
            },
            'users': {
                'total_users_count': len(User_Profile.objects.exclude(profile_user=super_user.id)),
                'age': {
                    'media': str(df.age.mean()).replace('nan', '--'),
                    'max': str(df.age.max()).replace('nan', '--'),
                    'min': str(df.age.min()).replace('nan', '--'),
                },
                'education_level': {
                    'primary': len(df[df.education_level == 1]),
                    'secondary': len(df[df.education_level == 2]),
                    'academic': len(df[df.education_level == 3]),
                },
            },
        })
    else:
        return(None)


def get_registro_stats(request):
    """ Returns registros statistics. 
        User_Profile:
            profile_user
            names
            last_name
            education_level
            age
            interest
    """
    data = list(Registro.objects.all().values())
    df = pd.DataFrame(data)
    if(len(data) > 0):
        return({
            'about': {
                'title': 'Records Statistics',
                'description': 'Small summary of statistics on the pothole records that the system has.'
            },
            'registros': {
                'total_count': len(Registro.objects.all()),
                'tipo_material': {
                    'asfalto': len(df[df.material_type_road == 1]),
                    'tierra': len(df[df.material_type_road == 2]),
                    'piedra': len(df[df.material_type_road == 3]),
                },
                'tipo_camino': {
                    'ruta': len(df[df.road_type == 1]),
                    'vecinal': len(df[df.road_type == 2]),
                    'nacional': len(df[df.road_type == 3]),
                },
                'tipo_trafico': {
                    'mucho': len(df[df.type_of_traffic == 1]),
                    'poco': len(df[df.type_of_traffic == 2]),
                    'bajo': len(df[df.type_of_traffic == 3]),
                }
            },
        })
    else:
        return(None)


class API_STATUS(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = {
            'version': 'v1',
        }
        return Response(data)


"""
 ██╗   ██╗███████╗███████╗██████╗ ███████╗
 ██║   ██║██╔════╝██╔════╝██╔══██╗██╔════╝
 ██║   ██║███████╗█████╗  ██████╔╝███████╗
 ██║   ██║╚════██║██╔══╝  ██╔══██╗╚════██║
 ╚██████╔╝███████║███████╗██║  ██║███████║
  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
"""


class User_Stats(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(get_user_stats(request))


class Login_User(ObtainAuthToken):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        


class Register_User(APIView):
    #  renderer_classes = [JSONRenderer]
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.instance.get_user_data(), status=status.HTTP_201_CREATED)
        else:
            #  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_201_CREATED)


class Caracteristicas_Stats(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(get_caracteristicas_stats(request))


class Caracteristicas_List(APIView):
    """
    List all snippets, or create a new snippet.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        caract = Caracteristicas.objects.all()
        serializer = Caracteristicas_Serializer(caract, many=True)
        return Response(serializer.data)
    # def post(self, request, format=None):
    #     serializer = Caracteristicas_Serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, stwatus=status.HTTP_400_BAD_REQUEST)


class Registros_List(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        reg_list = Registro.objects.all()
        serializer = Registro_Serializer(reg_list, many=True)
        return Response(serializer.data)


class Registros_New(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        serializer = Registro_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Registros_Stats(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(get_registro_stats(request))

 
