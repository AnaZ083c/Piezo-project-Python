from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import time

# Arduino LED is on pin 13
BOARD_LED = 13
RED_LED = 8
BUTTON = 2

# If you are having problems connecting, you may
# wish to add some time the arduino_wait parameter.

# replace:
# board = PyMata3()
# with:
# board = PyMata3(arduino_wait=5)

# adjust the arduino_wait value to meet the needs
# of your computer

# instantiate PyMata3

board = PyMata3(com_port='com6')

button_pushed = 0
led_state = 0
previous_button_state = 0
last_debounce_time = 0.0
debounce_delay = 150.0

times_pressed = 0

def setup():
    board.set_pin_mode(BUTTON, Constants.INPUT)

    board.set_pin_mode(BOARD_LED, Constants.OUTPUT)
    board.set_pin_mode(RED_LED, Constants.OUTPUT)

    board.digital_write(RED_LED, led_state)

def loop():
    global button_pushed
    global led_state
    global previous_button_state
    global last_debonce_time
    global debounce
    global times_pressed

    reading = board.digital_read(BUTTON)

    if reading != previous_button_state:
        last_debonce_time = float(time.time()/1000)

    if ((time.time()/1000) - last_debounce_time) > debounce_delay:
        if reading != button_pushed:
            button_pushed = reading
        if button_pushed == 1:
            led_state = int(not bool(led_state))

    board.digital_write(RED_LED, led_state)
    previous_button_state = reading

if __name__ == "__main__":
    setup()
    while True:
        loop()