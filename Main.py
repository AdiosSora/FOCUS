import eel
import traceback
import HandTracking
import cv2
import win32gui, win32con

start_flg = 0   #HandPose.py の開始フラグ、「1」で開始
end_flg = 0 #システム終了のフラグ、「1」で終了

#コンソールを消すときはここのコメントアウトを消してください。
#The_program_to_hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(The_program_to_hide , win32con.SW_HIDE)

@eel.expose
def start_flg():
    #起動する場合のフラグを立てる
    global start_flg
    start_flg = 1

@eel.expose
def end_flg():
    #正常終了する場合のフラグを立てる
    global end_flg
    end_flg = 1

if __name__ == '__main__':
    continue_flg = 0    #Start.html が起動しているか判別、「1」で起動中
    #eel.init("GUI/web")

#    def my_other_thread():
#        while True:
#            print("I'm a thread")
#            eel.sleep(1.0)                  # Use eel.sleep(), not time.sleep()

#    eel.spawn(my_other_thread)

    #eel.start('html/Start.html',size=(640,320),block=False)
    while True:
        keep_flg = 0    #HandPose.py 開始前に connect.html を起動したか、「1」で起動済み、 test.html が2つ起動するのを防ぐ
        if(continue_flg == 0):
            try:
                eel.init("GUI/web")
                eel.start('html/Start.html',size=(800,450),block=False)
                continue_flg = 1
                eel.sleep(0.01)
            except:
                #SystemExit および OSError をキャッチ
                traceback.print_exc()
                continue
        #print("I'm a main loop")
        #eel.sleep(1.0)
        elif(start_flg == 1):
            #「起動」を押下時の処理
            continue_flg = 0
            webcam_flg = 0  #connect.html が起動中か判別、「1」で起動中

            #カメラが接続されているか確認
            while(True):
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if(ret is True):
                    if(webcam_flg == 1):
                        eel.windowclose()
                    print("【通知】WebCamera検知")
                    break
                else:
                    if(webcam_flg == 0):
                        eel.init('GUI/web')
                        eel.start('html/connect.html',
                                    mode='chrome',
                                    size=(800,450),  #サイズ指定（横, 縦）
                                    #position=(width/2-250, height/2-300), #位置指定（left, top）
                                    block=False)
                        eel.sleep(0.01)
                        webcam_flg = 1
                        keep_flg = 1
                    else:
                        eel.sleep(0.01)

            print("【実行】HandTracking.py")
            HandTracking.HandTracking(keep_flg)    #HandPose.py が終了するまで、 Main.py の以降の処理を行わない
            start_flg = 0
        elif(end_flg == 1):
            #「終了」を押下時の処理
            print("【実行】終了処理")
            break
        else:
            eel.sleep(0.01)
    # while(i<10000):
    #     eel.sleep(0.01)
    #     print(i)
    #     i+=1
    #traceback.print_exc()
    print("【通知】システム終了")
