# Server for Eurotherm3200 thermo controller monitoring by Zabbix.

*The project base on [MinimalModbus](https://github.com/SarathM1/modbus.git) and adapted for Eurotherm 3200 series thermo controller.*

One of the challenges of high temperature electrochemistry is the strict control of the furnace.
In our laboratory we use different kinds of furnaces for different tasks: 
from sample annealing to making electrochemistry measurements. 
The biggest problem is an electricity power interrupt.
In this case, it is very important to obtain all the information in order to make the right decision 
about saving samples and laboratory equipment.

The furnace control unit consist of [Eurotherm 3216 controller](https://www.eurotherm.com/products/temperature-controllers/single-loop-temperature-controllers/3200-temperature-process-controller/) 
and [Raspberry Pi 4 single-board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) 
connected by USB-RS232 adapter.

## Installation

1. Install [minimalmodbus](https://minimalmodbus.readthedocs.io/en/stable/installation.html)
2. Install [Zabbix Agent](https://www.zabbix.com/download_agents)
3. Clone current repository to your home folder (*/home/pi*)
4. To automatically run the termocontroller server you can copy file [start-eurotherm.service](systemctl/start-eurotherm.service)
to ```/etc/systemd/system folder``` (*my Raspberry Pi work with Debian 1:6.1.73.*)
5. start *start-eurotherm.service*:</br> ```sudo systemctl enable start-eurotherm.service && sudo systemctl start start-eurotherm.service``` 
6. Check ```sudo systemctl status start-eurotherm.service```
7. Copy files from folder *Zabbix* to ```/etc/zabbix/zabbix_agent2.d```.

## Controller part Description
In *main.py* starts the server loop of accepting inlet connections. </br>
match-case construction filters inlet client commands by keywords:

 - ```Exit``` or ```Quit``` for externally stop the program;
 - ```Status``` should simply respond *Ok* if program is still alive;
 - ```Get:<cell number>``` will scan a thermo controller memory *cell* and send a cell value as respond;
 - ```Set:<cell number>:<new value>``` will change value in a thermo controller memory *cell*
 - ```Read``` make reading of parameters sequence and send back it's list separated by ```;```.

All interactions with furnace controller are described in *eurotherm3200.py*</br>
Class SocketServer rises server on port 9000. 

## Zabbix part

In *Zabbix* folder are: 
 - UserParameter config (*eurotherm_user_parameter.conf*) 
 - python script (*script_4_zabbix.py*)
