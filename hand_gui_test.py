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
width,height = autopy.screen.size()

@eel.expose
def open_endpage():
    #終了画面の、 endpage.html を立ち上げる
    eel.start("html/endpage.html",
                mode='chrome',
                size=(800,450),  #サイズ指定（横, 縦）
                position=(width/2-250, height/2-250), #位置指定（left, top）
                block=False
                )
    eel.sleep(0.01)

@eel.expose
def py_sysclose():
    #正常終了する場合のフラグを立てる
    global flg_end
    flg_end = 1

def start_gui(name_pose, flg_restart, keep_flg):
    #print("hand_gui_test.html だよ！！！！！！！！！！！！！！！！！！！！！！")
    if(flg_restart == 1):   #inde.html が立ち上がっているか
        eel.init("GUI/web")
        #eel.start("開きたい上記のフォルダ下のファイル名",～
        eel.start("html/index.html",
                    mode='chrome',
                    size=(500, 150),  #サイズ指定（横, 縦）
                    position=(width,height), #位置指定（left, top）
                    block=False
                    )
        flg_restart = 0
        print("html再スタート！！！")
    while(True):
        try:    #index.htmlが × をクリックして終了した場合をキャッチ
            eel.sleep(0.01) #コメントアウトするとindex.htmlにつながらないっぽい
            eel.set_posegauge(name_pose)
            return flg_end, flg_restart, keep_flg
        # except OSError as os_e:
        #     traceback.print_exc()
        #     continue
        except SystemExit as sys_e:
            #print("000000000000000000000")
            traceback.print_exc()
            #print("4444444444444444444444444")

            #ここから、test.html を使うときに使用
            eel.init("GUI/web")
            #eel.start("開きたい上記のフォルダ下のファイル名",～
            eel.start("html/index.html",
                        mode='chrome',
                        size=(500, 150),  #サイズ指定（横, 縦）
                        position=(width,height), #位置指定（left, top）
                        block=False
                        )
            eel.sleep(0.01)
            print("再起動！！！！")
            return flg_end, flg_restart, keep_flg

def cam_source():
    eel.init('GUI/web')
    eel.start('html/check.html',block=False)
    num = eel.js_function()()
    print(num)
    return int(num)
