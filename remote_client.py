import configparser
import curses
import socket

config = configparser.ConfigParser()
config.read('config.cfg.default')


class RemoteClient:
    @classmethod
    def new(cls):
        return curses.wrapper(cls)

    def __init__(self, screen):
        self.screen = screen

        while True:
            k = self.screen.getch()
            if chr(k) == 'q':
                break

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(
                str(k).encode(),
                (config.get('Remote', 'host'), config.getint('Remote', 'port')))


RemoteClient.new()
