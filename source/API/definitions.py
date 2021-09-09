from PIL import ImageTk, Image
from typing import *
from enum import Enum
from pytube import Search, YouTube, Playlist
import pytube

TkImage    = ImageTk.PhotoImage
PILImage   = Image.Image
Streams    = pytube.Stream
pyVideo    = pytube.YouTube
PytubeObj  = Union[Search, YouTube, Playlist]
Size       = Tuple[int, int]
Borders    = Tuple[int, int, int, int]
Porcentage = float

class ChannelIconRes(Enum):
    R_48P  = 0
    R_88P  = 1
    R_176P = 2