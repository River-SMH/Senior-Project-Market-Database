from API import connect, bazBuyInfo, bazSellInfo, npcSellInfo
from npcInfo import npcProfit, fixSyn
import pandas as pd
import time
from time import sleep
from datetime import datetime
from botNav import easySellInv, onServer, connectToSkyblock, connectToIsland, onIsland, goToCookie, goToBaz, searchItem, itemBuyMenu, isMenu, purchaseLogic, gotoSell
from Database import db_connect, isItem, insItem, printDB, update, itemtable, spreadarray, printMaster, advTable, findNpcPrice, findMarketPrice, advSpreadTable
from excelSheet import createSheet, makeAdvSheet

# start_time = time.time()

global bazAPI
global npcAPI

bazAPI = "https://api.hypixel.net/skyblock/bazaar"
npcAPI = "https://api.hypixel.net/resources/skyblock/items"


def mainBoard():
    print("Connecting to Database...")
    db_connect()
    print("Database Connection Confirmed...")
    print("Attempting to retrieve API data...")
    data = getData()
    commandList(data)


def commandList(data):
    print("Commands are now enabled. Type '-?' for a list of commands.")
    while (True):
        command = input("Enter a command: ")
        if (command == '-?'):
            commandManual()
        elif (command == '-update database'):
            print("Beginning Database Update...")
            # db_connect()
            updateDatabase(data)
        elif (command == '-print mastertable'):
            print('Printing the Master Table...')
            printMaster()
        elif (command == '-print dataframe'):
            print("Printing MySQL Data into an easy to read format...")
            printDataFrame(data)
        elif (command == '-print data array'):
            print("Printing MySQL Data into an Array...")
            printArray(data)
        elif (command == '-print item table'):
            command = input("Enter item: ")
            printDB(command)
        elif (command == '-adv table'):
            table = input("Enter MySQL code to print specific table with modifiers.\n")
            advTable(table)
        elif (command == '-adv spread'):
            print("Initializing advance spread sheet command...")
            advSpread()
        elif (command == '-enable auto update'):
            print("Auto Updating Enabled...")
            autoUpdate(False)
        elif (command == '-bot run'):
            print("Bot has been enabled, will run one time...")
            botMenu()
        elif (command == '-enable bot'):
            print("Bot Automation has been enabled...")
            autoUpdate(True)
        elif (command == '-get data'):
            print("Retrieving Data...")
            data = getData()
        elif (command == '-make spreadsheet'):
            print("Spreadsheet Command Recognized...")
            spreadSheet()
        elif (command == '-quit'):
            print("Exiting Program...")
            sleep(2)
            return
        else:
            print("'" + command + "' is not a valid command, try again.")


def commandManual():
    listOfCommands = ["'-get data': Connects to the API server to get all Data needed to update the Database.",
                      "'-update "
                      "database': Updates the Master Table and all its products' tables with info retrieved from "
                      "'-get data'.", "'-print mastertable': Prints out the Master Table from the database.", "'-print "
                      "dataframe': Prints out the Data from MySQL into a more readable format.",
                      "'-print data array': Prints out the info that was retrieved when connecting to the API and its "
                      "translation.","'-print item table': Prints out the table for the specified item.",
                      "'-adv table': Prints out a detailed table based on user's syntax of MySQL",
                      "'-adv spread': Creates an indepth Excel Sheet based on the user's wants and needs.(Can include "
                      "Pie/Line chart, both, or neither)","'-enable auto update': This allows the program to run itself"
                      " just updating the database.","'-bot run': Enables the bot to run once with the current "
                      "environment of the Database.", "'-enable bot': Runs the auto update while the bot is activated."
                      " This will run the bot once a minute after the database has been updated.",
                      "'-make spreadsheet': This creates a simple spread sheet that includes"
                      " both a line and pie chart when given an item name.", "'-quit': Exits out of the program."]
    for x in listOfCommands:
        print(x)


def getData():
    info = bazBuyInfo(connect(bazAPI))  # connects to the API server for all products
    npcInfo = npcSellInfo(connect(npcAPI))  # connects to NPC API for npc prices
    data = fixSyn(info, npcInfo)  # Fixes the syntax between the two API's for accurate data
    for x in data:
        if len(x) == 6:  # if there is no price matching, append 0
            x.append(0)
        npcProfit(x)
    print("Data Retrieved")
    return data


def spreadSheet():  # Creates an easy sheet for item requested.
    item = input("Select Item for Spread Sheet: ")
    spreaddata = spreadarray(item)
    if spreaddata == False:
        return
    createSheet(spreaddata)


def advSpread():  # Creates an advanced sheet for the item requested.
    lineGraph = False
    pieGraph = False
    advSheet = []
    spreadContents = []
    newContent = []
    contentsStr = ""

    itemName = input("Enter the Item you want a Spread Sheet of: ")  # gets the item the database should look for
    print("Say Yes or No to the data that you would like to see on your Spread Sheet")

    # Determines which columns the user wants
    spreadContents.append(addContent("Item Name: ", "Item"))
    spreadContents.append(addContent("Amount: ", "Amount"))
    spreadContents.append(addContent("Average Price: ", "Average_Price"))
    spreadContents.append(addContent("Total Coins: ", "Total_Coins"))
    spreadContents.append(addContent("Average Coins: ", "Avg_coins"))
    spreadContents.append(addContent("Percentage: ", "Percent"))
    spreadContents.append(addContent("NPC Price: ", "NPC_Price"))
    spreadContents.append(addContent("NPC Profit: ", "NPC_Profit"))
    spreadContents.append(addContent("Date/Time: ", "Date_Time"))
    spreadContents.append(addContent("Item ID: ", "itemID"))

    # applies changes to the list so that the syntax is MySQL compatible
    for y in spreadContents:
        if (y != None):  # only adds items that were approved to a new list
            newContent.append(y)
            print(y)
    if (len(newContent) == 0):  # cant have 0 fields, will send it back to the beginning
        print("You must enter in at least 1 field, try again.")
        return
    for x in newContent:
        contentsStr += (x + ",")  # changes the syntax and into a string so that the command is MySQL compatible
    contentsStr = contentsStr[:len(contentsStr) - 1]  # removes last comma.

    # gets the times that the user wants
    timePeriod1 = input(
        "Enter the earliest date you want to see from the Item Data(Leave Blank for no Time Constraint): ")  #
    timePeriod2 = input(
        "Enter the latest date you want to see from the Item Data(Leave Blank for no Time Constraint): ")

    # tests each possible time slot to change the syntax for MySQL command
    if (timePeriod1 == "" and timePeriod2 == ""):
        command = "SELECT " + contentsStr + " FROM " + itemName
    if (timePeriod1 == "" and timePeriod2 != ""):
        command = "SELECT " + contentsStr + " FROM " + itemName + " WHERE Date_Time <= '" + timePeriod2 + "'"
    if (timePeriod1 != "" and timePeriod2 == ""):
        command = "SELECT " + contentsStr + " FROM " + itemName + " WHERE Date_Time >= '" + timePeriod1 + "'"
    if (timePeriod1 != "" and timePeriod2 != ""):
        command = "SELECT " + contentsStr + " FROM " + itemName + " WHERE Date_Time >= '" + timePeriod1 + "' AND Date_Time <= '" + timePeriod2 + "'"

    lineList = []
    pieList = []

    # inputs the command into MySQL to find all specified data then uses it for the Excel Sheet.
    advSheet = advSpreadTable(command)
    if advSheet == False:  # if command was bad start from the beginning
        return
    line = input("Do you want to include a Line Graph?: ")
    # Creates a line graph and applies its axis/titles
    if (line == "Yes"):
        if (len(newContent) < 2):
            print("Not enough data fields for Line Graph")
        else:
            lineGraph = True
            xLine = input("Enter data name for x axis(I.E. Date_Time): ")
            lineList.append(xLine)
            yLine = input("Enter data name for y axis(I.E. Price): ")
            lineList.append(yLine)
    pie = input("Do you want to include a Pie Graph?: ")
    # creates a pie graph and applies its groups/data and titles
    if (pie == "Yes"):
        if (len(newContent) < 2):
            print("Not enough data fields for Pie Graph")
        else:
            pieGraph = True
            xPie = input("Enter data name for Group(I.E. Price): ")
            pieList.append(xPie)
            yPie = input("Enter data name for Data(I.E. Date Time): ")
            pieList.append(yPie)
    """for x in advSheet:
        print(x)"""
    makeAdvSheet(advSheet, newContent, lineGraph, pieGraph, lineList,pieList)
    # advsheet = data fields retrieved from command search mySQL. newContent = the columns/amount. line/pie graph is true or false to make. line/pie list sets the values for graphs


# Determines if the person wants said column or not
def addContent(name, item):
    col = input(name)
    if (col == "yes"):
        return item


# Updates the entire database such as master table and all its products
def updateDatabase(data):
    duration = time.time()
    ct = 0
    newitems = []
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    for x in data:
        if isItem(x[0]) == False:
            newitems.append(x[0])
            ct += 1
            insItem(x)
        else:
            update(x)
        itemtable(x, date)
    if (ct != 0):
        for item in newitems:
            print(item)
        print(str(ct) + " new items added.")
    else:
        print("No new items added.")
    print(str(round(time.time() - duration, 2)) + " seconds was needed to update the Database.")


# prints out the master table into the console/terminal
def printMasterTable():
    printMaster()


# pretty print for the data that was retrieved and translated
def printDataFrame(data):
    print("print dataframe test")
    labels = ['Name', 'Amount', 'Avg Price', 'Total Coins', 'Avg Coins', 'Percent', 'NPC Price', 'NPC Profit']
    df = pd.DataFrame(data, columns=labels)
    print(df.to_string())


# prints out the data array that the code sees before implementation
def printArray(data):
    print(data)


# Automatically updates the database every minute. If bot is set to true it will activate the bot once until the next minute
def autoUpdate(bot):
    check = datetime.now().strftime("%M")
    try:
        while True:
            if (datetime.now().strftime("%M") != check):
                data = getData()
                check = datetime.now().strftime("%M")
                updateDatabase(data)
                sleep(1)
                if bot == True:
                    botMenu()
            sleep(2)
    except KeyboardInterrupt:  # exit out of the infinite loop by using ^C
        print("update stopped")


# all commands and movement needed to complete a sale.
def botMenu():
    product = findNpcPrice()
    print(product[0][0])
    # Checks to see if you're on your personal island
    if onIsland() == False:
        onServer()
        connectToSkyblock()
        connectToIsland()
    # if on personal island commit to sale.
    if onIsland() == True:
        sleep(1)
        goToCookie()
        sleep(1)
        goToBaz()
        sleep(1)
        searchItem(product[0][0])
        if itemBuyMenu(product[0][0]) == True:  # checks if the item we're looking at is the one we want
            print("is true")
        if purchaseLogic() == True:  # if all settings are satisfactory then commit to sale.
            gotoSell()


mainBoard()  # Calls the main method to then initiate the program.
