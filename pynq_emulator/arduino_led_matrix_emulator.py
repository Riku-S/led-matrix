# Riku Salminen, riku.salminen@tuni.fi, 291634
#
# Simulaattori PYNQ-tehtäviä varten, käyttäen ktinter-kirjastoa
# A simulator for PYNQ exercises, made with ktinter library
#
# I import only the libraries I need to avoid the Button() class, that would
# overlap with a custom class. Buttons of tkinter are useless for this
# project anyway, so we lose nothing by not importing them.

from tkinter import Tk
from tkinter import Canvas
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import Scale
import time


GENERAL_SPACING = 16

# Constants for the LED matrix
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 8
LED_SIZE = 32
CANVAS_WIDTH = MATRIX_WIDTH * LED_SIZE
CANVAS_HEIGHT = MATRIX_HEIGHT * LED_SIZE
MIN_COLOR = 0  # The color value of the LED can only be 0 or higher
MAX_COLOR = 255  # The color value of the LED can only be 255 or lower

# Constants for the buttons
BUTTON_WIDTH = 32
BUTTON_HEIGHT = 32
BUTTON_SPACING = 16
NUM_BUTTONS = 4
BUTTON_CANVAS_WIDTH = (BUTTON_WIDTH * NUM_BUTTONS +
                       BUTTON_SPACING * (NUM_BUTTONS + 1))
BUTTON_CANVAS_HEIGHT = BUTTON_HEIGHT + BUTTON_SPACING * 2

# Constants for the switches
SWITCH_WIDTH = 64
SWITCH_HEIGHT = 32
SWITCH_SPACING = 16
NUM_SWITCHES = 2
SWITCH_CANVAS_WIDTH = (SWITCH_WIDTH * NUM_SWITCHES +
                       SWITCH_SPACING * (NUM_SWITCHES + 1))
SWITCH_CANVAS_HEIGHT = SWITCH_HEIGHT + SWITCH_SPACING * 2
BUTTON_UP_COLOR = "#f0f0f0"
BUTTON_DOWN_COLOR = "#c8c8c8"

# Constants for the sliders
SLIDER_SPACING = 16
SLIDER_WIDTH = (CANVAS_WIDTH + max(SWITCH_CANVAS_WIDTH, BUTTON_CANVAS_WIDTH) +
                GENERAL_SPACING) - 2 * SLIDER_SPACING
SLIDER_HEIGHT = 64
NUM_SLIDERS = 1
SLIDER_CANVAS_WIDTH = SLIDER_WIDTH + 2 * GENERAL_SPACING
SLIDER_CANVAS_HEIGHT = (SLIDER_HEIGHT * NUM_SLIDERS + SLIDER_SPACING *
                        (NUM_SLIDERS + 1))
SLIDER_MIN = 0
SLIDER_MAX = 20000

# Constants for the window
WINDOW_WIDTH = (CANVAS_WIDTH + max(SWITCH_CANVAS_WIDTH, BUTTON_CANVAS_WIDTH) +
                GENERAL_SPACING * 3)
WINDOW_HEIGHT = CANVAS_HEIGHT + SLIDER_CANVAS_HEIGHT + GENERAL_SPACING * 3
BG_COLOR = "#202020"
BG2_COLOR = "#404040"

# How many times per second does the wait_for_value method read the value
WAIT_FPS = 10
# How many times per second do the LEDs update if threading is used
# UPDATE_FPS = 20


class SimulatorWindow:
    """ A class made to simulate the led device functionalities"""

    def __init__(self):
        # The main window
        self.root = Tk(className=" Led matrix emulator")
        self.root.geometry("%sx%s"
                           % (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.root.configure(background=BG_COLOR)

        # The canvas we draw LEDs on
        self.canvas = Canvas(self.root, background=BG2_COLOR,
                             highlightthicknes=0,
                             width=CANVAS_WIDTH,
                             height=CANVAS_HEIGHT)
        self.canvas.place(x=GENERAL_SPACING, y=GENERAL_SPACING)

        # The widgets posing as leds
        self.grid_leds = [[self.canvas.create_oval(
            i * LED_SIZE + 2, j * LED_SIZE + 2, (i + 1) * LED_SIZE - 2,
            (j + 1) * LED_SIZE - 2,
            fill="#000000") for j in range(MATRIX_HEIGHT)]
            for i in range(MATRIX_WIDTH)]

        # Let's create a canvas for the buttons
        self.button_canvas = Canvas(self.root, background=BG2_COLOR,
                                    highlightthicknes=0)
        self.button_canvas.place(x=CANVAS_WIDTH + GENERAL_SPACING * 2,
                                 y=GENERAL_SPACING,
                                 width=BUTTON_CANVAS_WIDTH,
                                 height=BUTTON_CANVAS_HEIGHT)

        # Now let's place the buttons and put them in the list
        self.buttons = []
        self.buttons_down = []
        for i in range(NUM_BUTTONS):
            x = (i + 1) * BUTTON_SPACING + i * BUTTON_WIDTH
            y = BUTTON_SPACING
            button = self.button_canvas.create_rectangle(
                x,
                y,
                (i + 1) * BUTTON_SPACING + (i + 1) * BUTTON_WIDTH,
                BUTTON_SPACING + BUTTON_HEIGHT,
                fill=BUTTON_UP_COLOR,
            )
            self.buttons.append(button)
            self.buttons_down.append(False)

        for i in range(NUM_BUTTONS):
            x = (i + 1) * BUTTON_SPACING + (i + 0.5) * BUTTON_WIDTH
            y = BUTTON_SPACING + BUTTON_HEIGHT*0.5
            self.button_canvas.create_text(x, y, text="BTN%i" % i)

        # When buttons are pressed/released, execute functions to handle it
        self.button_canvas.bind('<Button-1>', self.button_clicked)
        self.button_canvas.bind('<ButtonRelease-1>', self.button_released)

        # Let's create a canvas for the switches
        self.switch_canvas = Canvas(self.root, background=BG2_COLOR,
                                    highlightthicknes=0)
        self.switch_canvas.place(x=CANVAS_WIDTH + GENERAL_SPACING * 2,
                                 y=BUTTON_CANVAS_HEIGHT + GENERAL_SPACING * 2,
                                 width=SWITCH_CANVAS_WIDTH,
                                 height=SWITCH_CANVAS_HEIGHT)

        # Now let's place the switches and put them in the list
        self.switches = []
        self.switches_activated = []
        for i in range(NUM_SWITCHES):
            self.switches_activated.append(IntVar())

            switch = Checkbutton(self.switch_canvas,
                                 text="SW%i" % i,
                                 var=self.switches_activated[i])
            switch.place(x=(i + 1) * SWITCH_SPACING + i * SWITCH_WIDTH,
                         y=SWITCH_SPACING,
                         width=SWITCH_WIDTH,
                         height=SWITCH_HEIGHT)

            self.switches.append(switch)

        self.slider_canvas = Canvas(self.root, background=BG2_COLOR,
                                    highlightthicknes=0)
        self.slider_canvas.place(x=GENERAL_SPACING,
                                 y=CANVAS_HEIGHT + GENERAL_SPACING * 2,
                                 width=SLIDER_CANVAS_WIDTH,
                                 height=SLIDER_CANVAS_HEIGHT)

        self.sliders = []
        for i in range(NUM_SLIDERS):
            slider = Scale(self.slider_canvas,
                           from_=SLIDER_MIN,
                           to=SLIDER_MAX,
                           orient="horizontal",
                           label="Sensor %i:" % i)
            slider.place(x=SLIDER_SPACING,
                         y=i*SLIDER_HEIGHT + (i+1)*SLIDER_SPACING,
                         width=SLIDER_WIDTH,
                         height=SLIDER_HEIGHT)

            self.sliders.append(slider)

            self.closed = False
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        print("Closing...")
        self.closed = True
        self.root.destroy()
        # The next command will stop the simulation

    def button_clicked(self, event):
        buttons_under_mouse = self.button_canvas.find_overlapping(
            event.x, event.y, event.x, event.y
        )
        if len(buttons_under_mouse) > 0:
            index = buttons_under_mouse[0]
            self.buttons_down[index - 1] = True
            self.button_canvas.itemconfig(index,
                                          fill=BUTTON_DOWN_COLOR)
            self.button_canvas.update()

    def button_released(self, event):
        for i in range(len(self.buttons_down)):
            self.buttons_down[i] = False
            self.button_canvas.itemconfig(i + 1,
                                          fill=BUTTON_UP_COLOR)
            self.button_canvas.update()

    def read_button(self, index: int):
        """ Checks is the button button is down, 0/1"""
        if 0 <= index < NUM_BUTTONS:
            if self.buttons_down[index]:
                return True
            return False

    def read_switch(self, index: int):
        """ Checks if the switch is activated, 0/1"""
        if 0 <= index < NUM_SWITCHES:
            return self.switches_activated[index].get()

    def refresh(self):
        """ Refreshes the simulation. Doesn't exist in the real PYNQ and
        shouldn't be used by anyone."""
        simulator_window.check_exit_state()

        self.root.update()

    def check_exit_state(self):
        """ If the simulator window in closed, exit the simulation. """
        if self.closed:
            exit()


# Should not be referred to by external files
simulator_window = SimulatorWindow()


# The Button
class Button:
    def __init__(self, index: int):
        if 0 <= index < NUM_BUTTONS:
            self.index = index
        else:
            raise ValueError("""Invalid button ID %i, 
            Please select an ID between 0 and %i""" % (index, NUM_BUTTONS - 1))

    def read(self):

        simulator_window.check_exit_state()
        return simulator_window.read_button(self.index)

    def wait_for_value(self, value: int):
        if value == 0 or value == 1:
            while True:

                simulator_window.check_exit_state()

                if self.read() == value:
                    break
                else:
                    simulator_window.refresh()
                    time.sleep(1 / WAIT_FPS)
        else:
            raise ValueError("""The button can't reach value %i. The accepted
            values are 0 and 1""" % value)


# The switch
class Switch:

    def __init__(self, index: int):
        if 0 <= index < NUM_BUTTONS:
            self.index = index
        else:
            raise ValueError("""Invalid switch ID %i. 
            Please select an ID between 0 and %i"""
                             % (index, NUM_SWITCHES - 1))

    def read(self):

        simulator_window.check_exit_state()
        return simulator_window.read_switch(self.index)

    def wait_for_value(self, value: int):
        if value == 0 or value == 1:
            while True:

                simulator_window.check_exit_state()

                if self.read() == value:
                    break
                else:
                    simulator_window.refresh()
                    time.sleep(1 / WAIT_FPS)
        else:
            raise ValueError("""The switch can't reach value %i. The accepted
                        values are 0 and 1""" % value)


class LedMatrix:
    def __init__(self):
        # List of colors in the led matrix
        self.matrix = [[[0, 0, 0] for j in range(MATRIX_HEIGHT)]
                       for i in range(MATRIX_WIDTH)]
        simulator_window.refresh()

    def set_led_color(self, x: int, y: int, r: int, g: int, b: int):
        """ Gives the led the correct color

        :param x: int, x coordinate of the led
        :param y: int, y coordinate of the led
        :param r: int, red amount (0-255)
        :param g: int, green amount (0-255)
        :param b: int, blue amount (0-255)
        :return: None
        """

        simulator_window.check_exit_state()

        rgb = [r, g, b]
        # We can't let the user light up LEDs that don't exist
        if not (0 <= x < MATRIX_WIDTH and 0 <= y < MATRIX_HEIGHT):
            raise ValueError("""Invalid coordinates: x = %i, y = %i. 
            Please give coordinates between 0 <= x <= %i and 0 <= y <= %i"""
                             % (x, y, MATRIX_WIDTH - 1, MATRIX_HEIGHT - 1))

        # We can't give invalid color values for the LEDs
        elif not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("""Invalid color values: r=%i, g=%i, b=%i. 
            Please give color values between %i and %i"""
                             % (r, g, b, MIN_COLOR, MAX_COLOR))
        else:
            for i in range(3):
                self.matrix[x][y][i] = max(MIN_COLOR,
                                           min(MAX_COLOR, rgb[i]))
            led_color = self.matrix[x][y]
            r = led_color[0]
            g = led_color[1]
            b = led_color[2]
            # This is where we change the color of the led!
            simulator_window.canvas.itemconfig(
                simulator_window.grid_leds[x][y],
                fill="#%02x%02x%02x" % (r, g, b))
            simulator_window.canvas.update()

    def clear(self):
        """ Clear the led matrix, make all the leds black"""

        simulator_window.check_exit_state()

        for i in range(MATRIX_WIDTH):
            for j in range(MATRIX_HEIGHT):
                self.matrix[i][j] = [0, 0, 0]
                simulator_window.canvas.itemconfig(
                    simulator_window.grid_leds[i][j],
                    fill="#%02x%02x%02x" % (0, 0, 0))
                simulator_window.canvas.update()

    def read_sensor(self):
        """ Read the light sensor. In led matrix class due to reasons"""

        simulator_window.check_exit_state()

        simulator_window.slider_canvas.update()
        return simulator_window.sliders[0].get()

    def init(self):
        """ Does basically nothing in the emulation, but important in
        the real device"""
        print("Led matrix initialized")


led_matrix = LedMatrix()
