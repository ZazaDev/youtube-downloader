#TODO: rename files with their respective quality after the video title, like "videotitle_1080p.mp4"
#Generally improve this trash code I made on a hurry :p

from os import utime
import pytube
from pytube import exceptions
#import os
from tkinter import *
from abc import ABC, abstractclassmethod
from enum import Enum

from pytube.request import stream

root = Tk()
root.title("YouTube Downloader by neonzada")
root.geometry("500x200")

#Gets URL from the text box then downloads it

def download(res: str) -> None:
    url = urlEntry.get()
    try:
        yt = pytube.YouTube(url)
    except:
        print("URL invalid")
        return
    
    stream = yt.streams.filter(res=res, mime_type="video/mp4")
    stream.get_highest_resolution().download(yt.title)
#GUI stuff

#Header
head = Label(root, text="YouTube Downloader", fg="red", font=("Calibri", 15))
head.pack(fill=X)

#URL stuff
holder = Frame(root)
holder.place(x=100, y=30)

urlText = Label(holder, text = "Enter URL", font=('Calibri', 12))
urlText.grid(row=0, column=0)

urlWarn = Label(holder, text = "360p/720p for Whatsapp", fg="red", font=('Calibri', 10))
urlWarn.grid(row=5, columnspan=2)

#Buttons

btn1080 = Button(holder, text="Download 1080p", command=lambda : download("1080p"), )
btn1080.grid(row=1, columnspan=1)

btn720 = Button(holder, text="Download 720p", command=lambda : download("720p"), )
btn720.grid(row=2, columnspan=1)

btn480 = Button(holder, text="Download 480p", command=lambda : download("480p"), )
btn480.grid(row=3, columnspan=1)

btn360 = Button(holder, text="Download 360p", command=lambda : download("360p"), )
btn360.grid(row=1, columnspan=2)

btn240 = Button(holder, text="Download 240p", command=lambda : download("240p"), )
btn240.grid(row=2, columnspan=2)

btn144 = Button(holder, text="Download 144p", command=lambda : download("144p"), )
btn144.grid(row=3, columnspan=2)

btns = [btn1080, btn720, btn480, btn360, btn240, btn144]
for b in btns:
    b.grid_remove()

sv = StringVar()

def validate(event):
    try:
        yt = pytube.YouTube(sv.get())
    except:
        print("URL invalid")
        return True

    streams = yt.streams.filter(mime_type="video/mp4")
    for s in streams:
        print(s)
    for btn in btns:
        res = btn['text'].split(' ')[-1]
        print(streams.filter(res=res))
        if(not streams.filter(res=res)):
            btn.grid_remove()
        else:
            btn.grid()
    return True

urlEntry = Entry(holder, textvariable=sv, font=('Calibri', 15))
urlEntry.bind('<Return>', validate)
urlEntry.bind('<KP_Enter>', validate)
urlEntry.grid(row=0, column=1, pady=20)

root.mainloop()