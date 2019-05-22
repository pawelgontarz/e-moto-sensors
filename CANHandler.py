from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
from time import sleep

def log_data(msg):
    print(msg)
    toCehckData = checkData(msg)

class checkData:
    def __init__(self, can_message):
        try:
            self.idx = hex(can_message.mid)
            self.data = can_message.get_data()
            decoded_data = general_decoder(self.idx, self.data)
        except:
            self.logger.log_error('Messages queue is EMPTY!')
        

def general_decoder(idx, data):
    if len(data) < 8:
        return {}
    elif idx == '0x19b50001':
        min_cell_voltage = data[0] / 100 + 2
        max_cell_voltage = data[1] / 100 + 2
        avg_cell_voltage = data[2] / 100 + 2
        total_cell_voltage = hex(data[5])[2:] + hex(data[6])[2:] + hex(data[3])[2:] + hex(data[4])[2:]
        total_cell_voltage = int(total_cell_voltage, 16) / 100
        print("min cell voltage: ",min_cell_voltage)
        print("max cell voltage: ",max_cell_voltage)
        print("avg cell voltage: ",avg_cell_voltage)
        print("total cell voltage: ",total_cell_voltage)
        #return DECODERS.battery_voltage_overall_parameters(data)
    elif idx == '0x19b50002':
        print("2")
        #return DECODERS.cell_module_temperature_overall_parameters(data)
    elif idx == '0x19b50500':
        print("3")

  
usbtin = USBtin()
usbtin.connect("/dev/ttyACM0")
usbtin.add_message_listener(log_data)
usbtin.open_can_channel(250000, USBtin.ACTIVE)

while(True):
    print("tick")
    #usbtin.send(CANMessage(0x100, "\x11"))
    sleep(1)

