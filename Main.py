import eel
import traceback
from utils import HandTracking
import cv2 as cv
import win32gui, win32con
from win32api import GetSystemMetrics
import tkinter as tk
import math
import autopy
import xml.etree.ElementTree as ET

import time
from utils import PoseAction
import argparse
import base64

start_flg = 0   #HandTracking.py の開始フラグ、「1」で開始
end_flg = 0 #システム終了のフラグ、「1」で終了
width,height = autopy.screen.size()
sel_cam = 999
decideFlg = 0

The_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(The_program_to_hide , win32con.SW_HIDE)


@eel.expose #手識別機能の起動ボタンを押されたときに呼ばれるeel関数
def start_flg():
    #起動する場合のフラグを立てる
    print("【通知】起動ボタン押下")
    global start_flg
    start_flg = 1

@eel.expose #手識別機能の終了ボタンを押された時のeel関数
def end_flg():
    #正常終了する場合のフラグを立てる
    print("【通知】終了ボタン押下")
    global end_flg
    end_flg = 1

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=1920)
    parser.add_argument("--height", help='cap height', type=int, default=1080)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args

@eel.expose
def decide_cam(num):
    decide_cam_py(num)

def decide_cam_py(decNum):
    global sel_cam
    sel_cam = decNum

@eel.expose
def decide_flg():
    decide_flg_py(1)

def decide_flg_py(flg):
    global decideFlg
    decideFlg = flg

if __name__ == '__main__':
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    focus_flg = 0   #index.html の表示・非表示の切り替え、「0」:Main.pyで開いた場合、「1」:HandTracking.pyで開いた場合
    eel.init("GUI/web")

    label = tk.Tk()
    label.title("splash")
    label.minsize(870, 490)

    splash = tk.PhotoImage(file="utils/splash.gif")
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

    label.master.destroy()
    eel.start('html/index.html',
                port = 0,
                mode='chrome',
                size=(1025,775),
                position=(width/4, height/4),
                block=False)
    eel.sleep(0.01)

    while True:
        #以降「終了」ボタンが押下されるまでループ
        if(start_flg == 1):
            #「起動」を押下時の処理
            eel.overlay_controll(True)
            eel.object_change("complete.html", True)
            eel.sleep(1)

            cap = cv.VideoCapture(cap_device)
            #cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
            #cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
            ret, frame = cap.read()
            if(ret is True):
                cap.release()
                eel.overlay_controll(True)
                eel.object_change("demo1.html", True)
                #eel.sleep(1)
                sel_cam_before = 999

                while(True):
                    if(decideFlg == 1):
                        if(sel_cam != sel_cam_before):
                            cap = cv.VideoCapture(sel_cam)
                            cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
                            cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
                            ret, frame = cap.read(sel_cam)
                            if(ret is False):
                                eel.alert_mess()
                                cap.release()
                                decide_cam_py(999)
                                decide_flg_py(0)
                                sel_cam_before = sel_cam
                                continue
                            else:
                                decide_flg_py(0)
                                break
                        decide_flg_py(0)
                        break
                    if(sel_cam != 999):
                        eel.sleep(0.01)
                        if(sel_cam != sel_cam_before):
                            if(sel_cam_before != 999):
                                cap.release()
                            cap = cv.VideoCapture(sel_cam)
                            cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
                            cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
                            sel_cam_before = sel_cam
                        ret, frame = cap.read()
                        if(ret is True):
                            # UI側へ転送(画像) #####################################################
                            _, imencode_image = cv.imencode('.jpg', frame)
                            base64_image = base64.b64encode(imencode_image)
                            eel.set_base64image("data:image/jpg;base64," + base64_image.decode("ascii"))
                            continue
                        else:
                            eel.alert_mess()
                            cap.release()
                            decide_cam_py(999)
                            sel_cam_before = sel_cam
                            if(decideFlg == 1):
                                decide_flg_py(0)
                            continue
                    else:
                        eel.sleep(0.01)

            else:
                cap.release()
                if(webcam_flg == 0):
                    print("【通知】WebCameraが接続されていません。")
                    eel.object_change("connect.html", True)
                    eel.sleep(0.01)
                    time.sleep(0.01)
                    webcam_flg = 1
                    continue
                else:
                    eel.sleep(0.01)
                    time.sleep(0.01)
                    continue
            eel.overlay_controll(True)
            eel.object_change("complete.html", True)
            eel.sleep(1)
            webcam_flg = 0  #connect.html が起動中か判別、「1」で起動中

            print("【実行】HandTracking.py")
            HandTracking.HandTracking(cap, width, height,)    #HandTracking.py が終了するまで、 Main.py の以降の処理を行わない
            eel.focusSwitch(width, height, focus_flg)
            cap.release()
            start_flg = 0
            decide_cam_py(999)
            decide_flg_py(0)
        elif(end_flg == 1):
            #「終了」を押下時の処理
            cap.release()
            print("【実行】終了処理")
            break
        else:
            eel.sleep(0.01)

    print("【通知】システム終了")
