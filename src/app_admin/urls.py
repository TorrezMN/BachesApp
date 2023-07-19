from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import Admin_Home
from .views import Admin_Listado_Usuarios

from .views import Admin_Estadisticas_Usaurios
from .views import Admin_Lista_Solicitud_Contacto
from .views import Admin_Ver_Solicitud
from .views import Admin_Lista_de_Aportes
from .views import Admin_Lista_General_Aportes
from .views import Admin_Ver_Bache
from .views import Admin_Mapa_General_Aportes
from .views import Admin_Descargar
from .views import Admin_Listado_de_Caracteristicas
from .views import Admin_Ver_Caracteristica
from .views import Admin_Editar_Solicitud


urlpatterns = [
    # path(r'ingresar', Admin_Home.as_view(), name='admin_home'),
    # path(r'registrarse', Registrarse.as_view(), name='accounts_registrarse'),
    
 
    path('', Admin_Home.as_view(), name='admin_home'),
    # Listado de Usuarios
    path(r'listado_usuarios', Admin_Listado_Usuarios.as_view(), name='admin_listado_usuarios'),
   
  
    # Estadisticas
    path(r'estadisticas_usuarios', Admin_Estadisticas_Usaurios.as_view(), name='admin_estadisticas_usuarios'),
    # Solicitud de contacto.
    path(r'listado_solicitud_de_contacto', Admin_Lista_Solicitud_Contacto.as_view(), name='admin_lista_solicitud_contacto'),
    path(r'admin_ver_solicitud/<int:pk>', Admin_Ver_Solicitud.as_view(), name='admin_ver_solicitud'),
    path(r'admin_editar_solicitud/<int:pk>', Admin_Editar_Solicitud.as_view(), name='admin_editar_solicitud'),
    # Caracteristicas
    path(r'admin_listado_de_caracteristicas', Admin_Listado_de_Caracteristicas.as_view(), name='admin_listado_de_caracteristicas'),
    path(r'admin_listado_de_caracteristicas/<int:pk>', Admin_Ver_Caracteristica.as_view(), name='admin_ver_caracteristica'),

    # Aportes
    path(r'admin_mis_aportes', Admin_Lista_de_Aportes.as_view(), name='admin_mis_aportes'),
    path(r'admin_todos_los_aportes', Admin_Lista_General_Aportes.as_view(), name='admin_lista_general_de_aportes'),
    path(r'admin_mapa_general', Admin_Mapa_General_Aportes.as_view(), name='admin_mapa_general_de_aportes'),
    path(r'admin_descargar', Admin_Descargar.as_view(), name='admin_descargar'),
    path(r'admin_ver_bache/<int:pk>', Admin_Ver_Bache.as_view(), name='admin_ver_bache_en_mapa'),


    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
