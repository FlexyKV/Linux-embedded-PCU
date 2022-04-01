import RPi.GPIO as gpio
from time import sleep

#IO FOR THE RELAY CONTROL (SEE HARDWARE FOLDER FOR PINOUT)
PORT0_GATE0 = 37
PORT0_GATE1 = 38
PORT1_GATE0 = 36
PORT1_GATE1 = 33
PORT2_GATE0 = 31
PORT2_GATE1 = 32
PORT3_GATE0 = 29
PORT3_GATE1 = 22
PORT4_GATE0 = 18
PORT4_GATE1 = 15
PORT5_GATE0 = 16
PORT5_GATE1 = 13
PORT6_GATE0 = 11
PORT6_GATE1 = 7
PORT7_GATE0 = 5
PORT7_GATE1 = 3
PORT_CONFIRM = 35
PORT_ANTICONFIRM = 40

#NECESSARY DELAY FOR THE RT314F12 RELAY GATE AND MOSFET DELAY (seconds)
RELAY_DELAY = 0.1


def gpio_setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    #Setup ANTICONFIRM TO FALSE SO THAT NO RELAY WILL CHANGE STATE IF NOISE
    gpio.setup(PORT_ANTICONFIRM, gpio.OUT)
    gpio.output(PORT_ANTICONFIRM, False)
    gpio.setup(PORT_CONFIRM, gpio.OUT)
    gpio.setup(PORT0_GATE0, gpio.OUT)
    gpio.setup(PORT0_GATE1, gpio.OUT)
    gpio.setup(PORT1_GATE0, gpio.OUT)
    gpio.setup(PORT1_GATE1, gpio.OUT)
    gpio.setup(PORT2_GATE0, gpio.OUT)
    gpio.setup(PORT2_GATE1, gpio.OUT)
    gpio.setup(PORT3_GATE0, gpio.OUT)
    gpio.setup(PORT3_GATE1, gpio.OUT)
    gpio.setup(PORT4_GATE0, gpio.OUT)
    gpio.setup(PORT4_GATE1, gpio.OUT)
    gpio.setup(PORT5_GATE0, gpio.OUT)
    gpio.setup(PORT5_GATE1, gpio.OUT)
    gpio.setup(PORT6_GATE0, gpio.OUT)
    gpio.setup(PORT6_GATE1, gpio.OUT)
    gpio.setup(PORT7_GATE0, gpio.OUT)
    gpio.setup(PORT7_GATE1, gpio.OUT)
    sleep(RELAY_DELAY)


def gpio_toggle_ON(gate_number):
    gate0 = "PORT" + str(gate_number) + "_GATE0"
    gate1 = "PORT" + str(gate_number) + "_GATE1"
    gpio.output(globals()[gate0], False)
    sleep(RELAY_DELAY)
    gpio.output(globals()[gate1], True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, False)
    print(f"port {gate_number} is on")


def gpio_toggle_OFF(gate_number):
    gate0 = "PORT" + str(gate_number) + "_GATE0"
    gate1 = "PORT" + str(gate_number) + "_GATE1"
    gpio.output(globals()[gate1], False)
    sleep(RELAY_DELAY)
    gpio.output(globals()[gate0], True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, False)
    print(f"port {gate_number} is off")


def Port_stress_test():
    # #NO DELAY ON - OFF
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


def gpio_test_function():
    gpio.setwarnings(False)
    gpio_setup()

    gpio_toggle_ON(2)


    print("success !!")



if __name__ == "__main__":
    gpio_test_function()
