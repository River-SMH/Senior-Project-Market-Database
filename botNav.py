import pyautogui as pt
from cdifflib import CSequenceMatcher
from time import sleep
import cv2
import os
import pytesseract


# connects to the Hypixel Server if not already on it
def connectToServer():
    sleep(1)
    directConnect = pt.locateCenterOnScreen('Images/Direct.png', confidence=.8)
    if directConnect:
        pt.moveTo(directConnect)
        pt.click()
        pt.write('mc.hypixel.net', interval=.1)
        pt.press('enter')


# Connects to the skyblock sub server
def connectToSkyblock():
    # hypixelLobby = pt.locateOnScreen('Images/HypixelHome.png',confidence=.8)
    hypixelLobby = getROI('Images/HypixelHome.png')
    if hypixelLobby:
        pt.press('1')
        sleep(.1)
        pt.click()
        pt.sleep(1)
        skyblock = pt.locateCenterOnScreen('Images/SkyblockImage.png', confidence=.8)
        if skyblock:
            pt.moveTo(skyblock)
            pt.click()
            sleep(8)


# connects to personal island
def connectToIsland():
    # island = pt.locateOnScreen('Images/Island.png',confidence=.8)
    island = getROI('Images/Island.png')
    if island == None:
        pt.press('t')
        sleep(.3)
        pt.write('/warp home', interval=.1)
        sleep(.2)
        pt.press('enter')
        sleep(8)
        connectToIsland()
    else:
        return True


# goes to the item menu that will navigate to the sale menu or bazaar menu
def goToCookie():
    sleep(1)
    pt.press('9')
    easyClick()
    pt.moveTo(100, 100)
    sleep(.3)
    bazImg = pt.locateCenterOnScreen('Images/toBazShop.png', grayscale=True, confidence=.8)
    if bazImg:
        #print("cookie found")
        pt.moveTo(bazImg)
        pt.click()
        return True


# Goes to the bazaar menu
def goToBaz():
    sleep(1)
    baz = pt.locateCenterOnScreen('Images/bazIcon.png', confidence=.8)
    if baz:
        pt.moveTo(baz)
        pt.click()


# determines if you're on the personal island or not
def onIsland():
    # island = pt.locateOnScreen('Images/Island.png',confidence=.8)
    island = getROI('Images/Island.png')
    if island:
        return True
    else:
        return False


# determines if youre on the server or not
def onServer():
    # server = pt.locateOnScreen('Images/Direct.png',confidence=.8)
    server = getROI('Images/Direct.png')
    if server:
        connectToServer()
        sleep(8)
        onServer()
    else:
        print("Currently on Hypixel Server.")


# Searches for the item that was retrieved from the Database
def searchItem(item):
    sleep(1)
    search = pt.locateCenterOnScreen('Images/itemSearch.png', confidence=.8)
    if search:
        #print("Found item")
        pt.moveTo(search)
        easyClick()
        if len(item) > 14:
            item = item[:14]
        pt.write(item, interval=.1)
        sleep(.3)
        done = pt.locateCenterOnScreen('Images/searchEnter.png', confidence=.8)
        if done:
            pt.moveTo(done)
            pt.sleep(.3)
            pt.click()


# Ensures that we are on the bazaar menu
def itemBuyMenu(product):
    sleep(1)
    ROI = pt.locateOnScreen('Images/BazaarMenu.png', confidence=.5)
    if ROI:
        #print("Got Bazaar Menu")
        for y in range(4):
            for x in range(6):
                pt.moveTo(ROI[0] + 100 + (x * 35), ROI[1] + 90 + (y * 35))
                menu = isMenu(product)
                if menu == True:
                    pt.click()
                    return True
                elif menu == "bad":
                    pt.press('esc')
                    return False



# Makes sure that we're on the bazaar menu AND tests each item to see if it is the item we want.
def isMenu(product):
    sleep(1)
    ROI = pt.locateOnScreen('Images/itemMenu2.png', confidence=.5)
    if ROI:
        #print(ROI)
        #print("Image Seen")
        text = readImg()
        for x in range(0, len(text)):
            if text[x] == '\n':
                compareText = text[:x]
                ratio = compareStr(product.lower(), compareText.lower())
                print(product)
                print(ratio)
                print(compareText)
                if ratio >= .9:
                    return True
                break

    return "bad"


# Uses Pytesseract to read text data from the image screenshotted.
def readImg():
    ROI = pt.locateOnScreen('Images/itemMenu2.png', confidence=.5)
    img = pt.screenshot(region=ROI)
    img.save('Images/tested.png')
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    img2 = cv2.imread('Images/tested.png')
    text = pytesseract.image_to_string(img2)
    return text


# Compares the original items name to the item read by Pytesseract
def compareStr(name, extract):
    return CSequenceMatcher(None, name, extract).ratio()


# Gets the region of interest of the screen to further focus on the item/menu
def getROI(imagePath):
    ROI = pt.locateOnScreen(imagePath, confidence=.8)
    return ROI


# Checks if inventory isn't empty. If it isn't then commits to the final stage for selling
def easySellInv():
    pt.moveTo(100, 100)
    sleep(.3)
    if pt.locateOnScreen('Images/emptyInv.png', confidence=.95):
        return
    ROI = pt.locateOnScreen('Images/newSell.png', confidence=.9)
    #print(ROI)
    if ROI:
        for y in range(4):
            for x in range(9):
                if (y == 3 and x == 8):
                    break
                pt.moveTo(ROI[0] + 28 + (35 * x), ROI[1] + 43 + (40 * y))
                sellInput()
                sleep(.15)


# input to sell the item to the shop
def sellInput():
    pt.keyDown('shift')
    pt.click()
    pt.keyUp('shift')


# Checks if the image seen is the image that we want. If so go to its buy menu then fill inventory with its stock
def purchaseLogic():
    pt.moveTo(100, 100)
    sleep(.3)
    ROI = getROI('Images/purchaseMenu.png')
    if ROI:
        price = pt.locateCenterOnScreen('Images/buyIcon.png', confidence=.80)
        if price:
            pt.moveTo(price)
            easyClick()
            pt.moveTo(100, 100)
            sleep(.3)
            fill = pt.locateCenterOnScreen('Images/inventoryFill.png', confidence=.8)
            if fill:
                pt.moveTo(fill)
                pt.click()
                return True
            else:
                return specificAmount()

    else:
        return False


def specificAmount():
    fill2 = pt.locateCenterOnScreen('Images/itemSearch.png', confidence=.8)
    if fill2:
        pt.moveTo(fill2)
        easyClick()
        pt.write('35', interval=.1)
    buy = pt.locateCenterOnScreen('Images/searchEnter.png', confidence=.8)
    if buy:
        pt.moveTo(buy)
        easyClick()
        pt.moveTo(960,430)
        easyClick()
        return True


# call gotocookie check if inventory is empty. if not commit sell
def gotoSell():
    pt.press('esc')
    if(goToCookie()==True):
        sleep(.3)
        easySellInv()
    pt.press('esc')


def easyClick():
    pt.sleep(.3)
    pt.click()
    pt.sleep(.3)


