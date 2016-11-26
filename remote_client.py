import configparser
import socket
from time import sleep

config = configparser.ConfigParser()
config.read('config.cfg.default')


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()

if __name__ == '__main__':
    while True:
        # TODO remove
        # replace this with some queue that limits the number
        # of events to be sent over the wire
        sleep(.1)

        k = getch()
        if k == 'q':
            break

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(
            str(ord(k)).encode(),
            (config.get('Remote', 'host'), config.getint('Remote', 'port')))
