import autopy


def action(sign_id,x,y):
    x = x * 1.1
    y = y * 1.1
    #palmの時
    if(sign_id==0):
        try:
            autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
            autopy.mouse.move(x,y)
        except Exception as e:
            print(e)
    if(sign_id==1):
        #Dangの処理
        autopy.mouse.click(autopy.mouse.Button.LEFT)
    # if(sign_id==2):
        #gunの時の処理

    if(sign_id==3):
        try:
            autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
            autopy.mouse.move(x,y)
        except Exception as e:
            print(e)
    if(sign_id==4):
        autopy.mouse.click(autopy.mouse.Button.RIGHT)

    # if(sign_id==5):
        #OKの

    # if(sign_id==6):
        #fourの時の処理
