# Server for Eurotherm3200 thermo controller monitoring by Zabbix.

*The project base on [MinimalModbus](https://github.com/SarathM1/modbus.git) and adapted for Eurotherm 3200 series thermo controller.*

One of the challenges in high-temperature electrochemistry is maintaining strict 
control over the furnace. In our laboratory, we employ various types of furnaces 
for different purposes, ranging from sample annealing to conducting electrochemical 
measurements. The most significant issue we encounter is power interruptions. In such 
instances, obtaining comprehensive information is crucial for making informed 
decisions regarding the preservation of samples and laboratory equipment.

The furnace control unit consist of a [Eurotherm 3216 controller](https://www.eurotherm.com/products/temperature-controllers/single-loop-temperature-controllers/3200-temperature-process-controller/) 
and [Raspberry Pi 4 single-board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) 
connected via a USB-RS232 adapter.

## Installation

1. Install [minimalmodbus](https://minimalmodbus.readthedocs.io/en/stable/installation.html)
2. Install Zabbix Agent: ```sudo apt install zabbix-agent2```
3. Configure file */etc/zabbixzabbix_agent2.conf*
4. Clone current repository to your home folder (*/home/pi*)
5. To automatically run the termocontroller server you can copy file [start-eurotherm.service]
(systemctl/start-eurotherm.service) to ```/etc/systemd/system folder``` 
(*my Raspberry Pi work with Debian 1:6.1.73.*)
6. start *start-eurotherm.service*:</br> ```sudo systemctl enable start-eurotherm.service && sudo systemctl start start-eurotherm.service``` 
7. Check ```sudo systemctl status start-eurotherm.service```
8. Copy files from folder *Zabbix* to ```/etc/zabbix/zabbix_agent2.d``` and give permissions for file *script_4_zabbix.py*.
9. Restart service ```systemctl restart zabbix-agent2``` and check service status ```systemctl status zabbix-agent2```


## Controller part Description
In *main.py*, the server loop begins, allowing it to accept incoming connections. </br>
The match-case construction filters the commands from the inlet client based on keywords:

 - ```Exit``` or ```Quit``` to externally stop the program;
 - ```Status``` should simply respond with *Ok* if the program is still alive;
 - ```Get:<cell number>``` will scan a thermo controller memory *cell* and send
a cell value in response;
 - ```Set:<cell number>:<new value>``` will change the value in a thermo controller 
memory *cell*
 - ```Read``` make reading of parameters sequence and send back it's list separated by ```;```.

All interactions with the furnace controller are described in *eurotherm3200.py*</br>
The *SocketServer* class raises a server on port 9000. 

## Zabbix part

*Zabbix* folder: 
 - UserParameter config (*eurotherm_user_parameter.conf*) 
 - python script (*script_4_zabbix.py*)
