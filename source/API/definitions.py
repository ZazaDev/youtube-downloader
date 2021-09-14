from PIL import ImageTk, Image
from typing import *
from enum import Enum
import pytube

TkImage    = ImageTk.PhotoImage
PILImage   = Image.Image
Streams    = pytube.Stream
pyVideo    = pytube.YouTube
PytubeObj  = Union[pytube.Search, pytube.YouTube, pytube.Playlist]
Size       = Tuple[int, int]
Borders    = Tuple[int, int, int, int]
Porcentage = float
R = int
G = int
B = int
A = int

class ChannelIconRes(Enum):
    R_48P  = 0
    R_88P  = 1
    R_176P = 2