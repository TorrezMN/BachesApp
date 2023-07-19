from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, User_Profile


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token





#########################################
#       Crear Perifil Personal          # 
#########################################

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(profile_user=instance).save()
        

#########################################
#       Crear AuthToken                 # 
#########################################


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
