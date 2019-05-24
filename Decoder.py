# CAN MESSEGES DECODER

class DECODERS:
    @staticmethod
    def battery_voltage_overall_parameters(data):
        min_cell_voltage = data[0] // 100 + 2
        max_cell_voltage = data[1] // 100 + 2
        average_cell_voltage = data[2] // 100 + 2
        total_cell_voltage = hex(data[5])[2:] + hex(data[6])[2:] + hex(data[3])[2:] + hex(data[4])[2:]
        decoded_data = {
            'min_cell_voltage':min_cell_voltage,
            'max_cell_voltage':max_cell_voltage,
            'average_cell_voltage':average_cell_voltage,
            'total_cell_voltage':total_cell_voltage
        }
        
        return decoded_data

    @staticmethod
    def cell_module_temperature_overall_parameters(data):
        min_cell_module_temp = data[0] - 100
        max_cell_module_temp = data[1] - 100
        average_cell_module_temp = data[2] - 100
        decoded_data = {
            'min_cell_module_temp': min_cell_module_temp,
            'max_cell_module_temp': max_cell_module_temp,
            'average_cell_module_temp': average_cell_module_temp
        }
        print(decoded_data)
        return decoded_data

    @staticmethod
    def cell_temperature_overall_parameters(data):
        min_cell_temp = data[0] - 100
        max_cell_temp = data[1] - 100
        average_cell_temp = data[2] - 100
        decoded_data = {
            'min_cell_temp': min_cell_temp,
            'max_cell_temp': max_cell_temp,
            'average_cell_temp': average_cell_temp
        }
        print(decoded_data)
        return decoded_data

    @staticmethod
    def state_of_charge_parameters(data):
        battery_current = (hex(data[0])[2:] + hex(data[1])[2:]) // 10
        estimated_charge = (hex(data[2])[2:] + hex(data[3])[2:]) // 10
        estimated_state_of_charge = data[6] 
        decoded_data = {
            'battery_current': battery_current,
            'estimated_charge': estimated_charge,
            'estimated_state_of_charge': estimated_state_of_charge
        }
        print(decoded_data)
        return decoded_data

    @staticmethod
    def energy_parameters(data):
        estimated_consumption = hex(data[0])[2:] + hex(data[1])[2:]
        estimated_energy = (hex(data[2])[2:] + hex(data[3])[2:]) // 100
        estimated_distance_left = (hex(data[4])[2:] + hex(data[5])[2:]) // 10
        distance_traveled = (hex(data[6])[2:] + hex(data[7])[2:]) // 10
        decoded_data = {
            'estimated_consumption': estimated_consumption,
            'estimated_energy': estimated_energy,
            'estimated_distance_left': estimated_distance_left,
            'distance_traveled': distance_traveled
        }
        print(decoded_data)
        return decoded_data

