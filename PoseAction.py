import autopy
import eel
import pyautogui as pgui
import xml.etree.ElementTree as ET
#倍率
magnification = 1
shortcutflag = 0

@eel.expose()
def set_shortcutflag():
    global shortcutflag
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    for item in root:
        shortcutflag = int(item.find("pose_flag").text)
        return item.find("pose_flag").text

@eel.expose()
def save_shortcutflag(value):
    global shortcutflag
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    shortcutflag = int(value)
    for item in root:
        item.find("pose_flag").text = value
    tree.write('conf.xml', encoding='UTF-8')


def sensitivity(value):
    global magnification
    #倍率を1.0から2.0までの範囲で実装
    magnification = 1 + int(value)*0.1

def action(sign_id,x,y,countpose,poseshortcut,poseshortcut2):
    #ショートカットキー読み込み
    shortcutone1,shortcutone2=poseshortcut.split(',')
    shortcutdang1,shortcutdang2=poseshortcut2.split(',')
    #画面端まで行くように処理
    global magnification
    x = x * magnification
    y = y * magnification
    #palmの時
    if(sign_id==0):
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
        pointermove(x,y)
        countpose = [0,0,0,0,0,0,0]


    if(sign_id==1):
        #Dangの処理
        #alt+f4押す処理
        global shortcutflag
        if(shortcutflag):
            if(countpose[1]<=10):
                countpose[1] += 1
            if(countpose[1]==10):
                pgui.hotkey(shortcutdang1,shortcutdang2)


    if(sign_id==2):
        #gunの時の処理
        if(countpose[2]<=3):
            countpose[2] += 1
        if(countpose[2]==3):
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
    if(sign_id==3):
        #peaceの時
        if(countpose[3]<4):
            countpose[3] += 1
        if(countpose[3]==3):
            autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
            pointermove(x,y)
        if(countpose[3]==4):
            pointermove(x,y)

    if(sign_id==4):
        #rockの時
        if(countpose[4]<=3):
            countpose[4] += 1
        if(countpose[4]==3):
            autopy.mouse.click(autopy.mouse.Button.LEFT)


    if(sign_id==5):
        #Threeの時
        if(countpose[5]<=3):
            countpose[5] += 1
        if(countpose[5]==3):
            autopy.mouse.click(autopy.mouse.Button.LEFT)
            autopy.mouse.click(autopy.mouse.Button.LEFT)

    if(sign_id==6):
        #oneの時の処理
        if(shortcutflag):
            if(countpose[6]<=10):
                countpose[6] += 1
            if(countpose[6]==10):
                pgui.hotkey(shortcutone1,shortcutone2)


    return countpose


def pointermove(x,y):
    try:
        autopy.mouse.move(x,y)
    except Exception as e:
        print(e)
