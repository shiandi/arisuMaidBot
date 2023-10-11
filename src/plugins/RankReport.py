import datetime
import json
import time

import requests
from nonebot.adapters.onebot.v11 import Event
from nonebot.plugin.on import on_command

user = {}
ops = {'1920379084','1138186957'}
cooldown = 120
rankSeason = 5


# 获取爬取地址
def getUrl(i: int):
    return 'http://ba.gamerhub.cn/api/get_ba_raid_ranking_data?season=' + str(i)


def isCooldown(id):
    # 在op名单里面，直接返回True
    if id in ops:
        return True

    # 不在op名单
    if id in user.keys():
        nowTime = time.time()
        if nowTime - user[id] > cooldown:
            user[id] = nowTime
            return True
        else:
            return cooldown - int(nowTime - user[id])
    else:
        nowTime = time.time()
        user[id] = nowTime
        return True


def getOfficialData(season: int):
    url = getUrl(season)
    response = requests.get(url)
    allData = json.loads(response.text)
    data = allData['data']
    ranks = list(data.keys())
    scores = list()
    for i in ranks:
        scores.append(data[i][-1][-1])
    lastUpdatedTime = toTime(int(allData['lastUpdatedTime']))
    return ranks, scores, lastUpdatedTime


def getBilibiliData(season: int):
    url = getUrl(season)
    response = requests.get(url)
    allData = json.loads(response.text)
    data = allData['data_bilibili']
    ranks = list(data.keys())
    scores = list()
    for i in ranks:
        scores.append(data[i][-1][-1])
    lastUpdatedTime = toTime(int(allData['lastUpdatedTime_bilibili']))
    return ranks, scores, lastUpdatedTime


def toTime(i: int):
    return str(datetime.datetime.fromtimestamp(i))


def messageToSend(ranks: list, scores: list, time: str):
    res = '总力战数据:'
    for i in range(len(ranks)):
        res += f'\n第{ranks[i]}名：{scores[i]}'
    res += f'\n数据时间：{time}'
    return res


rank_reporter = on_command('总力战')


@rank_reporter.handle()
async def reporter(event: Event):
    user_id = event.get_user_id()
    message = str(event.get_message())
    if len(message) != 6:
        await rank_reporter.finish(f'请正确使用命令，例子：\n/总力战官/B服')
    server = message[4:]
    if isCooldown(user_id) is True:
        if server == '官服':
            ranks, scores, lastUpdatedTime = getOfficialData(rankSeason)
            await rank_reporter.finish(messageToSend(ranks, scores, lastUpdatedTime))
        elif server in ['B服', 'b服']:
            ranks, scores, lastUpdatedTime = getBilibiliData(rankSeason)
            await rank_reporter.finish(messageToSend(ranks, scores, lastUpdatedTime))
        else:
            await rank_reporter.finish(f'请正确使用命令，例子：\n/总力战官/B服')
    else:
        await rank_reporter.finish(f'冷却时间{isCooldown(user_id)}秒')
