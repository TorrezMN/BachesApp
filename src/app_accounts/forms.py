from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from app_db.models import User
from app_db.models import User_Profile


# Extendemos del original
class New_User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class Login_Users_Form(AuthenticationForm):
    username = forms.CharField(
        required=True, min_length=6, label='<i class="fas fa-mail-bulk    "></i> Email')
    password = forms.CharField(required=True, min_length=8,
                               label='<i class="fa fa-unlock" aria-hidden="true"></i> Contraseña', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class Update_Profile_Form(ModelForm):
    class Meta:
        model = User_Profile
        fields = ['names', 'last_name', 'education_level', 'age', 'interest']
        widgets = {
            'interest': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        help_texts = {
            'interest': _('Describa el itenres que tiene en el sitio o simplemente sus intereses personales.'),
        }

 
class Update_User_Form_Admin(ModelForm):
    class Meta:
        model = User
        fields = ['is_staff', 'is_active','is_superuser','last_login', 'date_joined']
        widgets = {
            'interest': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        help_texts = {
            'interest': _('Describa el itenres que tiene en el sitio o simplemente sus intereses personales.'),
        }

 