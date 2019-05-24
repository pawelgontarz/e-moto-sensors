# MOTO PARAMETERSS CLASS
class Parameters:
    def __init__(self):
        #<-----------------------BATTERY PARAMETERS------------------------>
        #battery_voltage_overall_parameters
        self.min_cell_voltage = 0
        self.max_cell_voltage = 0
        self.average_cell_voltage = 0
        self.total_cell_voltage = 0
        #cell_module_temperature_overall_parameters
        self.min_cell_module_temp = 0
        self.max_cell_module_temp = 0
        self.average_cell_module_temp = 0
        #cell_temperature_overall_parameters
        self.min_cell_temp = 0
        self.max_cell_temp = 0
        self.average_cell_temp = 0
        #state_of_charge_parameters
        self.battery_current = 0
        self.estimated_charge = 0
        self.estimated_state_of_charge = 0
        #energy_parameters
        self.estimated_consumption = 0
        self.estimated_energy = 0
        self.estimated_distance_left = 0
        self.distance_traveled = 0
        #<----------------------------------------------------------------->