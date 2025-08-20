
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