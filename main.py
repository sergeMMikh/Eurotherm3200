#!/usr/bin/env python3

import minimalmodbus
from eurotherm3200 import Eurotherm3200
from cls_Server import SocketServer

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.clear_buffers_before_each_transaction = True
reg_1 = instrument.read_register(1, 0)


if __name__ == '__main__':
    print('main')

    instrument = Eurotherm3200('/dev/ttyUSB0', 1)
    instrument.serial.baudrate = 9600
    instrument.close_port_after_each_call = True

    server = SocketServer(port=9000)
    recvData={}
      
    while True:
       
        recvData=str(server.recvServerData())

        print(f'Received data: {recvData}')

        match recvData.split(':'):

            # Exrenal program stop 
            case ["b'Exit'"]|["b'Quit'"]:
                server.sendServerData('Exit')
                break
            
            # Check if program is alive
            case ["b'Status'"]:
                server.sendServerData('Ok')

            # Get cell data from furnace controller
            case ['Get', cell_num]:
                server.sendServerData(str(instrument.get_cell_val(cell_num=cell_num)))

            # Set a new value to controller memory cell
            case ['Set', cell_num, new_value]:
                server.sendServerData(str(instrument.get_cell_val(cell_num=cell_num)))

            # Get the data sequence for furnace conditions monitoring
            case ["b'Read'"]:
                server.sendServerData(str(instrument.read_furnace_data()))

            # Case of unknown message
            case _:
                server.sendServerData('Unknown command')


    print('Exiting')

