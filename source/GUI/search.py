from tkinter.constants import *
from GUI.definitions import *
from GUI import list
import tkinter

class QueryEntry(tkinter.Frame):
    def __init__(self, master: Union[tkinter.Misc, None], **kw) -> None:
        super().__init__(master, kw)
        self._frame = tkinter.Frame(self, bg="blue")
        self._frame.place(relx=0.5, rely=0.5, height=24, anchor=CENTER)

        self.entry = tkinter.Entry(self._frame, width=35, font=("Arial", 12))
        self.entry.pack(side=LEFT, fill=NONE)

        self.button = tkinter.Button(self._frame, text="X")
        self.button.pack(side=LEFT, fill=NONE)

class Search(tkinter.Frame):
    def __init__(self, master: Union[tkinter.Misc, None], **kw) -> None:
        super().__init__(master, kw)
        self.head = QueryEntry(self, bg="red", height=50, highlightthickness=0)
        self.head.pack(side=TOP, fill=X, expand=False)

        # self._content = list.UnorderedList(self, bg="yellow", highlightthickness=0)
        self.content = list.UnorderedList(self, bg="yellow", highlightthickness=0)
        self.content.pack(side=TOP, fill=BOTH, expand=True)

def p(evetn):
    print(evetn)

root = tkinter.Tk()
root.geometry("800x500")

s = Search(root)
s.pack(side=TOP, fill=BOTH, expand=True)

print(s.head)
print(s.head.entry)
s.head.entry.bind("<Return>", p) 
s.head.entry.bind("<KP_Enter>", p) 

root.mainloop()