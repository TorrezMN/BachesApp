from faker import Faker
from random import choice
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from app_db.models import User, User_Profile, Contact_Request, Caracteristicas
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class Admin_Views_Tests(TestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            email='test_email@correo.com', password='test_password_linda')
        self.client = Client()
        self.accounts_urls = {
            'ingresar': 'accounts_ingresar',
            'registrarse': 'accounts_registrarse',
            'salir': 'accounts_salir',
        }
        f = Faker()
        # Create some users.
        for i in range(0, 10):
            User(email=f.email(), password='prueba_user').save()
        self.profiles = User_Profile.objects.all()
    def test_ingresar_GET_basic_request(self):
        req = self.client.get(reverse(self.accounts_urls.get('ingresar')))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_registrarse_GET_basic_request(self):
        req = self.client.get(reverse(self.accounts_urls.get('registrarse')))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_salir_GET_basic_request(self):
        self.client.login(email='test_email@correo.com',
                          password='test_password_linda')
        req = self.client.get(
            reverse(self.accounts_urls.get('salir')), follow=True)
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
