import RPi.GPIO as gpio
from time import sleep

#IO FOR THE RELAY CONTROL (SEE HARDWARE FOLDER FOR PINOUT)
PORT1_GATE1 = 37
PORT1_GATE2 = 38
PORT2_GATE1 = 36
PORT2_GATE2 = 33
PORT3_GATE1 = 31
PORT3_GATE2 = 32
PORT4_GATE1 = 29
PORT4_GATE2 = 22
PORT5_GATE1 = 18
PORT5_GATE2 = 15
PORT6_GATE1 = 13
PORT6_GATE2 = 16
PORT7_GATE1 = 11
PORT7_GATE2 = 7
PORT8_GATE1 = 5
PORT8_GATE2 = 3
PORT_CONFIRM = 35
PORT_ANTICONFIRM = 40

#NECESSARY DELAY FOR THE RT314F12 RELAY GATE AND MOSFET DELAY (seconds)
RELAY_DELAY = 0.05


def gpio_setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    #Setup ANTICONFIRM TO FALSE SO THAT NO RELAY WILL CHANGE STATE IF NOISE
    gpio.setup(PORT_ANTICONFIRM, gpio.OUT)
    gpio.setup(PORT_ANTICONFIRM, False)
    gpio.setup(PORT_CONFIRM, gpio.OUT)
    gpio.setup(PORT1_GATE1, gpio.OUT)
    gpio.setup(PORT1_GATE2, gpio.OUT)
    gpio.setup(PORT2_GATE1, gpio.OUT)
    gpio.setup(PORT2_GATE2, gpio.OUT)
    gpio.setup(PORT3_GATE1, gpio.OUT)
    gpio.setup(PORT3_GATE2, gpio.OUT)
    gpio.setup(PORT4_GATE1, gpio.OUT)
    gpio.setup(PORT4_GATE2, gpio.OUT)
    gpio.setup(PORT5_GATE1, gpio.OUT)
    gpio.setup(PORT5_GATE2, gpio.OUT)
    gpio.setup(PORT6_GATE1, gpio.OUT)
    gpio.setup(PORT6_GATE2, gpio.OUT)
    gpio.setup(PORT7_GATE1, gpio.OUT)
    gpio.setup(PORT7_GATE2, gpio.OUT)
    gpio.setup(PORT8_GATE1, gpio.OUT)
    gpio.setup(PORT8_GATE2, gpio.OUT)
    sleep(RELAY_DELAY)


def gpio_toggle_ON(gate_number):
    gate1 = "PORT" + str(gate_number) + "_GATE1"
    gate2 = "PORT" + str(gate_number) + "_GATE2"
    gpio.output(globals()[gate2], False)
    sleep(RELAY_DELAY)
    gpio.output(globals()[gate1], True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, False)
    print(f"port {gate_number} is on")


def gpio_toggle_OFF(gate_number):
    gate1 = "PORT" + str(gate_number) + "_GATE1"
    gate2 = "PORT" + str(gate_number) + "_GATE2"
    gpio.output(globals()[gate1], False)
    sleep(RELAY_DELAY)
    gpio.output(globals()[gate2], True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, False)
    print(f"port {gate_number} is off")


def gpio_test_function():
    gpio.setwarnings(False)
    gpio_setup()


    #NO DELAY ON - OFF
    gpio_toggle_ON(1)
    sleep(0)
    gpio_toggle_OFF(1)
    sleep(3)

    #NO DELAY ON - OFF - ON
    gpio_toggle_ON(1)
    sleep(0)
    gpio_toggle_OFF(1)
    sleep(0)
    gpio_toggle_ON(1)
    sleep(3)

    #ON - ON
    gpio_toggle_ON(1)
    sleep(3)

    #OFF - OFF
    gpio_toggle_OFF(1)
    sleep(0.5)
    gpio_toggle_OFF(1)

    print("success !!")


if __name__ == "__main__":
    gpio_test_function()
