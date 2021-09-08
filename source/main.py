from GUI.sidebar import SideBar
from GUI.definitions import *
from GUI import Search
from API import downloader
import tkinter

class Aplication(tkinter.Tk):
    def __init__(self, geometry: str, screenName: Optional[str] = None, baseName: Optional[str] = None, className: Optional[str] = "Tk", useTk: Optional[bool] = True, sync: Optional[bool] = False, use: Optional[str] = None) -> None:
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        self.geometry(geometry)
        width = int(geometry.split('x')[0])

        self.sidebar = SideBar(150, 65)

        self.search = {'Container': tkinter.Frame(self), 'Search': None}
        self.search['Container'].place(x=150, y=0, width=width-150, relheight=1)
        self.search['Search'] = Search(self.search['Container'])
        self.search['Search'].place(x=0, y=0, relheight=1, relwidth=1)



def main():
    app = Aplication(geometry="800x800", className="App", sync=True)

    app.mainloop()

if __name__ == '__main__':
    main()