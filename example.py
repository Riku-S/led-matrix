# PYNQ led matrix simulator example

# Remember not to import this in your final product
from pynq_emulator.emulation import *

# These could be imported instead
# import tut.arduino_led_matrix as led_matrix
# from pynq.lib import Button
# from pynq.lib import Switch

import time


def set_all_leds(red, green, blue):
    """ Set the color value to all the LEDs

    :param red: Red value between 0 and 255
    :param green: Green value between 0 and 255
    :param blue: Blue value between 0 and 255
    :return: None
    """
    for i in range(8):
        for j in range(8):
            led_matrix.set_led_color(i, j, red, green, blue)


def main():
    # Always remember to initialize the led matrix!
    led_matrix.init()

    button0 = Button(0)
    switch0 = Switch(0)

    # Let's first set all LEDs green

    red = 0
    green = 255
    blue = 0

    set_all_leds(red, green, blue)

    # Advance to the next step when switch 0 is turned on
    switch0.wait_for_value(1)

    # From this point on the LEDs are red
    red = 255
    green = 0

    # Stop the program by turning off the switch
    while switch0.read() == 1:

        # If button 1 is pressed, turn the LEDs magenta colored
        # (full red + full blue)
        if button0.read() == 1:
            blue = 255
        else:
            blue = 0

        set_all_leds(red, green, blue)

        # Add a little delay between checks
        time.sleep(0.1)

    # Ending the simulation doesn't shut down the LEDs in real life
    led_matrix.clear()


main()
