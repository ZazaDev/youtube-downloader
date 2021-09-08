import pytube
from typing import Callable, List, Tuple
from tkinter import *
from GUI.definitions import *

class GUI:
    def __init__(self, title: str, geometry : str) -> None:
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(geometry)

        self.header = Label(self.root, text="YouTube Downloader", fg="red", font=("Calibri", 15))
        self.header.pack(side=TOP)
        
        self.frame = Frame(self.root)
        self.frame.pack(side=TOP)

        # URL Input Frame
        self.url_field = Frame(self.frame)
        self.url_field.grid(row=1, column=1, columnspan=2)

        self.url_label = Label(self.url_field, text = "Enter URL:", font=('Calibri', 12))
        self.url_label.grid(row=1, column=1)

        self.url_query = Entry(self.url_field, font=('Calibri', 15))
        self.url_query.grid(row=2, column=1, pady=5)


        # Resolutions Buttons
        self.res_field = Frame(self.frame, name="res_field")
        print(str(self.res_field))
        self.res_field.grid(row=2, column=1)

        resolutions = ["1444p", "1080p", "720p", "480p", "360p", "240p", "144p"]
        self.btns = [Button(self.res_field, text=f"Download {res}") for res in resolutions]

        GUI.arrangeButton(self.btns)

        # Bottom Text
        self.url_warn = Label(self.frame, text = "360p/720p for Whatsapp", fg="red", font=('Calibri', 10))
        self.url_warn.grid(row=3, columnspan=2)
    
    def start(self):
        self.root.mainloop()

    def setBtnFunc(self, func: Callable) -> None:
        for btn in self.btns:
            string = btn['text'].split(' ')[-1]
            btn.configure(command=lambda x=string: func(x))

    def setSearch(self, hooks: List[str], fun: Callable) -> None:
        for hook in hooks:
            self.url_query.bind(hook, fun)

    @staticmethod
    def arrangeButton(btns: List[Button]):
        for (index, btn) in enumerate(btns):
            print(btn['text'])
            half_way = len(btns) // 2
            if len(btns) % 2 == 1 and btn == btns[-1]:
                btn.grid(row=half_way+1, column=1, columnspan=2, sticky='nesw')
            elif index < half_way:
                btn.grid(row=index%half_way+1, column=1, sticky='nesw')
            else:
                btn.grid(row=index%half_way+1, column=2, sticky='nesw')
        


class Downloader:
    def __init__(self) -> None:
        self.stream    : List[pytube.Stream] = []
        self.relations : List[Tuple]         = []

    def __getParentWidget(self, widget: Widget) -> Widget:
        parent_name = widget.winfo_parent()
        return widget._nametowidget(parent_name)

    def search(self, event: Event) -> None:
        URL = event.widget.get()

        try:
            video = pytube.YouTube(URL)
        except:
            print("Invalid URL")
            return

        self.streams = video.streams.filter(mime_type="video/mp4")

        frames = self.__getParentWidget(self.__getParentWidget(event.widget)).winfo_children()
        frame = [frame for frame in frames if "res_field" in str(frame)][0]

        for child in frame.winfo_children():
            if isinstance(child, Button):
                print(child['text'])
                res = child['text'].split(' ')[-1]
                streams = self.streams.filter(res=res)
                print(streams)
                if(not streams):
                    child.grid_remove()
                else:
                    child.grid()
                    child['command'] = lambda x=streams.first(), y=f'{video.title}-{res}', z='mp4/': self.download(x, y, z)

    def download(self, stream: pytube.Stream, title: str, path: str) -> None:
        print(f'{title}:\n\t{stream}')
        stream.download(filename=f'{title}.mp4', output_path=path)


def main() -> None:
    gui = GUI("YouTube Downloader by Neonzada", "500x300")
    downloader = Downloader()
    gui.setSearch(["<KP_Enter>", "<Return>"], downloader.search)
    gui.start()

if __name__ == '__main__':
    main()