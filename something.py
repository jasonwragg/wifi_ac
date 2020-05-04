from pywifiac import Pywifiac
from os import path
import json

Pywifiac.WifiAcSession.password = ""
Pywifiac.WifiAcSession.account = ""

if path.exists("../data.txt"):
    print("token already found")
    with open('../data.txt') as json_file:
        data = json.load(json_file)
        Pywifiac.get_ac_units(data)
else:
    print('Requesting token')
    Pywifiac.get_ac_units(Pywifiac.get_token())
