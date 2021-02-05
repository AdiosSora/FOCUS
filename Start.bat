@echo off
bin\python.exe -m pip install tensorflow==2.4.0
bin\python.exe -m pip install mediapipe==0.8.2
bin\python.exe -m pip install eel==0.14.0
bin\python.exe -m pip install pywin32==300
bin\python.exe -m pip install autopy==4.0.0
bin\python.exe -m pip install PyAutoGUI==0.9.52
bin\python.exe Main.py
pause
