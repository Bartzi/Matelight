import curses
import numpy as np
from time import sleep

from cursesdisplay import CursesDisplay


if __name__ == '__main__':
    WIDTH = 16
    HEIGHT = 12

    display = CursesDisplay.new(HEIGHT, WIDTH)

    while True:
        arr = np.random.randint(0, 255, size=(HEIGHT-1, WIDTH-1, 3))
        display.update(arr)
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
