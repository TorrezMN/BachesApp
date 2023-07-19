from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
 
from rest_framework.authtoken import views as rest_framework_views

from .views import API_STATUS
from .views import User_Stats
from .views import Caracteristicas_Stats
from .views import Caracteristicas_List
from .views import Registros_List
from .views import Registros_New
from .views import Registros_Stats

from .views import Register_User
from .views import Login_User

"""
Stats Models
    User_Profile
    Contact_Request
    Registro
    Caracteristicas
"""
urlpatterns = [
    
    path(r'api_status', API_STATUS.as_view(), name='api_status'),
    # REGISTRATION AND LOGIN
    path(r'api-token-auth', rest_framework_views.obtain_auth_token),
    path(r'register_user', Register_User.as_view(), name='api_register_user'),
    path(r'login_user', Login_User.as_view(), name='api_login_user'),
    # User Stats
    path(r'user_stats', User_Stats.as_view(), name='api_user_stats'),
    # Caracteristicas Stats
    path(r'caracteristicas_stats', Caracteristicas_Stats.as_view(), name='api_caracteristicas_stats'),
    
    # List Urls
    path(r'caracteristicas_list', Caracteristicas_List.as_view(), name='api_caracteristicas_list'),


    # Registro Urls
    path(r'registro_list', Registros_List.as_view(), name='api_registros_list'),
    path(r'registro_new', Registros_New.as_view(), name='api_registro_new'),
    path(r'registro_stats', Registros_Stats.as_view(), name='api_registro_stats'),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
