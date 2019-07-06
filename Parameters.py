# MOTO PARAMETERSS CLASS
class Parameters:
    def __init__(self):
        #<-----------------------GPS PARAMETERS---------------------------->
        #speed
        self.speed = 0
        #position (default = AGH)
        self.lat = 50.066240
        self.lon = 19.918478
        #<----------------------------------------------------------------->

        #<-----------------------BATTERY PARAMETERS------------------------>
        #battery_voltage_overall_parameters
        self.min_cell_voltage = 0
        self.max_cell_voltage = 0
        self.average_cell_voltage = 0
        self.total_cell_voltage = 0 #<------------self.battery_voltage = 0
        #cell_module_temperature_overall_parameters
        self.min_cell_module_temp = 0
        self.max_cell_module_temp = 0
        self.average_cell_module_temp = 0 
        #cell_temperature_overall_parameters
        self.min_cell_temp = 0
        self.max_cell_temp = 0
        self.average_cell_temp = 38 #<------------self.battery_temp = 38
        #state_of_charge_parameters
        self.battery_current = 0 #<------------self.battery_current = 0
        self.estimated_charge = 0
        self.estimated_state_of_charge = 89 #<------------self.estimated_state_of_charge = 89
        #energy_parameters
        self.estimated_consumption = 0
        self.estimated_energy = 0
        self.estimated_distance_left = 112 #<------------self.distance_left = 112
        self.distance_traveled = 0
        #<----------------------------------------------------------------->

        #<-----------------------ELECTRIC PARAMETERS----------------------->
        #button
        self.button = 0 # 1 -> eco, 2->normal, 3->dynamic, 4-> mainWindow, 5-> navigation
        self.engine_current = 0
        self.engine_temp = 48
        #<----------------------------------------------------------------->

        #<-----------------------SMART PARAMETERS-------------------------->
        #button
        self.bluetoothData = 2 # 1-> start_simulation, 2-> stop_simulation, 3-> SOS, 4-> ECO, 5-> NORMAL, 6-> DYNAMIC, 7-> main, 8-> nawigation, 9->lightON, 10->lightOFF, 11->hornON, 12->hornOFF
        #<----------------------------------------------------------------->