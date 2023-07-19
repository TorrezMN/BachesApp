from django.forms import ModelForm, Textarea
from app_db.models import Caracteristicas
from django.utils.translation import gettext_lazy as _

class Solicitar_Caracteristica_Form(ModelForm):


	class Meta:
		model = Caracteristicas
		fields = ('descripcion',)
		widgets = {
            'descripcion': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
		help_texts = {
            'descripcion': _('Describa claramente las caracteristicas que desea incorporar.'),
        }