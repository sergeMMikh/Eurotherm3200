#!/usr/bin/env python3

import minimalmodbus
from eurotherm3200 import Eurotherm3200

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.clear_buffers_before_each_transaction = True
reg_1 = instrument.read_register(1, 0)


if __name__ == '__main__':
    print('main')

    instrument = Eurotherm3200('/dev/ttyUSB0', 1)
    instrument.serial.baudrate = 9600

    print(f'PV = {instrument.get_pv() * 10}') 
    print(f'SP = {instrument.get_sp() * 10}') 
    print(f'SPrate = {instrument.get_sprate()}') 

