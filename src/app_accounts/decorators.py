from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test



def Admin_Required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='error_cuentas_admin'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
#     print('\n'*5)
#     print('===================================================')
#     print('hello from decorator!')
#     print('LOGIN URL: ', login_url)
#     print('REDIRECT FIELD NAME: ', redirect_field_name)
#     print('help. ', help(        lambda u: u.is_active and u.is_superuser,
# ))
#     print('===================================================')
#     print('\n'*5)
    if function:
        return actual_decorator(function)
    return actual_decorator