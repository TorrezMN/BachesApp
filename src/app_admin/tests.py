from faker import Faker
from random import choice
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from app_db.models import User, User_Profile, Contact_Request, Caracteristicas
from .admin_forms import Editar_Caracteristica_Form
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class Admin_Views_Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email='test_email@correo.com', password='test_password_linda')
        self.client = Client()
        self.client.login(email='test_email@correo.com',
                          password='test_password_linda')
        self.admin_urls = {
            'home': 'admin_home',
            'listado_usuarios': 'admin_listado_usuarios',
            'estadisticas_usaurios': 'admin_estadisticas_usuarios',
            'solicitudes_de_contacto': 'admin_lista_solicitud_contacto',
            'ver_solicitud': 'admin_ver_solicitud',
            'editar_solicitud': 'admin_editar_solicitud',
            'listado_caracteristicas': 'admin_listado_de_caracteristicas',
            'ver_caracteristica': 'admin_ver_caracteristica',
            'mis_aportes': 'admin_mis_aportes',
            'lista_general_aportes': 'admin_lista_general_de_aportes',
            'mapa_general_aportes': 'admin_mapa_general_de_aportes',
            'descargar': 'admin_descargar',
            'ver_bache_mapa': 'admin_ver_bache_en_mapa',
        }
        f = Faker()
        # Create some users.
        for i in range(0, 10):
            User(email=f.email(), password='prueba_user').save()
        # Creating some contact requests.
        for i in range(0, 10):
            Contact_Request(
                full_name=f.name(),
                email=f.email(),
                message_body=f.text(),
                contact_requests_status=choice([1, 2, 3])
            ).save()
        # Creating some characteristics.
        for i in range(0, 10):
            Caracteristicas(
                usuario_solicitante=choice(User.objects.all()),
                caracteristica_estado=choice([0, 1, 2, 3, 4, 5]),
                descripcion=f.text(),
            ).save()
        self.solicitudes = Contact_Request.objects.all()
        self.caract = Caracteristicas.objects.all()
    def test_admin_home_GET(self):
        req = self.client.get(reverse(self.admin_urls.get('home')))
        self.assertEquals(req.status_code, 200, 'The URL can not be accessed.')
    def test_admin_home_GET_template_used(self):
        req = self.client.get(reverse(self.admin_urls.get('home')))
        self.assertTemplateUsed(req, 'admin_home.html',
                                'The Template received is not correct.')
    def test_admin_home_CONTEXT_head_title(self):
        req = self.client.get(reverse(self.admin_urls.get('home')))
        self.assertIsNotNone(req.context.get('head_title'),
                             'All pages must have title.')
    def test_admin_home_CONTEXT_head_title_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get('home')))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It must be a string.')
    def test_admin_home_CONTEXT_user_profile(self):
        req = self.client.get(reverse(self.admin_urls.get('home')))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must contain a User_Profile object.')
    def test_admin_home_CONTEXT_user_profile_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get('home')))
        self.assertIsInstance(req.context.get(
            'user_profile'), User_Profile, 'It does not correspond to the type of data.')
    def test_admin_listado_usuarios_GET(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_admin_listado_usuarios_GET_template_used(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertTemplateUsed(
            req, 'admin_listado_usuarios.html', 'It does not correspond to the template used.')
    def test_admin_listado_usuarios_GET_CONTEXT_has_user_profile(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must contain a User_Profile object.')
    def test_admin_listado_usuarios_GET_CONTEXT_user_profile_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertIsInstance(req.context.get('user_profile'), User_Profile,
                              'It does not correspond to the type of data of the response.')
    def test_admin_listado_usuarios_GET_CONTEXT_has_users(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertIsNotNone(req.context.get('users'),
                             'You must have a list of users.')
    def test_admin_listado_usuarios_GET_CONTEXT_has_users_length(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertTrue(len(req.context.get('users')) > 0,
                        'You must have at least one user in the list.')
    def test_admin_listado_usuarios_GET_CONTEXT_has_head_title(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The page must have a title.')
    def test_admin_listado_usuarios_GET_CONTEXT_head_title_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get('listado_usuarios')))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It does not correspond to the type of data.')
    def test_admin_estadisticas_usuarios_GET_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('estadisticas_usaurios')))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_admin_estadisticas_usuarios_GET_template_used(self):
        req = self.client.get(
            reverse(self.admin_urls.get('estadisticas_usaurios')))
        self.assertTemplateUsed(req, 'admin_estadisticas_usuarios.html',
                                'The template received does not correspond.')
    def test_admin_estadisticas_usuarios_CONTEXT_has_title(self):
        req = self.client.get(
            reverse(self.admin_urls.get('estadisticas_usaurios')))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The answer must have a title.')
    def test_admin_estadisticas_usuarios_CONTEXT_title_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('estadisticas_usaurios')))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It does not correspond to the type of data of the title.')
    def test_admin_estadisticas_usuarios_CONTEXT_has_user_profile(self):
        req = self.client.get(
            reverse(self.admin_urls.get('estadisticas_usaurios')))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'The answer must have a user_profile object. ')
    def test_admin_estadisticas_usuarios_CONTEXT_user_profile_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('estadisticas_usaurios')))
        self.assertIsInstance(req.context.get('user_profile'), User_Profile,
                              'It does not correspond to the type of USER_PROFILE data.')
    def test_admin_lista_solicitud_de_contacto_GET_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_admin_lista_solicitud_de_contacto_GET_template_used(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertTemplateUsed(req, 'admin_solicitud_contacto.html',
                                'It does not correspond to the tempered temlate.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_has_user_profile(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must contain a User_Profile object.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_user_profile_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertIsInstance(req.context.get(
            'user_profile'), User_Profile, 'It does not correspond to the type of data data.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_has_requests(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertIsNotNone(req.context.get('requests'),
                             'You must contain a list of contact requests.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_requests_list_size(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        # self.assertTrue(len(req.context.get('requests')) > 0,
        #                 'The list of requests must contain at least one element.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_has_title(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The answer must have a title.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_title_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'Does not correspond to the type of data received.')
    def test_admin_lista_solicitud_de_contacto_CONTEXT_title_has_content(self):
        req = self.client.get(
            reverse(self.admin_urls.get('solicitudes_de_contacto')))
        self.assertTrue(len(req.context.get('head_title')) > 0,
                        'The title must contain at least one character.')
    def test_admin_ver_solicitud_GET_basic_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_admin_ver_solicitud_GET_template_used(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertTemplateUsed(req, 'admin_ver_solicitud_contacto.html',
                                'The template received does not correspond.')
    def test_admin_ver_solicitud_GET_CONTEXT_has_title(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'head_title'), 'The answer does not have a title. You must have one.')
    def test_admin_ver_solicitud_GET_CONTEXT_title_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It does not correspond to the type of data of the title.')
    def test_admin_ver_solicitud_GET_CONTEXT_head_title_data_content(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.context.get(
            'head_title'), 'Solicitud de Contacto', 'The title received does not correspond.')
    def test_admin_ver_solicitud_GET_CONTEXT_user_isnot_none(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('user'),
                             'It does not correspond to the type of data.')
    def test_admin_ver_solicitud_GET_CONTEXT_user_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'user'), User, 'It does not correspond to the type of user data.')
    def test_admin_ver_solicitud_GET_CONTEXT_has_contact_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'contact_request'), 'You must contain a Contact Request object.')
    def test_admin_ver_solicitud_GET_CONTEXT_contact_request_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'contact_request'), Contact_Request, 'It does not correspond to the type of data received.')
    def test_admin_ver_solicitud_GET_CONTEXT_has_user_profile(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must contain a User_Profile object.')
    def test_admin_ver_solicitud_GET_CONTEXT_user_profile_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get('user_profile'), User_Profile,
                              'Do not correspond to the type of data.')
    def test_admin_ver_solicitud_GET_CONTEXT_has_object(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('object'),
                             'You must have an object that maps the request.')
    def test_admin_ver_solicitud_GET_CONTEXT_object_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('ver_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'object'), Contact_Request, 'It does not correspond to the type of data.')
    def test_editar_solicitud_GET_basic_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_editar_solicitud_GET_CONTEXT_has_title(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('head_title'))
    def test_editar_solicitud_GET_CONTEXT_title_is_string(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'Do not correspond to the type of data.')
    def test_editar_solicitud_GET_CONTEXT_title_value_coincides(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.context.get(
            'head_title'), 'Editar Solicitud de Contacto', 'The title received does not correspond.')
    def test_editar_solictud_GET_CONTEXT_has_context(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context, 'You must have a context object.')
    def test_editar_solicitud_GET_CONTEXT_has_form(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'form'), 'The answer must contain a form.')
    def test_editar_solicitud_GET_CONTEXT_form_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get('form'), Editar_Caracteristica_Form,
                              'It does not correspond to the type of data of the form.')
    def test_editar_solicitud_GET_CONTEXT_field_class(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'field_class'), str, 'It does not correspond to the type of data of the object.')
    def test_editar_solicitud_GET_CONTEXT_has_contact_request_object(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('object'),
                             'You must contain a Contact Request object.')
    def test_editar_solicitud_GET_CONTEXT_contact_request_object_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get('object'), Contact_Request,
                              'It does not correspond to the type of data of the object.')
    def test_editar_solicitud_GET_CONTEXT_has_form_show_errors(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'form_show_errors'), 'You must have a form-show-errors object.')
    def test_editar_solicitud_GET_CONTEXT_form_show_errors_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'form_show_errors'), bool, 'It does not correspond to the type of data received.')
    def test_editar_solicitud_GET_CONTEXT_form_has_user(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'user'), 'It must contain a user object.')
    def test_editar_solicitud_GET_CONTEXT_form_user_instance(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'user'), User,  'It does not correspond to the type of user data.')
    def test_editar_solicitud_GET_CONTEXT_has_field_template(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'field_template'), 'You must contain a Field-Template object.')
    def test_editar_solicitud_GET_CONTEXT_field_template_is_instance(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'field_template'), str, 'Do not correspond to the type of data received.')
    def test_editar_solicitud_GET_CONTEXT_has_contact_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get(
            'contact_request'), 'You must have a Contact-Request object.')
    def test_editar_solicitud_GET_CONTEXT_contact_request_is_instance(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get('contact_request'), Contact_Request,
                              'It does not correspond to the type of data received.')
    def test_editar_solicitud_GET_CONTEXT_has_option(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('option'),
                             'You must have an OPTION object.')
    def test_editar_solicitud_GET_CONTEXT_option_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get(
            'option'), dict, 'It does not correspond to the type of data received.')
    def test_editar_solicitud_GET_CONTEXT_option_data_content_length(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertTrue(len(req.context.get('option')) > 0,
                        'It must contain at least one element.')
    def test_editar_solicitud_GET_CONTEXT_option_data_content_name_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsInstance(req.context.get('option').get(
            'name'), str,  'It does not correspond to the type of data received.')
    def test_editar_solicitud_GET_CONTEXT_option_data_content_name_value(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.context.get('option').get(
            'name'), 'contact_requests_status', 'It does not correspond to the name received.')
    def test_editar_solicitud_GET_CONTEXT_option_data_content_type_isnot_none(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('option').get(
            'type'), 'You must have a type object.')
    def test_editar_solicitud_GET_CONTEXT_option_data_content_type_value(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.context.get('option').get(
            'type'), 'select', 'It does not correspond to the type of data received.')
    def test_editar_solicitud_GET_CONTEXT_option_has_template_name(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertIsNotNone(req.context.get('option').get(
            'template_name'), 'You must contain a Template-Name object.')
    def test_editar_solicitud_GET_CONTEXT_option_template_name_value(self):
        req = self.client.get(
            reverse(self.admin_urls.get('editar_solicitud'), kwargs={'pk': choice(self.solicitudes).id}))
        self.assertEquals(req.context.get('option').get('template_name'), 'django/forms/widgets/select_option.html',
                          'It does not correspond to the name of the temperate received.')
    def test_listado_de_caracteristicas_GET_basic_request(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_listado_de_caracteristicas_GET_basic_request_template_used(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertTemplateUsed(req, 'admin_listado_de_caracteristicas.html',
                                'It does not correspond to the template used.')
    def test_listado_de_caracteristicas_GET_CONTEXT_has_title(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The answer must contain a title.')
    def test_listado_de_caracteristicas_GET_CONTEXT_title_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It does not correspond to the type of data of the title.')
    def test_listado_de_caracteristicas_GET_CONTEXT_title_content(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertEquals(req.context.get('head_title'), 'Lista de Caracteristicas Solicitadas',
                          'It does not correspond to the content of the received title.')
    def test_listado_de_caracteristicas_GET_CONTEXT_title_lenght(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertTrue(len(req.context.get('head_title')) > 0,
                        'It does not correspond to the size of the title. You must have at least one character.')
    def test_listado_de_caracteristicas_GET_CONTEXT_has_user_profile(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'You must have a user-profile object.')
    def test_listado_de_caracteristicas_GET_CONTEXT_user_profile_data_type(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertIsInstance(req.context.get(
            'user_profile'), User_Profile, 'It does not correspond to the type of data received.')
    def test_listado_de_caracteristicas_GET_CONTEXT_has_caracteristicas(self):
        req = self.client.get(
            reverse(self.admin_urls.get('listado_caracteristicas')))
        self.assertIsNotNone(req.context.get(
            'caracteristicas'), 'You must convert a characteristic object.')
    def test_ver_caracteristicas_GET_basic_request(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertEquals(req.status_code, 200,
                          'It was not possible to access the resource.')
    def test_ver_caracteristicas_GET_template_used(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertTemplateUsed(req, 'admin_ver_solicitud_caracteristica.html',
                                'The template received does not correspond.')
    def test_ver_caracteristicas_GET_has_title(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('head_title'),
                             'The answer must have a title.')
    def test_ver_caracteristicas_GET_title_is_instance(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsInstance(req.context.get(
            'head_title'), str, 'It does not correspond to the type of data received.')
    def test_ver_caracteristicas_GET_title_is_equals(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertEquals(req.context.get(
            'head_title'), 'Caracteristica Solicitada', 'The title received does not correspond.')
    def test_ver_caracteristica_GET_CONTEXT_has_view(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get(
            'view'), 'The context object must have view. ')
    def test_ver_caracteristica_GET_CONTEXT_has_request(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('request'),
                             'The context object must have Request. ')
    def test_ver_caracteristica_GET_CONTEXT_has_DEFAULT_MESSAGE_LEVELS(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get(
            'DEFAULT_MESSAGE_LEVELS'), 'The Context object must have default_message_levels. ')
    def test_ver_caracteristica_GET_CONTEXT_DEFAULT_MESSAGE_LEVELS_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsInstance(req.context.get('DEFAULT_MESSAGE_LEVELS'),
                              dict, 'It does not correspond to the type of data received.')
    def test_ver_caracteristica_GET_CONTEXT_has_messages(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('messages'),
                             'The context object must have messages. ')
    def test_ver_caracteristica_GET_CONTEXT_has_False(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('False'),
                             'The context object must have false. ')
    def test_ver_caracteristica_GET_CONTEXT_False_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsInstance(req.context.get(
            'False'), bool, 'It does not correspond to the type of data of the object.')
    def test_ver_caracteristica_GET_CONTEXT_has_object(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('object'),
                             'The Context object must have Object. ')
    def test_ver_caracteristica_GET_CONTEXT_has_csrf_token(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('csrf_token'),
                             'The context object must have CSRF_TOKEN. ')
    def test_ver_caracteristica_GET_CONTEXT_has_True(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get(
            'True'), 'The Context object must have TRUE. ')
    def test_ver_caracteristica_GET_CONTEXT_has_user(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get(
            'user'), 'The Context object must have User. ')
    def test_ver_caracteristica_GET_CONTEXT_user_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsInstance(req.context.get(
            'user'), User, 'It does not correspond to the type of data received.')
    def test_ver_caracteristica_GET_CONTEXT_has_perms(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('perms'),
                             'The Context object must have percs. ')
    def test_ver_caracteristica_GET_CONTEXT_has_user_profile(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get('user_profile'),
                             'The Context object must have User_Profile. ')
    def test_ver_caracteristica_GET_CONTEXT_user_profile_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsInstance(req.context.get(
            'user_profile'), User_Profile, 'It does not correspond to the type of data received.')
    def test_ver_caracteristica_GET_CONTEXT_has_caracteristica(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsNotNone(req.context.get(
            'caracteristica'), 'The context object must be characteristic. ')
    def test_ver_caracteristica_GET_CONTEXT_caracteristica_data_type(self):
        req = self.client.get(reverse(self.admin_urls.get(
            'ver_caracteristica'), kwargs={'pk': choice(self.caract).id}))
        self.assertIsInstance(req.context.get('caracteristica'), Caracteristicas,
                              'It does not correspond to the type of data received.')
