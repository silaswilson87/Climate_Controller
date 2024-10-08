import board
import busio
#import adafruit_mcp9808
import adafruit_ahtx0
from util.debug import Debug


class TemperatureReader:
    def __init__(self, debug: Debug):
        self.debug = debug

        # Create sensor object, communicating over the board's default I2C bus
        # i2c = board.I2C()

        # For using the built-in STEMMA QT connector on a microcontroller
        i2c = board.STEMMA_I2C()

        # To initialise using the default address:
        self.sensor = adafruit_ahtx0.AHTx0(i2c)

    def read(self):
        tempC = int(self.sensor.temperature)
        tempF = int(tempC * 9 / 5 + 32)
        humidity = int(self.sensor.relative_humidity)
        # self.debug.print_debug("Reader","Temperature: {0:2d}C {1:2d}F {2:2d}H".format(tempC, tempF, humidity))
        return tempF, humidity

# class TemperatureReader:
#     def __init__(self, debug: Debug):
#         self.debug = debug
#         i2c = board.I2C()  # uses board.SCL and board.SDA
#         # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
#
#         # To initialise using the default address:
#         self.mcp = adafruit_mcp9808.MCP9808(i2c)
#
#     def read(self):
#         tempC = self.mcp.temperature
#         tempF = tempC * 9 / 5 + 32
#         self.debug.print_debug("Reader","Temperature: {} C {} F ".format(tempC, tempF))
#         return int(tempF)
#
