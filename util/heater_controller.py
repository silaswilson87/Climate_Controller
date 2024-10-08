import board
import digitalio
from util.debug import Debug


class HeaterController:
    def __init__(self, heater_pin: board.pin, debug: Debug):
        self.debug = debug
        self.relay = digitalio.DigitalInOut(heater_pin)
        self.relay.direction = digitalio.Direction.OUTPUT
        self.running = False
        self.relay.value = False
#        self.led = digitalio.DigitalInOut(board.A0)
#        self.led.direction = digitalio.Direction.OUTPUT


    def heater_on(self):
        self.running = True
        if not self.relay.value: # Only print once when value changes
            self.debug.print_debug("Heater", "Heater ON")
        self.relay.value = True
#        self.led.value = True


    def heater_off(self):
        self.running = False
#        self.led.value = False
        if self.relay.value:  # Only print once when value changes
            self.debug.print_debug("Heater", "Heater OFF")
        self.relay.value = False
