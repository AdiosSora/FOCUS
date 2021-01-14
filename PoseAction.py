import autopy
import eel
#倍率
magnification = 1

# @eel.expose
def sensitivity(value):
    global magnification
    #倍率を1.0から2.0までの範囲で実装
    magnification = 1 + value*0.1
def action(sign_id,x,y,countpose):
    #画面端まで行くように処理
    global magnification
    print(magnification)
    x = x * magnification
    y = y * magnification
    #palmの時
    if(sign_id==0):
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
        pointermove(x,y)
        countpose = [0,0,0,0,0,0,0]


    if(sign_id==1):
        #Dangの処理
        if(countpose[1]<=10):
            countpose[1] += 1
        if(countpose[1]==10):
            autopy.key.toggle(autopy.key.Code.F4,True,[autopy.key.Modifier.META])
            autopy.key.toggle(autopy.key.Code.ALT,True,[autopy.key.Modifier.META])
        if(countpose[1]==15):
            autopy.key.toggle(autopy.key.Code.F4,False,[autopy.key.Modifier.META])
            autopy.key.toggle(autopy.key.Code.ALT,False,[autopy.key.Modifier.META])

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

    # if(sign_id==6):
    #     #oneの時の処理
    #     if(countpose[6]<=3):
    #         countpose[6] += 1
    #     if(countpose[6]==3):
    #         autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    #         pointermove(x,y)
    #         countpose = [0,0,0,0,0,0,0]

    return countpose


def pointermove(x,y):
    try:
        autopy.mouse.move(x,y)
    except Exception as e:
        print(e)
