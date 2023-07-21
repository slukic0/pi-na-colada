from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(24)


def test_buzzer_on():
    '''
    Test that  the buzzer is active when on
    '''
    buzzer.on()
    sleep(3)
    assert buzzer.is_active
    buzzer.off()


# def test_buzzer_ff():
#     '''
#     Test that  the buzzer is not active when off
#     '''
#     buzzer.on()
#     sleep(3)
#     buzzer.off()
#     assert buzzer.is_active == False
