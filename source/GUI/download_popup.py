from __future__ import annotations
from dataclasses import dataclass
from tkinter.constants import EW, NE, NSEW, TOP, W, X
from pytube.request import stream

from setuptools import command

from GUI.definitions import *
from API.definitions import *
import API

import tkinter as tk

class ButtonGrid(tk.Frame):
    label: tk.Label
    buttons: List[tk.Button]
    command: Callable[[tk.Button, str], None]

    def __init__(self, master: Union[tk.Misc, None], info: ButtonGrid.ButtonInfo, **kw) -> None:
        super().__init__(master, **kw)
        self.label = tk.Label(self, anchor=W, bg="#101010", text=info.title, fg="white")
        self.label.pack(side=TOP, anchor=W, fill=X, expand=True)
        
        self._btns = tk.Frame(self, bg="")
        self._btns.pack(side=TOP, fill=X, expand=True)
        self.buttons = [tk.Button(self._btns, text=string) for string in info.texts]
        for i, btn in enumerate(self.buttons):
            self._btns.grid_columnconfigure(i%info.col_per_row, minsize=info.width)
            btn.grid(column=i%info.col_per_row, row=i//info.col_per_row, sticky=EW, padx=info.padx, pady=info.pady)
            btn.configure(command=lambda x=btn:self.onClick(x))

    def configureButtons(self, **kw):
        for btn in self.buttons:
            btn.configure(**kw)

    def setOnClick(self, command: Callable[[tk.Button, str], None]):
        self.command = command

    def onClick(self, button):
        print(self.command(button, self.label['text'][:-1]))


    @dataclass
    class ButtonInfo:
        title: str
        texts: List[str]
        col_per_row: int
        width: int
        padx: Tuple[int, int] = (0,0)
        pady: Tuple[int, int] = (0,0)


class DownloadMenu:
    def __init__(self, root: tk.Tk, streams: pytube.StreamQuery) -> None:
        self.menu = tk.Toplevel(root)
        self.menu.title("Download")
        self.menu.geometry("")
        self.menu.configure(background="black")
        self.on_click = None
        self.streams = streams


        video = ButtonGrid.ButtonInfo("Video:", DownloadMenu.sortVideoInfo(streams), 5, 70, padx=(0,2))
        self.video = ButtonGrid(self.menu, video, width=150, bg="black")
        self.video.configureButtons(highlightthickness=1, highlightbackground="#303030", border=0, bg="#121212", fg="#AAAAAA")
        self.video.command = self.onClick
        self.video.pack(side=TOP, fill=X, expand=True)

        audio = ButtonGrid.ButtonInfo("Audio:", DownloadMenu.sortAudioInfo(streams), 5, 70, padx=(0,2))
        self.audio = ButtonGrid(self.menu, audio, width=150, bg="black")
        self.audio.configureButtons(highlightthickness=1, highlightbackground="#303030", border=0, bg="#121212", fg="#AAAAAA")
        self.audio.command = self.onClick
        self.audio.pack(side=TOP, fill=X, expand=True)

        self.menu.update()
        width, height = self.menu.winfo_width()+10, self.menu.winfo_height()+10
        self.menu.minsize(width, height)
        self.menu.maxsize(width, height)
        self.menu.update()

    @staticmethod
    def sortVideoInfo(streams: pytube.StreamQuery) -> Tuple[str]:
        unsorted_res = [stream.resolution for stream in streams.filter(mime_type="video/mp4", progressive=True) if not stream is None ]
        sorted_res = [f"{r}p" for r in sorted([int(r[:-1]) for r in unsorted_res], reverse=True)]
        return tuple(dict.fromkeys(sorted_res).keys())

    @staticmethod
    def sortAudioInfo(streams: pytube.StreamQuery) -> Tuple[str]:
        streams = streams.filter(mime_type='audio/mp4')
        unsorted_qualities = [stream.abr for stream in streams]
        sorted_qualities = [str(abbr)+'kbps' for abbr in sorted([int(abr[:-4]) for abr in unsorted_qualities], reverse=True)]
        return tuple(dict.fromkeys(sorted_qualities).keys())

    def onClick(self, btn: tk.Button, type: str):
        self._on_click(btn, type, self.streams)

    def setOnClick(self, func: Callable[[tk.Button, str, pytube.StreamQuery], None]) -> None:
        self._on_click = func


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x400")
    root.iconify()
    vid = pytube.YouTube(r"https://www.youtube.com/watch?v=S0ChbadMH4s")
    dm = DownloadMenu(root, vid.streams)
    def foo(btn: tk.Button, type: str, video: pyVideo):
        if type == 'Audio':
            video.streams.filter(abr=btn['text']).first().download("./../music")
        elif type == 'Video':
            streams = video.streams.filter(res=btn['text'])
            stream = streams.get_highest_resolution()
            if stream is None:
                stream = streams.first()
            stream.download("./../videos")
        
    dm.setOnClick(foo)


    root.mainloop()