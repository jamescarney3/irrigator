from gpiozero import OutputDevice
import time

"""
use the GPIO outputs to turn the pump and drainage line
solenoid valve on and off, pressurize the line so it sprays
the plants with mist for some period of time
"""

# todo: this should log somewhere when it runs

# todo: pin numbers should be configurable
main_pump = OutputDevice(14, active_high=False, initial_value=False)
drain_solenoid = OutputDevice(15, active_high=False, initial_value=False)

main_pump.on()
time.sleep(4.5)
drain_solenoid.on()
main_pump.off()
time.sleep(30)
drain_solenoid.close()
main_pump.close()
