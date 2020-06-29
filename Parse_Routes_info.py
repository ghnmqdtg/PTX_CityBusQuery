# -*- coding: UTF-8 -*-
import requests
import json
import configparser
import Authorization

config = configparser.ConfigParser()
config.read("config.ini")

APP_ID = config["AUTH"]["APP_ID"]
APP_KEY = config["AUTH"]["APP_KEY"]
RESOURCE_PATH = config["API"]["Route_TNN"]


def Parse_Routes_info():
    # datatype : dict
    raw = requests.get(RESOURCE_PATH, headers=auth.get_auth_header()).json()
    data = raw["Routes"]
    for x in data:
        dict_routes[x["RouteName"]["Zh_tw"]] = x["RouteUID"]
    # print(json.dumps(dict_routes, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    count = 0
    dict_routes = {}
    auth = Authorization.Auth(APP_ID, APP_KEY)
    Parse_Routes_info()

    # Set the path and filename to save routeUID dictionary
    with open("QueryResults/" + "Routes_info" + '.json', 'w', encoding='utf-8') as outfile:
        json.dump(dict_routes, outfile, ensure_ascii=False)
        outfile.write('\n')
        outfile.close()
