from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import Ingresar
from .views import Registrarse
from .views import Logout
from .views import Detalle_Usuario
from .views import Delete_Usuario
from .views import Editar_Usuario
from .views import Editar_Perfil


urlpatterns = [
 
    # path('', public_views.Public_Home.as_view(), name='public_home'),
    
    path(r'ingresar', Ingresar.as_view(), name='accounts_ingresar'),
    path(r'registrarse', Registrarse.as_view(), name='accounts_registrarse'),
    path(r'salir', Logout.as_view(), name='accounts_salir'),
    

    # PROFILES
    path(r'detalle_usuario/<int:pk>', Detalle_Usuario.as_view(), name='accounts_detalle_usuario'),
    path(r'eliminar_usuario/<int:pk>', Delete_Usuario.as_view(), name='accounts_delete_usuario'),
    path(r'editar_usuario/<int:pk>', Editar_Usuario.as_view(), name='accounts_editar_usuario'),
    path(r'editar_perfil/<int:pk>', Editar_Perfil.as_view(), name='accounts_editar_perfil'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 