from threading import Thread
from Decoder import DECODERS
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
import time
import serial
import serial.tools.list_ports
import re

class CAN_Data_Handler(Thread):
    def __init__(self, parameters, debug):
        super().__init__()
        self.USB_port = ""
        self.bitRate = 250000
        self.can_detected = False
        self.running = True
        self.debug = debug
        self.parameters = parameters

    def run(self):
        #detecting USB device
        self.findDevice()
        # connect with device
        while self.running:
            print("[CAN THREAD] Connecting to USBTin port...")
            try:
                usbtin = USBtin()
                usbtin.connect(self.USB_port)
                usbtin.add_message_listener(self.log_data)
                usbtin.open_can_channel(self.bitRate, USBtin.ACTIVE)
                break
            except:
                print("[CAN THREAD] Something goes wrong...")
                time.sleep(1)
        print("[CAN THREAD] Connected to USBTin port successfully.")

    def findDevice(self):
        while self.can_detected == False:
            ports = list(serial.tools.list_ports.grep('/dev/ttyACM*'))
            regexp = re.compile(r'CAN')
            for port in ports:
                print("[CAN THREAD] Scanning USB Ports")
                if regexp.search(str(port)):
                    print('[CAN THREAD] CAN module: ' + str(port.product) + " detected on port: " + str(port.device))
                    self.USB_port = port.device
                    self.can_detected = True
                    break
                else:
                    print("[CAN THREAD] Can't find CAN USB device")
            time.sleep(0.5)
            print("[CAN THREAD] Searching CAN...")

    def log_data(self,msg):
        try:
            idx = hex(msg.mid)
            data = msg.get_data()
            self.general_decoder(idx, data)
        except:
            print('Messages queue is EMPTY!')
   
    def general_decoder(self,idx, data):
        if len(data) < 8:
            print('len(data) < 8')
            return {}
        elif idx == '0x19b50001': #battery_voltage_overall_parameters
            decoded_data = DECODERS.battery_voltage_overall_parameters(data, self.debug)
            self.parameters.min_cell_voltage = decoded_data['min_cell_voltage']
            self.parameters.max_cell_voltage = decoded_data['max_cell_voltage']
            self.parameters.average_cell_voltage = decoded_data['average_cell_voltage']
            self.parameters.total_cell_voltage = decoded_data['total_cell_voltage']
        elif idx == '0x19b50002': #cell_module_temperature_overall_parameters
            decoded_data = DECODERS.cell_module_temperature_overall_parameters(data, self.debug)
            self.parameters.min_cell_module_temp = decoded_data['min_cell_module_temp']
            self.parameters.max_cell_module_temp = decoded_data['max_cell_module_temp']
            self.parameters.average_cell_module_temp = decoded_data['average_cell_module_temp']        
        elif idx == '0x19b50008': #cell_temperature_overall_parameters
            decoded_data = DECODERS.cell_temperature_overall_parameters(data, self.debug)
            self.parameters.min_cell_temp = decoded_data['min_cell_temp']
            self.parameters.max_cell_temp = decoded_data['max_cell_temp']
            self.parameters.average_cell_temp = decoded_data['average_cell_temp']
        elif idx == '0x19b50500': #state_of_charge_parameters
            decoded_data = DECODERS.state_of_charge_parameters(data, self.debug)
            self.parameters.battery_current = decoded_data['battery_current']
            self.parameters.estimated_charge = decoded_data['estimated_charge']
            self.parameters.estimated_state_of_charge = decoded_data['estimated_state_of_charge']       
        elif idx == '0x19b50600': #energy_parameters
            decoded_data = DECODERS.energy_parameters(data, self.debug)
            self.parameters.estimated_consumption = decoded_data['estimated_consumption']
            self.parameters.estimated_energy = decoded_data['estimated_energy']
            self.parameters.estimated_distance_left = decoded_data['estimated_distance_left']
            self.parameters.distance_traveled = decoded_data['distance_traveled']


    