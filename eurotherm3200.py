"""

Based on https://github.com/SarathM1/modbus.git

"""

import minimalmodbus


class Eurotherm3200(minimalmodbus.Instrument):
    """Instrument class for Eurotherm 3200 process controller.     
    Communicates via Modbus RTU protocol (via RS232),
    using the *MinimalModbus* Python module."""

    def __init__(self, portname, subordinateaddress):
        minimalmodbus.Instrument.__init__(self, portname, subordinateaddress)

    # Get cell value

    def get_cell_val(self, cell_num: str) -> str:
        """Retrieve the value stored in the memory cell.
        :param cell_num: cell number
        :return: request from microcontroller
        """
        try:
            return self.read_register(int(cell_num), 1) * 10
        except minimalmodbus.NoResponseError:
            return None
        except Exception as error:
            return f'Exception occurred: {error}'

    # Set cell value
    def set_cell_value(self, cell_num: str, value: str):
        """Assign the new value to the memory cell
        :param cell_num: cell number
        :param value: new cell value
        :return: request from microcontroller
        """
        try:
            self.write_register(int(cell_num), int(value) / 10, 1)
            return 'Ok'
        except minimalmodbus.NoResponseError:
            return None
        except Exception as error:
            return f'Exception occurred: {error}'

    # Process value (current temperature)
    def get_pv(self):
        """Return the process value (PV)- current furnace temperature."""
        try:
            return self.read_register(1, 1)
        except minimalmodbus.NoResponseError:
            return None
        except Exception as error:
            return f'Exception occurred: {error}'

    def get_sp(self):
        """Return the current step setpoint (SP)."""
        try:
            return self.read_register(2, 1)
        except minimalmodbus.NoResponseError:
            return None
        except Exception as error:
            return f'Exception occurred: {error}'

    # Setpoint rate
    def get_sprate(self):
        """Return the setpoint rate."""
        try:
            return self.read_register(35, 1)
        except minimalmodbus.NoResponseError:
            return None
        except Exception as error:
            return f'Exception occurred: {error}'

    # Output value
    def get_wop(self):
        """Return the  actual working set point
        (calculated by the controller according to the set point rate)."""
        try:
            return self.read_register(4, 1)
        except minimalmodbus.NoResponseError:
            return None
        except Exception as error:
            return f'Exception occurred: {error}'

    # Read furnace data for furnace monitoring
    def read_furnace_data(self):
        return f'PV={self.get_pv()};SP={self.get_sp()};SPrate={self.get_sprate()};WOp={self.get_wop()}'
