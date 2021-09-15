from __future__ import annotations

from API.definitions import *
from API.image_op import ImageOps
import GUI

from abc import ABC, abstractmethod
from tkinter import Canvas, Tk
from dataclasses import dataclass
from copy import deepcopy
import threading


class Image:
    raw: PILImage
    value: TkImage

    def __init__(self, img: PILImage, **kw) -> None:
        self.raw = ImageOps.PILOperations(img, **kw)
        self.value = ImageOps.PILtoTkImage(img)

    def changeImage(self, func: Callable, **kw):
        self.raw = func(self.raw, **kw)
        self.value = ImageOps.PILtoTkImage(self.raw)

    def height(self):
        return self.value.height()

    def width(self):
        return self.value.width()

class DownloadTarget(ABC):
    bg: Image
    _bg: PILImage
    fg: Image
    stream: Stream
    animation_info: DownloadTarget.AnimationInfo = None

    def __init__(self, register_on_progress, register_on_complete, stream) -> None:
        on_progress = lambda s,c,b: threading.Thread(name="on_progress", target=self.onProgress, args=(s,c,b)).start()
        on_complete = lambda s,p: threading.Thread(name="on_complete", target=self.onComplete, args=(s,p)).start()
        register_on_progress(on_progress)
        register_on_complete(on_complete)
        self.stream = stream
        self.animation_info = deepcopy(DownloadTarget.AnimationInfo())
    
    @abstractmethod
    def animation(self, pixels: Pixels) -> None:
        """This connect the Animation.progress() with the tkinter"""

    @abstractmethod
    def onProgress(self, stream: Stream, chunk: bytes, bytes_remaning: int) -> None:
        """Called on progress"""

    @abstractmethod
    def onComplete(self, stream: Stream, path: Optional[str]) -> None:
        """Called when download finishes"""

    def getToplevel(self) -> Tk:
        """take the GUI's root to perform a root.after()"""

    def download(self, path: str) -> None:
        threading.Thread(name=f"Download: {self.stream.title}", target=self.stream.download, args=(path,)).start()

    @staticmethod
    def getProgress(stream: pytube.Stream, bytes_remaning: int) -> int:
        return int((stream.filesize - bytes_remaning)/stream.filesize * 100)
    
    @dataclass
    class AnimationInfo:
        last_pos:   GUI.Position   = GUI.Position(0,0)
        chunk:      GUI.Dimensions = None
        rest_chunk: GUI.Dimensions = None
        current_progress:  int = 0
        download_progress: int = 0
        done:    bool = False
        started: bool = False