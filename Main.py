import eel
import traceback
import HandTracking
import cv2
import win32gui, win32con
from win32api import GetSystemMetrics
import tkinter as tk
import math

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

    label = tk.Tk()
    label.title("splash")
    label.minsize(870, 490)

    splash = tk.PhotoImage(file="splash.gif")
    gif_index = 0

    def next_frame():
        global gif_index
        try:
            splash.configure(format="gif -index {}".format(gif_index))

            gif_index += 1
        except tk.TclError:
            gif_index = 0
            return next_frame()
        else:
            label.after(1, next_frame)

    label = tk.Canvas(bg="black", width=870, height=490)
    label.master.overrideredirect(True)
    label.place(x=0, y=0)
    label.create_image(0, 0, image=splash, anchor=tk.NW)
    window_width = 870
    window_height = 490
    create_width = math.floor(GetSystemMetrics(0)/2-window_width/2)
    create_height = math.floor(GetSystemMetrics(1)/2-window_height/2)
    label.master.geometry(str(window_width) + "x" + str(window_height) + "+" + str(create_width) + "+" + str(create_height))
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)

    label.pack()
    label.after(3000, lambda: [print("call_back_funcの実行"), label.quit()])
    label.after_idle(next_frame)
    label.mainloop()

    while True:
        keep_flg = 0    #HandPose.py 開始前に connect.html を起動したか、「1」で起動済み、 test.html が2つ起動するのを防ぐ
        if(continue_flg == 0):
            try:
                eel.init("GUI/web")
                label.master.destroy()
                eel.start('html/index.html',size=(800,450),block=False)
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
                        print("【通知】WebCameraが接続されていません。")
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
