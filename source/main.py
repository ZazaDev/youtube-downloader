from __future__ import annotations
import threading

import GUI
import API
from GUI.definitions import *
from API.definitions import *

from datetime import datetime
import tkinter as tk

from GUI.download_popup import DownloadMenu

class Image:
    _value: TkImage
    raw: PILImage

    def __init__(self, pil_img: PILImage, **kw) -> None:
        self.raw = pil_img
        self._value = API.ImageOps.PILtoTkImage(pil_img, **kw)

    def __repr__(self) -> str:
        return self._value

    def height(self):
        return self._value.height()

    def width(self):
        return self._value.width()

class Video(GUI.Item):
    title: str
    views: int
    publish_date: datetime
    streams: Streams
    thumbnail: Image
    channel: Channel

    def __init__(self, video: pyVideo) -> None:
        self.title = video.title
        self.views = video.views
        self.publish_date = video.publish_date
        self.streams = video.streams
        self.thumbnail = Image(API.ImageOps.getImageFromURL(video.thumbnail_url, new_size=(250,200), crop=(0,60,0,60)))
        self.channel = Channel(video)

    def __repr__(self) -> str:
        return self.title

    def draw(self, canvas: tk.Canvas, draw_area: GUI.Box) -> Ids:
        _tag = f"vid{str(hash(self.title))[:4]}"
        
        id = canvas.create_image((draw_area.left, draw_area.top), anchor=NW, tag=_tag, image=self.thumbnail._value)

        box = GUI.Box(canvas.bbox(id))
        text_width = draw_area.right-box.right
        id = canvas.create_text((box.right+10, box.top), tag=_tag, anchor=NW, width=text_width, text=self.title, fill="white")

        box = GUI.Box(canvas.bbox(id))
        id = canvas.create_image((box.left, box.bottom + 15), anchor=NW, image=self.channel.icon._value)

        box = GUI.Box(canvas.bbox(id))
        id = canvas.create_text((box.right + 10, box.top + (box.bottom - box.top) // 2 - 7), anchor=NW, width=text_width, text=self.channel.name, fill="#AAAAAA")
        canvas.tag_bind(_tag, "<1>", lambda x, y=self.title: print(y))
        return _tag

    def getDimensions(self) -> GUI.Dimensions:
        return GUI.Dimensions(-1, self.thumbnail.height())

    def onUpdate(self, canvas: tk.Canvas, event: Event) -> None:
        return super().onUpdate(canvas, event)


class Channel:
    name: str
    icon: Image

    def __init__(self, video: pyVideo, res: ChannelIconRes = ChannelIconRes.R_48P) -> None:
        self.name = video.author
        self.icon = Image(API.ImageOps.getImageFromURL(API.ImageOps.getIconUrl(video, res)))


class Miniature(GUI.Item):
    thumbnail: Image

    def __init__(self, video: Video) -> None:
        self.thumbnail = Image(video.thumbnail.raw, new_size=(150,85), pad_color=(0,0,0))

    def draw(self, canvas: tk.Canvas, draw_area: GUI.Box) -> TkTag:
        pos = GUI.Position((draw_area.right - draw_area.left - self.thumbnail.width()) // 2,\
                       draw_area.top + (draw_area.bottom - draw_area.top - self.thumbnail.height()) // 2)
        canvas.create_image(tuple(pos), image=self.thumbnail._value, anchor=NW)

    def getDimensions(self) -> GUI.Dimensions:
        return GUI.Dimensions(-1, self.thumbnail.height())
    
    def onUpdate(self, canvas: tk.Canvas, event: Event) -> None:
        pass


class Aplication(tk.Tk):
    def __init__(self, geometry: str, screenName: Optional[str] = None, baseName: Optional[str] = None, className: Optional[str] = "Tk", useTk: Optional[bool] = True, sync: Optional[bool] = False, use: Optional[str] = None) -> None:
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        self.geometry(geometry)
        self.dimensions = GUI.Dimensions(tuple([int(i) for i in geometry.split('x')]))
        self.minsize(self.dimensions.width, self.dimensions.height)
        width = int(geometry.split('x')[0])

        self.sidebar = GUI.SideBar(150, 65)
        self.sidebar.setFootImage(API.ImageOps.PILtoTkImage(GUI.Assets.settings.value, 0.95))
        self.sidebar_amount = 0
        
        self.videos: List[Video] = []

        self.search: Dict[tk.Frame, GUI.Search]= {'Container': tk.Frame(self), 'Search': None}
        self.search['Container'].place(x=150, y=0, width=width-150, relheight=1)
        self.search['Search'] = GUI.Search(self.search['Container'])
        self.search['Search'].place(x=0, y=0, relheight=1, relwidth=1)

        temp = lambda qe,e: threading.Thread(name="OnSubmit", target=self.onSubmit, args=(qe,e)).start()
        self.search['Search'].head.setOnSubmit(temp)
        self.bind("<Configure>", self.onResize)


    def onSubmit(self, entry: GUI.QueryEntry, event: Event):
        search = self.search['Search']
        search.content.clear()

        if not entry._place_holder:
            try:
                vid = API.parseURL(entry.entry.get())
            except Exception as e:
                print(e)
                return
            
            videos = API.parseVideos(vid)
            temp = lambda v,e: threading.Thread(name="OnClickVideo", target=self.onClick, args=(v,e)).start()
            API.populate(videos, self.videos, Video, search.content.addItem, 6, bind=(["<1>"], temp))

    def onResize(self, event: Event):
        if(event.widget == self and
           (self.dimensions.width != event.width or self.dimensions.height != event.height)):
            new_width = event.width - 150
            self.search['Container'].place_configure(width=new_width)
            self.dimensions = GUI.Dimensions(event.width, event.height)

    def onClick(self, video: Video, event: Event):
        dm = DownloadMenu(self, video.streams)
        temp = lambda b,t,s,v=video: threading.Thread(name="OnDownload", target=self.onDMClick, args=(b,t,s,v)).start()
        dm.setOnClick(temp)

    def onDMClick(self, btn: tk.Button, type: str, streams: pytube.StreamQuery, video: Video):
        if type == 'Audio':
                streams.filter(abr=btn['text']).first().download("./../music")
        elif type == 'Video':
            streams = streams.filter(res=btn['text'])
            stream = streams.get_highest_resolution()
            if stream is None:
                stream = streams.first()
            stream.download("./../videos")
        self.sidebar.getBase().addItem(Miniature(video), self.sidebar_amount)
        self.sidebar_amount += 1


def main():
    app = Aplication(geometry="800x800", className="App", sync=True)

    app.mainloop()

if __name__ == '__main__':
    main()