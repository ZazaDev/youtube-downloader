from GUI.definitions import *
from API.definitions import *
import requests
from io import BytesIO
from PIL import ImageOps, ImageTk
from time import time

import threading
import pytube

session = requests.Session()
class Query(Enum):
    Playlist = 0
    Search   = 1
    Video    = 1

def elapsed_time(funcao):
    def wrapper(*args, **kw):
        start = time()
        thread_name = funcao(*args, **kw)
        end = time()

        print(f"{thread_name} took {end-start}s")

    return wrapper

_threads = []

def populate(py_videos: List[pytube.YouTube], videos: List[Item], creator: object, callback: Callable[[Item], None], count: int = -1, **kw):
    if count == -1:
        count = len(py_videos)
    for i in range(count):
        t = threading.Thread(name=py_videos[i].title, target=_populate, args=(py_videos[i], videos, creator, callback), kwargs=kw)
        _threads.append(t)
        t.start()
    return "T"

def _populate(py_vid: pytube.YouTube, videos: List[Item], creator: object, callback: Callable[[Item], None], **kw):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        name = threading.currentThread().name
        try:
            vid = creator(py_vid)
        except:
            return name
        videos.append(vid)
        callback(vid)
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    return name

def parseURL(url: URL) -> PytubeObj:
    if url:
        if "watch?v=" in url:
            return pytube.YouTube(url)
        elif "playlist" in url:
            return pytube.Playlist(url)
        else:
            return pytube.Search(url)
    else:
        raise RuntimeError("Url empty")

def parseVideos(obj: PytubeObj) -> List[Item]:
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
    if isinstance(search, pytube.Search):
        search.get_next_results()


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
    data = session.get(url)
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

