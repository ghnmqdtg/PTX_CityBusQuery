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


def get_Estimated(routename, location, direction, dict_output):
    if(direction == "去程"):
        direction = 0  # 去程
    elif(direction == "回程"):
        direction = 1  # 返程
    else:
        direction = 2  # 迴圈

    # urllib.parse.quote() URL encode
    QUERY_OPTIONS = parse.quote(routename) + "?$format=JSON"
    RESOURCE_PATH = RESOURCE + QUERY_OPTIONS

    # fetch json data from the api
    response = requests.get(RESOURCE_PATH, headers=auth.get_auth_header())

    # requests.codes.ok == 200
    if(response.status_code == requests.codes.ok):
        data = response.json()["N1Datas"]
        # print(json.dumps(data, indent=4, ensure_ascii=False))  # for testing
        keyname = ["Routename", "Location", "EstimateTime", "destination"]

        token = 0

        # if the route exists
        if(data):
            # traverse the data dictionary
            for x in data:
                # check if the stop name exists, if so, token = 1
                if(x["StopName"]["Zh_tw"] == location):
                    token = 1
                    if(x["Direction"] == direction):
                        estimate = str(x["EstimateTime"] // 60) + "分"
                        destination = "往" + x["DestinationStopName"]["Zh_tw"]
                        list_results = [routename, location, estimate, destination]

                        # steps: list with keynames > dict output
                        # insert keynames into the list
                        for num in range(0, len(keyname)):
                            list_results.insert(num * 2, keyname[num])

                        # convert list to dict
                        final_output = List_Dict_Converter(list_results)

                        return final_output
                        break

            if(token == 0):
                print("No such stop")
        else:
            print("No such routename")
    else:
        print("Request fialed, status_code:", response.status_code)


if __name__ == '__main__':
    # fetch the authorization headers
    auth = Authorization.Auth(APP_ID, APP_KEY)

    # initialize the output format
    function_type = "Bus"
    description = "預估到站時間"
    dict_output = {
        "Type": function_type,
        "Description": description,
        "Info": []
    }

    # initial settings of data to be searched
    route_list = ["18", "藍幹線", "20"]
    stop_list = ["和順", "和順", "和順"]
    dir_list = ["去程", "去程", "回程"]

    for i in range(0, len(route_list)):
        output = get_Estimated(route_list[i], stop_list[i], dir_list[i], dict_output)
        dict_output["Info"].append(output)

    print(json.dumps(dict_output, indent=4, ensure_ascii=False))

# Results_JSON_format
'''
{
    "Type": "Bus",
    "Description": "預估到站時間",
    "Info": [
        {
            "Routename": "18",
            "Location": "和順",
            "EstimateTime": "14分",
            "destination": "往塭南里"
        },
        {
            "Routename": "藍幹線",
            "Location": "和順",
            "EstimateTime": "6分",
            "destination": "往佳里站"
        },
        {
            "Routename": "20",
            "Location": "和順",
            "EstimateTime": "14分",
            "destination": "往南紡購物中心(東光路)"
        }
    ]
}
'''
