 # Imports
 from random import choice
 from faker import Faker

 from app_db.models import User, Caracteristicas




 # A list of users.
 usrs = User.objects.all()

 for i in range(0,100): # 100 new caracteristics...
 	Caracteristicas.objects.create(

 		usuario_solicitante = choice(usrs),
		caracteristica_estado = choice([0,1,2,3,4,5]),
		descripcion = Faker().text()

 		).save()
 	print('===============================')
 	print('N°->', i)
 	print('===============================')

print('FINISH!')