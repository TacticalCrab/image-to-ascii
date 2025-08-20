from PIL import Image
from lib.braille_utils import array_to_braille
from math import ceil

def image_to_braille(image: str | Image.Image, scale_factor=1, threshold=120, invert_color=True):
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image

    gray_img = img.convert('L')

    if scale_factor > 1:
        gray_img = gray_img.resize((ceil(gray_img.width / scale_factor), ceil(gray_img.height / scale_factor)))

    buffer = ""
    for row in range(ceil(gray_img.height / 4)):
        for column in range(ceil(gray_img.width / 2)):
            sector = []

            for y_offset in range(4):
                for x_offset in range(2):
                    x_column_offset = column * 2
                    y_row_offset = row * 4

                    x = x_column_offset + x_offset
                    y = y_row_offset + y_offset
                    if x >= gray_img.width or y >= gray_img.height:
                        sector.append(0)
                        continue

                    pixel = gray_img.getpixel((x, y))
                    sector.append(1 - int(invert_color) if pixel > threshold else 0 + int(invert_color))
            braille = array_to_braille([sector[i:i+2] for i in range(0, len(sector), 2)])
            buffer += braille
        buffer += "\n"

    return buffer