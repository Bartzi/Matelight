import curses
import numpy as np

class CursesDisplay:

    @classmethod
    def new(cls, height, width):
        return curses.wrapper(cls, height, width)

    def __init__(self, screen, height, width):
        self.screen = screen
        self.screen.clear()
        self.pad = curses.newpad(height, width)

        curses.init_pair(1, curses.COLOR_RED,   curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE,  curses.COLOR_BLACK)

    def update(self, arr):
        self.pad.clear()

        it = np.nditer(arr[:,:,0], flags=['multi_index'])
        while not it.finished:
            y, x = it.multi_index
            c = np.argmax(arr[y, x]) + 1
            self.pad.addstr(y, x, "#", curses.color_pair(c))
            it.iternext()

        self.screen.refresh()
        self.pad.refresh( 0,0, 5,5, 20,75)
