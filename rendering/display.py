import numpy as np
import pygame

from led_control import LEDController


class Display(object):
    """
        Base class for the two different displays that can be handled by this matelight application.
        The first display type is the matelight itself.
        The second display type is an emulator that can render the matelight output on an ordinary screen
    """

    def __init__(self, matelight_config):
        self.config = matelight_config
        self.controller = LEDController(self.config)
        self.surface = pygame.display.set_mode(
            (self.controller.image_width, self.controller.image_height),
            pygame.RESIZABLE,
        )

    def display(self):
        raise NotImplementedError("Please use a subclass of Display!")

    def shutdown(self):
        self.controller.shutdown()


class MatelightDisplay(Display):

    def display(self):
        array = np.zeros((self.controller.image_width, self.controller.image_height, 3), dtype=np.uint8)
        pygame.pixelcopy.surface_to_array(array, self.surface)
        array = np.rot90(array, k=3)
        self.controller.display(array)


class MatelightEmulator(Display):

    def __init__(self, matelight_config):
        super(MatelightEmulator, self).__init__(matelight_config)
        self.surface = pygame.display.set_mode(
            (self.controller.image_width * 10, self.controller.image_height * 10),
            pygame.RESIZABLE,
        )

    def display(self):
        pygame.display.flip()
