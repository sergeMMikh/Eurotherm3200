"""

Based on https://github.com/SarathM1/modbus.git

"""

import minimalmodbus


class Eurotherm3200(minimalmodbus.Instrument):
    """Instrument class for Eurotherm 3200 process controller.     
    Communicates via Modbus RTU protocol (via RS232), using the *MinimalModbus* Python module.    

    """

    def __init__(self, portname, subordinateaddress):
        minimalmodbus.Instrument.__init__(self, portname, subordinateaddress)

    # Get cell value

    def get_cell_val(self, cell_num):
        """Return the process value (PV) for loop1."""
        return self.read_register(int(cell_num), 1) * 10

    # Set cell value
    def set_cell_value(self, cell_num, value):
        """Set the setpoint (SP) change rate for loop1.
        
        Args:
            value (float): Setpoint change rate (most often in degrees/minute)

        """
        self.write_register(int(cell_num), int(value) / 10, 1)

    # Process value (current temperature)
    def get_pv(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(1, 1)

    def get_sp(self):
        """Return the (working) setpoint (SP) for loop1."""
        return self.read_register(2, 1)

    # Setpoint rate
    def get_sprate(self):
        """Return the setpoint (SP) change rate for loop1."""
        return self.read_register(35, 1)

    # Output value
    def get_wop(self):
        """Return the setpoint (SP) change rate for loop1."""
        return self.read_register(4, 1)

    # Setpoint rate.
    def set_sprate(self, value):
        """Set the setpoint (SP) change rate for loop1.
        
        Args:
            value (float): Setpoint change rate (most often in degrees/minute)

        """
        self.write_register(35, value, 1)

    # Read furnace data for furnace monitoring
    def read_furnace_data(self):
        return f'PV={self.get_pv()};SP={self.get_sp()};SPrate={self.get_sprate()};WOp={self.get_wop()}'
