pump_pin1 = 22
pump_pin2 = 27
pump_pin3 = 17
pump_pin4 = 5

distance_sensor1_echo = 12
distance_sensor1_trigger = 6

distance_sensor2_echo = 20
distance_sensor2_trigger = 19

distance_sensor3_echo = 21
distance_sensor3_trigger = 26

distance_sensor4_echo = 16
distance_sensor4_trigger = 13

buzzer_pin = 4

full_res_level_distance = 15.0
distance_error_margin = full_res_level_distance * 0.1

g = (0, 255, 0)  # Green
r = (255, 0, 0)  # Red
b = (0, 0, 0)  # Black

checkmark_pixels = [
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, g,
    b, b, b, b, b, b, g, b,
    b, b, b, b, b, g, b, b,
    g, b, b, b, g, b, b, b,
    b, g, b, g, b, b, b, b,
    b, b, g, b, b, b, b, b,
    b, b, b, b, b, b, b, b
]

x_pixels = [
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, r, b, b, b, r, b, b,
    b, b, r, b, r, b, b, b,
    b, b, b, r, b, b, b, b,
    b, b, r, b, r, b, b, b,
    b, r, b, b, b, r, b, b,
    b, b, b, b, b, b, b, b
]

flow_rate = 27  # 27 mm per second
