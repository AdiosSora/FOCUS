#system起動時、右下に表示されるwindow呼び出しソース
import eel
import autopy
import tkinter as tk
from tkinter import messagebox

baseGround = tk.Tk()
baseGround.title("FOCUS")

ww=baseGround.winfo_screenwidth()
wh=baseGround.winfo_screenheight()
w = ww - 400
h = wh - 145

baseGround.geometry("400x75"+"+"+str(w)+"+"+str(h))
button = tk.Button(baseGround, text="Quit", command=baseGround.quit)
button.pack()


def on_exit():
    """When you click to exit, this function is called"""
    #width,height = autopy.screen.size()
    eel.init("GUI/web")
    eel.start('html/endpage.html',size=(800,450),block=False)
    eel.sleep(0.01)

baseGround.protocol("WM_DELETE_WINDOW", on_exit)

baseGround.mainloop()
# #
# class App(tk.Tk):
#
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.title("Handling WM_DELETE_WINDOW protocol")
#         self.geometry("200x100"+str(w)+str(h))
#         self.make_topmost()
#         self.protocol("WM_DELETE_WINDOW", self.on_exit)
#
#     def on_exit(self):
#         """When you click to exit, this function is called"""
#         if messagebox.askyesno("Exit", "Do you want to quit the application?"):
#             self.destroy()
#
#     def center(self):
#         """Centers this Tk window"""
#         self.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
#
#     def make_topmost(self):
#         """Makes this window the topmost window"""
#         self.lift()
#         self.attributes("-topmost", 1)
#         self.attributes("-topmost", 0)
#
#
# if __name__ == '__main__':
#     App().mainloop()
