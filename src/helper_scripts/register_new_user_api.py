import requests
from faker import Faker as F



f = F()


# BASE_URL = "https://baches-thesis.herokuapp.com/api_V1/register_user"
BASE_URL = "http://localhost:8000/api_V1/register_user"


datos = {
	'email':f.email(),
	'password':'23fasdfasdf42',
	
}


req = requests.post(BASE_URL, data=datos)

print(req)
print(req.reason)
print(req.content)
