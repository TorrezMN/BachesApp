from django.test import TestCase, Client
from django.urls import reverse

# PUBLIC URLS

# 'public_home'
# 'public_nosotros'
# 'public_api'
# 'public_estadisticas'
# 'error_cuentas_admin'

 

"""
 
 ████████╗███████╗███████╗████████╗███████╗
 ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
    ██║   █████╗  ███████╗   ██║   ███████╗
    ██║   ██╔══╝  ╚════██║   ██║   ╚════██║
    ██║   ███████╗███████║   ██║   ███████║
    ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝
                                           
 
"""


class Test_Public_VIEWS(TestCase):

    def setUp(self):
        self.client = Client()
        self.public_urls = {
            'home' :reverse('public_home'),
            'nosotros' :reverse('public_nosotros'),
            'api' :reverse('public_api'),
            'estadisticas' :reverse('public_estadisticas'),
            'error_cuentas' :reverse('error_cuentas_admin'),
        }
        
    
    def test_public_nosotros_GET(self):
        req = self.client.get(self.public_urls.get('nosotros'))
        self.assertEquals(req.status_code,200)
        self.assertTemplateUsed(req,'public_nosotros.html')
    
    
    def test_public_api_GET(self):
        req = self.client.get(self.public_urls.get('api'))
        self.assertEquals(req.status_code,200)
        self.assertTemplateUsed(req,'public_api.html')
    
    
    def test_public_estadisticas_GET(self):
        req = self.client.get(self.public_urls.get('estadisticas'))
        self.assertEquals(req.status_code,200)
        self.assertTemplateUsed(req,'public_estadisticas.html')
    
    def test_public_error_cuentas_GET(self):
        req = self.client.get(self.public_urls.get('error_cuentas'))
        self.assertEquals(req.status_code,200)
        self.assertTemplateUsed(req,'error_cuentas_admin.html')