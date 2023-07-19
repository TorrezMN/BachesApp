"""Baches_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


from app_public import views as public_views
from app_accounts import urls as accounts_urls


from django.views.generic import RedirectView
from django.conf.urls import url


from app_api import urls as api_urls
from app_admin import urls as admin_urls
from app_contributors import urls as contributor_urls


urlpatterns = [
    # path('admin/', admin.site.urls),
    # <=================================>#
    #            Api 		            #
    # <=================================>#
    path("api_V1/", include(api_urls)),
    # FAVICON
    path(r"favicon.ico", RedirectView.as_view(url="/static/img/favicon.ico")),
    # <=================================>#
    #            Public 		        #
    # <=================================>#
    path("", public_views.Public_Home.as_view(), name="public_home"),
    path(r"nosotros", public_views.Nosotros.as_view(), name="public_nosotros"),
    path(r"api", public_views.API.as_view(), name="public_api"),
    path(
        r"estadisticas", public_views.Estadisticas.as_view(), name="public_estadisticas"
    ),
    # <=================================>#
    #            Accounts    		    #
    # <=================================>#
    path("cuentas/", include(accounts_urls)),
    # <=================================>#
    #            Admin      		    #
    # <=================================>#
    path("admin/", include(admin_urls)),
    # <=================================>#
    #            Contributors     		#
    # <=================================>#
    path("contributor/", include(contributor_urls)),
    # <=================================>#
    #            Errores      		    #
    # <=================================>#
    path(
        r"error_cuentas_admin",
        public_views.Error_Cuentas_Admin.as_view(),
        name="error_cuentas_admin",
    ),
]


#  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
