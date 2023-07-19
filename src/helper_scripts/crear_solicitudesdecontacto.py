from faker import Faker as F
from random import choice
from app_db.models import Contact_Request



for i in range(0,100):
	Contact_Request.objects.create(
		full_name =  F().name(),
		email =  F().email(),
		message_body =  F().text(),
		contact_requests_status = choice([1,2,3])

		).save()
	print('============================')
	print('Se guardo uno... N°-> ', i)
	print('============================')


