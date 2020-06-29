# -*- coding: UTF-8 -*-
from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

APP_ID = config["AUTH"]["APP_ID"]
APP_KEY = config["AUTH"]["APP_KEY"]
RESOURCE_PATH = config["API"]["Route_TNN"]

class Auth():

    def __init__(self, APP_ID, APP_KEY):
        self.APP_ID = APP_ID
        self.APP_KEY = APP_KEY

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.APP_KEY.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.APP_ID + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


def Parse_Routes_info():
    # datatype : dict
    response = requests.get(RESOURCE_PATH, headers= auth.get_auth_header()).json()
    raw = response["Routes"]
    for x in raw:
        dict_routes[x["RouteName"]["Zh_tw"]] = x["RouteUID"]
    # print(json.dumps(dict_routes, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    count = 0
    dict_routes = {}
    auth = Auth(APP_ID, APP_KEY)
    Parse_Routes_info()

    # Set the path and filename to save routeUID dictionary
    with open("QueryResults/" + "Routes_info" + '.json', 'w', encoding='utf-8') as outfile:
        json.dump(dict_routes, outfile, ensure_ascii=False)
        outfile.write('\n')
        outfile.close()
