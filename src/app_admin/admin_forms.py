from django.forms import ModelForm, Textarea
from app_db.models import Contact_Request
from django.utils.translation import gettext_lazy as _

class Editar_Caracteristica_Form(ModelForm):


	class Meta:		
		model = Contact_Request
		fields = ('contact_requests_status',)
		