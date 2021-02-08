import eel
import base64
import cv2 as cv
import time
import datetime
import traceback
import autopy

flg_end = 0 #終了ボタンを押されたかのフラグ
flg_closePush = 0   #×ボタンを押されたかのフラグ(eelから管理)
width,height = autopy.screen.size()

@eel.expose
def open_endpage():
    #終了画面の、 endpage.html を立ち上げる
    eel.overlay_controll(True)
    eel.object_change("endpage.html", True)
    eel.sleep(0.01)

@eel.expose
def close_endpage():
    #終了画面の、 endpage.html を閉じる
    eel.overlay_controll(False)
    eel.object_change("endpage.html", False)
    eel.sleep(0.01)

@eel.expose
def sysclose_switch(end_switch):
    #正常終了する場合のフラグを立てる、元の数値（flg_end=0）に戻す
    global flg_end
    flg_end = end_switch

@eel.expose
def close_switch(closePush):
    #×ボタンが押されたフラグ(eelから)を別関数に渡す
    close_switch_py(closePush)

def close_switch_py(closePush_py):
    #×ボタンが押されたフラグの変更(pythonから)
    global flg_closePush
    flg_closePush = closePush_py

def start_gui():
    if(flg_closePush == 1 ):
        start = time.time()
        #×ボタンが押された際の動作
        eel.init("GUI/web")
        #eel.start("開きたい上記のフォルダ下のファイル名",～
        eel.start("html/index.html",
                    port = 0,
                    mode='chrome',
                    size=(400, 200),  #サイズ指定（横, 縦）
                    position=(width,height), #位置指定（left, top）
                    block=False
                    )
        eel.sleep(0.01)
        print("【通知】index.html再起動")
        #×ボタンのフラグの初期化
        close_switch_py(0)
        return flg_end
    else:
        try:
            #正常動作
            eel.sleep(0.01)
            #eel.set_posegauge(name_pose)
        except SystemExit:
            traceback.print_exc()
            print("【通知】SystemExit発生")
        finally:
            return flg_end

def cam_source():
    eel.init('GUI/web')
    eel.start('html/check.html',block=False)
    num = eel.js_function()()
    print(num)
    return int(num)
