from random import choice
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


# from app_accounts.decorators import Admin_Required

# Importing Models
from app_db.models import Registro
from app_db.models import User
from app_db.models import Caracteristicas
from app_db.models import User_Profile

import pandas as pd

# Folium
import folium
from numpy import interp

# Forms 
from .contributor_forms import Solicitar_Caracteristica_Form





# HELPER FUNCTIONS

def get_registro_stats(id):
    """ Returns Retistro statistics. 
        Registro:
            user
            pothole_diameter
            pothole_depth
            pothole_quantity
            material_type_road
            road_type
            type_of_traffic
            pothole_coordinates
            registered_date
            
    """

    data = list(Registro.objects.filter(user=id).values())
    # data = list(Registro.objects.get(user=id).values())
    if(len(data)>0):
        df = pd.DataFrame(data)
    
        stat = {
                "total_aportes_general": len(Registro.objects.all()),
                "total_aportes": len(data),
                "pothole": {
                    "diametro": {
                        "media": int(df.pothole_diameter.mean()),
                        "max": df.pothole_diameter.max(),
                        "min": df.pothole_diameter.min(),
                    },
                    "profundidad": {
                        "media": int(df.pothole_depth.mean()),
                        "max": df.pothole_depth.max(),
                        "min": df.pothole_depth.min(),
    
                    },
                    "cantidad":{
                        "media" : int(df.pothole_quantity.mean()),
                        "max": df.pothole_quantity.max(),
                        "min": df.pothole_quantity.min(),
                    }
                    
                },
                "tipo_camino": {
                    "ruta": len(df.loc[df["road_type"] == 1]),
                    "vecinal": len(df.loc[df["road_type"] == 2]),
                    "nacional": len(df.loc[df["road_type"] == 3]),
                },
    
                "tipo_trafico":{
                    "mucho": len(df.loc[df["type_of_traffic"] == 1]),
                    "poco": len(df.loc[df["type_of_traffic"] == 2]),
                    "bajo"    : len(df.loc[df["type_of_traffic"] == 3]),
                },
                "tipo_material":{
                    "asfaltado": len(df.loc[df["material_type_road"] == 1]),
                    "tierra": len(df.loc[df["material_type_road"] == 1]),
                    "piedra": len(df.loc[df["material_type_road"] == 1]),
                }
        }
        return(stat)
    else:
        return (None)


@method_decorator([login_required], name='get')
class Contributor_Home(TemplateView):
    template_name ='contributor_home.html'

    def get(self, request):
        user_id = request.user.id
        
    
        cont = {
            'head_title': 'Contributor Desk',
            'stats': get_registro_stats(user_id), 
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'registros': Registro.objects.filter(user=user_id),

        }
        return render(request, self.template_name, cont)


@method_decorator([login_required], name='get')
class Contrib_Listado_de_Aportes(TemplateView):
    template_name = 'contributor_listado_de_aportes.html'

    def get(self, request):
        user_id = request.user.id

        cont = {
            'head_title': 'Lista de Aportes',
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'registros': Registro.objects.filter(user=user_id),
            'total_registros' : int(len(Registro.objects.all()))

        }
        return render(request, self.template_name, cont)




#  class Contrib_Listado_General_de_Aportes(TemplateView):
@method_decorator([login_required], name='get')
class Contrib_Listado_General_de_Aportes(ListView):
    template_name = 'contrib_listado_general_aportes.html'
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
            #  'head_title': 'Lista General de TEST OPAAAA',
            #  'user_profile': User_Profile.objects.get(profile_user=user_id),
            #  'registros': Registro.objects.all(),
#
        #  }
        #  return render(request, self.template_name, cont)





@method_decorator([login_required], name='get')
class Contrib_Ver_Bache(TemplateView):
    template_name = 'contrib_ver_bache.html'

    def get(self, request, pk):
        bache = Registro.objects.get(id=pk)
        user_id = request.user.id

        color = ''
        if(bache.pothole_depth>5):
            color = '#FF0000'
        else: 
            color = "#3186cc"
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
         
        folium.raster_layers.TileLayer("Open Street Map").add_to(m)
        folium.raster_layers.TileLayer("Stamen Terrain").add_to(m)
        folium.raster_layers.TileLayer("Stamen Toner").add_to(m)
        folium.raster_layers.TileLayer("Stamen Watercolor").add_to(m)
        folium.raster_layers.TileLayer("CartoDB Positron").add_to(m)
        folium.raster_layers.TileLayer("CartoDB Dark_Matter").add_to(m)
        
         
      
        folium.LayerControl().add_to(m)
        # folium.CircleMarker(
           
        #     location=[bache.pothole_coordinates.x,
        #               bache.pothole_coordinates.y],
        #     popup='Diametro: {0} \n Profundidad: {1} \n Cantidad: {2}'.format(
        #         bache.pothole_diameter,
        #         bache.pothole_depth,
        #         bache.pothole_quantity
        #         ),
        #     radius=interp(bache.pothole_diameter, [1, 100], [1, 10]),
        #     color=color,
        #     fill=True,
        #     fill_color="#3186cc"
           

        # ).add_to(m)
      
        tooltip = "<b>Mas Info!</b>"
        
        if(bache.pothole_depth>0.5):
            folium.Marker(
            location=[bache.pothole_coordinates.x, bache.pothole_coordinates.y],
            popup="<b>Diametro:</b> {0} mts. \n <b>Profundidad:</b> {1} mts. \n <b>Cantidad:</b> {2}".format(
            bache.pothole_diameter,
            bache.pothole_depth,
            bache.pothole_quantity),
            icon=folium.Icon(color = "red", icon="exclamation-triangle", prefix="fa"),
            tooltip=tooltip
            ).add_to(m)
        else: 
            folium.Marker(
            location=[bache.pothole_coordinates.x, bache.pothole_coordinates.y],
            popup="<b>Diametro:</b> {0} mts. \n <b>Profundidad:</b> {1} mts. \n <b>Cantidad:</b> {2}".format(
            bache.pothole_diameter,
            bache.pothole_depth,
            bache.pothole_quantity),
            icon=folium.Icon(color = "blue", icon="crosshairs", prefix="fa"),
            tooltip=tooltip
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
            'head_title': 'Ver de Bache',
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'bache': Registro.objects.get(id=pk),
            'map': figure,

        }
        return render(request, self.template_name, cont)






@method_decorator([login_required], name='get')
class Contrib_Descargar_Datos(TemplateView):
    template_name = 'contrib_descargar_data.html'
    
    def get(self, request):
        user_id = request.user.id


        cont = {
            'head_title': 'Lista General - Descargas',
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'registros': Registro.objects.all(),

        }
        return render(request, self.template_name, cont)
#
#





@method_decorator([login_required], name='get')
class Contrib_Ver_Mapa(TemplateView):
    template_name = 'contrib_mapa_gneral.html'

    def get(self, request):
        user_id = request.user.id
        baches = Registro.objects.all()
    

        figure = folium.Figure()
        initial_point = choice(baches)
        m = folium.Map(
            location=[initial_point.pothole_coordinates.x,initial_point.pothole_coordinates.y ],
        
            zoom_start=100,
 
            # Size of the map.
            width='92%',
            height='80%', 
            left='0%', 
            top='0%', 
            position='relative',
            control_scale=True, 
            prefer_canvas=True
        )
        m.add_to(figure)
        
        folium.raster_layers.TileLayer("Open Street Map").add_to(m)
        folium.raster_layers.TileLayer("Stamen Terrain").add_to(m)
        folium.raster_layers.TileLayer("Stamen Toner").add_to(m)
        folium.raster_layers.TileLayer("Stamen Watercolor").add_to(m)
        folium.raster_layers.TileLayer("CartoDB Positron").add_to(m)
        folium.raster_layers.TileLayer("CartoDB Dark_Matter").add_to(m)
        
         
      
        folium.LayerControl().add_to(m)

        # for i in baches:
        #     color = ''
        #     if(i.pothole_depth>5):
        #         color = '#FF0000'
        #     else: 
        #         color = "#3186cc"

        #     folium.CircleMarker(
        #         location=[i.pothole_coordinates.x,
        #               i.pothole_coordinates.y],
        #     popup='Diametro: {0} \n Profundidad: {1} \n Cantidad: {2}'.format(
        #         i.pothole_diameter,
        #         i.pothole_depth,
        #         i.pothole_quantity
        #         ),
        #     radius=interp(i.pothole_diameter, [1, 100], [1, 20]),

        #     color=color,
        #     fill=True,
        #     fill_color="#3186cc"
           

        # ).add_to(m)
        tooltip = "<b>Mas Info!</b>"
        for i in baches:
            if(i.pothole_depth>0.5):
                folium.Marker(
                         location=[i.pothole_coordinates.x, i.pothole_coordinates.y],
                         popup="<b>Diametro:</b> {0} mts. \n <b>Profundidad:</b> {1} mts. \n <b>Cantidad:</b> {2}".format(
                             i.pothole_diameter,
                             i.pothole_depth,
                             i.pothole_quantity),
                         icon=folium.Icon(color = "red", icon="exclamation-triangle", prefix="fa"),
                         tooltip=tooltip
                     ).add_to(m)
            else: 
                folium.Marker(
                    location=[i.pothole_coordinates.x, i.pothole_coordinates.y],
                    popup="<b>Diametro:</b> {0} mts. \n <b>Profundidad:</b> {1} mts. \n <b>Cantidad:</b> {2}".format(
                        i.pothole_diameter,
                        i.pothole_depth,
                        i.pothole_quantity),
                    icon=folium.Icon(color = "blue", icon="crosshairs", prefix="fa"),
                    tooltip=tooltip
                ).add_to(m)

                
            

        figure.render()

        cont = {
            'head_title': 'Mapa General',
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'bache': Registro.objects.all(),
            'map': figure,

        }
        return render(request, self.template_name, cont)








@method_decorator([login_required], name='get')
class Solicitar_Nueva_Caracteristica(TemplateView):
    template_name = 'contrib_solicitar_nueva_caracteristica.html'


    def get(self, request):
        user_id = request.user.id
        
    
        cont = {
            'head_title': 'Solicitar Nueva Caracteristica',
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'form': Solicitar_Caracteristica_Form(),

        }
        return render(request, self.template_name, cont)

    def post(self, request):
        descrip =  request.POST['descripcion']
        usr =  User.objects.get(id=request.user.id)
        estado =  0
        


        caract = Caracteristicas.objects.create(
                usuario_solicitante = usr,
                caracteristica_estado = estado,
                descripcion = descrip
            )
        caract.save()
        print('\n'*5)
        print('Se guardo del registor.')
        return redirect('../contributor') 





@method_decorator([login_required], name='get')
class Listado_de_Caracteristicas_Solicitadas(TemplateView):
    template_name = 'contrib_listado_de_caracteristicas_solicitadas.html'    

    def get(self, request):
        user_id = request.user.id
        user = request.user
    
        cont = {
            'head_title': 'Lista Solicitudes de Nuevas Caracteristicas ',
            'user_profile': User_Profile.objects.get(profile_user=user_id),
            'user': user,
            'caract': Caracteristicas.objects.all(),

        }
        return render(request, self.template_name, cont)
