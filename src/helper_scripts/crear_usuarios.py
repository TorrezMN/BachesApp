from faker import Faker
from app_db.models import User
for i in range(0,100):
    User.objects.create_user(
    Faker().email(),
    password = 'unacontrasenamuybuena').save()
    print('---->')
