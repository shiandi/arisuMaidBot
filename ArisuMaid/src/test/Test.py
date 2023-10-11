import requests
import json

response = requests.get('http://ba.gamerhub.cn/api/get_ba_raid_ranking_data?season=4')

if response.status_code == 200:
    data = json.loads(response.text)
    data_1 = data['data']
    print(type(data_1))
    data_2 = data['data_bilibili']
    print(type(data_2))
    print(data_1.keys())
    for key in data_1.keys():
        print(data_1[key][-1][-1])
