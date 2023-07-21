from gpiozero import OutputDevice
from time import sleep

inPin1 = 22
inPin2 = 27
inPin3 = 17
inPin4 = 5

relayPump1 = OutputDevice(inPin1, active_high=False, initial_value=False)
relayPump2 = OutputDevice(inPin2, active_high=False, initial_value=False)
relayPump3 = OutputDevice(inPin3, active_high=False, initial_value=False)
relayPump4 = OutputDevice(inPin4, active_high=False, initial_value=False)

relayPump1.on()
relayPump2.on()
# relayPump3.on()
relayPump4.on()

sleep(3)

relayPump1.off()
relayPump2.off()
# relayPump3.off()
relayPump4.off()
