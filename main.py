from main_ref import download
import pytube
from typing import Callable, List, Tuple
from tkinter import *

class GUI:
    def __init__(self, title: str, geometry: str) -> None:
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)

        self.header = Label(self.root, text="YouTube Downloader", fg="red", font=("Calibri", 15))
        self.header.pack(fill=X)
        
        #URL Input Frame
        self.frame = Frame(self.root)
        self.frame.place(x=100, y=30)

        self.urlText = Label(self.frame, text = "Enter URL", font=('Calibri', 12))
        self.urlText.grid(row=0, column=0)

        self.urlWarn = Label(self.frame, text = "360p/720p for Whatsapp", fg="red", font=('Calibri', 10))
        self.urlWarn.grid(row=5, columnspan=2)

        self.url_field = Entry(self.frame, font=('Calibri', 15))
        self.url_field.grid(row=0, column=1, pady=20)


        #Resolutions Buttons
        resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        self.btns = [Button(self.frame, text=f"Download {res}") for res in resolutions]

        for (index, btn) in enumerate(self.btns):
            print(btn['text'])
            if index < 3:
                btn.grid(row=index%3+1, columnspan=1)
            else:
                btn.grid(row=index%3+1, columnspan=2)
    
    def start(self):
        self.root.mainloop()

    def setBtnFunc(self, func: Callable) -> None:
        for btn in self.btns:
            string = btn['text'].split(' ')[-1]
            btn.configure(command=lambda x=string: func(x))

    def setSearch(self, hooks: List[str], fun: Callable):
        for hook in hooks:
            self.url_field.bind(hook, fun)


class Downloader:
    def __init__(self) -> None:
        self.stream    : List[pytube.Stream] = []
        self.relations : List[Tuple]         = []

    def search(self, event: Event):
        URL = event.widget.get()

        try:
            video = pytube.YouTube(URL)
        except:
            print("Invalid URL")
            return

        self.streams = video.streams.filter(mime_type="video/mp4")

        frame_name = event.widget.winfo_parent()
        frame = event.widget._nametowidget(frame_name)

        for child in frame.winfo_children():
            if isinstance(child, Button):
                print(child['text'])
                res = child['text'].split(' ')[-1]
                streams = self.streams.filter(res=res)
                if(not streams):
                    child.grid_remove()
                else:
                    child.grid()
                    child['command'] = lambda x=streams.first(), y=video.title: self.download(x, y)

    def download(self, stream: pytube.Stream, title: str):
        print(f'{title}:\n\t{stream}')
        stream.download(title)


#TODO: Imbelezar
def search(event: Event):
    URL = event.widget.get()

    try:
        video = pytube.YouTube(URL)
    except:
        print("Invalid URL")
        return
    streams = video.streams.filter(mime_type="video/mp4")

    frame_name = event.widget.winfo_parent()
    frame = event.widget._nametowidget(frame_name)

    for child in frame.winfo_children():
        if isinstance(child, Button):
            print(child['text'])
            res = child['text'].split(' ')[-1]
            if(not streams.filter(res=res)):
                child.grid_remove()
            else:
                child.grid()

def main():
    gui = GUI("YouTube Downloader by Neonzada", "500x200")
    downloader = Downloader()
    gui.setSearch(["<KP_Enter>", "<Return>"], downloader.search)
    gui.start()

if __name__ == '__main__':
    main()