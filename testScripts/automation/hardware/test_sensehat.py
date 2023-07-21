from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

# Define some colours
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

# Display these colours on the LED matrix
sense.set_pixels(checkmark_pixels)
sleep(5)
sense.set_pixels(x_pixels)
sleep(5)
sense.clear()
