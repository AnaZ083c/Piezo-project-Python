import time
import sys
import signal

from PyMata.pymata import PyMata


BEEPER = 11  # pin that piezo device is attached to
LED = 12
BOARD_LED = 13

# create a PyMata instance
board = PyMata("COM6")


def signal_handler(sig, frm):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# play a continuous tone, wait 5 seconds and then turn tone off

# Blink for 10 times
for x in range(10):
    print(x + 1)
    # Set the output to 1 = High
    board.analog_write(LED, 254)
    # Wait a half second between toggles.
    time.sleep(.5)
    # Set the output to 0 = Low
    board.analog_write(LED, 0)
    time.sleep(.5)

# Close PyMata when we are done
board.close()

# board.play_tone(BEEPER, board.TONE_TONE, 1000, 0)
# board.digital_write(LED, board.HIGH)
# time.sleep(5)
# board.play_tone(BEEPER, board.TONE_NO_TONE, 1000, 0)
#
# board.close()