from django.forms import ModelForm, Textarea



# Importing templates.
from app_db.models import Contact_Request


class Request_Contact_Form(ModelForm):
    

    class Meta:
    
        model = Contact_Request
        fields = ('full_name','email','message_body')
        widgets = {
            'message_body': Textarea(attrs={
                'rows': 2,
                'maxlength': 500,
                'placeholder': '500 digitos maximo.',
                }),
   }