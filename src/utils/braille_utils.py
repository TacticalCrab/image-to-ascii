
def get_braille_char(value: int) -> str:
    return chr(0x2800 + value)


def array_to_braille(arr):
    dot_map = [
        (0, 0),  # dot 1
        (1, 0),  # dot 2
        (2, 0),  # dot 3
        (0, 1),  # dot 4
        (1, 1),  # dot 5
        (2, 1),  # dot 6
        (3, 0),  # dot 7
        (3, 1),  # dot 8
    ]
    value = 0
    for i, (row, col) in enumerate(dot_map):
        if arr[row][col]:
            value |= (1 << i)

    return get_braille_char(value)

def array_to_ascii(arr):
    pixel_count = sum(row.count(True) for row in arr)
    
    if pixel_count == 0:
        return chr(0x2800)
    elif pixel_count == 1:
        return '.'
    elif pixel_count == 2:
        return ':'
    elif pixel_count == 3:
        return '+'
    elif pixel_count == 4:
        return '#'
    elif pixel_count == 5:
        return '%'
    elif pixel_count == 6:
        return '@'
    elif pixel_count == 7:
        return 'M'
    elif pixel_count == 8:
        return '█'

    return '?'