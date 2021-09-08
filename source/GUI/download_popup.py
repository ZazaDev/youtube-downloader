from __future__ import annotations
from sys import path
from tkinter.constants import EW, NE, NSEW, TOP, W, X
path.append('/home/yadard/Dev/One_Language_Projects/Python/youtube-downloader/source')

from GUI.definitions import *
from API.definitions import *

import tkinter as Tk

class DownloadMenu:
    def __init__(self, root: Tk.Tk) -> None:
        self.menu = Tk.Toplevel(root)
        self.menu.title("Menu")
        self.menu.geometry("500x400")

        self.head = Tk.Frame(self.menu, bg="black")
        self.head.pack(side=TOP, fill=X)

        self.foot = Tk.Frame(self.menu, bg="green")
        self.foot.pack(side=TOP, fill=X)

        self.head_label = Tk.Label(self.head, text="Videos:", background="black", fg="white", anchor=W)
        self.head_label.pack(side=TOP, fill=X, anchor=NW)

        self.buttons_frame = Tk.Frame(self.head, bg='red')
        self.buttons_frame.pack(side=TOP, fill=X)

        self.buttons = [Tk.Button(self.buttons_frame, width=5, background="blue", text=f"{i}") for i in range(10)]
        for index, btn in enumerate(self.buttons):
            half = len(self.buttons) // 2
            if index < half:
                btn.grid(row=0, column=index, padx=(0, 5), sticky=EW)
            else:
                btn.grid(row=1, column=index-half, padx=(0, 5), sticky=EW)
        
        self.foot_label = Tk.Label(self.head, text="Audio:", background="black", fg="white", anchor=W)
        self.foot_label.pack(side=TOP, fill=X, anchor=NW)

        self.foot_btns = Tk.Frame(self.head, bg='red')
        self.foot_btns.pack(side=TOP, fill=X)

        self.btns = [Tk.Button(self.foot_btns, width=5, background="yellow", text=f"{i}") for i in range(10)]
        for index, btn in enumerate(self.btns):
            half = len(self.btns) // 2
            if index < half:
                btn.grid(row=0, column=index, padx=(0, 5))
            else:
                btn.grid(row=1, column=index-half, padx=(0, 5))


root = Tk.Tk()
root.geometry("800x400")
root.iconify()
DownloadMenu(root)

root.mainloop()