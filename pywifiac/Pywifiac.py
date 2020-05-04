""" Pywifiac"""

import requests
import datetime
import threading
import json
from os import path


class WifiAcSession:
    """Initiate Wifi AC Session Class."""
    account = ""
    password = ""
    authkey = account + password


class WifiAcApiDetails:
    url = 'http://www.iconcgo.com:80/icongo.server/client-Client-oemEntrance.action'
    identifier = "&GUID=iOS-E07CBA81-B622-4728-919E-5B1706AAA3AE&OEMTYPE=OEM_WIFIAC&CLIENT=OEM_WIFIAC_APP&OEM_LANGUAGE" \
                 "=en_US "


WIFI_AC_API = WifiAcApiDetails()


def epoch_seconds():
    return int(datetime.datetime.now().strftime("%s"))


def get_token():
    task = {"password": WifiAcSession.password, "account": WifiAcSession.account, "cmd": 100000,
            "authkey": WifiAcSession.authkey}
    body = "jsonString=" + task.__str__() + WIFI_AC_API.identifier
    print(body)
    resp = requests.post(WIFI_AC_API.url, data=body,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    sessionid = "JSESSIONID=" + resp.cookies['JSESSIONID']
    token = resp.cookies['JSESSIONID']
    cookies = dict(name='JSESSIONID', password=sessionid, )
    with open('../data.txt', 'w') as outfile:
        json.dump(sessionid, outfile)
    resp.close()
    return sessionid


def get_ac_units(token):
    command = {"cmd": 10001, "req_timestamp": epoch_seconds(), "pageSize": 10000, "pageNo": 1}
    body = "jsonString=" + command.__str__() + WIFI_AC_API.identifier

    print(body)
    resp = requests.post(WIFI_AC_API.url, data=body,
                         headers={"Content-Type": "application/x-www-form-urlencoded", "Cookie": token})
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    print('Returned Code is: {}'.format(resp.json()))
    y = resp.json()
    x = y["result"]
    if x["code"] == 0:
        for results in y["content"]:
            print('{}'.format(results["id"]))
            command = {"cmd": 10002, "token": token, "req_timestamp": epoch_seconds(), "aircondid": results["id"]}
            body = "jsonString=" + command.__str__() + WIFI_AC_API.identifier
            resp = requests.post(WIFI_AC_API.url, data=body,
                                 headers={"Content-Type": "application/x-www-form-urlencoded", "Cookie": token})
            print('{}'.format(resp.json()))
            return resp.json()
    else:
        print('Token is not valid, lets try again.')
        get_ac_units(get_token())


class Pywifiac:
    """Pywifiac Class"""

    def __init__(self):
        """Initialise the base variable values."""
        self.lock = threading.Lock()


    #if path.exists("../data.txt"):
    #    print("token already found")
    #    with open('../data.txt') as json_file:
    #        data = json.load(json_file)
    #    get_ac_units(data)
    #else:
    #    print('Requesting token')
    #    get_ac_units(get_token())
