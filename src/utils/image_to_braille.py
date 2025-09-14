from typing import Callable
from PIL import Image

from math import ceil

def image_to_braille(image: str | Image.Image, pixel_transformer: Callable[[list[list[int]]], str], scale_factor=1, threshold=120, invert_color=True, char_pixel_dimentions=(4, 2)) -> str:
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image

    gray_img = img.convert('L')

    if scale_factor > 1:
        gray_img = gray_img.resize((ceil(gray_img.width / scale_factor), ceil(gray_img.height / scale_factor)))

    buffer = ""
    for row in range(ceil(gray_img.height / char_pixel_dimentions[0])):
        for column in range(ceil(gray_img.width / char_pixel_dimentions[1])):
            sector = []

            for y_offset in range(char_pixel_dimentions[0]):
                for x_offset in range(char_pixel_dimentions[1]):
                    x_column_offset = column * char_pixel_dimentions[1]
                    y_row_offset = row * char_pixel_dimentions[0]

                    x = x_column_offset + x_offset
                    y = y_row_offset + y_offset
                    if x >= gray_img.width or y >= gray_img.height:
                        sector.append(0)
                        continue

                    pixel = gray_img.getpixel((x, y))
                    sector.append(1 - int(invert_color) if pixel > threshold else 0 + int(invert_color))
            braille = pixel_transformer([sector[i:i+2] for i in range(0, len(sector), 2)])
            buffer += braille
        buffer += "\n"

    return buffer