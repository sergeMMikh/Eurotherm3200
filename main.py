#!/usr/bin/env python3

import time
import minimalmodbus
from eurotherm3200 import Eurotherm3200
from cls_Server import SocketServer

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.clear_buffers_before_each_transaction = True

if __name__ == '__main__':
    """ Connection via a USB-RS232 adapter """
    instrument = Eurotherm3200('/dev/ttyUSB0', 1)

    """Set COM Port baud rate"""
    instrument.serial.baudrate = 9600

    """Set Keep connection open after each request."""
    instrument.close_port_after_each_call = False  # True- Makes connection safty

    """Open Port 9000 for client connection"""
    server = SocketServer(port=9000)

    recvData = {}

    while True:

        recvData = str(server.recvServerData().decode())

        spl = recvData.split(':')

        print(f'spl: {spl}')

        # External program stop
        if 'Exit' in spl[0] or 'Quit' in spl[0]:
            server.sendServerData('Exit')
            break

        # Check if program is alive
        elif 'Status' in spl[0]:
            server.sendServerData('Ok')

        # Get cell data from furnace controller
        elif 'Get' in spl[0] and len(spl[1]) > 0:
            server.sendServerData(str(instrument.get_cell_val(cell_num=spl[1])))

        # Set a new value to controller memory cell
        elif 'Set' in spl[0] and spl[1] and spl[2]:
            server.sendServerData(str(instrument.set_cell_value(cell_num=spl[1], value=spl[2])))

        # Get the data sequence for furnace conditions monitoring
        elif 'Read' in spl[0]:
            server.sendServerData(str(instrument.read_furnace_data()))
        # Case of unknown message
        else:
            server.sendServerData('Unknown command')

        time.sleep(0.1)

    print('Exiting')
