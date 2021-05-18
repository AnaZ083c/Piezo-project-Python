from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

class Led2:
    def __init__(self, led_pin, button_pin, button_pushed, led_state, previous_button_state, last_debounce_time, debounce_delay, times_pressed):
        self.led_pin = led_pin
        self.button_pin = button_pin
        self.button_pushed = button_pushed
        self.led_state = led_state
        self.previous_button_state = previous_button_state
        self.last_debounce_time = last_debounce_time
        self.debounce_delay = debounce_delay
        self.times_pressed = times_pressed

    def led_on_button(self, board, time):
        reading = board.digital_read(self.button_pin)

        if reading != self.previous_button_state:
            self.last_debounce_time = float(time.time() / 1000)

        if ((time.time() / 1000) - self.last_debounce_time) > self.debounce_delay:
            if reading != self.button_pushed:
                self.button_pushed = reading
            if self.button_pushed == 1:
                self.led_state = int(not bool(self.led_state))

        board.digital_write(self.led_pin, self.led_state)
        self.previous_button_state = reading