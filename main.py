# -*- coding: UTF-8 -*-
import requests
import json
import configparser
from urllib import parse
import Authorization
import re

config = configparser.ConfigParser()
config.read("config.ini")

APP_ID = config["AUTH"]["APP_ID"]
APP_KEY = config["AUTH"]["APP_KEY"]
RESOURCE = config["API"]["Estimated_TNN"]


class Bus:

    def __init__(self, routename, location, direction):
        self.routename = routename
        self.location = location
        if(direction == "去程"):
            self.direction = "1"  # 回程
        elif(direction == "回程"):
            self.direction = "2"  # 返程
        else:
            self.direction = "0"  # 迴圈

    def get_Estimated(self):
        # urllib.parse.quote() URL encode
        QUERY_OPTIONS = parse.quote(self.routename) + "?$format=JSON"
        RESOURCE_PATH = RESOURCE + QUERY_OPTIONS
        raw = requests.get(RESOURCE_PATH, headers=auth.get_auth_header()).json()
        # print(json.dumps(raw, indent=4, ensure_ascii=False))
        data = raw["N1Datas"]

        for x in data:
            try:
                # print(x["SubRouteUID"])
                if(x["SubRouteUID"].endswith(self.direction)):
                    if(x["StopName"]["Zh_tw"] == self.location):
                        time = x["EstimateTime"]
                        print(self.location, time)
            except:
                pass


if __name__ == '__main__':
    auth = Authorization.Auth(APP_ID, APP_KEY)

    # Fetche the RouteUID from file
    with open("QueryResults/" + "Routes_info.json", 'r', encoding='utf-8') as outfile:
        Route_UID_dict = json.loads(outfile.read())
        outfile.close()

    bus = Bus("藍幹線", "和順", "去程").get_Estimated()
