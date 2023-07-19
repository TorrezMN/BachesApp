import requests


url = 'http://localhost:8000/api_V1/api-token-auth'
dat = {
	'username':'carajo@gmail.com',
	 'password':'contras3na',
}


req = requests.post(url, data = dat).json()

print(req)