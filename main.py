# -*- coding: UTF-8 -*-
import requests
import json
import configparser
from urllib import parse
import Authorization

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
            self.direction = "0"  # 回程
        elif(direction == "回程"):
            self.direction = "1"  # 返程
        else:
            self.direction = "2"  # 迴圈

    def get_Estimated(self):
        count = 0
        # urllib.parse.quote() URL encode
        QUERY_OPTIONS = parse.quote(self.routename) + "?$format=JSON"
        RESOURCE_PATH = RESOURCE + QUERY_OPTIONS
        raw = requests.get(RESOURCE_PATH, headers=auth.get_auth_header()).json()
        # print(json.dumps(raw, indent=4, ensure_ascii=False))
        data = raw["N1Datas"]

        for x in data:
            try:
                aaa = x["SubRouteUID"] + " " + x["StopName"]["Zh_tw"] +  x["SubRouteName"]["Zh_tw"]
                print(count, aaa)
            except:
                pass
            count += 1

        # SubRoute_UID = Route_UID_dict[self.routename] + self.direction


if __name__ == '__main__':
    auth = Authorization.Auth(APP_ID, APP_KEY)

    # Fetche the RouteUID from file
    with open("QueryResults/" + "Routes_info.json", 'r', encoding='utf-8') as outfile:
        Route_UID_dict = json.loads(outfile.read())
        outfile.close()

    bus = Bus("藍幹線", "  ", "去程").get_Estimated()
