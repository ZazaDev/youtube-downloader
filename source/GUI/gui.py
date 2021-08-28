from __future__ import annotations

import tkinter as Tk
from tkinter.constants import CENTER
from typing import List
from PIL import ImageTk, Image

class GUI:
    def __init__(self, title: str, geometry: str) -> None:
        self.root = Tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)

        self.header = Tk.Frame(self.root, bg=self._fromRGB((115,155,155)))
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.10) 

        self.side_bar = Tk.Frame(self.root, bg=self._fromRGB((100,0,0)))
        self.side_bar.place(relx=0, rely=self.header.place_info()['relheight'], relwidth=0.2, relheight=1)

        self.render_view = Tk.Frame(self.root, bg=self._fromRGB((0,0,0)))
        render_x = self.side_bar.place_info()['relwidth']
        self.render_view.place(relx=render_x, rely=self.header.place_info()['relheight'], relwidth=str(1.0-float(render_x)), relheight=1)

        self.menu_field = Tk.Frame(self.header, bg=self._fromRGB((12,12,15)))
        self.menu_field.place(relx=0, rely=0, relwidth=0.20, relheight=1)

        self.url_field = Tk.Frame(self.header, bg=self.menu_field['bg'])
        width = self.menu_field.place_info()['relwidth']
        self.url_field.place(relx=width, rely=0, relwidth=1.0-float(width), relheight=1)

        self.url_query = Tk.Entry(self.url_field)
        self.url_query.place(relx=0.15, rely=0.4, relwidth=0.6, relheight=0.25)

        self.menu_icon = self._Icon(Tk.Canvas(self.menu_field, bg=self.side_bar['bg'], relief='ridge', highlightbackground=self.menu_field['bg'], highlightthickness=2), ImageTk.PhotoImage(Image.open("./source/GUI/assets/menu_icon90px.png")))
        self.menu_icon.canvas.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        self.menu_icon.canvas.bind("<Configure>", lambda event, x=self.menu_icon: self._resizeIcons(event, x))
        self.menu_icon.canvas.bind("<Enter>", self._expandMenu)
        self.menu_icon.canvas.bind("<Leave>", self._shrinkMenu)
        self.menu_icon.addId(self.menu_icon.canvas.create_image((0, 0), anchor=CENTER, image=self.menu_icon.image, tag='menu'))

    def start(self):
        self.root.mainloop()

    class _Icon:
        def __init__(self, canvas: Tk.Canvas, image: ImageTk, ids: List[int] = []) -> None:
            self.canvas = canvas
            self.image  = image
            self.ids    = ids

        def addId(self, id: int):
            self.ids.append(id)

    def _expandMenu(self, event: Tk.Event):
        self.side_bar.place_configure(relwidth=0.5)
        self.side_bar.tkraise()

    def _shrinkMenu(self, event: Tk.Event):
        self.side_bar.place_configure(relwidth=0.2)

    def _resizeIcons(self, event: Tk.Event, icon: GUI._Icon):
        box = icon.canvas.bbox(icon.ids[0])
        width, height = (box[2] - box[0], box[3] - box[1])
        icon.canvas.moveto(icon.ids[0], (event.width - width) // 2, (event.height - height) // 2)

    def _fromRGB(self, rgb: tuple) -> str:
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % rgb 


def main():
    gui = GUI("Demo", "1000x800")
    gui.start()

if __name__ == '__main__':
    main()