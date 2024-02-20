"""

Based on https://github.com/SarathM1/modbus.git

"""

import minimalmodbus


class Eurotherm3200( minimalmodbus.Instrument ):
    """Instrument class for Eurotherm 3200 process controller.     
    Communicates via Modbus RTU protocol (via RS232), using the *MinimalModbus* Python module.    

    """
    
    def __init__(self, portname, subordinateaddress):
        minimalmodbus.Instrument.__init__(self, portname, subordinateaddress)
    
    ## Process value
    
    def get_pv(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(1, 1)
    
    def get_sp(self):
        """Return the (working) setpoint (SP) for loop1."""
        return self.read_register(2, 1)
    
    ## Setpoint rate
    
    def get_sprate(self):
        """Return the setpoint (SP) change rate for loop1."""
        return self.read_register(35, 1)   
    
    def set_sprate(self, value):
        """Set the setpoint (SP) change rate for loop1.
        
        Args:
            value (float): Setpoint change rate (most often in degrees/minute)

        """
        self.write_register(35, value, 1)  
    
    