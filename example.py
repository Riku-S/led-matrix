# PYNQ led matrix simulator example

# Remember not to import this in your final product
from pynq_emulator.arduino_led_matrix_emulator import *

# These could be imported instead
# import tut.arduino_led_matrix as led_matrix
# from pynq.lib import Button
# from pynq.lib import Switch

import time


def turn(x_dir, y_dir):
    """ Turn -90 degrees

    :param x_dir: x direction
    :param y_dir: y direction
    :return: new x dirction, new y direction
    """

    new_x_dir = -y_dir
    new_y_dir = x_dir
    return new_x_dir, new_y_dir



def main():
    # Always remember to initialize the led matrix!
    led_matrix.init()

    # Let's paint the whole matrix yellow with a red dot moving in a spiral
    x = 0           # x coordinate of the painter
    y = 0           # y coordinate of the painter
    x_dir = 1       # how fast the painter goes right
    y_dir = 0       # how fast the painter goes down

    # Let's initialize a 2 dimensional array of leds painted
    led_painted_list = [[False for i in range(8)] for j in range(8)]

    leds_painted = 0
    while leds_painted < 64:        # 8 * 8 LEDs = 64 LEDs
        # We first paint our dot red
        led_matrix.set_led_color(x, y, 255, 0, 0)

        time.sleep(0.1)

        #Then yellow
        led_matrix.set_led_color(x, y, 255, 255, 0)

        # Remember this led later
        led_painted_list[x][y] = 1
        leds_painted += 1

        # The next led is painted already / doesn't exist
        if (not 0 <= x + x_dir <= 7 or not 0 <= y + y_dir <= 7 or
                led_painted_list[x + x_dir][y + y_dir] == 1):
            x_dir, y_dir = turn(x_dir, y_dir)

        # Change the coordinates
        x += x_dir
        y += y_dir

    # Ending the simulation doesn't shut down the LEDS in real life
    led_matrix.clear()


main()
