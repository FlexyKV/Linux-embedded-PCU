import Adafruit_GPIO.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
import threading


#Classe MCP3008 permettant d'instancier un objet ADC
class MCP3008(object):
    """Class to represent an Adafruit MCP3008 analog to digital converter.
    """
    def __init__(self, clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
        self._spi = None
        # Handle hardware SPI
        if spi is not None:
            self._spi = spi
        elif clk is not None and cs is not None and miso is not None and mosi is not None:
            # Default to platform GPIO if not provided.
            if gpio is None:
                gpio = GPIO.get_platform_gpio()
            self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
        else:
            raise ValueError('Must specify either spi for for hardware SPI or clk, cs, miso, and mosi for software SPI!')
        self._spi.set_clock_hz(3600000)
        self._spi.set_mode(0)
        self._spi.set_bit_order(SPI.MSBFIRST)

    def read_adc(self, adc_number):
        """Read the current value of the specified ADC channel (0-7).  The values
        can range from 0 to 1023 (10-bits).
        """
        assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
        # Build a single channel read command.
        # For example channel zero = 0b11000000
        command = 0b11 << 6                  # Start bit, single channel read
        command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.transfer([command, 0x0, 0x0])
        # Parse out the 10 bits of response data and return it.
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF

    def read_adc_difference(self, differential):
        """Read the difference between two channels.  Differential should be a
        value of:
          - 0: Return channel 0 minus channel 1
          - 1: Return channel 1 minus channel 0
          - 2: Return channel 2 minus channel 3
          - 3: Return channel 3 minus channel 2
          - 4: Return channel 4 minus channel 5
          - 5: Return channel 5 minus channel 4
          - 6: Return channel 6 minus channel 7
          - 7: Return channel 7 minus channel 6
        """
        assert 0 <= differential <= 7, 'Differential number must be a value of 0-7!'
        # Build a difference channel read command.
        command = 0b10 << 6  # Start bit, differential read
        command |= (differential & 0x07) << 3  # Channel number (in 3 bits)
        # Note the bottom 3 bits of command are 0, this is to account for the
        # extra clock to do the conversion, and the low null bit returned at
        # the start of the response.
        resp = self._spi.transfer([command, 0x0, 0x0])
        # Parse out the 10 bits of response data and return it.
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF

#Fonction permettant d'initialiser le port SPI et les ADC
def ADC_setup():
    SPI_PORT   = 0
    SPI_DEVICE_0 = 0
    SPI_DEVICE_1 = 1
    mcp0 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_0))
    mcp1 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_1))
    adc_port = [mcp0, mcp1]
    return adc_port


#Fonction permettant de faire la lecture des ADC ainsis que les calcules de conversion
def calculate_read(voltage_num, currents_num, power_inst, adc_port, flag):

    def conv_factor_current(adc_data):
        voltage_ref = (adc_port[1].read_adc(1)/1023 * 5.20)

        retVal = ((((((adc_data)/1023 * 5.2)-voltage_ref)/110)*30)/0.053)/1.41
        return retVal

    while(1):
        if flag[0] == 0:
            start_time = time.time()
            voltage_num[0] = (adc_port[1].read_adc(0))/1023 * 5.3

            currents_num[0] = conv_factor_current(adc_port[0].read_adc(0))
            currents_num[1] = conv_factor_current(adc_port[0].read_adc(1))
            currents_num[2] = conv_factor_current(adc_port[0].read_adc(2))
            currents_num[3] = conv_factor_current(adc_port[0].read_adc(3))
            currents_num[4] = conv_factor_current(adc_port[0].read_adc(4))
            currents_num[5] = conv_factor_current(adc_port[0].read_adc(5))
            currents_num[6] = conv_factor_current(adc_port[0].read_adc(6))
            currents_num[7] = conv_factor_current(adc_port[0].read_adc(7))

            power_inst[0] = voltage_num[0]*currents_num[0]
            power_inst[1] = voltage_num[0]*currents_num[1]
            power_inst[2] = voltage_num[0]*currents_num[2]
            power_inst[3] = voltage_num[0]*currents_num[3]
            power_inst[4] = voltage_num[0]*currents_num[4]
            power_inst[5] = voltage_num[0]*currents_num[5]
            power_inst[6] = voltage_num[0]*currents_num[6]
            power_inst[7] = voltage_num[0]*currents_num[7]
            flag[0] = 1


        # print("--- %s seconds ---" % (time.time() - start_time))
        # print('Voltage | {0:.4f} |'.format(*voltage_num))
        # print('Courant | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*currents_num))
        # print('Puissan | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*power_inst))


#Fonction permettant de faire différent debug selon le niveau d'abtraction (branchement, lecture, encodage, etc..)
def debug_adc_read(v_inst_moy, I_inst_moy, adc_port):
    currents_num = [0.0] * 8
    voltage_num = [0.0] * 2
    power_inst = [0] * 8

    while(1):
        start_time = time.time()
        voltage_num[0] = (adc_port[1].read_adc(0))
        currents_num[0] = (adc_port[0].read_adc(0))
        currents_num[1] = (adc_port[0].read_adc(1))
        currents_num[2] = (adc_port[0].read_adc(2))
        currents_num[3] = (adc_port[0].read_adc(3))

        voltage_num[1] = (adc_port[1].read_adc(0))
        currents_num[4] = (adc_port[0].read_adc(4))
        currents_num[5] = (adc_port[0].read_adc(5))
        currents_num[6] = (adc_port[0].read_adc(6))
        currents_num[7] = (adc_port[0].read_adc(7))

        # power = voltage_num[0]*currents_num[0]
        # print("--- %s seconds ---" % (time.time() - start_time))

        # print('Voltage | {0:.4f} | {1:.4f} |'.format(*voltage_num))
        # print('Courant | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*currents_num))
        print(currents_num[0])


    currents_num = [0] * 5000
    voltage_num = [0] * 1000
    power_inst = [0] * 5000
    start_time = time.time()
    data_out = [0]
    counter = 0


    # temp_time = 0
    # while (temp_time <= 0.1):
    #     temp_time = time.time() - start_time
    #     currents_num[counter] = (adc_port[1].read_adc(0)) / 1024 * 5.3
    #     print(currents_num[counter])
    #     counter += 1



    # counter = 0
    # temp_time = 0
    # while(temp_time <=0.1):
    #     temp_time = time.time() - start_time
    #     currents_num[counter] = ((((((adc_port[0].read_adc(0)) / 1024 * 5.3) - 2.65) / 110) * 30) / 0.053) / 1.41
    #
    # min_array = min(len(currents_num), len(voltage_num))
    # print("BELLLLLLO")
    # print(len(currents_num))
    # print(len(voltage_num))
    #
    # for i in range(min_array):
    #     power_inst[i] = voltage_num[i]*currents_num[i]
    #     data_out.append((power_inst[i]))


    # while(1):
    #     temp_time = time.time() - start_time
    #     voltage_num[0] = (adc_port[1].read_adc(0))/1024 * 5.3
    #     currents_num[0] = ((((((adc_port[0].read_adc(0))/1024 * 5.3)-2.65)/110)*30)/0.053)/1.41
    #     currents_num[1] = (((adc_port[0].read_adc(1))/1024 * 5.3)/110)*30/0.053
    #     currents_num[2] = (((adc_port[0].read_adc(2))/1024 * 5.3)/110)*30/0.053
    #     currents_num[3] = ((((((adc_port[0].read_adc(3))/1024 * 5.3)-2.65)/110)*30)/0.053)/1.41
    #
    #     currents_num[4] = (((adc_port[0].read_adc(4))/1024 * 5.3)-2.65)/115
    #     currents_num[5] = (((adc_port[0].read_adc(5))/1024 * 5.3)-2.65)/115
    #     currents_num[6] = (((adc_port[0].read_adc(6))/1024 * 5.3)-2.65)/115
    #     currents_num[7] = (((adc_port[0].read_adc(7))/1024 * 5.3)-2.65)/115
    #
    #     power_inst = [voltage_num[0]*currents_num[0], voltage_num[0]*currents_num[1], voltage_num[0]*currents_num[2],
    #                   voltage_num[0]*currents_num[3], voltage_num[0]*currents_num[4], voltage_num[0]*currents_num[5],
    #                   voltage_num[0]*currents_num[6], voltage_num[0]*currents_num[7]]
    #
    #
    #     # print('Voltage | {0:.4f} | {1:.4f} |'.format(*voltage_num))
    #     # print('Courant | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*currents_num))
    #     # print('Puissan | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*power_inst))
    #     # print("{:.3f}".format(power_inst[0]))
    #     print(power_inst[0])




def adc_print(v_inst_moy,I_inst_moy,P_inst_moy, flag):
    while(1):
        if flag[0] == 1:
            start_time = time.time()
            print('Voltage | {0:.4f} |'.format(*v_inst_moy))
            print('Courant | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*I_inst_moy))
            print('Puissan | {0:.4f} | {1:.4f} | {2:.4f} | {3:.4f} | {4:.4f} | {5:.4f} | {6:.4f} | {7:.4f} |'.format(*P_inst_moy))
            print("--- %s seconds ---" % (time.time() - start_time))
            flag[0] = 0


def get_data_API():
    pass


def main():

    I_inst_moy = [0] * 8
    v_inst_moy = [0] * 2
    P_inst_moy = [0] * 8
    flag = [0]

    adc_port = ADC_setup()

    #test(v_inst_moy, I_inst_moy, adc_port, data_Out)

    calculate_thread = threading.Thread(target=calculate_read, args=(v_inst_moy, I_inst_moy, P_inst_moy, adc_port, flag))
    adc_print_thread = threading.Thread(target=adc_print, args=(v_inst_moy, I_inst_moy, P_inst_moy, flag))

    calculate_thread.start()
    adc_print_thread.start()





main()






