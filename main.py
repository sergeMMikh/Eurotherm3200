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
       
        recvData=server.recvServerData()

        print(f'Received data: {recvData}')
        
        if b'Exit' in recvData: break

        elif b'Status' in recvData: 
            server.sendServerData('Ok')
            print('Sended data -> Ok')
            trg_v=0
        
        elif b'Get' in recvData:
            arry = recvData.split(b":")
            if len(arry) >=1:
                cell_num = arry[1].decode()
                server.sendServerData(str(instrument.get_cell_val(cell_num=cell_num)))
            else:
                server.sendServerData('Error')

        elif b'Set' in recvData:
            arry = recvData.split(b":")
            if len(arry) >=2:
                cell_num = arry[1].decode()
                new_value = arry[2].decode()

                instrument.set_cell_value(cell_num=cell_num, value=new_value)

                server.sendServerData(str(instrument.get_cell_val(cell_num=cell_num)))
            else:
                server.sendServerData('Error')

        elif b'Red' in recvData:
            server.sendServerData(str(instrument.read_furnace_data()))

        else:
            server.sendServerData('Error')
        

    print('Exiting')

