import pyfirmata
import time

board = pyfirmata.Arduino('COM6')

it = pyfirmata.util.Iterator(board)
it.start()

piezzo = board.get_pin('d:11:o')
analog_pot = board.get_pin('a:0:i')

while True:

    pot_val = analog_pot.read()
    if pot_val is not None:
        delay = pot_val + 0.01
        piezzo.write(1)
        time.sleep(delay)
        piezzo.write(0)
        time.sleep(delay)
    else:
        time.sleep(0.1)

    # piezzo_in.write(1)
    # time.sleep(1)
    # piezzo_in.write(0)
    # time.sleep(1)



