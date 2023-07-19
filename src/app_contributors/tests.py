from __future__ import division
from django.test import TestCase, Client, override_settings
from app_db.models import Registro, User, User_Profile
from django.urls import reverse
from random import choice
# ===========================================================================================
import numpy as np
from faker import Faker
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
import json
from faker.providers import geo


def create_random_point(x0, y0, distance):
    """
            Utility method for simulation of the points
    """
    r = distance / 111300
    u = np.random.uniform(0, 1)
    v = np.random.uniform(0, 1)
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t)
    x1 = x / np.cos(y0)
    y = w * np.sin(t)
    return (x0+x1, y0 + y)


# ===========================================================================================
"""
 ████████╗███████╗███████╗████████╗███████╗
 ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
    ██║   █████╗  ███████╗   ██║   ███████╗
    ██║   ██╔══╝  ╚════██║   ██║   ╚════██║
    ██║   ███████╗███████║   ██║   ███████║
    ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝
"""


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class Contributors_Views_Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test_email@correo.com', password='test_password_linda')
        self.client = Client()
        self.client.login(email='test_email@correo.com',
                          password='test_password_linda')
        # CREATING USERS
        f = Faker()
        for i in range(0, 10):
            User.objects.create_user(
                email=f.email(), password='una_contrasena_muy_buena')
        # CREATING REGISTER POINTS
        latitude1, longitude1 = -25.28646, -57.647
        # locations = [list(f.local_latlng(country_code='AR', coords_only=True)) for i in range(0,1000)]
        # locations = [list(f.local_latlng(country_code='AR', coords_only=True)) for i in range(0,1000)]
        locations = [create_random_point(
            latitude1, longitude1, 1500) for i in range(0, 10)]
        coordenadas = []
        for l in locations:
            coordenadas.append([float(l[0]), float(l[1])])
        for coord in coordenadas:
            point = {
                "type": "Point",
                "coordinates": coord
            }
            # print(GEOSGeometry(json.dumps(point)))
            Registro.objects.create(
                user=choice(User.objects.all()),
                # user = User.objects.get(id=103),
                pothole_coordinates=GEOSGeometry(json.dumps(point)),
                pothole_diameter=choice([i for i in range(0, 10)]),
                pothole_depth=choice([i for i in range(0, 10)]),
                pothole_quantity=choice([i for i in range(0, 10)]),
                material_type_road=choice([1, 2, 3]),
                road_type=choice([1, 2, 3]),
                type_of_traffic=choice([1, 2, 3]),
            )
            # SET URL DICT
            self.contrib_urls = {
                'home': reverse('contrib_home'),
                'listado_de_aportes': reverse('contrib_listado_de_aportes'),
                'listado_general_de_aportes': reverse('contrib_listado_general_de_aportes'),
                'ver_bache': reverse('admin_ver_bache', kwargs={'pk': choice([i.id for i in Registro.objects.all()])}),
                'descargar_datos': reverse('contrib_descargar_datos'),
                'ver_mapa': reverse('contrib_ver_mapa'),
                'solicitar_nueva_caracteristica': reverse('contrib_solicitar_nueva_caracteristica'),
                'caracteristicas_solicitadas': reverse('contrib_listado_de_caracteristicas_solicitadas'),
            }

    def test_contrib_home_GET(self):
        req = self.client.get(self.contrib_urls.get('home'))
        self.assertEquals(req.status_code, 200,
                          'GET LANDING HOME: The website could not be accessed.')

    def test_contrib_home_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get('home'))
        self.assertTemplateUsed(req, 'contributor_home.html',
                                'GET LANDING HOME: The Template does not match the answer.')

    def test_contrib_listado_de_aportes_GET(self):
        req = self.client.get(self.contrib_urls.get('listado_de_aportes'))
        self.assertEquals(req.status_code, 200,
                          'GET LISTADO DE APORTES: The website could not be accessed.')

    def test_contrib_listado_de_aportes_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get('listado_de_aportes'))
        self.assertTemplateUsed(req, 'contributor_listado_de_aportes.html',
                                'GET LISTADO DE APORTES: The template used does not coincide with the answer.')

    def test_contrib_listado_general_de_aportes_GET(self):
        req = self.client.get(self.contrib_urls.get(
            'listado_general_de_aportes'))
        self.assertEqual(
            req.status_code, 200, 'GET LISTADO GENERAL DE APORTES: The resource can not be accessed.')

    def test_contrib_listado_de_aportes_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get(
            'listado_general_de_aportes'))
        self.assertTemplateUsed(req, 'contrib_listado_general_aportes.html',
                                'GET LISTADO GENERAL DE APORTES: The template used does not coincide with the answer.')

    def test_contrib_ver_bache_GET(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertEqual(req.status_code, 200,
                         'GET VER BACHE: The URL can not be accessed.')

    def test_contrib_ver_bache_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertTemplateUsed(req, 'contrib_ver_bache.html',
                                'GET VER BACHE: The template used does not match.')

    def test_contrib_ver_bache_CONTEXT(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertTrue(req.context.get('head_title'), 'Ver Bache')

    def test_contrib_ver_bache_CONTEXT_head_title_instance(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It does not correspond to the type of data title of the page.')

    def test_contrib_ver_bache_CONTEXT_head_title_content(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertTrue(req.context.get('head_title') != None,
                        'Must contain a title the page.')

    def test_contrib_ver_bache_CONTEXT_user_profile_instance(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertIsInstance(req.context.get('user_profile'), User_Profile,
                              'CONTRIB VER BACHE CONTEXT: User_profile does not correspond to the type of data.')

    def test_contrib_ver_bache_CONTEXT_user_instance(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertIsInstance(req.context.get(
            'user'), User, 'It does not correspond to the type of user data.')

    def test_contrib_ver_bache_CONTEXT_bache_instance(self):
        req = self.client.get(self.contrib_urls.get('ver_bache'))
        self.assertIsInstance(req.context.get(
            'bache'), Registro, 'It does not correspond to the type of bump data.')

    def test_descargar_datos_GET(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertEquals(req.status_code, 200,
                          'The resource can not be accessed.')

    def test_descargar_datos_GET_context_head_title_not_null(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertIsNotNone(req.context.get('head_title'),
                             'It must contain a title.')

    def test_dexcargar_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertTemplateUsed(
            req, 'contrib_descargar_data.html', 'The template used does not match.')

    def test_descargar_datos_GET_context_title_data(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertEquals(req.context.get(
            'head_title'), 'Lista General - Descargas', 'The title of the page does not match.')

    def test_descargar_datos_GET_context_user_profile_not_null(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertTrue(req.context.get('user_profile') != None,
                        'You must contain a User_Profile object.')

    def test_descargar_datos_GET_context_registros_not_null(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertIsNotNone(req.context.get('registros'),
                             'You have to contain the records object.')

    def test_descargar_datos_GET_context_registros_data_content_size(self):
        req = self.client.get(self.contrib_urls.get('descargar_datos'))
        self.assertTrue(len(req.context.get(
            'registros')) > 0, 'Must contain at least one record.')

    def test_ver_mapa_GET_request(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertEquals(req.status_code, 200,
                          'The resource can not be accessed.')

    def test_ver_mapa_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertTemplateUsed(
            req,  'contrib_mapa_gneral.html', 'The Template received does not match.')


#         'user'
#  'head_title': 'Mapa General',
#  'user_profile': <User_Profile: U

#  'bache':
#  'map'


    def test_ver_mapa_GET_context_user_isnot_none(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertIsNotNone(req.context.get(
            'user'), 'A user was not found in the answer.')

    def test_ver_mapa_GET_context_user_data_type(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertIsInstance(req.context.get(
            'user'), User, 'The type of user data corresponds.')

    def test_ver_mapa_GET_context_head_title_isnot_none(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The page must contain a title.')

    def test_ver_mapa_GET_context_head_title_value(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertEquals(req.context.get('head_title'),
                          'Mapa General', 'The title of the page does not match.')

    def test_ver_mapa_GET_context_user_profile_isnot_none(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must contain a User_Profile object.')

    def test_ver_mapa_GET_context_user_profile_data_type(self):
        req = self.client.get(self.contrib_urls.get('ver_mapa'))
        self.assertIsInstance(req.context.get(
            'user_profile'), User_Profile, 'It does not correspond to the type of data.')

    def test_nueva_caracteristica_GET_request(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertEquals(req.status_code, 200, 'No se pudo acceder.')

    def test_nueva_caracteristica_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertTemplateUsed(
            req, 'contrib_solicitar_nueva_caracteristica.html', 'The template used is not correct.')

    def test_nueva_caracteristica_GET_has_title(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The resource must contain a title.')

    def test_nueva_caracteristica_GET_title_coincidence(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertEquals(req.context.get('head_title'), 'Solicitar Nueva Caracteristica',
                          'The title received does not coincide with the specification.')

    def test_nueva_caracteristica_GET_has_profile(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must have a user profile.')

    def test_nueva_caracteristica_GET_profile_data_type(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertIsInstance(req.context.get(
            'user_profile'), User_Profile, 'Do not match the type of data.')

    def test_nueva_caracteristica_GET_has_form(self):
        req = self.client.get(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'))
        self.assertIsNotNone(req.context.get(
            'form'), 'It must contain a form.')

    def test_nueva_caracteristica_POST_new_data(self):
        user = choice(User.objects.all())
        _data = {
            'usuario_solicitante': user,
            'caracteristica_estado': choice([0, 1, 2, 3, 4, 5]),
            'descripcion': 'fañlksdjfalksdjflñakjñflkja'
        }
        req = self.client.post(self.contrib_urls.get(
            'solicitar_nueva_caracteristica'), data=_data)
        self.assertEquals(req.status_code, 302,
                          'The new feature could not be created.')

    def test_listado_caracteristicas_solicitadas_GET_request(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')

    def test_listado_caracteristicas_solicitadas_GET_template_used(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertTemplateUsed(
            req, 'contrib_listado_de_caracteristicas_solicitadas.html', 'The Template received is not correct.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_has_title(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The page must have a title.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_title_value(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertEquals(req.context.get(
            'head_title'), 'Lista Solicitudes de Nuevas Caracteristicas ', 'The title received is not correct.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_has_user_profile(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'The answer must contain a USSER_PROFILE object.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_user_profile_data_type(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertIsInstance(req.context.get('user_profile'), User_Profile,
                              'It does not correspond to the type of data. Of the user profile.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_has_user(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertIsNotNone(req.context.get(
            'user'), 'You must have a user object.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_user_data_type(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        self.assertIsInstance(req.context.get(
            'user'), User, 'It does not correspond to the type of data.')

    def test_listado_caracteristicas_solicitadas_CONTEXT_has_caract(self):
        req = self.client.get(self.contrib_urls.get(
            'caracteristicas_solicitadas'))
        
        self.assertIsNotNone(req.context.get('caract'),
                             'The answer must contain a list of features.')

    # def test_listado_caracteristicas_solicitadas_CONTEXT_has_caract(self):
    #     req = self.client.get(self.contrib_urls.get(
    #         'caracteristicas_solicitadas'))
    #     self.assertTrue(len(req.context.get('caract'))>0, 'The answer must contain at least one element.')