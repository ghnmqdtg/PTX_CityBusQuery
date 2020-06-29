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
from urllib import parse

config = configparser.ConfigParser()
config.read("config.ini")

APP_ID = config["AUTH"]["APP_ID"]
APP_KEY = config["AUTH"]["APP_KEY"]
RESOURCE = config["API"]["Estimated_TNN"]

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


class Bus:

    def __init__(self, routename, location, direction):
        self.routename = routename
        self.location = location
        if(direction == "去程"):
            self.direction = "0"  # 回程
        elif(direction == "回程"):
            self.direction = "1"  # 返程
        else:
            self.direction = "2"  # 迴圈

    def get_Estimated(self):
        count = 0
        # urllib.parse.quote() URL encode
        QUERY_OPTIONS = parse.quote(self.routename) + "?$format=JSON"
        response = requests.get(RESOURCE + QUERY_OPTIONS, headers= auth.get_auth_header()).json()
        # print(json.dumps(response, indent=4, ensure_ascii=False))
        raw = response["N1Datas"]
        for x in raw:
            try:
                aaa = x["SubRouteUID"] + " " + x["StopName"]["Zh_tw"] +  x["SubRouteName"]["Zh_tw"]
                print(count, aaa)
            except:
                pass
            count += 1
        #SubRoute_UID = Route_UID_dict[self.routename] + self.direction


if __name__ == '__main__':
    auth = Auth(APP_ID, APP_KEY)

    # Fetche the RouteUID from file
    with open("Routes_info.json", 'r', encoding='utf-8') as outfile:
        Route_UID_dict = json.loads(outfile.read())
        outfile.close()

    bus = Bus("藍幹線", "  ", "去程").get_Estimated()
