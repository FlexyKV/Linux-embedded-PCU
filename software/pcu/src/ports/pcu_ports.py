import RPi.GPIO as gpio
from time import sleep


def gpio_test_function():
    gpio.setwarnings(False)

    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.output(17, True)
    sleep(2)
    gpio.output(17, False)
    print("success!")


if __name__ == "__main__":
    gpio_test_function()
