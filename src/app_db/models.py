from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import datetime as dt
from rest_framework.authtoken.models import Token

# GEO
from django.contrib.gis import forms
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point




"""
 
 ██╗   ██╗███████╗██████╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     ███████╗
 ██║   ██║██╔════╝██╔══██╗    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     ██╔════╝
 ██║   ██║███████╗██████╔╝    ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     ███████╗
 ██║   ██║╚════██║██╔══██╗    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     ╚════██║
 ╚██████╔╝███████║██║  ██║    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗███████║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
                                                                                  
 
"""
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def get_email_name(self):
        return(self.email.split('@')[0])


    def get_user_data(self):
        data = {
            'user_id': self.id,
            'user_token': Token.objects.get(user=self.id).key,
        }
        
        return(data)


class User_Profile(models.Model):
    """
    Class representing the profile of the system user.
    ...
    Attributes
    ----------
    profile_user : int
        It corresponds to a relation 'fk' with the model 'User'.
    names : str
        Corresponds to the name or names of the user. Maximum of 50 characters.
    last_name : str
        Corresponds to the surname or surnames of the user. Maximum of 50 characters.
    education_level : int
        Integer representing the user's educational level. By default it is assigned the value 3.
    age : int
        It corresponds to the age of the system user.
    interest : str
        Describe the user's itinerary on the site. Maximum of 1500 characters.
    Methods
    -------
    its_new_user()
        Check if the user is new, calculating the difference between the current day and the registration day.
    get_full_name()
        Returns the full name of the user. Check the size of the string before returning the value.
    get_education_level_templates()
        Method to use in templates. Returns an html string with an awesome-icon.
    get_education_level_templates_basic()
        Same as get_education_level_templates (). Method to be used in templates. Returns an html string with an awesome-icon.
    """
    primary = 1
    secondary = 2
    academic = 3
    opciones_nivel_educativo = (
        (primary, 'Primario' ),
        (secondary, 'Secundario' ),
        (academic, 'Universitario' ),
    )
    profile_user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True)
    names = models.CharField('Nombre', max_length=50, blank=True)
    last_name = models.CharField('Apellido', max_length=50, blank=True)
    education_level = models.IntegerField(
        'Nivel Educativo', choices=opciones_nivel_educativo, default=academic)
    age = models.IntegerField('Edad', blank=True, null=True)
    interest = models.CharField(
        'Cual es su interes en el sitio?', max_length=1500, blank=True)
    def its_new_user(self):
        today = dt.today().date()
        if(today == self.profile_user.date_joined.date()):
            return("<i class='fa fa-leaf'  style='color:green;'></i> Si")
        else:
            return("<i class='fa fa-times' style='color:red;'></i> No")
    def get_full_name(self):
        full_name = self.last_name+', '+self.names
        if(len(full_name) <= 2):
            return(self.profile_user.get_email_name())
        else:
            return(full_name)
    def get_education_level_templates(self):
        levels = {
            1: "<center data-toggle='tooltip' title='Educacion Primaria'><i class='fa fa-graduation-cap'  style='color:#81D4FA;'></i></center>",  # 'primary'
            2: "<center  data-toggle='tooltip' title='Educacion Secundaria'><i class='fa fa-graduation-cap' style='color:#FFB74D;'></i><i class='fa fa-graduation-cap' style='color:#FFB74D;'></i></center>",  # 'secondary'
            3: "<center  data-toggle='tooltip' title='Educacion Universitaria'><i class='fa fa-graduation-cap' style='color:#81C784;'></i><i class='fa fa-graduation-cap' style='color:#81C784;'></i><i class='fa fa-graduation-cap' style='color:#81C784;'></i></center>",  # 'academic'
        }
        return(levels[self.education_level])
    def get_education_level_templates_basic(self):
        levels = {
            1: "<span class='education_label'  data-toggle='tooltip' title='Educacion Primaria'>Primaria</span>",
            2: "<span class='education_label'  data-toggle='tooltip' title='Educacion Secundaria'>Secundaria</span>",
            3: "<span class='education_label'  data-toggle='tooltip' title='Educacion Universitaria'>Universitaria</span>",
        }
        return(levels[self.education_level])
        # return('TEST EDUCACION!')

"""
 
  █████╗ ██████╗ ██████╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     ███████╗
 ██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     ██╔════╝
 ███████║██████╔╝██████╔╝    ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     ███████╗
 ██╔══██║██╔═══╝ ██╔═══╝     ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     ╚════██║
 ██║  ██║██║     ██║         ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗███████║
 ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
                                                                                 
 
"""
class Contact_Request(models.Model):
    """
    Class that corresponds to the 'contact requests' of the main page.
    ...
    Attributes
    ----------
    full_name : str
        It corresponds to the full name of the person requesting to be contacted. Maximum of 50 characters.
    email : str
        Corresponds to the contact email of the person requesting to be contacted. Maximum 100 characters.
    message_body : str
        Corresponds to the body of the contact request message. Maximum 500 characters.
    contact_requests_status : int
        Corresponds to the status of the 'contact request': seen, pending, important. By default it gets the value 2.
    fecha : date
        Corresponds to the date the application was registered. By default, the date it is received is saved.
    Methods
    -------
    get_status_for_template()
        Method to be used in templates. Returns an html string that specifies the status of the request.
    """
    seen = 1
    pending = 2
    important = 3
    contact_requests_status_choices = (
        (seen, 'Visto'),
        (pending, 'Pendiente'),
        (important, 'Importante'),
    )
    full_name = models.CharField('Nombre', max_length=50)
    email = models.EmailField('Email', max_length=100)
    message_body = models.CharField('Mensaje', max_length=500)
    contact_requests_status = models.IntegerField(
        choices=contact_requests_status_choices, blank=True, default=pending)
    fecha = models.DateTimeField('Fecha del Mensaje',  auto_now_add=True)
 
    def get_status_for_template(self):
        msg = {
            1: "<i style='font-weight: 2px;  color:green;' class='fa fa-check-circle-o'  data-toggle='tooltip' title='Visto'></i>",
            2: "<i style='font-weight: 2px;  color:orange;' class='fa fa-envelope-o'  data-toggle='tooltip' title='Pendiente'></i>",
            3: "<i style='font-weight: 2px;  color:red;' class='fa fa-exclamation-circle'  data-toggle='tooltip' title='Importante'></i>",
        }
        return(msg[self.contact_requests_status])
    def get_status_for_template_no_icon(self):
        msg = {
            1: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#388E3C;' class='label label-danger'> Visto</span>",
            2: "<span style='font-weight: 2px; font-size:15px; color: #A1887F;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#FFEE58;' class='label label-danger'> Pendiente</span>",
            3: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#ef5350;' class='label label-danger'> Importante</span>",
        }
        return(msg[self.contact_requests_status])

class Registro(models.Model):
    """
    Clase que corresponde al registro de cada bache.
    ...
    Attributes
    ----------
    user : int
        Key fk that corresponds to the id of the user who registers the pothole.
    pothole_diameter : float
        It corresponds to the average or individual diameter of each pothole.
    pothole_depth : float
        It corresponds to the individual or average depth of the potholes that are being registered.
    pothole_quantity : int
        It corresponds to the number of potholes to register. They can be one or more.
    material_type_road : int
        Integer value that corresponds to the type of road material where the potholes to be recorded are found. Default value 3.
    road_type : int
        Integer value that corresponds to the type of road on which the pothole (s) to be registered is located. Default value is 2.
    type_of_traffic : int
        Integer that corresponds to the type of traffic on the road where the potholes to be registered are located. Default value 2.
    pothole_coordinates : PointField
        Coordinate point that corresponds to the GPS position of the pothole location.
    registered_date : date
        It corresponds to the date on which the pothole was registered.
    Methods
    -------
    get_tipo_trafico_templates()
        Method to be used in templates. Returns an html string that specifies the status of the request.
    get_tipo_camino_templates()
        Method to be used in templates. Returns an html string depending on the type of path.
    get_tipo_material()
        Method to be used in templates. Returns an html string that represents the type of material.
    """


    fast_record = 0


    asfaltado = 1
    tierra = 2
    piedra = 3
    camino_tipo_material_options = (
        (fast_record, 'Reg. Rapido'),
        (asfaltado, 'asfaltado'),
        (tierra, 'tierra'),
        (piedra, 'piedra'),
    )
    ruta = 1
    vecinal = 2
    nacional = 3
    tipo_camino_options = (
        (fast_record, 'Reg. Rapido'),
        (ruta, 'ruta'),
        (vecinal, 'vecinal'),
        (nacional, 'nacional'),
    )
    mucho = 1
    poco = 2
    bajo = 3
    tipo_trafico_options = (
        (fast_record, 'Reg. Rapido'),
        (mucho, 'mucho'),
        (poco, 'poco'),
        (bajo, 'bajo'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_fast_record = models.BooleanField(default=False)
    pothole_diameter = models.FloatField('Diametro')
    pothole_depth = models.FloatField('Profundidad')
    pothole_quantity = models.IntegerField('Cantidad')
    material_type_road = models.IntegerField(
        'Tipo de Material',  choices=camino_tipo_material_options, default=piedra, null=True, help_text='Seleccione el tipo de material del camino.')
    road_type = models.IntegerField(
        'Tipo de Camino',  choices=tipo_camino_options, default=vecinal, null=True, help_text='Seleccione el tipo de camino.')
    type_of_traffic = models.IntegerField(
        'Tipo de Trafico',  choices=tipo_trafico_options, default=poco, null=True, help_text='Seleccione el tipo de trafico.')
    pothole_coordinates = models.PointField(
        geography=True, default=Point(0.0, 0.0))
    registered_date = models.DateTimeField(auto_now_add=True)

    def get_tipo_trafico_templates(self):
        tipo_trafico = {
            0: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#22A39F;' class='label'><i class='fa fa-clock'></i> RR</span>",
            1: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:red;' class='label label-danger'><i class='fa fa-exclamation'></i> Mucho</span>",
            2: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:orange;' class='label label-warning'><i class='fa fa-thumbs-o-down'></i> Poco</span>",
            3: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:green;' class='label label-info'><i class='fa fa-thumbs-up'></i> Bajo</span>",
        }
        return(tipo_trafico[self.type_of_traffic])
    def get_tipo_camino_templates(self):
        tipo_camino = {
            0: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#22A39F;' class='label'><i class='fa fa-clock'></i> RR</span>",
            1: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#73879c;' class='label label-danger'> Ruta</span>",
            2: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#73879c;' class='label label-warning'> Vecinal</span>",
            3: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#73879c;' class='label label-info'> Nacional</span>",
        }
        return(tipo_camino[self.road_type])
    def get_tipo_material(self):
        tipo_material = {
            0: "<span style='font-weight: 2px; font-size:15px; color: white;margin:0 auto; padding:3px 5px 3px 5px; border-radius:5px; background:#22A39F;' class='label'><i class='fa fa-clock'></i> RR</span>",
            1: "<span style=' color: white; padding: 3px 5px  3px 5px; border-radius:5px; background:#212f3d;'> asfaltado</span>",
            2: "<span style=' color: white; padding: 3px 5px  3px 5px; border-radius:5px; background:#a04000;'> tierra</span>",
            3: "<span style=' color: white; padding: 3px 5px  3px 5px; border-radius:5px; background: #99a3a4;'> piedra</span>",
        }
        return(tipo_material[self.material_type_road])

class Caracteristicas(models.Model):
    """
    Class that corresponds to the 'requests for new features' that users can make.
    ...
    Attributes
    ----------
    usuario_solicitante : int
        Integer representing an 'fk' to the User table.
    caracteristica_estado : int
        Represents the state of the 'requested feature'. Gets the value 0 by default.
    descripcion : str
        It corresponds to the description of the characteristic requested by the user. Maximum 500 characters.
    caracteristica_registered_date : date
        It corresponds to the date the order was placed. It is completed automatically with the date of the day.
    Methods
    -------
    get_estado_template_tag()
        Method to be used in templates. Returns an html string with styles according to the status of the request.
    """
    recibido = 0
    visto = 1
    confirmado = 2
    en_desarrollo = 3
    en_produccion = 4
    rechazado = 5
    caracteristica_choices = (
        (recibido, 'Recibido'),
        (visto, 'Visto'),
        (confirmado, 'Confirmado'),
        (en_desarrollo, 'en desarrollo'),
        (en_produccion, 'en produccion'),
        (rechazado, 'Rechazado'),
    )
    usuario_solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    caracteristica_estado = models.IntegerField(
        'Estado', default=recibido, choices=caracteristica_choices)
    descripcion = models.CharField('Descripcion', max_length=500)
    caracteristica_registered_date = models.DateTimeField(auto_now_add=True)
    def get_estado_template_tag(self):
        options_dict = {
            0: "<span style='color:whitesmoke; padding: 4px 3px 4px 3px; border-radius:4px; background:purple'>Recibido</span>",
            1: "<span style='color:whitesmoke; padding: 4px 3px 4px 3px; border-radius:4px; background:blue'>Visto</span>",
            2: "<span style='color:whitesmoke; padding: 4px 3px 4px 3px; border-radius:4px; background:green'>Confirmado</span>",
            3: "<span style='color:whitesmoke; padding: 4px 3px 4px 3px; border-radius:4px; background:brown'>En Desarrollo</span>",
            4: "<span style='color:#424242; padding: 4px 3px 4px 3px; border-radius:4px; background:pink'>En Produccion</span>",
            5: "<span style='color:whitesmoke; padding: 4px 3px 4px 3px; border-radius:4px; background:red'>Rechazado</span>",
        }
        return(options_dict[int(self.caracteristica_estado)])
