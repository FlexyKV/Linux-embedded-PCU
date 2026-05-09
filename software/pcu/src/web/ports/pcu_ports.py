from time import sleep

import RPi.GPIO as gpio

# Relay control pins (board numbering). See hardware/pinout.md.
PORT_GATES = {
    0: (37, 38),
    1: (36, 33),
    2: (31, 32),
    3: (29, 22),
    4: (18, 15),
    5: (16, 13),
    6: (11, 7),
    7: (5, 3),
}

PORT_CONFIRM = 35
PORT_ANTICONFIRM = 40

# RT314F12 relay gate + MOSFET settling delay, in seconds.
RELAY_DELAY = 0.1


def gpio_setup():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)

    # Hold ANTICONFIRM low so noise on CONFIRM cannot trigger a relay change.
    gpio.setup(PORT_ANTICONFIRM, gpio.OUT)
    gpio.output(PORT_ANTICONFIRM, False)
    gpio.setup(PORT_CONFIRM, gpio.OUT)

    for gate0, gate1 in PORT_GATES.values():
        gpio.setup(gate0, gpio.OUT)
        gpio.setup(gate1, gpio.OUT)

    sleep(RELAY_DELAY)


def _pulse_confirm():
    gpio.output(PORT_CONFIRM, True)
    sleep(RELAY_DELAY)
    gpio.output(PORT_CONFIRM, False)


def gpio_toggle_on(port_id):
    gate0, gate1 = PORT_GATES[port_id]
    gpio.output(gate0, False)
    sleep(RELAY_DELAY)
    gpio.output(gate1, True)
    sleep(RELAY_DELAY)
    _pulse_confirm()
    print(f"port {port_id} is on")


def gpio_toggle_off(port_id):
    gate0, gate1 = PORT_GATES[port_id]
    gpio.output(gate1, False)
    sleep(RELAY_DELAY)
    gpio.output(gate0, True)
    sleep(RELAY_DELAY)
    _pulse_confirm()
    print(f"port {port_id} is off")
