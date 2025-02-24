class ThermostatStateMachine:
    def __init__(self, target_temp, target_humidity, temp_hysteresis=1):
        self.target_temp = target_temp
        self.target_humidity = target_humidity
        self.temp_hysteresis = temp_hysteresis
        self.current_temp = 0
        self.current_humidity = 0
        self.state = "IDLE"

    def update_conditions(self, current_temp, current_humidity):
        self.current_temp = current_temp
        self.current_humidity = current_humidity
        self.transition_state()

    def transition_state(self):
        if self.state == "IDLE":
            if self.current_temp < self.target_temp - self.temp_hysteresis:
                self.state = "HEATING"
            elif self.current_temp > self.target_temp + self.temp_hysteresis:
                self.state = "COOLING"

        elif self.state == "HEATING":
            if self.current_temp >= self.target_temp:
                self.state = "IDLE"

        elif self.state == "COOLING":
            if self.current_temp <= self.target_temp:
                self.state = "IDLE"

        elif self.state == "CONFIGURE":
            self.apply_settings()

    def control_actuators(self):
        if self.state == "HEATING":
            print("Turning on heating")
            # Code to turn on heating
        elif self.state == "COOLING":
            print("Turning on cooling")
            # Code to turn on cooling
        else:
            print("System is idle or configuring")
            # Code to turn off both heating and cooling

    def apply_settings(self, new_temp=None, new_humidity=None, new_hysteresis=None):
        if new_temp is not None:
            self.target_temp = new_temp
        if new_humidity is not None:
            self.target_humidity = new_humidity
        if new_hysteresis is not None:
            self.temp_hysteresis = new_hysteresis
        self.state = "IDLE"  # Return to IDLE after applying settings

    def run(self):
        while True:
            if self.state != "CONFIGURE":
                self.control_actuators()
            # Sleep or wait to reduce loop frequency

# Usage example:
thermostat = ThermostatStateMachine(target_temp=22, target_humidity=50)

# Update loop for sensing and acting
current_temp = 20  # Replace with actual temperature reading
current_humidity = 45  # Replace with actual humidity reading
thermostat.update_conditions(current_temp, current_humidity)

# If you want to change settings:
thermostat.state = "CONFIGURE"
thermostat.apply_settings(new_temp=24, new_hysteresis=2)

thermostat.run()