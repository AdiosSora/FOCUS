import tkinter as tk

# ウィンドウ作成
label = tk.Tk()
label.title("splash")
label.minsize(870, 490)

# 画像表示
#fileに適当なpng画像を指定してください。
haruna = tk.PhotoImage(file="splash.png")

label = tk.Canvas(bg="black", width=870, height=490)
label.master.overrideredirect(True)
label.place(x=0, y=0)
label.create_image(0, 0, image=haruna, anchor=tk.NW)
window_width = 870
window_height = 490
label.master.geometry(str(window_width) + "x" + str(window_height) + "+400+300")
label.master.lift()
label.master.wm_attributes("-topmost", True)
label.master.wm_attributes("-disabled", True)

def call_back_func():
    print("call_back_funcの実行")
    label.quit()
    # label.destroy()
    # =============================
    # 色々と実験しましたが、結局 quit() すれば、mainloopを抜けることができることを発見しました。
    # destroyではmainloopを抜けられないので、注意されたし。
    # ==============================


label.pack()
# label.after(3000, call_back_func)
# label.after(3000, lambda: label.quit())
label.after(3000, lambda: [print("call_back_funcの実行"), label.quit()])
label.mainloop()

# メインループ
