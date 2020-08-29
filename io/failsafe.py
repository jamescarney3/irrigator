from gpiozero import OutputDevice
import time

"""
turn off the pump, open the drainage line, don't flood the
apartment. this should probably run every 5-10 minutes to
minimize risk of the bad kind of irrigation
"""

# todo: make this log somewhere when it runs

# todo: pin numbers should be configurable
main_pump = OutputDevice(14, active_high=False, initial_value=False)
drain_solenoid = OutputDevice(15, active_high=False, initial_value=False)

time.sleep(45)
main_pump.off()
drain_solenoid.off()
