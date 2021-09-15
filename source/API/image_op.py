import GUI
from GUI.definitions import *
from API.definitions import *

from copy import deepcopy
from requests import Session
from io import BytesIO
from PIL import ImageOps as PILImageOps, Image

class ImageOps:
    session: Session = Session()

    @staticmethod
    def getAspectRatio(img: PILImage) -> float:
        width, height = img.size
        ratio = width / height
        return ratio

    @staticmethod
    def resize(img: PILImage, size: GUI.Dimensions) -> PILImage:
        aspect_ratio = ImageOps.getAspectRatio(img)
        if isinstance(size, tuple):
            size = GUI.Dimensions(size)
        new_size = deepcopy(size)

        new_height = int(new_size.width // aspect_ratio)
        if new_size.height < new_height:
            new_size.width  = int(new_size.height * aspect_ratio)
        else:
            new_size.height = new_height

        return img.resize(new_size, Image.ANTIALIAS)

    @staticmethod
    def pad(img: PILImage, expected_size: GUI.Dimensions, color: Tuple[R, B, G]) -> PILImage:
        bg = Image.new(img.mode, tuple(expected_size), color)
        center = GUI.Position(int((bg.width - img.width) // 2), int((bg.height - img.height) // 2))
        bg.paste(img, tuple(center))

        return bg

    @staticmethod
    def blend(target: PILImage, rgba: Tuple[R, G, B, A]) -> PILImage:
        overlay = Image.new('RGBA', target.size, rgba)
        target = target.convert('RGBA')
        target.paste(overlay, (0,0), overlay)
        return target

    @staticmethod
    def PILOperations(img: PILImage, crop: Optional[Borders] = None, new_size: Optional[GUI.Dimensions] = None, pad_color: Optional[Tuple[R, B, G]] = None) -> PILImage:
        if not crop is None:
            img = PILImageOps.crop(img, crop)
        if not new_size is None:
            img = ImageOps.resize(img, new_size)
        if not pad_color is None:
            img = ImageOps.pad(img, new_size, pad_color)

        return img

    @staticmethod
    def getImageFromURL(url: str, crop: Optional[Borders] = None, new_size: Optional[GUI.Dimensions] = None, pad_color: Optional[Tuple[R, B, G]] = None) -> PILImage:
        data = ImageOps.session.get(url)
        img = Image.open(BytesIO(data.content))
        return ImageOps.PILOperations(img, crop, new_size, pad_color)

    @staticmethod
    def PILtoTkImage(img: PILImage, crop: Optional[Borders] = None, new_size: Optional[GUI.Dimensions] = None, pad_color: Optional[Tuple[R, B, G]] = None) -> TkImage:
        img = ImageOps.PILOperations(img, crop, new_size, pad_color)
        return ImageTk.PhotoImage(img)

    @staticmethod
    def getIconUrl(vid: pytube.YouTube, res: ChannelIconRes) -> str:
        url = ""
        start = vid.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents']
        for i in range(len(start)):
            try:
                url = start[i]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']\
                    ['thumbnail']['thumbnails'][res.value]['url']
            except KeyError:
                pass
            if url:
                return url