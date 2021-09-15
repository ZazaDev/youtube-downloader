from GUI.definitions import *
from API.definitions import *
from GUI import list
import tkinter

class SideBar:
    def __init__(self, base_width: int, spawm_width: int, master: Optional[tkinter.Misc] = None, **kw) -> None:
        self._frame = tkinter.Frame(master, kw)
        self.foot: Dict[tkinter.Frame, tkinter.Label] = {'Container': tkinter.Frame(self._frame, bg="blue", width=150, height=65), 'Label': None}
        self.foot['Label'] = tkinter.Label(self.foot['Container'], bg=self.foot['Container']['bg'])
        self.content  = list.OrderedList(self._frame, bg="red", width=150, highlightthickness=0, name="content")
        self.settings = list.OrderedList(self._frame, bg="orange", width=65, highlightthickness=0, name="settings")

        self.base_width = base_width
        self.spawn_width = spawm_width

        self._frame.place(x=0, y=0, width=base_width, relheight=1)
        self.foot['Container'].pack(side=BOTTOM, anchor=W)
        self.foot['Label'].place(relx=0.5, rely=0.5, anchor=CENTER)
        self.content.pack(side=BOTTOM, anchor=W, fill=Y, expand=True)

        self._frame.bind("<Enter>", self.onEnter)
        self._frame.bind("<Leave>", self.onLeave)

    def onEnter(self, event: Event):
        ext_width = self.base_width + self.spawn_width
        self._frame.place_configure(width=ext_width)
        self.content.pack_forget()
        self.foot['Container'].configure(width=65)
        self.settings.pack(side=BOTTOM, anchor=W, fill=Y, expand=True)
        self.content.place(x=65, y=0, width=self.base_width, relheight=1)
        self._frame.tkraise()


    def onLeave(self, event: Event):
        self._frame.place_configure(width=self.base_width)
        self.settings.pack_forget()
        self.content.pack(side=BOTTOM, anchor=W, fill=Y, expand=True)
        self.foot['Container'].configure(width=150)

    def setFootImage(self, image: TkImage):
        self.foot['Image'] = image
        self.foot['Label'].configure(image=image)

    def getFoot(self) -> tkinter.Label:
        return self.foot['Label']
    
    def getBase(self) -> list.OrderedList:
        return self.content

    def getExtend(self) -> list.OrderedList:
        return self.settings

if __name__ == '__main__':
    from API import ImageOps
    
    root = tkinter.Tk()
    root.geometry("800x500")

    sb = SideBar(150, 65, root)

    from os import getcwd

    print(getcwd())
    p = Image.open("./GUI/assets/options.png")
    # p.show()
    p = ImageOps.getImageFromURL("https://i.ytimg.com/vi/CXKSGbbQsVk/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAoWmsQjohtE-hhv2X_GFmNs1AcJg", 0.2)
    # p.show()
    print(p.size)

    root.mainloop()