from __future__ import annotations
from re import I, T

from GUI.sidebar import SideBar
from GUI.definitions import *
from GUI import Search
import API.downloader as downloader
import tkinter

class Video(Item):
    title: str
    views: int
    publish_date: datetime
    streams: Streams
    thumbnail: Union[PILImage, TkImage]
    channel: Channel

    def __init__(self, video: pyVideo) -> None:
        self.title = video.title
        self.views = video.views
        self.publish_date = video.publish_date
        self.streams = video.streams
        self.thumbnail = downloader.getImageFromURL(video.thumbnail_url, 0.5, (0,45,0,45))
        self.channel = Channel(video)

    def __repr__(self) -> str:
        return self.title

    def draw(self, canvas: Canvas, draw_area: Box) -> Ids:
        _tag = f"vid{str(hash(self.title))[:4]}"
        
        self.thumbnail = downloader.PILtoTkImage(self.thumbnail)
        id = canvas.create_image((draw_area.left, draw_area.top), anchor=NW, tag=_tag, image=self.thumbnail)

        box = Box(canvas.bbox(id))
        text_width = draw_area.right-box.right
        id = canvas.create_text((box.right+10, box.top), tag=_tag, anchor=NW, width=text_width, text=self.title, fill="white")

        box = Box(canvas.bbox(id))
        self.channel.icon = downloader.PILtoTkImage(self.channel.icon)
        id = canvas.create_image((box.left, box.bottom + 15), anchor=NW, image=self.channel.icon)

        box = Box(canvas.bbox(id))
        id = canvas.create_text((box.right + 10, box.top + (box.bottom - box.top) // 2 - 7), anchor=NW, width=text_width, text=self.channel.name, fill="#AAAAAA")
        canvas.tag_bind(_tag, "<1>", lambda x, y=self.title: print(y))
        return [id]

    def getDimensions(self) -> Dimensions:
        return Dimensions(-1, self.thumbnail.height)

    def onUpdate(self, canvas: Canvas, event: Event) -> None:
        return super().onUpdate(canvas, event)


class Channel:
    name: str
    icon: Union[PILImage, TkImage]

    def __init__(self, video: pyVideo, res: ChannelIconRes = ChannelIconRes.R_48P) -> None:
        self.name = video.author
        self.icon = downloader.getImageFromURL(downloader.getIconUrl(video, res))


class Aplication(tkinter.Tk):
    def __init__(self, geometry: str, screenName: Optional[str] = None, baseName: Optional[str] = None, className: Optional[str] = "Tk", useTk: Optional[bool] = True, sync: Optional[bool] = False, use: Optional[str] = None) -> None:
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        self.geometry(geometry)
        width = int(geometry.split('x')[0])

        self.sidebar = SideBar(150, 65)
        self.videos: List[Video] = []

        self.search: Dict[tkinter.Frame, Search]= {'Container': tkinter.Frame(self), 'Search': None}
        self.search['Container'].place(x=150, y=0, width=width-150, relheight=1)
        self.search['Search'] = Search(self.search['Container'])
        self.search['Search'].place(x=0, y=0, relheight=1, relwidth=1)

        self.search['Search'].head.setOnSubmit(self.onSubmit)

    def onSubmit(self, entry: tkinter.Event, event: Event):
        search = self.search['Search']
        search.content.clear()

        try:
            vid = downloader.parseURL(entry.get())
        except Exception as e:
            print(e)
            return
        
        videos = downloader.parseVideos(vid)
        downloader.populate(videos, self.videos, Video, search.content.addItem, 6)


def main():
    app = Aplication(geometry="800x800", className="App", sync=True)

    app.mainloop()

if __name__ == '__main__':
    main()