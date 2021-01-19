#試作用！！！！！！！！！！##############################
#うまくいけば、hand_gui.py にそのまま移行予定######################

import eel
import base64
import cv2 as cv
import time
import datetime
import traceback
import autopy

flg_end = 0 #終了ボタンを押されたかのフラグ
flg_closePush = 0   #×ボタンを押されたかのフラグ(eelから管理)
#flg_closePush_py = 0    #×ボタンを押されたかのフラグ(pythonから管理)
width,height = autopy.screen.size()

@eel.expose
def open_endpage():
    #終了画面の、 endpage.html を立ち上げる
    eel.start("html/endpage.html",
                mode='chrome',
                size=(800,450),  #サイズ指定（横, 縦）
                position=(width/4, height/4), #位置指定（left, top）
                block=False
                )
    eel.sleep(0.01)

@eel.expose
def sysclose_switch(end_switch):
    #正常終了する場合のフラグを立てる、元の数値（flg_end=0）に戻す
    global flg_end
    flg_end = end_switch

@eel.expose
def close_switch(closePush):
    #×ボタンが押されたフラグの変更(eelから)
    close_switch_py(closePush)

def close_switch_py(closePush_py):
    #×ボタンが押されたフラグの変更(pythonから)
    global flg_closePush
    flg_closePush = closePush_py

def start_gui(name_pose, flg_restart, keep_flg):
    print("flg_closePush:", flg_closePush)
    if(flg_restart == 1):   #inde.html が立ち上がっているか
        eel.windowclose()
        eel.init("GUI/web")
        #eel.start("開きたい上記のフォルダ下のファイル名",～
        eel.start("html/index.html",
                    mode='chrome',
                    size=(400, 200),  #サイズ指定（横, 縦）
                    position=(width,height), #位置指定（left, top）
                    block=False
                    )
        flg_restart = 0
        print("html再スタート！！！")

    if(flg_closePush == 1):
        #×ボタンが押された際の動作
        eel.init("GUI/web")
        #eel.start("開きたい上記のフォルダ下のファイル名",～
        eel.start("html/index.html",
                    mode='chrome',
                    size=(400, 200),  #サイズ指定（横, 縦）
                    position=(width,height), #位置指定（left, top）
                    block=False
                    )
        eel.sleep(0.01)
        print("再起動！！！！")
        close_switch_py(0)
        return flg_end, flg_restart, keep_flg
    else:
        #正常動作
        eel.sleep(0.01)
        #eel.set_posegauge(name_pose)
        return flg_end, flg_restart, keep_flg

def cam_source():
    eel.init('GUI/web')
    eel.start('html/check.html',block=False)
    num = eel.js_function()()
    print(num)
    return int(num)
