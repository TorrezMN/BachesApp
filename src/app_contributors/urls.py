from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import Contributor_Home
from .views import Contrib_Listado_de_Aportes
from .views import Contrib_Listado_General_de_Aportes
from .views import Contrib_Ver_Bache
from .views import Contrib_Descargar_Datos
from .views import Contrib_Ver_Mapa
from .views import Solicitar_Nueva_Caracteristica
from .views import Listado_de_Caracteristicas_Solicitadas


urlpatterns = [
    
    
 
    path('', Contributor_Home.as_view(), name='contrib_home'),
    # Listado de aportes.
    path(r'listado_de_aportes', Contrib_Listado_de_Aportes.as_view(), name='contrib_listado_de_aportes'),
    # Listado general de aportes.
    path(r'listado_general_de_aportes', Contrib_Listado_General_de_Aportes.as_view(), name='contrib_listado_general_de_aportes'),
    # Ver Bache.
    path(r'ver_bache/<int:pk>', Contrib_Ver_Bache.as_view(), name='admin_ver_bache'),
    # Descargar datos.
    path(r'descargar_datos', Contrib_Descargar_Datos.as_view(), name='contrib_descargar_datos'),
    # Ver Mapa General.
    path(r'ver_mapa', Contrib_Ver_Mapa.as_view(), name='contrib_ver_mapa'),
    # Solicitar nuevas caracteristicas.
    path(r'solicitar_nueva_caracteristica', Solicitar_Nueva_Caracteristica.as_view(), name='contrib_solicitar_nueva_caracteristica'),
    # Ver listado de caracteristicas solicitadas.
    path(r'Listado_de_Caracteristicas_Solicitadas', Listado_de_Caracteristicas_Solicitadas.as_view(), name='contrib_listado_de_caracteristicas_solicitadas'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
