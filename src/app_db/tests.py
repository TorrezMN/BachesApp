from django.test import TestCase
from .models import User, User_Profile, Contact_Request, Caracteristicas
from faker import Faker
from random import choice
from django.core.validators import validate_email
import datetime
from django.core.exceptions import ValidationError
"""
 ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗     ███████╗██╗   ██╗███╗   ██╗ ██████╗
 ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║   ██║████╗  ██║██╔════╝
 ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝    █████╗  ██║   ██║██╔██╗ ██║██║     
 ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗    ██╔══╝  ██║   ██║██║╚██╗██║██║     
 ██║  ██║███████╗███████╗██║     ███████╗██║  ██║    ██║     ╚██████╔╝██║ ╚████║╚██████╗
 ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝
"""


def check_email(email):
    try:
        validate_email(email)
        return (True)
    except ValidationError:
        return (False)


def check_clean_message_body(message):
    forbidden_words = ['select', 'delete', '<', '>']
    is_ok = True
    for i in forbidden_words:
        if (i in message):
            is_ok = False
    return(is_ok)


"""
 ████████╗███████╗███████╗████████╗███████╗
 ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
    ██║   █████╗  ███████╗   ██║   ███████╗
    ██║   ██╔══╝  ╚════██║   ██║   ╚════██║
    ██║   ███████╗███████║   ██║   ███████║
    ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝
"""


class UserModelTest(TestCase):
    def setUp(self):
        f = Faker()
        for i in range(0, 10):
            User(email=f.email(), password='prueba_user').save()
        self.users = User.objects.all()

    def test_user_createion_length(self):
        self.assertEquals(self.users.count(
        ), 10, 'Error in the creation of test users. The size does not match.')

    def test_username_None(self):
        for i in self.users:
            self.assertIsNone(
                i.username, 'Error username. It must be equal to -> None.')

    def test_check_email_length(self):
        for i in self.users:
            self.assertTrue(len(i.email) >= 8,
                            'The size of the email address is less than 8.')

    def test_get_email_name_method(self):
        for i in self.users:
            self.assertIsInstance(i.get_email_field_name(
            ), str, 'Fails in the email name. It does not correspond to the type of data. It must be string.')

    def test_type_get_user_data_method(self):
        for i in self.users:
            self.assertIsInstance(i.get_user_data(), dict,
                                  'Incorrect user data type. It must be dict.')

    def test_user_token_from_user_data_method(self):
        for i in self.users:
            self.assertTrue(len(i.get_user_data().get('user_token'))
                            > 20, 'The size of the user token is incorrect.')


class User_Profile_Model_Test(TestCase):
    def setUp(self):
        f = Faker()
        for i in range(0, 10):
            User(email=f.email(), password='prueba_user').save()
        self.users_profiles = User_Profile.objects.all()

    def test_profile_user_id_not_zero(self):
        for i in self.users_profiles:
            self.assertTrue(i.profile_user.id > 0, 'Error in user IDs.')

    def test_profile_creation_size(self):
        self.assertEquals(self.users_profiles.count(
        ), 10, 'Error the creation of user profiles. Size does not match users.')

    def test_names_data_type(self):
        for i in self.users_profiles:
            self.assertIsInstance(
                i.names, str, 'The type of data does not match. It must be string.')

    def test_last_name_data_type(self):
        for i in self.users_profiles:
            self.assertIsInstance(
                i.last_name, str, 'The type of data does not match. It must be string.')

    def test_education_level_data_type(self):
        for i in self.users_profiles:
            self.assertIsInstance(
                i.education_level, int, 'The type of data does not match. It must be integer.')

    def test_age_data_type(self):
        for i in self.users_profiles:
            self.assertIsNone(
                i.age, 'Profile recently created. It should not have age.')

    def test_interest_data_type(self):
        for i in self.users_profiles:
            self.assertIsInstance(
                i.interest, str, 'The type of data does not match. It must be string type.')
    # Testing methods.

    def test_is_new_user_method(self):
        for i in self.users_profiles:
            self.assertTrue(
                i.its_new_user(), 'Error user_nuevo. Newly created users. It must be true.')

    def test_get_education_level_templates_method(self):
        for i in self.users_profiles:
            self.assertIsInstance(i.get_education_level_templates(
            ), str, 'Data type error. It must be String.')

    def test_get_education_level_templates_method_response_length(self):
        for i in self.users_profiles:
            self.assertTrue(len(i.get_education_level_templates())
                            > 0, 'Data length error. It must be a long string.')

    def test_get_education_level_templates_method_response_is_valid_html_tag(self):
        for i in self.users_profiles:
            self.assertTrue('<' in i.get_education_level_templates() or '>' in i.get_education_level_templates(
            ), 'Error in the chain. It is not a tag for templates.')

    def test_get_education_level_templates_basci_method(self):
        for i in self.users_profiles:
            self.assertIsInstance(i.get_education_level_templates_basic(
            ), str, 'Error in data type. It must be string.')

    def test_get_eduacation_level_template_basic_method_response_lenght(self):
        for i in self.users_profiles:
            self.assertTrue(len(i.get_education_level_templates_basic(
            )) > 0, 'Data length error. It must be a long string.')

    def test_get_education_level_template_basic_method_response_is_html_tag(self):
        for i in self.users_profiles:
            self.assertTrue('<' in i.get_education_level_templates_basic(
            ) or '>' in i.get_education_level_templates(), 'Error in the chain. It is not a tag for templates.')


class Contact_Request_Model_Test(TestCase):
    def setUp(self):
        f = Faker()
        for i in range(0, 10):
            Contact_Request(
                full_name=f.name(),
                email=f.email(),
                message_body=f.text(),
                contact_requests_status=2
            ).save()
        self.contact_requests = Contact_Request.objects.all()

    def test_verify_load_size(self):
        self.assertTrue(len(self.contact_requests) == 10,
                        'ERROR: Load size. Do not match the specified size and loaded size.')

    def test_check_full_name(self):
        for i in self.contact_requests:
            self.assertIsInstance(
                i.full_name, str, 'Contact Request - Full Name: Type of invalid data. Debe ser a string.')

    def test_check_full_name_length(self):
        for i in self.contact_requests:
            self.assertTrue(len(i.full_name) > 0,
                            'Contact Request - Full Name: Must contain name.')

    def test_check_email(self):
        for i in self.contact_requests:
            self.assertTrue(
                '@' in i.email, 'Contact Request - Email: It is not an email address.')

    def test_check_email_data_type(self):
        for i in self.contact_requests:
            self.assertIsInstance(
                i.email, str, 'Contact Request - Email: It does not correspond to the type of data. It must be string.')

    def test_check_email_length_size(self):
        for i in self.contact_requests:
            self.assertTrue(len(
                i.email) >= 8, 'Contact Request - Email:It does not correspond to the length of the email address. It must be greater than or equal to 8.')

    def test_check_email_is_valid(self):
        for i in self.contact_requests:
            self.assertTrue(check_email(
                i.email), 'Contact Request - Email: It is not a valid email address.')

    def test_message_body(self):
        for i in self.contact_requests:
            self.assertIsInstance(
                i.message_body, str, 'Contact Request - Message Body: The type of data is not correct. It must contain a Strign.')

    def test_message_body_length(self):
        for i in self.contact_requests:
            self.assertTrue(len(i.message_body) > 0,
                            'Contact Request - Message Body: The size of the message is not correct. You must contain at least 1 word. ')

    def test_message_body_forbiden_words(self):
        for i in self.contact_requests:
            self.assertTrue(check_clean_message_body(
                i.message_body), 'Contact Request - Message Body: El mensaje contiene palabras prohibidas.')

    def test_contact_request_status_data_type(self):
        for i in self.contact_requests:
            self.assertIsInstance(i.contact_requests_status, int,
                                  'Contact Request Status - Error in the type of data. It must be whole.')

    def test_contact_request_status_default_value(self):
        for i in self.contact_requests:
            self.assertTrue(i.contact_requests_status == 2,
                            'Contact Request Status - Error in the default value. It must be equal to 2.')

    def test_get_status_for_template_method_data_type(self):
        for i in self.contact_requests:
            self.assertIsInstance(i.get_status_for_template(
            ), str, 'Error GET STATUS FOR TEMPLATE METHOD: The type of data does not correspond. It must be string.')

    def test_get_status_for_template_method_data_length(self):
        for i in self.contact_requests:
            self.assertTrue(len(i.get_status_for_template(
            )) > 0, 'Error GET STATUS FOR TEMPLATE METHOD: The size of the answer is not correct. It must be greater than 0.')

    def test_get_status_for_template_method_data_is_html_tag(self):
        for i in self.contact_requests:
            self.assertTrue('>' in i.get_status_for_template(
            ), 'Error GET STATUS FOR TEMPLATE METHOD: No it un day html.')

    def test_get_status_for_template_no_icon_method_data_type(self):
        for i in self.contact_requests:
            self.assertIsInstance(i.get_status_for_template_no_icon(
            ), str, 'Error GET STATUS FOR TEMPLATE NO ICON METHOD: Error in data type. It must be a string.')

    def test_get_status_for_template_no_icon_method_data_length(self):
        for i in self.contact_requests:
            self.assertTrue(len(i.get_status_for_template_no_icon(
            )) > 0, 'Error GET STATUS FOR TEMPLATE NO ICON METHOD: Error in the size of the string. Must contain at least one character.')

    def test_get_status_for_template_no_icon_method_data_No_Contains_icons(self):
        for i in self.contact_requests:
            self.assertTrue('</i>' not in i.get_status_for_template_no_icon(),
                            'Error GET STATUS FOR TEMPLATE NO ICON METHOD: It should not contain icons.')

    def test_get_status_for_template_no_icon_method_data_contains_a_tag_html(self):
        for i in self.contact_requests:
            self.assertTrue('</' in i.get_status_for_template_no_icon(),
                            'Error GET STATUS FOR TEMPLATE NO ICON METHOD: Does not have any html tags.')


class Caracteristicas_Model_Test(TestCase):
    def setUp(self):
        f = Faker()
        for i in range(0, 10):
            User(email=f.email(), password='prueba_user').save()
            self.users = User.objects.all()

        for i in range(0, 10):
            Caracteristicas(
                usuario_solicitante=choice(self.users),
                caracteristica_estado=choice([0, 1, 2, 3, 4, 5]),
                descripcion=f.text(),
                caracteristica_registered_date=f.date()
            ).save()
        self.caracteristicas = Caracteristicas.objects.all()

    def test_TOTAL_CARACTERISTICS_CREATED(self):
        self.assertTrue(len(self.caracteristicas) == 10,
                        'CARACTERISTICA: ERROR Data creation. The specified amount does not match the data created.')

    def test_usuario_solicitante_data_type(self):
        for i in self.caracteristicas:
            self.assertIsInstance(
                i.usuario_solicitante, User, 'CARACTERISTICA: It does not correspond to the type of data from the requesting user of the characteristic. It must be a string.')

    def test_caracteristica_estado_data_type(self):
        for i in self.caracteristicas:
            self.assertIsInstance(i.caracteristica_estado, int,
                                  'CARACTERISTICA: type of data does not correspond. It must be whole. ')

    def test_caracteristica_estado_data_value(self):
        for i in self.caracteristicas:
            self.assertTrue(i.caracteristica_estado in [
                            0, 1, 2, 3, 4, 5], 'CARACTERISTICA: It does not correspond the value. It must be less than 5.')

    def test_caracteristica_estado_data_length(self):
        for i in self.caracteristicas:
            self.assertTrue(len(str(i.caracteristica_estado)) < 10,
                            'CARACTERISTICA: It does not correspond the value. It must be less than 10.')

    def test_caracteristica_descripcion_data_type(self):
        for i in self.caracteristicas:
            self.assertIsInstance(
                i.descripcion, str, 'CARACTERISTICA: Error in data type. It must be a string.')

    def test_caracteristica_descripcion_data_length(self):
        for i in self.caracteristicas:
            self.assertTrue(len(
                i.descripcion) > 0, 'CARACTERISTICA: Error in the data size. It must contain at least one character.')

    def test_caracteristica_descripcion_is_valid_string(self):
        for i in self.caracteristicas:
            self.assertTrue(check_clean_message_body(
                i.descripcion), 'CARACTERISTICA: Error in the content of the description. It contains words not allowed.')

    def test_caracteristica_registered_date_data_type(self):
        for i in self.caracteristicas:
            self.assertIsInstance(i.caracteristica_registered_date, datetime.date,
                                  'CARACTERISTICA: Error in the type of data. It must be DateTime type.')

    def test_get_estado_template_tag_method_data_type(self):
        for i in self.caracteristicas:
            self.assertIsInstance(i.get_estado_template_tag(
            ), str, 'CARACTERISTICA: It does not correspond to the type of data of the response. It must be string type.')

    def test_get_estado_template_tag_method_data_length(self):
        for i in self.caracteristicas:
            self.assertTrue(len(i.get_estado_template_tag(
            )) > 0, 'CARACTERISTICA: No corresponde el tamaño de la respuesta. Debe contener al menos un caracter.')

    def test_get_estado_template_tag_method_is_html_tag(self):
        for i in self.caracteristicas:
            self.assertTrue('<span' in i.get_estado_template_tag(
            ), 'CARACTERISTICA: Error in the response of the method. It does not contain an HTML tag.')
