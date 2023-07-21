from time import sleep
from statistics import median
from sense_hat import SenseHat
from . import constants


sense = SenseHat()


def mock_check_fluid_level(pump_num: int) -> float:
    '''
    Returns the water distance from a given sensor in centimeters
    pump_num - pump number corresponding to reservoir
    raises ValueError if pump_num is invalid
    '''
    # Python 3.9 does not have a switch statement so we'll use if's
    # Start counting from 1

    distance = 0.20   # 20 cm

    if pump_num == 1:
        sense.show_message("Checking pump 1 level", 0.05)
    elif pump_num == 2:
        sense.show_message("Checking pump 2 level", 0.05)
    elif pump_num == 3:
        sense.show_message("Checking pump 3 level", 0.05)
    elif pump_num == 4:
        sense.show_message("Checking pump 4 level", 0.05)
    else:
        raise ValueError("Pump not in range (1,4) inclusive")

    values = []
    for i in range(0, 5):
        values.append(distance*100)   # Get distance in cm
        sleep(0.25)
    return median(values)   # Return median instead of avg


def mock_pour_selected_pump(pump_num: int, pour_time: float) -> None:
    '''
    Check the fluid level of a given reservoir
    pump_num - pump number
    pour_time - time to pour in seconds
    raises ValueError if pump_num is invalid
    '''
    # Python 3.9 does not have a switch statement so we'll use if's
    # Start counting from 1
    if pump_num == 1:
        relay_pump_message = "Pump 1"
    elif pump_num == 2:
        relay_pump_message = "Pump 2"
    elif pump_num == 3:
        relay_pump_message = "Pump 3"
    elif pump_num == 4:
        relay_pump_message = "Pump 4"
    else:
        raise ValueError("Pump not in range (1,4) inclusive")

    sense.show_message(f'{relay_pump_message} pouring...', 0.05)
    sleep(pour_time)
    return


def mock_sound_buzzer() -> None:
    '''
    Play a 1000 Hz tone from the buzzer
    '''

    sense.show_message("Sounding buzzer", 0.05)
    return


def mock_display_sense_hat_msg_success() -> None:
    '''
    Display a check mark on success
    '''
    sense.set_pixels(constants.checkmark_pixels)
    sleep(3)
    sense.clear()
    return


def mock_display_sense_hat_msg_failure() -> None:
    '''
    Display a X on failure
    '''
    sense.set_pixels(constants.x_pixels)
    sleep(3)
    sense.clear()
    return
