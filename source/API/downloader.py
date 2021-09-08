import multiprocessing
from sys import argv
from time import sleep
from tkinter.constants import Y
from pytube import query

from pytube.contrib.playlist import Playlist
from GUI.definitions import *
from API.definitions import *
import requests
from io import BytesIO
from PIL import ImageOps, ImageTk
from time import time
import asyncio

import threading
import pytube

class Query(Enum):
    Playlist = 0
    Search   = 1
    Video    = 1

def elapsed_time(funcao):
    def wrapper(*args, **kw):
        # Calcula o tempo de execução
        start = time()
        thread_name = funcao(*args, **kw)
        end = time()

        # Formata a mensagem que será mostrada na tela
        print(f"{thread_name} took {end-start}s")

    return wrapper

@dataclass
class Video(Video):
    title: str
    views: int
    publish_date: datetime
    thumbnail: Union[TkImage, PILImage, None]
    channel: Channel

    def __init__(self, video: pytube.YouTube, res: Optional[ChannelIconRes] = ChannelIconRes.R_48P, **kw):
        self.title = video.title
        self.views = video.views
        self.publish_date = video.publish_date
        self.thumbnail = getImageFromURL(video.thumbnail_url, **kw)
        self.channel = Channel(video, res)

class Channel(Channel):
    name: str
    channel_icon: Union[TkImage, PILImage, None]

    def __init__(self, video: pytube.YouTube, res: ChannelIconRes):
        self.name = video.author
        self.channel_icon = getImageFromURL(getIconUrl(video, res))

_threads = []

def populate(py_videos: List[pytube.YouTube], videos: List[Video], callback: Callable, count: int = -1, **kw):
    if count == -1:
        count = len(py_videos)
    for i in range(count):
        t = threading.Thread(name=py_videos[i].title, target=_populate, args=(py_videos[i], videos, callback), kwargs=kw)
        _threads.append(t)
        t.start()
    return "T"

@elapsed_time
def _populate(py_vid: pytube.YouTube, videos: List[Video], callback: Callable, **kw):
    vid = Video(py_vid, **kw)
    videos.append(vid)
    name = threading.currentThread().name
    callback(vid)
    return name

def parseURL(url: URL) -> PytubeObj:
    if url:
        if "watch?v=" in url:
            return pytube.YouTube(url)
        elif "playlist" in url:
            return pytube.Playlist(url)
        else:
            return pytube.Search(url)

def parseVideos(obj: PytubeObj) -> List[Video]:
    if isinstance(obj, pytube.Search):
        return obj.results
    if isinstance(obj, pytube.YouTube):
        return [obj]
    if isinstance(obj, pytube.Playlist):
        vids = []
        for vid in obj.videos:
            vids.append(vid)
        return vids

def getMoreResults(search: pytube.Search):
    if not isinstance(search, pytube.Search):
        return
    pytube.Search.get_next_results()


def getAspectRatio(img: Image.Image) -> float:
    width, height = img.size
    ratio = width / height
    return ratio

def getNewSize(img: Image.Image, resize: Porcentage):
    height = img.size[1]
    ratio = getAspectRatio(img)
    new_height = int(height * resize)
    new_width = int(new_height * ratio)
    return (new_width, new_height)

def getImageFromURL(url: URL, resize: Optional[Porcentage] = None, crop: Optional[Borders] = None) -> PILImage:
    data = requests.get(url)
    img = Image.open(BytesIO(data.content))
    if not crop is None:
        img = ImageOps.crop(img, crop)
    if not resize is None:
        img = img.resize(getNewSize(img, resize), Image.ANTIALIAS)
    return img

def PILtoTkImage(img: PILImage, resize: Optional[Porcentage] = None, crop: Optional[Borders] = None) -> TkImage:
    if not crop is None:
        img = ImageOps.crop(img, crop)
    if not resize is None:
        img = img.resize(getNewSize(img, resize), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def getIconUrl(vid: pytube.YouTube, res: ChannelIconRes) -> URL:
    url = ""
    start = vid.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents']
    for i in range(len(start)):
        try:
            url = start[i]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']\
                ['thumbnail']['thumbnails'][res.value]['url']
        except KeyError:
            pass
        if url:
            return url

