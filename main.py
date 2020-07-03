# -*- coding: UTF-8 -*-
import requests
import configparser
from urllib import parse
import Authorization
# import json

config = configparser.ConfigParser()
config.read("config.ini")

APP_ID = config["AUTH"]["APP_ID"]
APP_KEY = config["AUTH"]["APP_KEY"]
RESOURCE = config["API"]["Estimated_TNN"]


class Bus:

    # initail settings
    def __init__(self, routename, location, direction):
        self.routename = routename
        self.location = location
        if(direction == "去程"):
            self.direction = 0  # 去程
        elif(direction == "回程"):
            self.direction = 1  # 返程
        else:
            self.direction = 2  # 迴圈

    def get_Estimated(self):
        # urllib.parse.quote() URL encode
        QUERY_OPTIONS = parse.quote(self.routename) + "?$format=JSON"
        RESOURCE_PATH = RESOURCE + QUERY_OPTIONS
        # fetch json data from the api
        raw = requests.get(RESOURCE_PATH, headers=auth.get_auth_header()).json()
        data = raw["N1Datas"]
        # print(json.dumps(data, indent=4, ensure_ascii=False))  # for testing
        token = 0

        # if the stop exists
        if(data):
            # traverse the data dictionary
            for x in data:
                # check if the stop name exists, if so, token = 1
                 if(x["StopName"]["Zh_tw"] == self.location):
                    token = 1
                    if(x["Direction"] == self.direction):
                        destination = "往" + x["DestinationStopName"]["Zh_tw"]
                        result = [self.routename, self.location, x["EstimateTime"], destination]
                        print(result)
                        break

            # stop name not exists
            if(token == 0):
                print("No such stop")
        else:
            print("No such routename")


if __name__ == '__main__':
    # fetch the authorization headers
    auth = Authorization.Auth(APP_ID, APP_KEY)
    bus_1 = Bus("藍幹線", "和順", "回程").get_Estimated()
