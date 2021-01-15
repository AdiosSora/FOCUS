import autopy
import eel
import pyautogui as pgui

#倍率
magnification = 1
shortcutflag = False

@eel.expose
def shortcuton():
    global shortcutflag
    shortcutflag = True
def sensitivity(value):
    global magnification
    #倍率を1.0から2.0までの範囲で実装
    magnification = 1 + int(value)*0.1
def action(sign_id,x,y,countpose):
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
                pgui.hotkey('alt','f4')


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
                pgui.hotkey('ctrl', 'c')


    return countpose


def pointermove(x,y):
    try:
        autopy.mouse.move(x,y)
    except Exception as e:
        print(e)
