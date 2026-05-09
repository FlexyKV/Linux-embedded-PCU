import math
import time
from datetime import datetime

import Adafruit_GPIO.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

NUM_PORTS = 8
ADC_RESOLUTION = 1023
SAMPLING_PERIOD_S = 1.0
VOLTAGE_CONV_FACTOR = 67
NOISE_FLOOR = 4
SQRT2 = math.sqrt(2)

# Per-port calibration. Each port has its own resistor tolerance, so factors differ.
CURRENT_CONV_FACTORS = [
    0.028840173 * SQRT2,
    0.028552811 * SQRT2,
    0.0288662513 * SQRT2,
    0.028663481 * SQRT2,
    0.02855166 * SQRT2,
    0.02884985015 * SQRT2,
    0.028224279 * SQRT2,
    0.020484626 * SQRT2,  # 20A clamp; to be replaced
]

POWER_CAL_FACTORS = [
    0.04038357044,
    0.04014649503,
    0.040416841,
    0.040462253,
    0.040599104,
    0.041873727,
    0.040877261,
    0.031791492,
]


class MCP3008(object):
    """Adafruit MCP3008 analog-to-digital converter."""

    def __init__(self, clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
        if spi is not None:
            self._spi = spi
        elif clk is not None and cs is not None and miso is not None and mosi is not None:
            if gpio is None:
                gpio = GPIO.get_platform_gpio()
            self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
        else:
            raise ValueError(
                "Must specify either spi for hardware SPI or clk, cs, miso, and mosi for software SPI"
            )
        self._spi.set_clock_hz(3600000)
        self._spi.set_mode(0)
        self._spi.set_bit_order(SPI.MSBFIRST)

    def read_adc(self, adc_number):
        """Read the value of the specified ADC channel (0-7), range 0..1023."""
        assert 0 <= adc_number <= 7, "ADC number must be in 0..7"
        command = 0b11 << 6
        command |= (adc_number & 0x07) << 3
        resp = self._spi.transfer([command, 0x0, 0x0])
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF


def adc_setup():
    """Initialise the SPI bus and the two MCP3008 ADCs."""
    spi_port = 0
    mcp0 = MCP3008(spi=SPI.SpiDev(spi_port, 0))
    mcp1 = MCP3008(spi=SPI.SpiDev(spi_port, 1))
    return [mcp0, mcp1]


def _denoise(adc_data, vref_reading):
    if adc_data < NOISE_FLOOR:
        return 0
    return adc_data - vref_reading


def _rms_current(samples, conv_factor):
    squared = [(s * conv_factor) ** 2 for s in samples]
    return math.sqrt(sum(squared) / len(squared))


def _avg_power(voltage_samples, current_samples, conv_factor):
    instantaneous = [
        (current_samples[i] * conv_factor) * voltage_samples[i]
        for i in range(len(voltage_samples))
    ]
    avg = sum(instantaneous) / len(instantaneous)
    return max(avg, 0)


def calculate_read(adc_port, adc_repo, voltage_ref):
    """Sample all 8 ports for one period and persist the RMS/average results."""
    currents = [[] for _ in range(NUM_PORTS)]
    voltages = []

    start_time = time.time()
    while (time.time() - start_time) <= SAMPLING_PERIOD_S:
        # Read order matters for electrical timing — keep voltage_ref first,
        # currents 0..3, then the line voltage, then currents 4..7.
        vref_reading = adc_port[1].read_adc(1)

        for ch in range(4):
            currents[ch].append(_denoise(adc_port[0].read_adc(ch), vref_reading))

        line_voltage = (
            ((adc_port[1].read_adc(0) - vref_reading) / ADC_RESOLUTION)
            * voltage_ref
            * VOLTAGE_CONV_FACTOR
            * SQRT2
        )
        voltages.append(line_voltage)

        for ch in range(4, 8):
            currents[ch].append(_denoise(adc_port[0].read_adc(ch), vref_reading))

    voltage_rms = max(voltages) / SQRT2
    rms_currents = [_rms_current(currents[i], CURRENT_CONV_FACTORS[i]) for i in range(NUM_PORTS)]
    powers = [abs(_avg_power(voltages, currents[i], POWER_CAL_FACTORS[i])) for i in range(NUM_PORTS)]

    adc_repo.insert_port_measures(datetime.now(), rms_currents, voltage_rms, powers)
