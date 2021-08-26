import pytube
from typing import Callable, List
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
            self.url_field.bind(hook, lambda event, x=self.url_field: fun(event, x))


class Downloader:
    def __init__(self) -> None:
        pass

    def search(event: Event, caller: Entry):
        url = caller.get()
        try:
            pytube.YouTube(url)
        except:
            print("Invalid URL")
            return
        

def search(event: Event, caller: Entry):
    print(caller.get())


def main():
    gui = GUI("YouTube Downloader by Neonzada", "500x200")
    gui.setSearch(["<KP_Enter>", "<Return>"], search)
    gui.start()

if __name__ == '__main__':
    main()