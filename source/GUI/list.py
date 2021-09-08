from PIL.Image import init
from GUI.definitions import *
from API.definitions import *
import tkinter
import threading

_colors = [RGBtoHex(255,0,0), RGBtoHex(0,255,0), RGBtoHex(0,0,255)]

class _i(Item):
    def __init__(self, I) -> None:
        self.dimensions = Dimensions(-1, 200)
        self.i = I

    def __repr__(self) -> str:
        return f"{__class__.__name__}: id = {self.i}"

    def draw(self, canvas: Canvas, draw_area: Box) -> Ids:
        pos = draw_area
        pos.bottom = draw_area.top + (draw_area.bottom - draw_area.top) //2
        id = canvas.create_rectangle(tuple(pos), fill='#AAAAAA')
        position = Position(pos.left + (pos.right - pos.left) / 2, pos.top + (pos.bottom - pos.top) / 2)
        canvas.create_text(tuple(position), text=str(self.i), fill=RGBtoHex(255,255,255))

    def getDimensions(self) -> Dimensions:
        return Dimensions(tuple(self.dimensions))

    def onUpdate(self, canvas: Canvas, event: Event) -> None:
        return super().onUpdate(canvas, event)

class _List(tkinter.Canvas):
    def __init__(self, master: Optional[Any], **kw) -> None:
        super().__init__(master, **kw)
        self.lock = threading.Lock()
        self.dimensions: Dimensions = None
        self.content_dimensions: Dimensions = Dimensions(0,0)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
    
    def _convertDimensions(self, dimesions: Dimensions) -> Dimensions:
        if dimesions.width < 0:
            dimesions.width = self.dimensions.width
        if dimesions.height < 0:
            dimesions.height = self.dimensions.height
        return dimesions

    def _DimensionstoBox(self, id: int, dimesions: Dimensions) -> Box:
        box = Box(self.bbox(id))
        pos = Position(tuple(box))
        return Box(pos.x, pos.y, pos.x + dimesions.width, pos.y + dimesions.height)

    def leave(self, event: Event):
        self.unbind("<Button-4>")
        self.unbind("<Button-5>")
        print(f"{self.__class__.__name__}: leaves")

    def enter(self, event: Event):
        self.bind("<Button-4>", self.mwup)
        self.bind("<Button-5>", self.mwdown)
        print(f"{self.__class__.__name__}: enter")

    def mwup(self, event: Event):
        if self.content_dimensions.height > self.dimensions.height:
            self.yview_scroll(-1, "unit")

    def mwdown(self, event: Event):
        if self.content_dimensions.height > self.dimensions.height:
            self.yview_scroll(1, "unit")


    def place_configure(self, **kw: Any) -> None:
        super().place_configure(**kw)
        self.update()
        self.dimensions = Dimensions(self.winfo_width(), self.winfo_height())

    def pack_configure(self, **kw: Any) -> None:
        super().pack_configure(**kw)
        self.update()
        self.dimensions = Dimensions(self.winfo_width(), self.winfo_height())

    def grid_configure(self, **kw: Any) -> None:
        super().grid_configure(**kw)
        self.update()
        self.dimensions = Dimensions(self.winfo_width(), self.winfo_height())

    place = place_configure
    pack = pack_configure
    grid = grid_configure


class UnorderedList(_List):
    def __init__(self, master: Optional[Any], **kw) -> None:
        super().__init__(master, **kw)
        self.next_pos: Position = Position(0,0)
        self.items: List[Tuple[Item, int, Position]] = []
        self.bind("<Configure>", self.onUpdate)
        self.i = 0

    def addItem(self, item: Item) -> int:
        dimension: Dimensions = self._convertDimensions(item.getDimensions())

        self.lock.acquire()
        draw_area: Box = Box(self.next_pos.x, self.next_pos.y ,\
                        self.next_pos.x + dimension.width,\
                        self.next_pos.y + dimension.height)
        id = self.create_rectangle(tuple(draw_area), fill="", outline="")
        item.draw(self, draw_area)
        self.items.append((item, id, Position(tuple(draw_area))))
        self.next_pos += (0, dimension.height)
        self.content_dimensions += (0, dimension.height)
        self.configure(scrollregion=self.bbox("all"))
        self.lock.release()

        return self.items.index(self.items[-1])

    def getItem(self, id) -> Item:
        return self.items[id][0]

    def onUpdate(self, event: tkinter.Event) -> None:
        print(f"{self.__class__.__name__}: {event}")
        self.dimensions = Dimensions(event.width, event.height)
        for (item, rect_id, init_pos) in self.items:
            dimensions = self._convertDimensions(item.getDimensions())
            rect = Box(init_pos.x, init_pos.y, init_pos.x + dimensions.width, init_pos.y + dimensions.height)
            self.coords(rect_id, rect.left, rect.top, rect.right, rect.bottom)
            print(f"\texpected: {rect}, actual: {self.bbox(rect_id)}")
            item.onUpdate(self, event)


class OrderedList(_List):
    def __init__(self, master: Optional[Any], **kw) -> None:
        super().__init__(master, **kw)
        self.items: List[Tuple[Item, int, int]] = []
        self.item_dimensions: Dimensions = None
        self.bind("<Configure>", self.onUpdate)
        self.i = 0
    
    def addItem(self, item: Item, index: int):
        if self.item_dimensions is None:
            self.item_dimensions = self._convertDimensions(item.getDimensions())
        init_pos = Position(0, self.item_dimensions.height*index)
        draw_area = Box((init_pos.x, init_pos.y, self.item_dimensions.width, init_pos.y+self.item_dimensions.height))

        self.lock.acquire()
        id = self.create_rectangle(tuple(draw_area), fill="", outline="")
        self.configure(scrollregion=self.bbox("all"))
        self.content_dimensions += (0, self.item_dimensions.height)
        self.lock.release()

        item.draw(self, draw_area)
        self.items.append((item, id, index))
        return self.items.index(self.items[-1])

    def getItem(self, id: int) -> Item:
        return self.items[id][0]

    def onUpdate(self, event: tkinter.Event) -> None:
        print(f"{self.__class__.__name__}: {event}")
        self.dimensions = Dimensions(event.width, event.height)
        for (item, rect_id, index) in self.items:
            dimensions = self._convertDimensions(item.getDimensions())
            rect = Box(0, self.item_dimensions.height * index, 0 + dimensions.width, self.item_dimensions.height * index + dimensions.height)
            self.coords(rect_id, rect.left, rect.top, rect.right, rect.bottom)
            print(f"\texpected: {rect}, actual: {self.bbox(rect_id)}")
            item.onUpdate(self, event)

def workul(ul, _):
    ul.addItem(_i(_))
    print(f"{threading.currentThread().name}: finished")

def workol(ol, _):
    ol.addItem(_i(_), _)
    print(f"{threading.currentThread().name}: finished")


def main():
    root = tkinter.Tk()
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

