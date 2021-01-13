import tkinter as tk
import math
from win32api import GetSystemMetrics
# ウィンドウ作成
label = tk.Tk()
label.title("splash")
label.minsize(870, 490)

# 画像表示
#fileに適当なpng画像を指定してください。
haruna1 = tk.PhotoImage(file="splash.png")

label = tk.Canvas(bg="black", width=870, height=490)
label.master.overrideredirect(True)
label.place(x=0, y=0)
label.create_image(0, 0, image=haruna1, anchor=tk.NW)
window_width = 870
window_height = 490
create_width = math.floor(GetSystemMetrics(0)/2-window_width/2)
create_height = math.floor(GetSystemMetrics(1)/2-window_height/2)
label.master.geometry(str(window_width) + "x" + str(window_height) + "+" + str(create_width) + "+" + str(create_height))
label.master.lift()
label.master.wm_attributes("-topmost", True)
label.master.wm_attributes("-disabled", True)

label.pack()
# label.after(3000, call_back_func)
# label.after(3000, lambda: label.quit())
label.after(2000, lambda: [print("call_back_funcの実行"), label.quit()])
label.mainloop()
label.destroy()
