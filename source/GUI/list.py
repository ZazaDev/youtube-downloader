from GUI import objects as GUIObj
from GUI.definitions import *
from API.definitions import *
from sys import platform
import tkinter as tk
import threading

_colors = [RGBtoHex(255,0,0), RGBtoHex(0,255,0), RGBtoHex(0,0,255)]

class _i(GUIObj.Item):
    def __init__(self, I) -> None:
        self.dimensions = GUIObj.Dimensions(-1, 200)
        self.i = I

    def __repr__(self) -> str:
        return f"{__class__.__name__}: id = {self.i}"

    def draw(self, canvas: tk.Canvas, draw_area: GUIObj.Box) -> Ids:
        pos = draw_area
        pos.bottom = draw_area.top + (draw_area.bottom - draw_area.top) //2
        id = canvas.create_rectangle(tuple(pos), fill='#AAAAAA')
        position = GUIObj.Position(pos.left + (pos.right - pos.left) / 2, pos.top + (pos.bottom - pos.top) / 2)
        canvas.create_text(tuple(position), text=str(self.i), fill=RGBtoHex(255,255,255))

    def getDimensions(self) -> GUIObj.Dimensions:
        return GUIObj.Dimensions(tuple(self.dimensions))

    def onUpdate(self, canvas: tk.Canvas, event: Event) -> None:
        return super().onUpdate(canvas, event)

class _List(tk.Canvas):
    def __init__(self, master: Optional[Any], **kw) -> None:
        try:
            self.name = kw.pop('name')
        except KeyError:
            self.name = "None"
        super().__init__(master, **kw)
        self.lock = threading.Lock()
        self.dimensions: GUIObj.Dimensions = None
        self.content_dimensions: GUIObj.Dimensions = GUIObj.Dimensions(0,0)

        name = "{d}: ".format(d=self.name)
        enter = lambda e: threading.Thread(name=name+"enter", target=self.enter, args=(e, )).start()
        leave = lambda e: threading.Thread(name=name+"leave", target=self.leave, args=(e, )).start()
        self.bind("<Enter>", enter)
        self.bind("<Leave>", leave)
    
    def _convertDimensions(self, dimesions: GUIObj.Dimensions) -> GUIObj.Dimensions:
        if dimesions.width < 0:
            dimesions.width = self.dimensions.width
        if dimesions.height < 0:
            dimesions.height = self.dimensions.height
        return dimesions

    def _DimensionstoBox(self, id: int, dimesions: GUIObj.Dimensions) -> GUIObj.Box:
        box = GUIObj.Box(self.bbox(id))
        pos = GUIObj.Position(tuple(box))
        return GUIObj.Box(pos.x, pos.y, pos.x + dimesions.width, pos.y + dimesions.height)

    if platform == 'linux':
        def leave(self, event: Event):
            self.unbind("<Button-4>")
            self.unbind("<Button-5>")
            print(f"{self.name}: leaves")

        def enter(self, event: Event):
            mwheelup   = lambda e: threading.Thread(name="mwheelup", target=self.mwup, args=(e,)).start()
            mwheeldowm = lambda e: threading.Thread(name="mwheeldown", target=self.mwdown, args=(e,)).start()
            self.bind("<Button-4>", mwheelup)
            self.bind("<Button-5>", mwheeldowm)
            print(f"{self.name}: enter")

        def mwup(self, event: Event):
            if self.content_dimensions.height > self.dimensions.height:
                self.yview_scroll(-1, "unit")

        def mwdown(self, event: Event):
            if self.content_dimensions.height > self.dimensions.height:
                self.yview_scroll(1, "unit")
    
    elif platform == "win32":
        def leave(self, event: Event):
            self.unbind("<MouseWheel>")
            print(f"{self.name}: leaves")

        def enter(self, event: Event):
            mwheel = lambda e: threading.Thread(name="Win: mwheel", target=self.mwheel, args=(e,)).start()
            self.bind("<MouseWheel>", mwheel)
            print(f"{self.name}: enter")

        def mwheel(self, event: Event):
            if self.content_dimensions.height > self.dimensions.height:
                self.yview_scroll(int(-1*(event.delta/120)), "units")

    def place_configure(self, **kw: Any) -> None:
        super().place_configure(**kw)
        self.update()
        self.dimensions = GUIObj.Dimensions(self.winfo_width(), self.winfo_height())

    def pack_configure(self, **kw: Any) -> None:
        super().pack_configure(**kw)
        self.update()
        self.dimensions = GUIObj.Dimensions(self.winfo_width(), self.winfo_height())

    def grid_configure(self, **kw: Any) -> None:
        super().grid_configure(**kw)
        self.update()
        self.dimensions = GUIObj.Dimensions(self.winfo_width(), self.winfo_height())

    place = place_configure
    pack = pack_configure
    grid = grid_configure


class UnorderedList(_List):
    def __init__(self, master: Optional[Any], **kw) -> None:
        super().__init__(master, **kw)
        self.next_pos: GUIObj.Position = GUIObj.Position(0,0)
        self.items: List[Tuple[GUIObj.Item, int, GUIObj.Position]] = []
        self.bind("<Configure>", self.onUpdate)
        self.i = 0

    def addItem(self, item: GUIObj.Item, offset: Optional[Tuple[int,int]] = (0,0), bind: Optional[Tuple[List[str], Callable[[GUIObj.Item, Event], None]]] = None) -> int:
        dimension: GUIObj.Dimensions = self._convertDimensions(item.getDimensions())

        self.lock.acquire()
        draw_area: GUIObj.Box = GUIObj.Box(self.next_pos.x, self.next_pos.y ,\
                        self.next_pos.x + dimension.width,\
                        self.next_pos.y + dimension.height)
        id = self.create_rectangle(tuple(draw_area), fill="", outline="")
        tag = item.draw(self, draw_area)
        self.itemconfigure(id, tag=tag)

        if not bind is None:
            for hook in bind[0]:
                self.tag_bind(tag, hook, lambda e, v=item: bind[1](v, e))
        
        self.items.append((item, id, GUIObj.Position(tuple(draw_area))))
        if isinstance(offset, tuple):
            offset = GUIObj.Position(offset)
        size = offset + (0, dimension.height)
        self.next_pos += tuple(size)
        self.content_dimensions += tuple(size)
        self.configure(scrollregion=self.bbox("all"))
        self.lock.release()

        return self.items.index(self.items[-1])

    def getItem(self, id) -> GUIObj.Item:
        return self.items[id][0]

    def onUpdate(self, event: tk.Event) -> None:
        print(f"{self.__class__.__name__}: {event}")
        self.dimensions = GUIObj.Dimensions(event.width, event.height)
        for (item, rect_id, init_pos) in self.items:
            dimensions = self._convertDimensions(item.getDimensions())
            rect = GUIObj.Box(init_pos.x, init_pos.y, init_pos.x + dimensions.width, init_pos.y + dimensions.height)
            self.coords(rect_id, rect.left, rect.top, rect.right, rect.bottom)
            print(f"\texpected: {rect}, actual: {self.bbox(rect_id)}")
            item.onUpdate(self, event)

    def clear(self):
        self.next_pos = GUIObj.Position(0,0)
        self.items = []
        self.delete('all')


class OrderedList(_List):
    def __init__(self, master: Optional[Any], **kw) -> None:
        super().__init__(master, **kw)
        self.items: List[Tuple[GUIObj.Item, int, int]] = []
        self.item_dimensions: GUIObj.Dimensions = None
        self.bind("<Configure>", self.onUpdate)
        self.i = 0
    
    def addItem(self, item: GUIObj.Item, index: int):
        if self.item_dimensions is None:
            self.item_dimensions = self._convertDimensions(item.getDimensions())
        init_pos = GUIObj.Position(0, self.item_dimensions.height*index)
        draw_area = GUIObj.Box((init_pos.x, init_pos.y, self.item_dimensions.width, init_pos.y+self.item_dimensions.height))

        self.lock.acquire()
        id = self.create_rectangle(tuple(draw_area), fill="", outline="")
        self.configure(scrollregion=self.bbox("all"))
        self.content_dimensions += (0, self.item_dimensions.height)
        self.lock.release()

        item.draw(self, draw_area)
        self.items.append((item, id, index))
        return self.items.index(self.items[-1])

    def getItem(self, id: int) -> GUIObj.Item:
        return self.items[id][0]

    def onUpdate(self, event: tk.Event) -> None:
        print(f"{self.name}: {event}")
        self.dimensions = GUIObj.Dimensions(event.width, event.height)
        for (item, rect_id, index) in self.items:
            dimensions = self._convertDimensions(item.getDimensions())
            rect = GUIObj.Box(0, self.item_dimensions.height * index, 0 + dimensions.width, self.item_dimensions.height * index + dimensions.height)
            self.coords(rect_id, rect.left, rect.top, rect.right, rect.bottom)
            print(f"\texpected: {rect}, actual: {self.bbox(rect_id)}")
            item.onUpdate(self, event)
    
    def clear(self):
        self.item_dimensions = None
        self.items = []
        self.delete('all')



def workul(ul, _):
    ul.addItem(_i(_))
    print(f"{threading.currentThread().name}: finished")

def workol(ol, _):
    ol.addItem(_i(_), _)
    print(f"{threading.currentThread().name}: finished")


def main():
    root = tk.Tk()
    root.title("Demo")
    root.geometry("800x600")

    ul = UnorderedList(root, bg="black")
    ul.place(relx=0.05, rely=0.0, relheight=0.45, relwidth=0.9)

    ol = OrderedList(root, bg="black")
    ol.place(relx=0.05, rely=0.449, relheight=0.45, relwidth=0.9)
    
    threads = []
    ids = []
    for _ in range(2):
        t = (threading.Thread(name=f"ul {_}", target=workul, args=(ul, _)), threading.Thread(name=f"ol {_}", target=workol, args=(ol, _)))
        threads.append(t)
        t[0].start()
        t[1].start()

    for id in ids:
        print(ul.getItem(id))

    root.mainloop()

if __name__ == "__main__":
    main()

