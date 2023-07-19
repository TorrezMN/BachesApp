import json
from random import choice

import pandas as pd
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
# Importing Models
from app_db.models import User
from app_db.models import User_Profile
from app_db.models import Contact_Request
from app_db.models import Registro
from app_db.models import Caracteristicas

# Importing Forms
from .admin_forms import Editar_Caracteristica_Form

# Folium
import folium
from numpy import interp
# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from app_accounts.decorators import Admin_Required

from django.views.generic import ListView

# HELPER FUNCTIONS
def get_user_profile(id):
    return (User_Profile.objects.get(profile_user=id))


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
    data = list(User_Profile.objects.exclude(
        profile_user=request.user.id).values())
    df = pd.DataFrame(data)



    if(len(data) > 0):
        return({
            'total_users_count': len(User_Profile.objects.all()),
            'age': {
                'media': str(int(df.age.fillna(0).mean())),
                'max': str(int(df.age.fillna(0).max())),
                'min': str(int(df.age.fillna(0).min())),
            },
            'education_level': {
                'primary': len(df[df.education_level == 1]),
                'secondary': len(df[df.education_level == 2]),
                'academic': len(df[df.education_level == 3]),
            }
        })
    else:
        return(None)


def get_solicitudes_stats():
    """ Returns Contact_Request statistics.
        solicitudes:
            full_name
            email
            message_body
            contact_requests_status
            fecha
    """
    data = list(Contact_Request.objects.all().values())
    # data = list(Registro.objects.get(user=id).values())
    df = pd.DataFrame(data)
    if(len(df) > 0):
        return (
            {'total': len(df),
            'contact_requests_status': {
                'Visto': len(df[df.contact_requests_status == 1]),
                'Pendiente': len(df[df.contact_requests_status == 2]),
                'Importante': len(df[df.contact_requests_status == 3]),
            }
            }
        )
    else:
        return(None)


def get_caracteristicas_stats():
    """ Returns statistics on 'Characteristics'.
    Caracteristicas:
        usuario_solicitante
        caracteristica_estado
        descripcion
    """
    data = list(Caracteristicas.objects.all().values())
    df = pd.DataFrame(data)
    if (len(df) > 0):
        caracteristica_choices = {
        0: 'Recibido',
        1: 'Visto',
        2: 'Confirmado',
        3: 'en desarrollo',
        4: 'en produccion',
        5: 'Rechazado',
         }
        solicitudes= json.loads(df.usuario_solicitante_id.value_counts().sort_index().to_json())
        estado = json.loads(df.caracteristica_estado.value_counts().sort_index().to_json())
        vals_solicitudes_users = []
        vals_solicitudes_estado = []
        for i in solicitudes:
            vals_solicitudes_users.append([get_user_profile(i).profile_user.email,solicitudes[i]])
        for i in estado:
            vals_solicitudes_estado.append([caracteristica_choices[int(i)],estado[i]])

      
        
        return(
            { 
                'total_solicitudes': len(data),
                'caracteristicas_usuarios':vals_solicitudes_users,
                'caracteristicas_estado': vals_solicitudes_estado,
        
        })
    else:
        return(None)




@method_decorator([login_required, Admin_Required], name='get')
class Admin_Home(TemplateView):
    template_name = 'admin_home.html'
    def get(self, request):
        cont = {
            'head_title': 'Administracion',
            'user_profile': get_user_profile(request.user.id),
            'user_stats': get_user_stats(request),
            'solicitudes_stats': get_solicitudes_stats(),
            'caracteristicas_stats': get_caracteristicas_stats(),
        }
        return render(request, self.template_name, cont)
# USUARIOS
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Listado_Usuarios(ListView):
    """Controls the 'user list' view. It allows to display a complete list of users."""
    template_name = 'admin_listado_usuarios.html'
    paginate_by = 100
    model = User_Profile
    context_object_name = "users"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_registros'] = int(len(Registro.objects.all()))
        #  context['user_profile'] = get_user_profile(request.user.id)
        context['head_title'] = 'Listado de Usuarios'
        return context


    #  def get(self, request):
        #  cont = {
            #  'user_profile': get_user_profile(request.user.id),
            #  'users': User_Profile.objects.exclude(profile_user=request.user.id),
            #  'head_title': 'Lista de Usuarios',
        #  }
        #  return render(request, self.template_name, cont)
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Estadisticas_Usaurios(TemplateView):
    template_name = 'admin_estadisticas_usuarios.html'
    def get(self, request):
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'user_stats': get_user_stats(request),
            'head_title': 'Estadisticas Usuarios',
        }
        return render(request, self.template_name, cont)
# CONTACT
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Lista_Solicitud_Contacto(TemplateView):
    template_name = 'admin_solicitud_contacto.html'
    def get(self, request):
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'requests': Contact_Request.objects.all(),
            'stats_solicitudes': get_solicitudes_stats(),
            'head_title': 'Lista Solicitud de Contacto',
        }
        return render(request, self.template_name, cont)
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Ver_Solicitud(DetailView):
    template_name = 'admin_ver_solicitud_contacto.html'
    model = Contact_Request
    context_object_name = 'contact_request'
    queryset = Contact_Request.objects.all()
    extra_context = {
        'head_title': 'Solicitud de Contacto',
    }
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['user_profile'] = get_user_profile(self.request.user.id)
        return context


@method_decorator([login_required, Admin_Required], name='get')
class Admin_Editar_Solicitud(UpdateView):
    template_name = ''
    form = Editar_Caracteristica_Form()
    model = Contact_Request
    form_class = Editar_Caracteristica_Form
    success_message = "El perfil de usuario fue actualizado correctamente."
    extra_context = {
        'head_title': 'Editar Solicitud de Contacto',
    }
        

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    
        self.template_name = 'admin_edit_contact_request.html'
        

        return context

    def get_success_url(self, **kwargs):
        return (reverse('admin_lista_solicitud_contacto'))
        


# APORTES
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Ver_Bache(TemplateView):
    template_name = 'admin_ver_bache.html'
    def get(self, request, pk):
        bache = Registro.objects.get(id=pk)
        color = ''
        if(bache.pothole_depth > 5):
            color = '#FF0000'
        else:
            color = "#3186cc"
        figure = folium.Figure()
        m = folium.Map(
            location=[bache.pothole_coordinates.x,
                      bache.pothole_coordinates.y],
            zoom_start=100,
            # tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            tiles='Stamen Toner',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            # Size of the map.
            width='92%',
            height='80%',
            left='0%',
            top='0%',
            position='relative'
        )
        m.add_to(figure)
        folium.CircleMarker(
            location=[bache.pothole_coordinates.x,
                      bache.pothole_coordinates.y],
            popup='Diametro: {0} \n Profundidad: {1} \n Cantidad: {2}'.format(
                bache.pothole_diameter,
                bache.pothole_depth,
                bache.pothole_quantity
            ),
            radius=interp(bache.pothole_diameter, [1, 100], [1, 10]),
            color=color,
            fill=True,
            fill_color="#3186cc"
        ).add_to(m)
        figure.render()
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'head_title': 'Ver de Bache',
            'bache': Registro.objects.get(id=pk),
            'map': figure,
        }
        return render(request, self.template_name, cont)
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Mapa_General_Aportes(TemplateView):
    template_name = 'admin_mapa_gneral.html'
    def get(self, request):
        baches = Registro.objects.all()
        # print('\n')
        # print('\n')
        # print('\n')
        # print('\n')
        # print('BACHE----------->', bache.pothole_coordinates.x)
        # print('BACHE----------->', bache.pothole_coordinates.y)
        # print('\n')
        # print('\n')
        # print('\n')
        # print('\n')
        figure = folium.Figure()
        initial_point = choice(baches)
        m = folium.Map(
            location=[initial_point.pothole_coordinates.x,initial_point.pothole_coordinates.y ],
            zoom_start=100,
            # tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            tiles='Stamen Toner',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            # Size of the map.
            width='92%',
            height='80%',
            left='0%',
            top='0%',
            position='relative'
        )
        m.add_to(figure)
        for i in baches:
            color = ''
            if(i.pothole_depth > 5):
                color = '#FF0000'
            else:
                color = "#3186cc"
            folium.CircleMarker(
                location=[i.pothole_coordinates.x,
                          i.pothole_coordinates.y],
                popup='Diametro: {0} \n Profundidad: {1} \n Cantidad: {2}'.format(
                    i.pothole_diameter,
                    i.pothole_depth,
                    i.pothole_quantity
                ),
                radius=interp(i.pothole_diameter, [1, 100], [1, 20]),
                color=color,
                fill=True,
                fill_color="#3186cc"
            ).add_to(m)
        # folium.Marker(
        #     location=[bache.pothole_coordinates.x, bache.pothole_coordinates.y],
        #     popup='Diametro: {0} \n Profundidad: {1} \n Cantidad: {2}'.format(
        #         bache.pothole_diameter,
        #         bache.pothole_depth,
        #         bache.pothole_quantity),
        #     icon=folium.Icon(icon='cloud')
        # ).add_to(m)
        figure.render()
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'head_title': 'Mapa General',
            'bache': Registro.objects.all(),
            'map': figure,
        }
        return render(request, self.template_name, cont)
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Lista_de_Aportes(TemplateView):
    template_name = 'admin_listado_de_aportes.html'
    def get(self, request):
        user_id = request.user.id
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'head_title': 'Lista de Aportes',
            'registros': Registro.objects.filter(user=user_id),
        }
        return render(request, self.template_name, cont)

@method_decorator([login_required, Admin_Required], name='get')
class Admin_Lista_General_Aportes(ListView):
    template_name = 'admin_listado_general_aportes.html'

    paginate_by = 50
    model = Registro
    context_object_name = "registros"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_registros'] = int(len(Registro.objects.all()))
        return context



     
    #  def get(self, request):
        #  user_id = request.user.id
        #  cont = {
            #  'user_profile': get_user_profile(request.user.id),
            #  'head_title': 'Lista General de Aportes',
            #  'registros': Registro.objects.all(),
        #  }
        #  return render(request, self.template_name, cont)




@method_decorator([login_required, Admin_Required], name='get')
class Admin_Descargar(TemplateView):
    template_name = 'admin_descargas.html'
    def get(self, request):
        user_id = request.user.id
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'head_title': 'Lista General - Descargas',
            'registros': Registro.objects.all(),
        }
        return render(request, self.template_name, cont)
# CARACTERISTICAS
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Listado_de_Caracteristicas(TemplateView):
    template_name = 'admin_listado_de_caracteristicas.html'
    def get(self, request):
        user_id = request.user.id
        cont = {
            'user_profile': get_user_profile(request.user.id),
            'head_title': 'Lista de Caracteristicas Solicitadas',
            'caracteristicas': Caracteristicas.objects.all(),
        }
        return render(request, self.template_name, cont)
@method_decorator([login_required, Admin_Required], name='get')
class Admin_Ver_Caracteristica(DetailView):
    template_name = 'admin_ver_solicitud_caracteristica.html'
    model = Caracteristicas
    context_object_name = 'caracteristica'
    queryset = Caracteristicas.objects.all()
    extra_context = {
        'head_title': 'Caracteristica Solicitada',
    }
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['user_profile'] = get_user_profile(self.request.user.id)
        return context
