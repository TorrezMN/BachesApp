#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Torrez, Milton N.

import requests
from faker import Faker
from time import sleep

BASE_URL_REGISTER_USER = "https://baches-thesis.herokuapp.com/api_V1/register_user"



def get_data():
    data = {
    'email': Faker().email(),
    'password': 'elpasswordqueanda',
    }
    return(data)


#  for i in range(0,10):
    #  req = requests.post(BASE_URL_REGISTER_USER, data= get_data()).json()
    #  print(req)

for i in range(0,10):
    req = requests.post(BASE_URL_REGISTER_USER, data= {
        'email': 'caramelito@lindo.com',
        'password':'lacontraseña',


    }).json()
    print(req)
