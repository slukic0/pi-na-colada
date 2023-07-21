from time import sleep
from statistics import median
from sense_hat import SenseHat
from gpiozero import DistanceSensor, TonalBuzzer, OutputDevice
from gpiozero.tones import Tone
from . import constants
from . import sql as local_db


sense = SenseHat()

sensor1 = DistanceSensor(echo=constants.distance_sensor1_echo,
                         trigger=constants.distance_sensor1_trigger)
sensor2 = DistanceSensor(echo=constants.distance_sensor2_echo,
                         trigger=constants.distance_sensor2_trigger)
sensor3 = DistanceSensor(echo=constants.distance_sensor3_echo,
                         trigger=constants.distance_sensor3_trigger)
sensor4 = DistanceSensor(echo=constants.distance_sensor4_echo,
                         trigger=constants.distance_sensor4_trigger)


# Relay board is active low, so make sure the device uses active low as on
relay_pump1 = OutputDevice(
    constants.pump_pin1, active_high=False, initial_value=False)
relay_pump2 = OutputDevice(
    constants.pump_pin2, active_high=False, initial_value=False)
relay_pump3 = OutputDevice(
    constants.pump_pin3, active_high=False, initial_value=False)
relay_pump4 = OutputDevice(
    constants.pump_pin4, active_high=False, initial_value=False)

buzzer = TonalBuzzer(pin=constants.buzzer_pin, mid_tone=500, octaves=2)


def check_fluid_level(pump_num: int) -> float:
    '''
    Returns the water distance from a given sensor in centimeters
    pump_num - pump number corresponding to reservoir
    raises ValueError if pump_num is invalid
    '''
    # Python 3.9 does not have a switch statement so we'll use if's
    # Start counting from 1
    if pump_num == 1:
        distance_sensor = sensor1
    elif pump_num == 2:
        distance_sensor = sensor2
    elif pump_num == 3:
        distance_sensor = sensor3
    elif pump_num == 4:
        distance_sensor = sensor4
    else:
        raise ValueError("Pump not in range (1,4) inclusive")

    values = []
    for i in range(0, 5):
        values.append(distance_sensor.distance*1000)   # Get distance in mm
        sleep(0.25)
    return median(values)   # Return median instead of avg


def pour_selected_pump(pump_num: int, pour_amount: float) -> None:
    '''
    Check the fluid level of a given reservoir
    pump_num - pump number
    pour_time - time to pour in seconds
    raises ValueError if pump_num is invalid
    '''
    # Python 3.9 does not have a switch statement so we'll use if's
    # Start counting from 1
    if pump_num == 1:
        relay_pump = relay_pump1
    elif pump_num == 2:
        relay_pump = relay_pump2
    elif pump_num == 3:
        relay_pump = relay_pump3
    elif pump_num == 4:
        relay_pump = relay_pump4
    else:
        raise ValueError("Pump not in range (1,4) inclusive")

    pour_time = pour_amount / constants.flow_rate
    # Since we leveraged the OutputDevice class, we can simply use on and off
    relay_pump.on()
    sleep(pour_time)
    relay_pump.off()
    local_db.write_to_SQL_Table("OK", "INFO", "")
    return


def sound_buzzer() -> None:
    '''
    Play a 1000 Hz tone from the buzzer
    '''
    # buzzer.play(Tone("A4"))
    for i in range(0, 3):
        buzzer.play(Tone.from_frequency(500))
        sleep(0.25)
        buzzer.stop()
        sleep(0.25)
    return


def display_sense_hat_msg_success() -> None:
    '''
    Display a check mark on success
    '''
    sense.set_pixels(constants.checkmark_pixels)
    sleep(3)
    sense.clear()
    return


def display_sense_hat_msg_failure() -> None:
    '''
    Display a X on failure
    '''
    sense.set_pixels(constants.x_pixels)
    sleep(3)
    sense.clear()
    return
