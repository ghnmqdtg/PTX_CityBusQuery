# -*- coding: UTF-8 -*-
import requests
import configparser
from urllib import parse
import Authorization
import json

config = configparser.ConfigParser()
config.read("config.ini")

APP_ID = config["AUTH"]["APP_ID"]
APP_KEY = config["AUTH"]["APP_KEY"]
RESOURCE = config["API"]["Estimated_TNN"]


def List_Dict_Converter(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

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

        function_type = "Bus"
        description = "預估到站時間"
        keyname = ["Type", "Description", "Routename", "Location", "EstimateTime", "destination"]

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
                        estimate = str(x["EstimateTime"] // 60) + "分"
                        list_results = [self.routename, self.location, estimate, destination]
                        list_results.insert(0, function_type)
                        list_results.insert(1, description)

                        # Steps: list with keynames > dict  > final list for output
                        # insert keynames into the list
                        for num in range(0, len(keyname)):
                            list_results.insert(num * 2, keyname[num])

                        final_output = json.dumps(List_Dict_Converter(list_results), indent=4, ensure_ascii=False)
                        print(final_output)
                        break

            # stop name not exists
            if(token == 0):
                print("No such stop")
        else:
            print("No such routename")


if __name__ == '__main__':
    # fetch the authorization headers
    auth = Authorization.Auth(APP_ID, APP_KEY)
    bus_1 = Bus("18", "和順", "去程").get_Estimated()
    # bus_2 = Bus("藍幹線", "和順", "去程").get_Estimated()

'''
{
    "Type": "Bus",
    "Description": "預估到站時間",
    "Routename": "18",
    "Location": "和順",
    "EstimateTime": "3分",
    "destination": "往塭南里"
}
'''
