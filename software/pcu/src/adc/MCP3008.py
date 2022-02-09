import Adafruit_GPIO.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time

import math
import threading
from spidev import SpiDev


class MCP3008:
    def init(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read_adc(self, channel=0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()


# class MCP3008(object):
#     """Class to represent an Adafruit MCP3008 analog to digital converter.
#     """
#     def __init__(self, clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
#         self._spi = None
#         # Handle hardware SPI
#         if spi is not None:
#             self._spi = spi
#         elif clk is not None and cs is not None and miso is not None and mosi is not None:
#             # Default to platform GPIO if not provided.
#             if gpio is None:
#                 gpio = GPIO.get_platform_gpio()
#             self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
#         else:
#             raise ValueError('Must specify either spi for for hardware SPI or clk, cs, miso, and mosi for software SPI!')
#         self._spi.set_clock_hz(3600000)
#         self._spi.set_mode(0)
#         self._spi.set_bit_order(SPI.MSBFIRST)
#
#     def read_adc(self, adc_number):
#         """Read the current value of the specified ADC channel (0-7).  The values
#         can range from 0 to 1023 (10-bits).
#         """
#         assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
#         # Build a single channel read command.
#         # For example channel zero = 0b11000000
#         command = 0b11 << 6                  # Start bit, single channel read
#         command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
#         # Note the bottom 3 bits of command are 0, this is to account for the
#         # extra clock to do the conversion, and the low null bit returned at
#         # the start of the response.
#         resp = self._spi.transfer([command, 0x0, 0x0])
#         # Parse out the 10 bits of response data and return it.
#         result = (resp[0] & 0x01) << 9
#         result |= (resp[1] & 0xFF) << 1
#         result |= (resp[2] & 0x80) >> 7
#         return result & 0x3FF
#
#     def read_adc_difference(self, differential):
#         """Read the difference between two channels.  Differential should be a
#         value of:
#           - 0: Return channel 0 minus channel 1
#           - 1: Return channel 1 minus channel 0
#           - 2: Return channel 2 minus channel 3
#           - 3: Return channel 3 minus channel 2
#           - 4: Return channel 4 minus channel 5
#           - 5: Return channel 5 minus channel 4
#           - 6: Return channel 6 minus channel 7
#           - 7: Return channel 7 minus channel 6
#         """
#         assert 0 <= differential <= 7, 'Differential number must be a value of 0-7!'
#         # Build a difference channel read command.
#         command = 0b10 << 6  # Start bit, differential read
#         command |= (differential & 0x07) << 3  # Channel number (in 3 bits)
#         # Note the bottom 3 bits of command are 0, this is to account for the
#         # extra clock to do the conversion, and the low null bit returned at
#         # the start of the response.
#         resp = self._spi.transfer([command, 0x0, 0x0])
#         # Parse out the 10 bits of response data and return it.
#         result = (resp[0] & 0x01) << 9
#         result |= (resp[1] & 0xFF) << 1
#         result |= (resp[2] & 0x80) >> 7
#         return result & 0x3FF
# class MCP3008(object):
#     """Class to represent an Adafruit MCP3008 analog to digital converter.
#     """
#     def __init__(self, clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
#         self._spi = None
#         # Handle hardware SPI
#         if spi is not None:
#             self._spi = spi
#         elif clk is not None and cs is not None and miso is not None and mosi is not None:
#             # Default to platform GPIO if not provided.
#             if gpio is None:
#                 gpio = GPIO.get_platform_gpio()
#             self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
#         else:
#             raise ValueError('Must specify either spi for for hardware SPI or clk, cs, miso, and mosi for software SPI!')
#         self._spi.set_clock_hz(3600000)
#         self._spi.set_mode(0)
#         self._spi.set_bit_order(SPI.MSBFIRST)
#
#     def read_adc(self, adc_number):
#         """Read the current value of the specified ADC channel (0-7).  The values
#         can range from 0 to 1023 (10-bits).
#         """
#         assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
#         # Build a single channel read command.
#         # For example channel zero = 0b11000000
#         command = 0b11 << 6                  # Start bit, single channel read
#         command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
#         # Note the bottom 3 bits of command are 0, this is to account for the
#         # extra clock to do the conversion, and the low null bit returned at
#         # the start of the response.
#         resp = self._spi.transfer([command, 0x0, 0x0])
#         # Parse out the 10 bits of response data and return it.
#         result = (resp[0] & 0x01) << 9
#         result |= (resp[1] & 0xFF) << 1
#         result |= (resp[2] & 0x80) >> 7
#         return result & 0x3FF
#
#     def read_adc_difference(self, differential):
#         """Read the difference between two channels.  Differential should be a
#         value of:
#           - 0: Return channel 0 minus channel 1
#           - 1: Return channel 1 minus channel 0
#           - 2: Return channel 2 minus channel 3
#           - 3: Return channel 3 minus channel 2
#           - 4: Return channel 4 minus channel 5
#           - 5: Return channel 5 minus channel 4
#           - 6: Return channel 6 minus channel 7
#           - 7: Return channel 7 minus channel 6
#         """
#         assert 0 <= differential <= 7, 'Differential number must be a value of 0-7!'
#         # Build a difference channel read command.
#         command = 0b10 << 6  # Start bit, differential read
#         command |= (differential & 0x07) << 3  # Channel number (in 3 bits)
#         # Note the bottom 3 bits of command are 0, this is to account for the
#         # extra clock to do the conversion, and the low null bit returned at
#         # the start of the response.
#         resp = self._spi.transfer([command, 0x0, 0x0])
#         # Parse out the 10 bits of response data and return it.
#         result = (resp[0] & 0x01) << 9
#         result |= (resp[1] & 0xFF) << 1
#         result |= (resp[2] & 0x80) >> 7
#         return result & 0x3FF

def ADC_setup():
    SPI_PORT   = 0
    SPI_DEVICE_0 = 0
    SPI_DEVICE_1 = 1
    mcp0 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_0))
    mcp1 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_1))
    adc_port = [mcp0, mcp1]
    return adc_port


def read_test(v_inst_moy, I_inst_moy, adc_port):

    currents_num = [0] * 8
    voltage_num = [0] * 2
    power_inst = [0] * 8

    while(1):
        start_time = time.time()
        voltage_num[0] = (adc_port[1].read_adc(0))/1024 * 5.3
        currents_num[0] = ((((((adc_port[0].read_adc(0))/1024 * 5.3)-2.65)/110)*30)/0.053)/1.41
        currents_num[1] = (((adc_port[0].read_adc(1))/1024 * 5.3)/110)*30/0.053
        currents_num[2] = (((adc_port[0].read_adc(2))/1024 * 5.3)/110)*30/0.053
        currents_num[3] = (((adc_port[0].read_adc(3))/1024 * 5.3)/110)*30/0.053

        voltage_num[1] = (adc_port[1].read_adc(0)) / 1024 * 5.3
        currents_num[4] = (((adc_port[0].read_adc(4))/1024 * 5.3)-2.65)/115
        currents_num[5] = (((adc_port[0].read_adc(5))/1024 * 5.3)-2.65)/115
        currents_num[6] = (((adc_port[0].read_adc(6))/1024 * 5.3)-2.65)/115
        currents_num[7] = (((adc_port[0].read_adc(7))/1024 * 5.3)-2.65)/115

        power_inst = [voltage_num[0]*currents_num[0], voltage_num[0]*currents_num[1], voltage_num[0]*currents_num[2],
                      voltage_num[0]*currents_num[3], voltage_num[0]*currents_num[4], voltage_num[0]*currents_num[5],
                      voltage_num[0]*currents_num[6], voltage_num[0]*currents_num[7]]


        power = voltage_num[0]*currents_num[0]
        # print("--- %s seconds ---" % (time.time() - start_time))

        # print('Voltage | {0:>4} | {1:>4} |'.format(*voltage_num))
        # print('Courant | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*currents_num))
        # print('Puissan | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*power_inst))
        print(currents_num[0])

def read_value(v_inst_moy, I_inst_moy, adc_port):

    longueur_Echantillon = 50
    currents_num = [0] * longueur_Echantillon
    voltage_num = [0] * longueur_Echantillon

    while(1):
        start_time = time.time()
        for i in range(longueur_Echantillon):
            voltage_num[i] = (adc_port[1].read_adc(0))
        v_inst_moy[0] = (((max(voltage_num)) / 2)/1024)*5.3

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(0))
        I_inst_moy[0] = (((max(voltage_num) - min(voltage_num)) / 2))

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(1))
        I_inst_moy[1] =(((max(voltage_num) - min(voltage_num)) / 2)/1024)

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(2))
        I_inst_moy[2] = (((max(voltage_num) - min(voltage_num)) / 2)/1024)

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(3))
        I_inst_moy[3] = (((max(voltage_num) - min(voltage_num)) / 2)/1024)

        for i in range(longueur_Echantillon):
            voltage_num[i] = (adc_port[1].read_adc(0))
        v_inst_moy[1] = (((max(voltage_num) - min(voltage_num)) / 2)/1024)*5.3

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(4))
        I_inst_moy[4] = (((max(voltage_num) - min(voltage_num)) / 2)/1024)

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(5))
        I_inst_moy[5] = (((max(voltage_num) - min(voltage_num)) / 2)/1024)

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(6))
        I_inst_moy[6] = (((max(voltage_num) - min(voltage_num)) / 2)/1024)

        for i in range(longueur_Echantillon):
            currents_num[i] = (adc_port[0].read_adc(7))
        I_inst_moy[7] = (max(currents_num) - min(currents_num)) / 2

        print("--- %s seconds ---" % (time.time() - start_time))

        print('ADC 0 | {0:>4} | {1:>4} |'.format(*v_inst_moy))
        print('ADC 0 | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*I_inst_moy))


#
# def calculate_value(I_inst_moy, v_inst_moy, P_inst_moy):
#
#     while(1):
#





def main():
    longueur_Echantillon = 200
    #adc_port = ADC_setup()

    test = MCP3008
    while(1):
        blabla = test.read_adc(self, 0)
        print(blabla)


    I_inst_moy = [0] * 8
    v_inst_moy = [0] * 2

    adc_thread_read = threading.Thread(target=read_test, args=(v_inst_moy, I_inst_moy, adc_port))
    #calculate_thread = threading.Thread(target=calculate_value, args=(I_inst_moy, V_inst_moy, P_inst_moy))

    #adc_thread_read.start()
    #calculate_thread.start()

    # while((len(plot_Value)<=500)):
    #     lock = 0
    #
    # print("DEBUT !!!")
    # print("--- %s seconds ---" % (time.time() - start_time[0]))
    # for i in range(500):
    #     print(plot_Value[i])
    #
    # print("FIN!!!")



    # test_current_stack = queue.Queue()
    # for i in range(500):
    #     test_current_stack.put(i)
    #     if test_current_stack.full() == True:
    #         print("TERMINADO")
    # print(test_current_stack.qsize())
    ready_val = 0




main()






# start_time = time.time()
# while (1):
#     # Read all the ADC channel values in a list.
#     values0 = [0] * 8
#     values1 = [0] * 8
#
#     for i in range(8):
#         values0[i] = mcp0.read_adc(i)
#     values1[i] = mcp1.read_adc(i)
#
#     # Print the ADC values.
#     print(values0)
#     print(values1)
#    # print('ADC 0 | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values0))
#    # print('ADC 1 | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values1))
#     # print("---------------------------------------------------------------")
#     counter +=1
#     print(counter)
#     print("--- %s seconds ---" % (time.time() - start_time))
