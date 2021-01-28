import autopy
import eel
import pyautogui as pgui
import xml.etree.ElementTree as ET
import subprocess
#倍率
magnification = 1
shortcutflag = 0
#ドラッグ解除フラグ
drag_flag = False

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

def shortcut_flag():
    global shortcutflag
    #倍率を1.0から2.0までの範囲で実装
    shortcutflag = int(set_shortcutflag())

def action(sign_id,x,y,countpose,countmotion,ShortCutList):
    #画面端まで行くように処理
    global magnification
    global drag_flag
    x = x * magnification
    y = y * magnification
    #palmの時
    if(sign_id==0):
        if(drag_flag):
            # autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
            pgui.mouseUp(button='left')
            drag_flag = False
        pointermove(x,y)
        countpose = [0,0,0,0,0,0,0]


    if(sign_id==1):
        #Dangの処理
        #alt+f4押す処理
        global shortcutflag
        if(shortcutflag):
            # if(countpose[1]<=10):
            #     countpose[1] += 1
            # if(countpose[1]==10):
            #     pgui.hotkey(shortcutdang1,shortcutdang2)

            print(countmotion)
            for index,item in enumerate(countmotion):
                print(item)
                if item == 15:
                    hotkeyLen = len(ShortCutList[index])
                    if hotkeyLen == 1:
                        break
                    elif hotkeyLen == 2:
                        pgui.hotkey(ShortCutList[index][0],ShortCutList[index][1])
                    elif hotkeyLen == 3:
                        pgui.hotkey(ShortCutList[index][0],ShortCutList[index][1],ShortCutList[index][2])

    if(sign_id==2):
        #gunの時の処理
        if(countpose[2]<=3):
            countpose[2] += 1
        if(drag_flag==False):
            if(countpose[2]==3):
                autopy.mouse.click(autopy.mouse.Button.RIGHT)


    if(sign_id==3):
        #peaceの時
        if(countpose[3]<4):
            countpose[3] += 1
        if(countpose[3]==3):
            # autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
            pgui.mouseDown(button='left')
            pointermove(x,y)
            drag_flag = True
        if(countpose[3]==4):
            pointermove(x,y)

    if(sign_id==4):
        #rockの時
        if(countpose[4]<=3):
            countpose[4] += 1
        if(drag_flag==False):
            if(countpose[4]==3):
                autopy.mouse.click(autopy.mouse.Button.LEFT)

    if(sign_id==5):
        #Threeの時
        if(countpose[5]<=3):
            countpose[5] += 1
        if(drag_flag==False):
            if(countpose[5]==3):
                autopy.mouse.click(autopy.mouse.Button.LEFT)
                autopy.mouse.click(autopy.mouse.Button.LEFT)

    if(sign_id==6):
        #oneの時の処理
        tree =  ET.parse('conf.xml')
        root = tree.getroot()
        one_flag = True
        for item in root:
            one_flag = item.find("keyboard").text
        if(countpose[6]<=3):
            countpose[6] += 1
        if(countpose[6]==3):
            print(one_flag)
            # if(one_flag == 'True'):
            subprocess.Popen(r'.\GUI\flikkey\exe\keyBoard.exe')
                # for item in root:
                #     # item.find("keyboard").text = 'False'
                # tree.write('conf.xml', encoding='UTF-8')


    return countpose,countmotion

def pointermove(x,y):
    try:
        autopy.mouse.move(x,y)
    except Exception as e:
        print(e)
