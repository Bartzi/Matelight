import curses
import numpy as np
from time import sleep
import argparse

from cursesdisplay import CursesDisplay
from led_control import LEDController


if __name__ == '__main__':
    WIDTH = 16
    HEIGHT = 12

    parser = argparse.ArgumentParser()
    parser.add_argument('config', help="Path to config for matelight")
    parser.add_argument(
        '-e',
        '--emulate',
        action='store_true',
        default=False,
        help="use emulator instead of real matelight"
    )
    args = parser.parse_args()

    if args.emulate:
        display = CursesDisplay.new(HEIGHT, WIDTH)
    else:
        display = LEDController(args.config)

    while True:
        arr = np.random.randint(0, 255, size=(HEIGHT-1, WIDTH-1, 3))
        display.display(arr)
        sleep(0.5)

#         k = chr(stdscr.getch())
#         if k == 'w':
#             y = max(0, y-1)
#         elif k == 's':
#             y = min(HEIGHT-1, y+1)
#         elif k == 'a':
#             x = max(0, x-1)
#         elif k == 'd':
#             x = min(WIDTH-2, x+1)
