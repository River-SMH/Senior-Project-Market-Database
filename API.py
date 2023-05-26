import requests
from APIExtract import extractAPIinfo
from npcInfo import npcCost


def connect(call):  # connects to the API and returns a json for translation
    response = requests.get(call)
    return response.json()


def bazBuyInfo(buyData):  # gets the buy info from the API
    return extractAPIinfo(buyData, True)


def bazSellInfo(sellData):  # gets the sell info from the API
    return extractAPIinfo(sellData, False)


def npcSellInfo(npcData):  # gets the npc info from the API
    return npcCost(npcData)
