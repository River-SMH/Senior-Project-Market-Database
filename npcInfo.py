import re


def npcCost(item_data):  # connects to the NPC API and creates an array that holds names and npc costs
    npc_price_list = []
    for index, item_info in enumerate(item_data.get("items", [])):
        indie_List = []
        npc_item_name = item_info.get("name")
        npc_price = item_info.get("npc_sell_price")
        if npc_price != None:  # if there is a price add it to data array.
            indie_List.extend((npc_item_name, (npc_price)))
            npc_price_list.append(indie_List)
    return npc_price_list


def fixSyn(order, npcList):  # fixes any errors in name before attempting to enlist the item onto the array
    info = order
    for i in range(len(info)):  # Removes the _ from the name for the NPC price comparison to be appended to the item
        name = str(info[i][0])
        new = re.sub('\_+', ' ', name)
        new = re.sub(':','',new)
        info[i][0] = new
        for x in range(len(npcList)):
            if npcList[x][0].casefold() == new.casefold():  # if the new name is the same as original array then append the price
                info[i].append(npcList[x][1])
                break
    return info


def npcProfit(data):  # returns a seperate field for the database that compares NPC price to average cost
    profit = data[6] - data[2]
    data.append(profit)
