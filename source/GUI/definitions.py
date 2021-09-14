from __future__ import annotations

from tkinter import Event
from tkinter.constants import *
from typing import *

URL        = str
Ids        = Tuple[int, ...]
Point      = Tuple[int,int]
Bbox       = Tuple[int,int,int,int]
Event      = Event
TkTag      = str

def RGBtoHex(R: int, G: int, B: int):
    return "#{:02x}{:02x}{:02x}".format(R,G,B)