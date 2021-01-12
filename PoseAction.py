import autopy


def action(sign_id,x,y,countpose):
    #画面端まで行くように処理
    x = x * 1.1
    y = y * 1.1
    #palmの時
    if(sign_id==0):
        try:
            autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
            pointermove(x,y)
            countpose = [0,0,0,0,0,0,0]
        except Exception as e:
            print(e)

    # if(sign_id==1):
    #     #Dangの処理
    #     if(countpose[1]<=3):
    #         countpose[1] += 1
    #     if(countpose[1]==3):
    #         autopy.mouse.click(autopy.mouse.Button.LEFT)

    if(sign_id==2):
        #gunの時の処理
        if(countpose[4]<=3):
            countpose[4] += 1
        if(countpose[4]==3):
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
        if(countpose[2]<=3):
            countpose[2] += 1
        if(countpose[2]==3):
            autopy.mouse.click(autopy.mouse.Button.LEFT)


    # if(sign_id==5):
        #OKの

    # if(sign_id==6):
        #fourの時の処理

    return countpose


def pointermove(x,y):
    try:
        autopy.mouse.move(x,y)
    except Exception as e:
        print(e)
