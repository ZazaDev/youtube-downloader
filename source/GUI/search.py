from tkinter.constants import *
from GUI.definitions import *
from GUI import list
import tkinter
from PIL import ImageTk, Image

class QueryEntry(tkinter.Frame):
    def __init__(self, master: Union[tkinter.Misc, None], **kw) -> None:
        super().__init__(master, kw)
        self._frame = tkinter.Frame(self, bg="")
        self._frame.place(relx=0.5, rely=0.5, height=24, anchor=CENTER)

        self._entry_var = tkinter.StringVar(value="Search")
        self._place_holder = True

        self.entry = tkinter.Entry(self._frame, width=35, font=("Arial", 12), textvariable=self._entry_var)
        self.entry.configure(highlightbackground="#303030", insertbackground='white', highlightcolor="#303030", highlightthickness=1, bg="#121212", border=0, fg="#AAAAAA")
        self.entry.pack(side=LEFT, fill=BOTH, expand=True)

        self._img = ImageTk.PhotoImage(Image.open(r"./source/GUI/assets/search.png"))
        self.button = tkinter.Label(self._frame, image=self._img, width=50)
        self.button.configure(highlightthickness=0, bg="#303030", border=0)
        self.button.pack(side=LEFT, fill=BOTH, expand=True)

        self._on_submit = None
        self.entry.bind("<FocusIn>", self.onFocusIn)
        self.entry.bind("<FocusOut>", self.onFocusOut)
        self.entry.bind("<Return>", self.onSubmit)
        self.entry.bind("<KP_Enter>", self.onSubmit)
        self.entry.bind("<Control-a>", self._ctrl_a)
        self.button.bind("<1>", self.onSubmit)

    def onFocusIn(self, event: Event):
        if self._place_holder:
            self.entry.configure(fg="white")
            self._entry_var.set("")
            self._place_holder = False


    def onFocusOut(self, event: Event):
        if not self._entry_var.get():
            self.entry.configure(fg="#AAAAAA")
            self._entry_var.set("Search")
            self._place_holder = True

    def _ctrl_a(self, event:Event):
        self.entry.select_range(0, END)
        self.entry.icursor(0)
        return 'break'

    def onSubmit(self, event: Event):
        if not self._on_submit is None:
            self._on_submit(self.entry, event)

    def setOnSubmit(self, callback: Callable[[tkinter.Entry, tkinter.Event], None]):
        self._on_submit = callback


class Search(tkinter.Frame):
    def __init__(self, master: Union[tkinter.Misc, None], **kw) -> None:
        super().__init__(master, kw)
        self.head = QueryEntry(self, bg="#0f0f0f", height=50, highlightthickness=0)
        self.head.pack(side=TOP, fill=X, expand=False)

        # self._content = list.UnorderedList(self, bg="yellow", highlightthickness=0)
        self.content = list.UnorderedList(self, bg="#181818", highlightthickness=0)
        self.content.pack(side=TOP, fill=BOTH, expand=True)

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("800x500")

    s = Search(root)
    s.pack(side=TOP, fill=BOTH, expand=True)
    s.head.setOnSubmit(lambda entry, event: print(entry.get()))

    print(s.head)
    print(s.head.entry)

    root.mainloop()