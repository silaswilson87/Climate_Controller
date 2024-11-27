import os
import time
import board
import digitalio
import analogio
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn

from util.common import CommonFunctions
#from traceback import format_exception

from util.debug import Debug
from util.fan_motor_controller import FanMotorController
from util.heater_controller import HeaterController
from util.properties import Properties
from util.simple_timer import Timer
# from util.simple_timer import Timer
from util.temperature import TemperatureReader
from traceback import format_exception

red = digitalio.DigitalInOut(board.A5)
red.direction = digitalio.Direction.OUTPUT
green = digitalio.DigitalInOut(board.D13)
green.direction = digitalio.Direction.OUTPUT
yellow = digitalio.DigitalInOut(board.D12)
yellow.direction = digitalio.Direction.OUTPUT
blue = digitalio.DigitalInOut(board.D11)
blue.direction = digitalio.Direction.OUTPUT


locked = DigitalInOut(board.D5)
locked.direction = digitalio.Direction.INPUT
locked_val = locked.value

unlocked = DigitalInOut(board.D6)
unlocked.direction = digitalio.Direction.INPUT
unlocked_val = unlocked.value

targetheat = AnalogIn(board.A0)
targetcold = AnalogIn(board.A1)
targethumidity = AnalogIn(board.A2)

swingheat = 0
swingcold = 0
swinghumidity = 0
swinghumidity = 0

timer_time = 20 # 480
loop_count = 0
temp_avg = 0

debug = Debug()

intake_motor = FanMotorController(board.D9, debug)
exhaust_motor = FanMotorController(board.A4, debug)
heater = HeaterController(board.A3, debug)

humidity_pin = digitalio.DigitalInOut(board.D10)
humidity_pin.direction = digitalio.Direction.OUTPUT

debug.check_debug_enable()
debug.print_debug("code","CircuitPython version " + str(os.uname().version))

temperature = TemperatureReader(debug)
timer = Timer()
timer.start_timer(timer_time)

properties = Properties(debug)

from util.Climate_display import ClimateDisplay
display = ClimateDisplay(debug, properties)

program_start_time = time.monotonic()

max_temp = -99999999
min_temp =  99999999

avg = 0

pretendtemp = 0.0
pretendhumidity = 0.0

def get_voltage(x):
    return (x.value * 3.3) / 65536
def percentage(x):
    return (get_voltage(x)/3 * 100)

#display.display_remote("Start up")
display.display_messages(["Booting"])
while True:
    loop_count += 1
    debug.check_debug_enable()
    temp, humidity = temperature.read()
    temp_avg += temp
    time.sleep(0)
    if unlocked.value:
            yellow.value = True
            blue.value = False
            swingheat = (percentage(targetheat))
            swingcold = (percentage(targetcold))
            swinghumidity = (percentage(targethumidity))
            #debug.print_debug("Debug Unlocked", " Heater set to warm when bellow %2d - Temp %2d avg | Cooling fan set cool when above at %2d - Temp %2d | Humidity tolerance set at %2d - Humidity: %2d" % (swingheat,avg,swingcold,avg,swinghumidity,humidity))

    elif locked.value:
            yellow.value = False
            blue.value = True
            pretendtemp = (percentage(targetcold))
            pretendhumidity = (percentage(targethumidity))
            #debug.print_debug("Debug Locked", " Heater set to warm when bellow %2d - Simulated Temp %2d | Cooling fan set cool when above at %2d - Simulated temp %2d | Humidity tolerance set at %2d - Simulated Humidity: %2d" % (swingheat,pretendtemp,swingcold,pretendtemp,swinghumidity,pretendhumidity))
    try:
        if loop_count % 10 is 0: # Read temp 10 times and compute avg temp
            avg = int(temp_avg/loop_count)
            max_temp = max(max_temp, avg)
            min_temp = min(min_temp, avg)
            lines=["Temp:"+str(avg),"Min:"+str(min_temp),"Max:"+str(max_temp)]
            display.display_messages(lines)
            # timer.reset_timer(properties.defaults["send_interval"])
            loop_count = 0
            temp_avg = 0
            green.value = True
            time.sleep(.1)
            green.value = False

            if  pretendtemp > swingcold and pretendhumidity < swinghumidity and avg > swingheat:       # Intake on, exhaust on, heater off
                intake_motor.fan_on()
                exhaust_motor.fan_on()
                heater.heater_off()

            elif pretendtemp > swingcold and pretendhumidity < swinghumidity  and avg > swingheat:    # Intake on, exhaust off, heater off
                intake_motor.fan1_on()
                exhaust_motor.fan2_off()
                heater.heater_off()

            elif pretendtemp < swingcold and humidity < swinghumidity  and avg > swingheat:    # Intake off, exhaust on, heater off
                intake_motor.fan1_on()
                exhaust_motor.fan2_off()
                heater.heater_off()

            elif pretendtemp < swingcold and pretendhumidity < swinghumidity and avg < swingheat:    # Intake off, exhaust off, heater on
                intake_motor.fan1_off()
                exhaust_motor.fan2_off()
                heater.heater_on()

            elif pretendtemp < swingcold and pretendhumidity < swinghumidity  and avg > swingheat:    # Intake off, exhaust off, heater off
                intake_motor.fan1_off()
                exhaust_motor.fan2_off()
                heater.heater_off()

            elif pretendtemp < swingcold and pretendhumidity < swinghumidity  and avg < swingheat:    # Intake off, exhaust off, heater off
                intake_motor.fan1_off()
                exhaust_motor.fan2_off()
                heater.heater_off()
            elif pretendtemp < swingcold and pretendhumidity > swinghumidity  and avg < swingheat:    # Intake off, exhaust off, heater off
                intake_motor.fan1_off()
                exhaust_motor.fan2_off()
                heater.heater_off()

        if not timer is None and timer.is_timed_out():
            start_elapsed = CommonFunctions.format_elapsed_ms(program_start_time)
#           debug.print_debug("code", "runtime %s, min: %2d, max:%2s, humidity:%2d" % (start_elapsed, min_temp, max_temp, humidity))
            timer.reset_timer(timer_time)

        time.sleep(.1)

    except Exception as e:
        error = str(format_exception(e))
        #error = str(e)
        debug.print_debug("code","Exception in main: "+error)
        red.value = True
