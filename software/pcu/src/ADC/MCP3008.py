import Adafruit_GPIO.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
import threading


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
        self._spi.set_clock_hz(500000)
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

def ADC_setup():
    SPI_PORT   = 0
    SPI_DEVICE_0 = 0
    SPI_DEVICE_1 = 1
    mcp0 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_0))
    mcp1 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_1))
    adc_port = [mcp0, mcp1]
    return adc_port



def read_value(currents, voltage, adc_port, plot_Value,start_time):
    toggle = 1
    while(1):
        for i in range(8):
            currents.append(adc_port[0].read_adc(i))
        voltage.append(adc_port[1].read_adc(0))
        if toggle == 1:
            start_time[0] = time.time()
            toggle = 0
        plot_Value.append(voltage[-1])



def calculate_value(currents, voltage):
    instantPower = [0]*8
    start_time = time.time()
    counter = 0
    while(1):
        if len(voltage) >= 1 and len(currents) >= 8:
            voltage_val = (voltage.pop(0) / 1024) * 5.3
            for i in range(8):
                instantPower[i] = ((currents.pop(0) / 1024 * 15) * voltage_val)


            #print("Consommation: {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format(instantPower[0], instantPower[1] ,instantPower[2], instantPower[3],
            #                                               instantPower[4],instantPower[5], instantPower[6], instantPower[7]))

       # print("--- %s seconds ---" % (time.time() - start_time))


def main():
    adc_port = ADC_setup()

    currents_num = [0] * 8
    voltage_num = [0]
    plot_Value = [0]
    start_time = [0]

    start_time[0] = time.time()
    for j in range(10000):
        for i in range(8):
            currents_num.append(adc_port[0].read_adc(i))
        voltage_num.append(adc_port[1].read_adc(0))
    print("--- %s seconds ---" % (time.time() - start_time[0]))
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    for i in range(6000,10000,1):
        print(voltage_num[i])






    #adc_thread_read = threading.Thread(target=read_value, args=(currents_num, voltage_num, adc_port, plot_Value, start_time))
    #calculate_thread = threading.Thread(target=calculate_value, args=(currents_num, voltage_num))

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