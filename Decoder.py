# CAN MESSEGES DECODER

class DECODERS:
    @staticmethod
    def battery_voltage_overall_parameters(data, debug):
        min_cell_voltage = data[0] // 100 + 2
        max_cell_voltage = data[1] // 100 + 2
        average_cell_voltage = data[2] // 100 + 2
        total_cell_voltage = int((hex(data[5])[2:] + hex(data[6])[2:] + hex(data[3])[2:] + hex(data[4])[2:]),16) // 100
        decoded_data = {
            'min_cell_voltage':min_cell_voltage,
            'max_cell_voltage':max_cell_voltage,
            'average_cell_voltage':average_cell_voltage,
            'total_cell_voltage':total_cell_voltage
        }
        if debug:
            print(decoded_data)
        return decoded_data

    @staticmethod
    def cell_module_temperature_overall_parameters(data, debug):
        min_cell_module_temp = data[0] - 100
        max_cell_module_temp = data[1] - 100
        average_cell_module_temp = data[2] - 100
        decoded_data = {
            'min_cell_module_temp': min_cell_module_temp,
            'max_cell_module_temp': max_cell_module_temp,
            'average_cell_module_temp': average_cell_module_temp
        }
        if debug:
            print(decoded_data)
        return decoded_data

    @staticmethod
    def cell_temperature_overall_parameters(data, debug):
        min_cell_temp = data[0] - 100
        max_cell_temp = data[1] - 100
        average_cell_temp = data[2] - 100
        decoded_data = {
            'min_cell_temp': min_cell_temp,
            'max_cell_temp': max_cell_temp,
            'average_cell_temp': average_cell_temp
        }
        if debug:
            print(decoded_data)
        return decoded_data

    @staticmethod
    def state_of_charge_parameters(data, debug):
        battery_current = (65536 - int((hex(data[0])[2:] + hex(data[1])[2:]),16)) // 10
        if(battery_current > 6500):
            battery_current = int((hex(data[0])[2:] + hex(data[1])[2:]),16) // 10
        estimated_charge = int((hex(data[2])[2:] + hex(data[3])[2:]),16) // 10
        estimated_state_of_charge = data[6] 
        decoded_data = {
            'battery_current': battery_current,
            'estimated_charge': estimated_charge,
            'estimated_state_of_charge': estimated_state_of_charge
        }
        if debug:
            print(decoded_data)
        return decoded_data

    @staticmethod
    def energy_parameters(data, debug):
        estimated_consumption = int((hex(data[0])[2:] + hex(data[1])[2:]),16)
        estimated_energy = int((hex(data[2])[2:] + hex(data[3])[2:]),16) // 100
        estimated_distance_left = int((hex(data[4])[2:] + hex(data[5])[2:]),16) // 10 #
        distance_traveled = int((hex(data[6])[2:] + hex(data[7])[2:]),16) // 10
        decoded_data = {
            'estimated_consumption': estimated_consumption,
            'estimated_energy': estimated_energy,
            'estimated_distance_left': estimated_distance_left,
            'distance_traveled': distance_traveled
        }
        if debug:
            print(decoded_data)
        return decoded_data

