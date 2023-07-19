from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

# Create your tests here.
from faker import Faker
from random import choice
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from app_db.models import User, User_Profile, Contact_Request, Caracteristicas



@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class Api_Tests(TestCase):
    def setUp(self):
        f = Faker()
        self.user = User.objects.create_user(
            email='test_email@correo.com', password='test_passwdfsdford_linda')
        self.client = Client()
        self.client.login(email='test_email@correo.com',
                          password='test_password_linda')
        self.api_urls = {
            'status': 'api_status',
            'registro': 'api_register_user',
            'login': 'api_login_user',
            'user_stats': 'api_user_stats',
            'stats_caracteristicas': 'api_caracteristicas_stats',
            'lista_caracteristicas': 'api_caracteristicas_list',
            'lista_registro': 'api_registros_list',
            'new_registro': 'api_registro_new',
            'stats_registro': 'api_registro_stats',
        }
        f = Faker()
        # Create some users.
        User.objects.create_superuser(
            email= 'torrez.mn@gmail.com', password='falksdjfñalksdjfñlaksjdfñlaksjdflk'
        ).save()
        for i in range(0, 20):
            User(email=f.email(), password='prueba_userfasdfasdfsd').save()

    # def test_api_status_GET_basic_request(self):
    #     req = self.client.get(reverse(self.api_urls.get('status')))
    #     self.assertEquals(req.status_code, 200, 'It was not possible to access the resource.')

    # def test_api_registro_GET_basic_request(self):
    #     usr = {
    #         'email' : 'correso@gmail.com',
    #         'password' : 'una_contrfkalsdjf',
    #     }
    #     req = self.client.post(reverse(self.api_urls.get('registro')),data= usr,  follow=True)
    #     self.assertEquals(req.status_code, 201 ,'It was not possible to register the user.')
    
    # def test_api_login_GET_basic_request(self):
    #     usr = {
    #         'username' : 'test_email@correo.com',
    #         'password' : 'test_password_linda',
    #     }
    #     c = Client()
    #     req = c.post(reverse(self.api_urls.get('login')),data= usr,  follow=True)
    #     self.assertEquals(req.status_code, 200, 'It was not possible to perform the request.')
    def test_api_user_stats_GET_basic_request(self):
        api_client = APIRequestFactory()
        req = api_client.get(reverse(self.api_urls.get('user_stats')), format='json')
        print('========================')
        print(str(req))
        print('========================')
        print(req.content_params)
        print('========================')
        print(req.content_type)
        print('========================')
        
















 