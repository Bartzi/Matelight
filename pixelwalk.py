import curses
import numpy as np
from time import sleep
import argparse

import socketserver
import threading

from cursesdisplay import CursesDisplay
from led_control import LEDController


class PixelEngine():

    def __init__(self, args):
        self.height = 12
        self.width = 15
        self.displays = []
        if not args.emulate:
            self.displays.append(LEDController(args.config))

        self.displays.append(CursesDisplay.new(self.height, self.width+1))

        self.start_position = (6, 8)
        self.clients = {}
        self.colours = [np.array([255, 0, 0]), np.array([0, 255, 0]), np.array([0, 0, 255])]
        self.fps = 30

    def run(self):
        def game_loop():
            while True:
                sleep(1 / self.fps)

                output = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                for client_data in self.clients.values():
                    y, x = client_data["position"]
                    output[y, x, :] = client_data["colour"]

                for d in self.displays:
                    d.display(output)

        t = threading.Thread(target=game_loop)
        t.start()


    def handle(self, data, client_address):
        try:
            client = self.clients[client_address]
        except KeyError:
            if len(self.clients) >= 3:
                return

            client = {
                "colour": self.colours[len(self.clients)],
                "position": self.start_position
            }
            self.clients[client_address] = client
        # print()

        y, x = client["position"]

        k = chr(int(data))
        if k == 'w':
            y = max(0, y-1)
        elif k == 's':
            y = min(self.height-1, y+1)
        elif k == 'a':
            x = max(0, x-1)
        elif k == 'd':
            x = min(self.width-1, x+1)

        client["position"] = (y, x)

        self.clients[client_address] = client



class PixelServer(socketserver.UDPServer, socketserver.ThreadingMixIn):

    request_size = 1

    def __init__(self, *args, **kwargs):
        self.controller = kwargs.pop('controller')
        super(PixelServer, self).__init__(*args, **kwargs)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(
            request,
            client_address,
            self,
            controller=self.controller
        )


class PixelHandler(socketserver.DatagramRequestHandler):

    def __init__(self, *args, **kwargs):
        self.controller = kwargs.pop('controller')
        super(PixelHandler, self).__init__(*args, **kwargs)

    def handle(self):
        data = self.rfile.read().decode("utf-8").strip()
        self.controller.handle(data, self.client_address[0])


if __name__ == '__main__':
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

    engine = PixelEngine(args)
    server = PixelServer(
        ("0.0.0.0", 9999),
        PixelHandler,
        controller=engine
    )
    engine.run()
    server.serve_forever()
