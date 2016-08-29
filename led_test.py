import random
import time
import argparse

import numpy as np
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from led_control import LEDController


def interpolate(controller):
    colorize = np.vectorize(lambda x: random.randint(0, 255))
    start_data = colorize(np.full((args.num_leds, 1, 3), 0, dtype=np.uint8))
    end_data = colorize(np.full((args.num_leds, 1, 3), 255, dtype=np.uint8))
    interpolate_func = np.vectorize(lambda start, end, progress: (1 - progress) * start + progress * end)
    progress = 0
    step_value = args.progress_step
    positive_direction = True

    for _ in range(50):
        data = interpolate_func(start_data, end_data, progress)
        controller.display(data)
        progress = np.clip(progress + step_value, 0, 1)
        if progress >= 1 and positive_direction:
            step_value *= -1
            positive_direction = False
        if progress <= 0 and not positive_direction:
            step_value *= -1
            positive_direction = True
        time.sleep(args.refresh_rate / 1000)


def display_image(controller, image, slide_image=False):
    image_data = np.array(image)
    window_size = (12, 15)
    window_position = 0
    while True:
        data = image_data.copy()[:, window_position:min(window_position + window_size[1], image.width), ...]

        height, width, channels = data.shape
        fill_data = np.zeros((height, window_size[1] - width, channels))
        data = np.hstack((data, fill_data))

        controller.display(data)
        if slide_image:
            window_position += 1
            if window_position >= image.width:
                window_position = 0
        time.sleep(args.refresh_rate / 1000)


def show_image(controller):
    image = Image.open(args.image)
    image = image.resize((10, 8), Image.LANCZOS).convert("RGB")
    while True:
        controller.display(np.array(image.getdata()).reshape((image.height, image.width, len(image.getbands()))))
        break
        time.sleep(args.refresh_rate / 1000)


def render_text(controller):
    font_size = 20
    font = None

    while True:
        font = ImageFont.truetype(args.font, font_size)
        if font.getsize(args.text)[1] <= 12:
            break
        font_size -= 1
    print(font_size)

    while True:

        text_image = Image.new('RGB', font.getsize(args.text))
        draw = ImageDraw.Draw(text_image)
        draw.fontmode = "1"
        draw.text((0, 0), args.text, font=font, fill=(255, 0, 0))

        display_image(controller, text_image, slide_image=True)

def render_random(controller):

    while True:
        number = random.randint(1, 4)
        if number == 3:
            render_text(controller)
        else:
            interpolate(controller)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tool for running different LED Controller Tests')
    subparsers = parser.add_subparsers(help='commands for each mode')
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("config", help="path to config file for matelight")
    common_parser.add_argument("-r", "--refresh-rate", dest='refresh_rate', action='store', type=int, default=10, help='Refresh rate in ms')
    interpolate_parser = subparsers.add_parser('interpolate', parents=[common_parser], help="Interpolate mode options")
    interpolate_parser.set_defaults(program=interpolate)
    interpolate_parser.add_argument("-p", "--progress-step", dest='progress_step', action='store', type=float, default=0.01, help="step size for interpolation")
    text_render_parser = subparsers.add_parser('render-text', parents=[common_parser], help="Text Rendering options")
    text_render_parser.set_defaults(program=render_text)
    text_render_parser.add_argument("-f", "--font", dest='font', action='store', help='font to use for rendering', required=True)
    text_render_parser.add_argument("text", action='store', help="text to render")
    image_display_parser = subparsers.add_parser('display_image', parents=[common_parser], help="Image display options")
    image_display_parser.set_defaults(program=show_image)
    image_display_parser.add_argument("image", action="store", help="path to image to display")
    random_parser = subparsers.add_parser('random', parents=[common_parser], help="Random mode options")
    random_parser.set_defaults(program=render_random)
    random_parser.add_argument("-f", "--font", dest='font', action='store', help='font to use for rendering', required=True)
    random_parser.add_argument("text", action='store', help="text to render")
    random_parser.add_argument("-p", "--progress-step", dest='progress_step', action='store', type=float, default=0.01, help="step size for interpolation")

    args = parser.parse_args()
    controller = LEDController(args.config)
    # controller = None

    try:
        args.program(controller)
    except KeyboardInterrupt:
        controller.shutdown()
