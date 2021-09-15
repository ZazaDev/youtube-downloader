from re import I
from GUI import Item
from GUI.definitions import *
from API.definitions import *

from time import time

import threading
import pytube
from moviepy.editor import VideoFileClip, AudioFileClip
from os import remove
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

def populate(py_videos: List[pytube.YouTube], videos: List[Item], creator: object, after: Callable, callback: Callable[[Item], None], count: int = -1, **kw):
    if count == -1 or count > len(py_videos):
        count = len(py_videos)
    for i in range(count):
        t = threading.Thread(name=py_videos[i].title, target=_populate, args=(py_videos[i], videos, creator, after, callback), kwargs=kw)
        _threads.append(t)
        t.start()
    return "T"

@elapsed_time
def _populate(py_vid: pytube.YouTube, videos: List[Item], creator: object, after: Callable, callback: Callable[[Item], None], **kw):
    name = threading.currentThread().name
    try:
        vid = creator(py_vid)
    except Exception as e:
        print(e)
        return name
    videos.append(vid) 
    after(0, lambda: callback(vid, **kw))
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

# This take way to long
def uniteAudioAndVideo(video_path: str, audio_path: str) -> None:
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    videoclip = video.set_audio(audio)
    videoclip.write_videofile(video_path)
    remove(video_path)
    remove(audio_path)

if __name__ == '__main__':
    uniteAudioAndVideo(r"C:\Dev\One_Language_Projects\Python\youtube-downloader\source\API\ALL OF THE UI!  Hazel Dev Log.mp4", r"C:\Dev\One_Language_Projects\Python\youtube-downloader\source\API\【PV】【血界战线 OP】【Helloworld!】 无字幕版.mp4")