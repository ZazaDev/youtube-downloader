#TODO: rename files with their respective quality after the video title, like "videotitle_1080p.mp4"
#Generally improve this trash code I made on a hurry :p

import pytube

#import os

from tkinter import *

root = Tk()
root.title("YouTube Downloader by neonzada")
root.geometry("500x200")

#Gets URL from the text box then downloads it
def download1080():
    url = urlEntry.get()
    yt = pytube.YouTube(url)
    video = yt.streams.filter(res="1080p").first().download()

    #os.rename(video,"1080.mp4")

    video.download('')

def download720():
    url = urlEntry.get()
    yt = pytube.YouTube(url)
    video = yt.streams.filter(res="720p").first().download()
    video.download('')

def download480():
    url = urlEntry.get()
    yt = pytube.YouTube(url)
    video = yt.streams.filter(res="480p").first().download()
    video.download('')

def download360():
    url = urlEntry.get()
    yt = pytube.YouTube(url)
    video = yt.streams.filter(res="360p").first().download()
    video.download('')

def download240():
    url = urlEntry.get()
    yt = pytube.YouTube(url)
    video = yt.streams.filter(res="240p").first().download()
    video.download('')

def download144():
    url = urlEntry.get()
    yt = pytube.YouTube(url)
    video = yt.streams.filter(res="144p").first().download()
    video.download('')

#GUI stuff

#Header
head = Label(root, text="YouTube Downloader", fg="red", font=("Calibri", 15))
head.pack(fill=X)

#URL stuff
holder = Frame(root)
holder.place(x=100, y=30)

urlText = Label(holder, text = "Enter URL", font=('Calibri', 12))
urlText.grid(row=0, column=0)

urlEntry = Entry(holder, font=('Calibri', 15))
urlEntry.grid(row=0, column=1, pady=20)

urlWarn = Label(holder, text = "360p/720p for Whatsapp", fg="red", font=('Calibri', 10))
urlWarn.grid(row=5, columnspan=2)

#Buttons

btn = Button(holder, text="Download 1080p",command=download1080)
btn.grid(row=1, columnspan=1)

btn = Button(holder, text="Download 720p", command=download720)
btn.grid(row=2, columnspan=1)

btn = Button(holder, text="Download 480p",command=download480)
btn.grid(row=3, columnspan=1)

btn = Button(holder, text="Download 360p",command=download360)
btn.grid(row=1, columnspan=2)

btn = Button(holder, text="Download 240p",command=download240)
btn.grid(row=2, columnspan=2)

btn = Button(holder, text="Download 144p",command=download144)
btn.grid(row=3, columnspan=2)

root.mainloop()