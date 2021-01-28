#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp
import eel
import autopy
import base64

from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier

import PoseAction
#import hand_gui
import hand_gui_test
import traceback
import time
import xml.etree.ElementTree as ET

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
def set_confvalue():
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    for item in root:
        return item.find("mouse_sensitivity").text
@eel.expose
def set_poseshortcut():
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    for item in root:
        return item.find("poseshortcut").text
@eel.expose
def set_poseshortcut2():
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    for item in root:
        return item.find("poseshortcut2").text
@eel.expose
def set_poseshortcut3():
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    for item in root:
        return item.find("poseshortcut3").text
@eel.expose
def set_poseshortcut4():
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    for item in root:
        return item.find("poseshortcut4").text


@eel.expose #Conf.htmlで設定を保存する時に呼ばれるeel関数
def save_confvalue(value,shortcut_value1,shortcut_value2,shortcut_value3,shortcut_value4):
    tree =  ET.parse('conf.xml')
    root = tree.getroot()
    #for item in root.iter('setting'):
    for item in root:
        item.find("mouse_sensitivity").text = value
        item.find("poseshortcut").text = shortcut_value1
        item.find("poseshortcut2").text = shortcut_value2
        item.find("poseshortcut3").text = shortcut_value3
        item.find("poseshortcut4").text = shortcut_value4
    tree.write('conf.xml', encoding='UTF-8')

def HandTracking(cap, width, height, conf_flg = 0):
    # ×ボタンが押されたかのフラグ(hand_gui_test.py内の変数、flg_closePush)の初期化
    hand_gui_test.close_switch_py(0)
    # 引数解析 #################################################################
    args = get_args()

    flg_video = 0   #「1」でカメラが接続されていない
    flg_break = 0   #「1」で最初のループを抜け終了する⇒正常終了
    name_pose = "Unknown"
    focus_flg = 1   #index.html の表示・非表示の切り替え、「0」:Main.pyで開いた場合、「1」:HandTracking.pyで開いた場合
    namePose_flg = 1    #complete_old.htmlの開始・終了フラグ
    #flg_closePush = 0

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = True
    #width,height = autopy.screen.size() #eel で立ち上げた際の表示位置を指定するために取得
    PoseAction.sensitivity(set_confvalue()) #ポーズアクション用のマウス感度関数を初期設定
    PoseAction.shortcut_flag() #ショートカットポーズの動作ON/OFFのフラグを初期設定
    ShortCutList = [set_poseshortcut().split(","),set_poseshortcut2().split(","),set_poseshortcut3().split(","),set_poseshortcut4().split(",")]
    print(ShortCutList)

    while(True):    #カメラが再度接続するまでループ処理
        #カメラが接続されていないフラグの場合
        if(flg_video == 1):
            #カメラが接続されているか確認
            cap = cv.VideoCapture(cap_device)
            ret, frame = cap.read()
            if(ret is True):
                #カメラが接続されている場合
                name_pose = "Unknown"
                focus_flg = 1
                namePose_flg = 1
                #cap.release()
                eel.object_change("complete.html", True)
                eel.sleep(1)
                flg_video = 0
                print("【通知】WebCamera検知")
                #×ボタンフラグの初期化
                hand_gui_test.close_switch_py(0)
                #complete_html(width, height)
                continue    #最初の while に戻る
            else:
            #カメラが接続されていない場合
            #print("webcamないよ！！！")
                eel.sleep(0.01)
                time.sleep(0.01)
                continue    #最初の while に戻る
        elif(flg_break == 1):
            break   #最初の while を抜けて正常終了

        # カメラ準備 ###############################################################
        cap = cv.VideoCapture(cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

        # モデルロード #############################################################
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        keypoint_classifier = KeyPointClassifier()

        point_history_classifier = PointHistoryClassifier()

        # ラベル読み込み ###########################################################
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        with open(
                'model/point_history_classifier/point_history_classifier_label.csv',
                encoding='utf-8-sig') as f:
            point_history_classifier_labels = csv.reader(f)
            point_history_classifier_labels = [
                row[0] for row in point_history_classifier_labels
            ]

        # FPS計測モジュール ########################################################
        cvFpsCalc = CvFpsCalc(buffer_len=10)

        # 座標履歴 #################################################################
        history_length = 16
        point_history = deque(maxlen=history_length)

        # フィンガージェスチャー履歴 ################################################
        finger_gesture_history = deque(maxlen=history_length)

        #  ########################################################################
        mode = 0
        CountPose = [0,0,0,0,0,0,0]
        CountMotion = [0,0,0,0] # [Top,Right,Down,Left]
        identification = False
        while True:
            fps = cvFpsCalc.get()
            # キー処理(ESC：終了) #################################################
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break
            number, mode = select_mode(key, mode)

            # カメラキャプチャ #####################################################
            ret, image = cap.read()
            if not ret:
                #それぞれのフラグを立てて、システムを終了させ、最初の while に戻る
                flg_video = 1
                focus_flg = 0

                print("【通知】WebCameraが接続されていません。")
                eel.focusSwitch(width, height, focus_flg)
                eel.overlay_controll(True)
                eel.object_change("connect.html", True)
                cap.release()
                cv.destroyAllWindows()
                break

            image = cv.flip(image, 1)  # ミラー表示
            debug_image = copy.deepcopy(image)

            # 検出実施 #############################################################
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True

            #  ####################################################################
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                      results.multi_handedness):
                    # 外接矩形の計算
                    brect = calc_bounding_rect(debug_image, hand_landmarks)
                    # ランドマークの計算
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                    # 相対座標・正規化座標への変換
                    pre_processed_landmark_list = pre_process_landmark(
                        landmark_list)
                    pre_processed_point_history_list = pre_process_point_history(
                        debug_image, point_history)
                    # 学習データ保存
                    logging_csv(number, mode, pre_processed_landmark_list,
                                pre_processed_point_history_list)

                    # ハンドサイン分類
                    hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                    if hand_sign_id == 1:  # Dangサイン
                        point_history.append(landmark_list[8])  # 人差指座標
                    else:
                        point_history.append([0, 0])

                    # フィンガージェスチャー分類
                    finger_gesture_id = 0
                    point_history_len = len(pre_processed_point_history_list)
                    if point_history_len == (history_length * 2):
                        finger_gesture_id = point_history_classifier(
                            pre_processed_point_history_list)

                    # 直近検出の中で最多のジェスチャーIDを算出
                    finger_gesture_history.append(finger_gesture_id)
                    most_common_fg_id = Counter(
                        finger_gesture_history).most_common()

                    gesture_name = point_history_classifier_labels[most_common_fg_id[0][0]]

                    # 描画
                    debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                    debug_image = draw_landmarks(debug_image, landmark_list)
                    debug_image = draw_info_text(
                        debug_image,
                        brect,
                        handedness,
                        keypoint_classifier_labels[hand_sign_id],
                        gesture_name,
                    )

                    #人差し指の先の座標を取得
                    x,y = landmark_list[8]
                    #ジェスチャーが判定された回数をカウント
                    if gesture_name == 'Stop':
                        CountMotion = [0,0,0,0]
                    elif gesture_name == 'Move_Top':
                        Count_temp =  CountMotion[0]
                        Count_temp += 1
                        CountMotion = [Count_temp,0,0,0]
                    elif gesture_name == 'Move_Right':
                        Count_temp =  CountMotion[1]
                        Count_temp += 1
                        CountMotion = [0,Count_temp,0,0]
                    elif gesture_name == 'Move_Down':
                        Count_temp =  CountMotion[2]
                        Count_temp += 1
                        CountMotion = [0,0,Count_temp,0]
                    elif gesture_name == 'Move_Left':
                        Count_temp =  CountMotion[3]
                        Count_temp += 1
                        CountMotion = [0,0,0,Count_temp]

                    #各種操作の実行
                    CountPose,CountMotion = PoseAction.action(hand_sign_id,x,y,CountPose,CountMotion,ShortCutList)
                    name_pose = keypoint_classifier_labels[hand_sign_id]
                    eel.set_posegauge(str(name_pose))
                    identification = True

            else:
                point_history.append([0, 0])
                if identification == True:
                    eel.set_posegauge('None')
                    identification = False

            debug_image = draw_point_history(debug_image, point_history)
            debug_image = draw_info(debug_image, fps, mode, number)

            # 画面反映 #############################################################
            debug_image = cv.resize(debug_image,dsize=(400, 200))
            cv.imshow('Hand Gesture Recognition', debug_image)

            # eel立ち上げ #############################################################
            #cnt_gui, flg_end, flg_restart, flg_start, keep_flg = hand_gui.start_gui(cnt_gui, name_pose, flg_restart, flg_start, keep_flg)

            if(namePose_flg == 1):
                eel.object_change("complete_old.html", True)
                eel.sleep(0.01)
                print("【通知】準備完了")
                namePose_flg = 0
            elif(focus_flg == 1 and name_pose != 'Unknown'):
                eel.object_change("complete_old.html", False)
                eel.overlay_controll(False)
                eel.focusSwitch(width, height, focus_flg)
                print("【実行】index.html")
                eel.sleep(0.01)
                focus_flg = 0

            # eel立ち上げ #############################################################
            flg_end = hand_gui_test.start_gui()

            if(flg_end == 1):
                #正常に終了する処理(中間のループを抜ける)
                flg_break = 1
                eel.endSwitch() #flg_end の値をもとに戻す関数
                cap.release()
                cv.destroyAllWindows()
                eel.overlay_controll(False)
                eel.object_change("endpage.html", False)
                break

def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1
    if key == 104:  # h
        mode = 2
    return number, mode


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # キーポイント
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # 相対座標に変換
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # 1次元リストに変換
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # 正規化
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def pre_process_point_history(image, point_history):
    image_width, image_height = image.shape[1], image.shape[0]

    temp_point_history = copy.deepcopy(point_history)

    # 相対座標に変換
    base_x, base_y = 0, 0
    for index, point in enumerate(temp_point_history):
        if index == 0:
            base_x, base_y = point[0], point[1]

        temp_point_history[index][0] = (temp_point_history[index][0] -
                                        base_x) / image_width
        temp_point_history[index][1] = (temp_point_history[index][1] -
                                        base_y) / image_height

    # 1次元リストに変換
    temp_point_history = list(
        itertools.chain.from_iterable(temp_point_history))

    return temp_point_history


def logging_csv(number, mode, landmark_list, point_history_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
    if mode == 2 and (0 <= number <= 9):
        csv_path = 'model/point_history_classifier/point_history.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *point_history_list])
    return


def draw_landmarks(image, landmark_point):
    # 接続線
    if len(landmark_point) > 0:
        # 親指
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
            (255, 255, 255), 2)

        # 人差指
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
            (255, 255, 255), 2)

        # 中指
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
            (255, 255, 255), 2)
        # 薬指
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
            (255, 255, 255), 2)

        # 小指
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
            (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
            (255, 255, 255), 2)

        # 手の平
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
            (0, 255, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
            (0, 255, 0), 6)

    # キーポイント
    for index, landmark in enumerate(landmark_point):
        cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 255), -1)
        cv.putText(image,str(index),(landmark[0], landmark[1]), cv.FONT_HERSHEY_SIMPLEX, 0.6,(255,255,255),2,cv.LINE_AA)
    return image


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # 外接矩形
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (200, 255, 0), 1)

    return image


def draw_info_text(image, brect, handedness, hand_sign_text,
                   finger_gesture_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (200, 255, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    cv.putText(image, 'Pose:'+hand_sign_text, (10, 120),cv.FONT_HERSHEY_SIMPLEX, 1.0, (200, 255, 0), 4, cv.LINE_AA)
    cv.putText(image, 'Pose:'+hand_sign_text, (10, 120),cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)

    if finger_gesture_text != "":
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (200, 255, 0), 4, cv.LINE_AA)
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)

    return image


def draw_point_history(image, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv.circle(image, (point[0], point[1]), 1 + int(index / 2),
                      (152, 251, 152), 2)

    return image


def draw_info(image, fps, mode, number):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (200, 255, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (255, 255, 255), 2, cv.LINE_AA)

    mode_string = ['Logging Key Point', 'Logging Point History']
    if 1 <= mode <= 2:
        cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                   cv.LINE_AA)
        if 0 <= number <= 9:
            cv.putText(image, "NUM:" + str(number), (10, 110),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                       cv.LINE_AA)
    return image
