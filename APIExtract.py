def extractAPIinfo(order, sumSummary): #Retrieves a specific dictionary from the API
    itemList = []
    if sumSummary == True:
        summary = "buy_summary" #what people are currently selling the product for
    else:
        summary = "sell_summary" #what people are currently buying the product at.

    for product_name, product_data in order.get("products", {}).items(): #sieves through the prodcuts dictionary to retrieve product info

        item_info_list = []
        avgPrice = 0
        product_sum = 0
        product_amount = 0
        counter = 0

        data = inputDataInfo(avgPrice, product_sum, product_amount, product_data, summary, 1.1, counter) #data from current item turned into array

        # [0] = avgPrice [1] = product_sum [2] = product_amount [3] = counter
        if data[0] != 0 and data[2] != 0: #ensures that neither item is 0
            price = data[0] / data[3]
            averageSum = data[2] * round(price)
            if round(averageSum) != 0:
                percent = float(format((round(data[1]) / round(averageSum)) * 100, ".2f")) #retrieves the percent difference between average and actual coins in product

        item_info_list.extend((product_name, (data[2]), round(price), (round(data[1])), round(averageSum), percent)) #appends the new info to the data array
        itemList.append(item_info_list)

    return itemList


def inputDataInfo(avgPrice, product_sum, product_amount, product_data, summary, thresh_hold, counter): #math used to get the average price, total coins in product, total amount
    for index, product_order in enumerate(product_data.get(summary, [])):

        if index == 0:
            product_price = product_order.get("pricePerUnit", 0)
            product_amount += product_order.get("amount", 0)
            avgPrice += product_order.get("pricePerUnit")
            product_sum += product_amount * product_price
            counter += 1
        else:
            if product_order.get("pricePerUnit", 0) <= (product_price * thresh_hold):
                product_sum += product_order.get("amount", 0) * product_order.get("pricePerUnit", 0)
                product_amount += product_order.get("amount", 0)
                avgPrice += product_order.get("pricePerUnit")
                counter += 1

    return avgPrice, product_sum, product_amount, counter

