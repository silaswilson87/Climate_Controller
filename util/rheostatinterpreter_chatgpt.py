import analogio
from board import A0  # Assuming the rheostat is connected to analog pin A0
import time


class RheostatInterpreter:
    def __init__(self, pin, min_value=0, max_value=65535, hysteresis=1):
        self.rheostat = analogio.AnalogIn(pin)
        self.min_value = min_value  # Calibration min (default to 0)
        self.max_value = max_value  # Calibration max (default to maximum ADC value)
        self.hysteresis = hysteresis  # Hysteresis threshold
        self.last_output = None  # Last output percentage

    def read_raw(self):
        """Returns the raw reading from the rheostat."""
        return self.rheostat.value

    def read_percentage(self):
        """Converts the raw reading to a percentage based on calibration."""
        raw_value = self.read_raw()
        adjusted_value = (raw_value - self.min_value) / (self.max_value - self.min_value)
        percentage = max(0, min(100, adjusted_value * 100))
        return percentage

    def get_stable_output(self):
        """Returns the current percentage output with hysteresis applied."""
        current_output = self.read_percentage()

        # Apply hysteresis
        if self.last_output is None or abs(current_output - self.last_output) >= self.hysteresis:
            self.last_output = current_output

        return self.last_output

    def calibrate(self, min_value=None, max_value=None):
        """Sets new calibration min and max values for the rheostat."""
        if min_value is not None:
            self.min_value = min_value
        if max_value is not None:
            self.max_value = max_value


# Example usage
rheostat_interpreter = RheostatInterpreter(pin=A0)

# To calibrate, measure known minimum and maximum resistance values:
initial_reading = rheostat_interpreter.read_raw()  # e.g., when fully turned down
final_reading = rheostat_interpreter.read_raw()  # e.g., when fully turned up

rheostat_interpreter.calibrate(min_value=initial_reading, max_value=final_reading)

# Loop to continuously print the output with hysteresis
while True:
    stable_output = rheostat_interpreter.get_stable_output()
    print(f"Rheostat Value: {stable_output:.2f}%")
    time.sleep(0.5)  # Adjust the delay as needed
