from gpiozero import DistanceSensor
from time import sleep

sensor1 = DistanceSensor(echo=12, trigger=6)
# sensor2 = DistanceSensor(echo=16, trigger=13)
sensor3 = DistanceSensor(echo=20, trigger=19)
sensor4 = DistanceSensor(echo=21, trigger=26)


def test_sensor1_distance_measurements():
    '''
    Take 5 distance measurements at 30 cm for sensor 1 and find the average
    If the average is in an aceptable range, then the test passes
    '''
    values = []
    for i in range(0, 5):
        values.append(sensor1.distance)
        sleep(0.5)
    average_val = (values[0] + values[1] + values[2] +
                   values[3] + values[4]) / 5
    print("Sensor 1 (echo12, trig6) distance read: ", average_val)
    assert ((average_val * 100 >= 27) and (average_val * 100 <= 33))


# def test_sensor2_distance_measurements():
    # '''
    # Take 5 distance measurements at 30 cm for sensor 2 and find the average
    # If the average is in an aceptable range, then the test passes
    # '''
    # sleep(5)
    # values = []
    # for i in range(0, 5):
    #     values.append(sensor2.distance)
    #     sleep(0.5)
    # average_val = (values[0] + values[1] + values[2] +
    #                values[3] + values[4]) / 5
    # print("Sensor 2 (echo16, trig13) distance read: ", average_val)
    # assert ((average_val * 100 >= 27) and (average_val * 100 <= 33))


def test_sensor3_distance_measurements():
    '''
    Take 5 distance measurements at 30 cm for sensor 3 and find the average
    If the average is in an aceptable range, then the test passes
    '''
    sleep(5)
    values = []
    for i in range(0, 5):
        values.append(sensor3.distance)
        sleep(0.5)
    average_val = (values[0] + values[1] + values[2] +
                   values[3] + values[4]) / 5
    print("Sensor 3 (echo20, trig19) distance read: ", average_val)
    assert ((average_val * 100 >= 27) and (average_val * 100 <= 33))


def test_sensor4_distance_measurements():
    '''
    Take 5 distance measurements at 30 cm for sensor 4 and find the average
    If the average is in an aceptable range, then the test passes
    '''
    sleep(5)
    values = []
    for i in range(0, 5):
        values.append(sensor4.distance)
        sleep(0.5)
    average_val = (values[0] + values[1] + values[2] +
                   values[3] + values[4]) / 5
    print("Sensor 4 (echo21, trig26) distance read: ", average_val * 100, " cm")
    assert ((average_val * 100 >= 27) and (average_val * 100 <= 33))
