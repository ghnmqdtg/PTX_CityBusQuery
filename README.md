# PTX_CityBusQuery

## Intro
To get an estimated time of the bus I usually take, I write this program to fetch the information about bus stops near me. 

By cascading the PTX (公共運輸整合資訊流通服務平臺) Open API of MOTC (中華民國交通部)
, this program can fetch real-time bus information in Tainan, Taiwan. 

After fetching responses from the API, I have to check if the requests succeed and if the routes and stop names exist. Also, I have to filter out no needed information to get a clear output.

## Functions
1. Enter the route, stop name and the direction of the bus in the list Sequentially.

    ![](https://i.imgur.com/vhhEYAI.png)

2. Run the program, you can get output

    ![](https://i.imgur.com/Mr5uVjJ.png)

The output is in JSON format, so it's easier for me to set up an API in the future.


## Basic knowledge
Besides the Python syntax, You should understand basic HTTP methods and JSON format to send requests and sort and filter the response from the API.


## Requirements
The program can run normally in **python 3.6.8(64 bits) or higher**.

You can run the following instruction in the CMD or PowerShell to install them:
```
pip install -r requirements.txt
```