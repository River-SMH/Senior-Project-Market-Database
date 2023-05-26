import mysql.connector
from datetime import datetime

db = mysql.connector.connect(host="localhost", user="root", passwd="root")
mycursor = db.cursor()


def db_connect():  # Creates the database if it doesnt exist, updates the cursor and creates the master table.
    mycursor.execute("CREATE DATABASE IF NOT EXISTS BazaarDB")

    global db
    db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="BazaarDB")
    newCursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS Master_Item_Table (Item VARCHAR(50), Amount VARCHAR(50), "
                     "Average_Price VARCHAR(50), Total_Coins VARCHAR(50), Avg_coins VARCHAR(50), "
                     "Percent float UNSIGNED, NPC_Price int UNSIGNED, NPC_Profit int,"
                     " itemID int PRIMARY KEY AUTO_INCREMENT)")


def newCursor():  # changes the global cursor to the new cursor
    global mycursor
    mycursor = db.cursor()


def isItem(name):  # checks to see if the item is within the master table. Returns true or false
    check = "SELECT * FROM Master_Item_Table WHERE Item = " + "'" + name + "'"
    mycursor.execute(check)
    result = mycursor.fetchone()
    if result == None:
        return False
    else:
        return True


def update(item_log):  # Updates the info in the master table for all items within the database
    if len(item_log) == 6:
        item_log.append(0)
    mycursor.execute(
        "UPDATE Master_Item_Table SET Amount=%s, Average_Price=%s, Total_Coins=%s, Avg_Coins=%s, Percent=%s, NPC_Price=%s, NPC_Profit=%s WHERE Item=%s",
        (item_log[1], item_log[2], item_log[3], item_log[4], item_log[5], item_log[6], item_log[7], item_log[0]))
    db.commit()


def insItem(item_log):  # If the item isn't in the master table, insert it into the database with its values
    command = "INSERT INTO Master_Item_Table (Item, Amount, Average_Price, Total_Coins, Avg_Coins, Percent, NPC_Price, NPC_Profit) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(command,
                     (item_log[0], item_log[1], item_log[2], item_log[3], item_log[4], item_log[5], item_log[6],
                      item_log[7]))
    db.commit()


def printDB(item):  # Prints out what the table looks like for the specific item requested
    try:
        mycursor.execute("SELECT * FROM " + item)
        for x in mycursor:
            print(x)
    except mysql.connector.Error as err:
        print("Wrong Syntax try again. " + str(err))
        return False


def printMaster():  # prints ou the master table
    mycursor.execute("SELECT * FROM Master_Item_Table")
    for x in mycursor:
        print(x)


def advTable(command):  # Prints out a specified table using only MySQL syntax provided by the user
    try:
        mycursor.execute(command)
        for x in mycursor:
            print(x)
    except mysql.connector.Error as err:
        print("Wrong syntax try again. " + str(err))
        return False


def advSpreadTable(command):  # returns a specified table for the advance spread sheet
    spreadList = []
    try:
        mycursor.execute(command)
        for x in mycursor:
            spreadList.append(x)
        return spreadList
    except mysql.connector.Error as err:
        print("Wrong syntax try again. " + str(err))
        return False


def spreadarray(item):  # returns the table info from an item as an array
    spreadList = []
    try:
        mycursor.execute("SELECT * FROM " + item)
        for x in mycursor:
            spreadList.append(x)
        return spreadList
    except mysql.connector.Error as err:
        print("Wrong syntax try again. " + str(err))
        return False


def Itemkey(key):  # quick table return of an item based on item ID
    itemInfo = []
    mycursor.execute("SELECT * FROM Master_Item_Table WHERE itemID = " + key)
    for x in mycursor:
        itemInfo.append(x)
    return itemInfo


def findNpcPrice():  # Returns the best possible profit from an item in the master table
    npcList = []
    mycursor.execute("SELECT Item, NPC_Profit FROM master_item_table WHERE (Average_Price*2240 < "
                     "100000000 and NPC_Profit > 1) ORDER BY NPC_Profit DESC LIMIT 1")
    for x in mycursor:
        npcList.append(x)
        print(x)
    return npcList


def findMarketPrice():  # returns the item with the highest percentage profit
    marketList = []
    mycursor.execute("SELECT Item, Percent FROM BazaarDB.master_item_table WHERE Percent = (SELECT "
                     "min(Percent) FROM BazaarDB.master_item_table)")
    for x in mycursor:
        marketList.append(x)
        print(x)
    return marketList


def childInsert(x, name, date):  # Inserts the data fields for the item's specific table
    command = "INSERT INTO " + name + " (Item, Amount, Average_Price, Total_Coins, Avg_Coins, Percent, NPC_Price, " \
                                      "NPC_Profit, Date_Time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(command,
                     (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], date))
    db.commit()


def itemtable(x, date):  # creates the table for the item itself.
    name = x[0].replace(" ", "_").replace(":", "_")
    command = "CREATE TABLE IF NOT  EXISTS " + name + " (Item VARCHAR(50), Amount VARCHAR(50)," \
                                                      " Average_Price VARCHAR(50), Total_Coins VARCHAR(50), " \
                                                      "Avg_coins VARCHAR(50), Percent float UNSIGNED, " \
                                                      "NPC_Price  int UNSIGNED,NPC_Profit int, Date_Time VARCHAR(50), " \
                                                      "itemID int PRIMARY KEY AUTO_INCREMENT," \
                                                      " FOREIGN KEY(itemID) " \
                                                      "REFERENCES Master_Item_Table(itemID))"
    mycursor.execute(command)
    childInsert(x, name, date)
