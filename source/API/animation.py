import GUI
from API import objects as Obj

import numpy as np
from PIL import Image
from time import sleep
import threading

def calcChunk(img_size: GUI.Dimensions) -> GUI.Dimensions:
    chunk_size = GUI.Dimensions(int(img_size.width / 10), int(img_size.height / 10))
    chunk_rest = GUI.Dimensions(img_size.width % 10, img_size.height % 10)

    return chunk_size, chunk_rest

def progress(item: Obj.DownloadTarget):
    def isLastCellInRow(current_chunk: int) -> bool:
        return current_chunk % 10 == 9

    def isFirstCellInRow(current_chunk: int) -> bool:
        return current_chunk % 10 == 0

    def isInRow(current_chunk: int, row: int) -> bool:
        start = 10*row
        end = start + 9
        return start <= current_chunk <= end

    info = item.animation_info
    if info.chunk is None:
        info.chunk, info.rest_chunk = calcChunk( GUI.Dimensions(item.fg.raw.size))
    x, y = 0, 0
    bg_pixels = np.array(item._bg)
    fg_pixels = np.array(item.fg.raw)
    _progress = 0

    while _progress < 100:
        if _progress == info.download_progress:
            sleep(0.1)
            continue
        else:
            _progress = info.download_progress

            for chunk in range(info.current_progress, _progress):
                height = info.chunk.height
                if info.rest_chunk.height:
                    if isFirstCellInRow(chunk) and not isInRow(chunk, 0):
                        info.rest_chunk.height -= 1
                    if info.rest_chunk.height:
                        height += 1

                for row in range(height):
                    y = info.last_pos.y + row

                    width = info.chunk.width
                    if info.rest_chunk.width:
                        width += 1
                        info.rest_chunk.width -= 1
                    
                    for col in range(width):
                        x = info.last_pos.x + col
                        for channel in range(3): # (R, G, B)
                            bg_pixels[y, x, channel] = fg_pixels[y, x, channel]
                        bg_pixels[y, x, 3] = 255 # A

                    if row == height - 1:
                        if isLastCellInRow(chunk):
                            info.last_pos.y = y + 1
                            info.last_pos.x = 0
                        else:
                            info.last_pos.x = x + 1
                sleep(0.010)
                item.getToplevel().after(0, item.animation, bg_pixels)
            info.current_progress = _progress