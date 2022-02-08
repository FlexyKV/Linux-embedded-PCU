# myapp.py
import logging
import logging.handlers
import random
import sys
import threading


class loggingSyslog(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        syslog = logging.handlers.SysLogHandler(address=(self.address, self.port))
        logger.addHandler(syslog)

    def logging_valeurs(self):
        #mcp0 = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE_0))
        a = random.randrange(10)
        b = random.randrange(50)
        #threading.Timer(10.0, self.logging_valeurs).start()
        logging.info('Puissance moyenne: %s  Courant:%s ', a, b)
        #logging.info('Puissance moyenne: %s  Courant:%s  ADC0: %s  ADC1: %s', a, b,c,d)


logging1 = loggingSyslog("192.168.1.80",514)
logging1.logging_valeurs()
