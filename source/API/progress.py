from __future__ import annotations
from enum import Flag
from logging import disable, root
from numpy.core.fromnumeric import resize
from numpy.lib.arraysetops import isin

from numpy.lib.stride_tricks import DummyArray
from API import ImageOps
from API.definitions import *
from GUI.definitions import *
import threading
from PIL import Image as PImage
import pytube
import tkinter as tk
import numpy as np
from time import sleep
from os import system
from math import sqrt
from copy import deepcopy
import queue

class Image:
    raw: PILImage
    value: TkImage

    def __init__(self, img: PILImage, **kw) -> None:
        self.raw = ImageOps.PILOperations(img, **kw)
        self.value = ImageOps.PILtoTkImage(img)

    def changeImage(self, func: Callable, **kw):
        self.raw = func(self.raw, **kw)
        self.value = ImageOps.PILtoTkImage(self.raw)

class Item:
    bg: Image
    fg: Image
    frames: queue.Queue[TkImage] = queue.Queue()
    animation_thread: threading.Thread = None
    animation_info: Item.AnimationInfo = None
    _done: bool = False

    def __init__(self, video: pytube.YouTube) -> None:
        img = ImageOps.getImageFromURL(video.thumbnail_url)
        self.fg = Image(img, crop=(0,65,0,65), new_size=(150,85))
        self.bg = Image(self.fg.raw)
        self.bg.changeImage(ImageOps.blend, rgba=(255,255,255,180))
        self.animation_info = self.AnimationInfo()

    def animation(self, canvas: tk.Canvas, id: int):
        while not self._done:
            frame = self.frames.get()
            canvas.after(0, self._animation, frame, canvas, id)
            self.animation_info.frames_shown += 1
            if self.animation_info.frames_shown == 100:
                self._done = True
            sleep(1)
    
    def _animation(self, canvas: tk.Canvas, id: int):
        self.animation_info.current_frame.value = ImageOps.PILtoTkImage(self.animation_info.current_frame.raw)
        canvas.itemconfigure(id, image=self.animation_info.current_frame.value)
        canvas.update()
    
    @dataclass
    class AnimationInfo:
        last_pos:   Position   = Position(0,0)
        chunk:      Dimensions = None
        rest_chunk: Dimensions = None
        current_progress: int  = 0
        frames_shown: int = 0
        current_frame: Image = None




def calcChunk(img_size: Dimensions) -> Dimensions:
    chunk_size = Dimensions(int(img_size.width / 10), int(img_size.height / 10))
    chunk_rest = Dimensions(img_size.width % 10, img_size.height % 10)

    return chunk_size, chunk_rest

prog = 0
started = False

def progress(item: Item, canvas, id):
    def isLastCellInRow(current_chunk: int) -> bool:
        return current_chunk % 10 == 9

    def isFirstCellInRow(current_chunk: int) -> bool:
        return current_chunk % 10 == 0

    def isInRow(current_chunk: int, row: int) -> bool:
        start = 10*row
        end = start + 9
        return start <= current_chunk <= end

    info = item.animation_info
    if info.chunk is None:
        info.chunk, info.rest_chunk = calcChunk(Dimensions(item.fg.raw.size))
    x, y = 0, 0
    bg_pixels = np.array(item.bg.raw)
    fg_pixels = np.array(item.fg.raw)
    info.current_frame = Image(PImage.fromarray(bg_pixels))
    _progress = 0

    global prog

    while _progress < 100:
        if _progress == prog:
            sleep(0.1)
            continue
        else:
            _progress = prog

            for chunk in range(info.current_progress, _progress):
                height = info.chunk.height
                if info.rest_chunk.height:
                    if isFirstCellInRow(chunk) and not isInRow(chunk, 0):
                        info.rest_chunk.height -= 1
                    if info.rest_chunk.height:
                        height += 1

                for row in range(height):
                    y = info.last_pos.y + row

                    width = info.chunk.width
                    if info.rest_chunk.width:
                        width += 1
                        info.rest_chunk.width -= 1
                    
                    for col in range(width):
                        x = info.last_pos.x + col
                        for channel in range(3): # (R, G, B)
                            bg_pixels[y, x, channel] = fg_pixels[y, x, channel]
                        bg_pixels[y, x, 3] = 255 # A

                    if row == height - 1:
                        if isLastCellInRow(chunk):
                            info.last_pos.y = y + 1
                            info.last_pos.x = 0
                        else:
                            info.last_pos.x = x + 1
                sleep(0.010)
                canvas.after(0, item._animation, canvas, id)
            info.current_progress = _progress
    print('finished')


def onProgress(stream: pytube.Stream, chunk: bytes, bytes_remaning: int, **kw):
    pro = int((stream.filesize - bytes_remaning) / stream.filesize * 100)

    global prog, started
    prog = pro
    if not started:
        started = True
        # item = kw.pop('item')
        # threading.Thread(name='animation', target=item.animation, kwargs=kw, daemon=True).start()
        progress(**kw)

root = tk.Tk()
root.geometry("800x500")

canvas = Canvas(root)
canvas.place(x=0,y=0,relwidth=1,relheight=1)

bg = canvas.create_image((0,0), anchor=NW)
fg = canvas.create_image((0,0), anchor=NW)

vid = pytube.YouTube(r"https://youtu.be/HXV3zeQKqGY")
it = Item(vid)
it.fg.changeImage(ImageOps.PILOperations)
it.bg.changeImage(ImageOps.PILOperations)

# print(calcChunk(Dimensions(i.fg.raw.size)))
canvas.itemconfigure(bg, image=it.bg.value) 

vid.register_on_progress_callback(lambda s,c,b,canvas=canvas,id=fg,item=it: threading.Thread(target=onProgress, args=(s,c,b), kwargs={'canvas':canvas, 'id':id, 'item':item}).start())
def foo(x,y):
    system(r"rm -rf /home/yadard/Dev/One_Language_Projects/Python/youtube-downloader/tests/image/test.mp4")
vid.register_on_complete_callback(foo)
root.update()
root.after(20, threading.Thread(name="download", target=vid.streams.first().download, args=(r"/home/yadard/Dev/One_Language_Projects/Python/youtube-downloader/tests/image/test.mp4",)).start)

root.mainloop()