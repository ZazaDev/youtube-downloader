from __future__ import annotations

from tkinter import Event, Canvas, Widget
from tkinter.constants import *
from typing import *
from API.definitions import *
from dataclasses import dataclass
from abc import ABC, abstractclassmethod
from collections.abc import Iterable

URL        = str
Ids        = Tuple[int, ...]
Point      = Tuple[int,int]
Bbox       = Tuple[int,int,int,int]
Event      = Event

class Arithmetic:
    def _operation(self, operation: str, value: Union[int, Iterable[int, int]]):
        p = list(self)
        for i in range(len(p)):
            try:
                y = value[i]
                p[i] = eval(f"p[i] {operation} y")
            except TypeError:
                p[i] = eval(f"p[i] {operation} value")
            except IndexError:
                if operation == '//':
                    p[i] = eval(f"p[i] {operation} 1")
                else:
                    p[i] = eval(f"p[i] {operation} 0")
        return self.__class__(p)
    
    def __add__(self, value):
        return self._operation('+', value)

    def __sub__(self, value: Union[int, Iterable[int, int]]):
        return self._operation('-', value)
    
    def __mul__(self, value: Union[int, Iterable[int, int]]):
        return self._operation('*', value)
    
    def __truediv__(self, value: Union[int, Iterable[int, int]]):
        return self._operation('//', value)

@dataclass
class Position(Arithmetic):
    x: int
    y: int

    def __init__(self, *args: Union[Point, (int, int)]) -> None:
        """can be initialized with Position(x,y) or Position((x,y))"""
        try:
            self.x = args[0][0]
            self.y = args[0][1]
        except TypeError:
            self.x = args[0]
            self.y = args[1]

    def __iter__(self) -> Point:
        for num in (self.x, self.y):
            yield num

@dataclass
class Dimensions(Arithmetic):
    width : int
    height: int

    def __init__(self, *args: Union[Point, (int, int)]) -> None:
        """can be initialized with Dimensions(width,height) or Dimensions((width,height))"""
        try:
            self.width  = args[0][0]
            self.height = args[0][1]
        except TypeError:
            self.width  = args[0]
            self.height = args[1]

    def __iter__(self):
        for value in (self.width, self.height):
            yield value


@dataclass
class Box(Arithmetic):
    left:   int
    top:    int
    right:  int
    bottom: int

    def __init__(self, *args: Union[Bbox, (int, int, int, int)]) -> None:
        try:
            self.left   = args[0][0]
            self.top    = args[0][1]
            self.right  = args[0][2]
            self.bottom = args[0][3]
        except TypeError:
            self.left   = args[0]
            self.top    = args[1]
            self.right  = args[2]
            self.bottom = args[3]

    def __iter__(self):
        for value in (self.left, self.top, self.right, self.bottom):
            yield value

    def __repr__(self):
        return tuple(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: (left = {self.left}, top = {self.top}, right = {self.right}, bottom = {self.bottom})"



class Item(ABC):
    @abstractclassmethod
    def draw(self, canvas: Canvas, draw_area: Box) -> Ids:
        """Draw the item and all its components, takes the canvas as arg."""

    @abstractclassmethod
    def getDimensions(self) -> Dimensions:
        """Return a Tuple containing Width and Height in this order.
           Returning -1 means that it takes the whole dimention available."""

    @abstractclassmethod
    def onUpdate(self, canvas: Canvas, event: Event) -> None:
        """Function that will be called on update in the parent canvas"""

def RGBtoHex(R: int, G: int, B: int):
    return "#{:02x}{:02x}{:02x}".format(R,G,B)