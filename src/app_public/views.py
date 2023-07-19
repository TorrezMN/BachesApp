
import random
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView

# Importing DB models.
from app_db.models import Contact_Request


# Importing forms.
from .public_forms import Request_Contact_Form

class Public_Home(TemplateView):
    template_name = 'public_home.html'
    form = Request_Contact_Form()
    def get(self, request):
        cont = {
            'head_title': 'Home',
            'stats':{
                'total_contributors': random.randint(300,10000),
                'total_records': random.randint(300,10000),
            },
            'contact_form': Request_Contact_Form(),
        }
        return render(request, self.template_name, cont)
    

    def post(self, request):
        form = Request_Contact_Form(request.POST)
        c = {
            'head_title': 'Home',
            'contact_form': self.form,
        }
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(
                request, 'Recibimos su mensaje, nos estaremos comunicando en breve. Gracias :)')
            # return render(request, self.template_name, c)
            return redirect('/#section_contac_form', c)
        else:
            messages.error(request, form.errors)
            return redirect('/#section_contac_form', c)
            # return render(request, self.template_name, c)




class API (TemplateView):
    template_name = 'public_api.html'
class Nosotros (TemplateView):
    template_name = 'public_nosotros.html'
class Estadisticas (TemplateView):
    template_name = 'public_estadisticas.html'



"""
 
 ███████╗██████╗ ██████╗  ██████╗ ██████╗     ██████╗  █████╗  ██████╗ ███████╗███████╗
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝██╔════╝
 █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    ██████╔╝███████║██║  ███╗█████╗  ███████╗
 ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗    ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ╚════██║
 ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║    ██║     ██║  ██║╚██████╔╝███████╗███████║
 ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
                                                                                       
 
"""
class Error_Cuentas_Admin(TemplateView):
    template_name = 'error_cuentas_admin.html'



