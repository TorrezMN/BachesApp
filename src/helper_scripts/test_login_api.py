import requests


BASE_URL = 'https://baches-thesis.herokuapp.com/api_V1/login_user'
user_data = {
	'username': 'fulano@gmail.com',
	'password':'unacontras3na',
}


req = requests.post(BASE_URL, data=user_data)

print('====================')
print(req)

print('====================')
print(req.content)
print('====================')