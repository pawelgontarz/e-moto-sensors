from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
from Parameters import Parameters
from Decoder import DECODERS
import time
import socket

file=open("/home/parallels/Desktop/log.txt","w")
file.write("Starting script!")
file.close()

# CREATE PARAMETERS OBJECT
moto_parameters = Parameters

def log_data(msg):
    try:
        idx = hex(msg.mid)
        data = msg.get_data()
        general_decoder(idx, data)
    except:
        print('Messages queue is EMPTY!')
   
def general_decoder(idx, data):
    if len(data) < 8:
        print('len(data) < 8')
        return {}
    elif idx == '0x19b50001': #battery_voltage_overall_parameters
        decoded_data = DECODERS.battery_voltage_overall_parameters(data)
    elif idx == '0x19b50002': #cell_module_temperature_overall_parameters
        decoded_data = DECODERS.cell_module_temperature_overall_parameters(data)
    elif idx == '0x19b50008': #cell_temperature_overall_parameters
        decoded_data = DECODERS.cell_temperature_overall_parameters(data)
    elif idx == '0x19b50500': #state_of_charge_parameters
        decoded_data = DECODERS.state_of_charge_parameters(data)
    elif idx == '0x19b50600': #energy_parameters
        decoded_data = DECODERS.energy_parameters(data)

while True:
    print("[USBTin] Connecting to USBTin port...")
    try:
        usbtin = USBtin()
        usbtin.connect("/dev/ttyACM0")
        usbtin.add_message_listener(log_data)
        usbtin.open_can_channel(250000, USBtin.ACTIVE)
        break
    except ValueError:
        print("Something goes wrong...")
        time.sleep(1)
    except:
        print("No port detected...")
        time.sleep(1)

print("[USBTin] Connected to USBTin port!")

file=open("/home/parallels/Desktop/log1.txt","w")
file.write("Connected to USBTin CAN Converter!")
file.close()

#CREATE SERVER
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10001)
print('[Server] Starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

#while(True):
    #print("tick")
    #print("Dziala?: " + str(moto_parameters.total_cell_voltage))
    #usbtin.send(CANMessage(0x100, "\x11"))
    #sleep(1)

while True:
    # Wait for a connection
    print('[Server] Waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('[Server] Connection from: ', client_address)
        speed = 0
        current = 0
        voltage = 0
        soc = 10       
        while True:           
            data = connection.recv(1024)
            moto_parameters.total_cell_voltage = voltage
            #print("total_cell_voltage value: " + str(voltage))
            voltage = voltage + 2
            soc = soc + 1

            if voltage >= 160:
                voltage = 0
                               
            if soc > 100:
                soc = 0

            print(data.decode("utf-8"))
            if data:
                if(data.decode("utf-8")=="speed"):
                    connection.sendall(str(speed).encode())
                elif(data.decode("utf-8")=="current"):
                    connection.sendall(str(current).encode())
                elif(data.decode("utf-8")=="voltage"):
                    connection.sendall(str(voltage).encode())
                elif(data.decode("utf-8")=="soc"):
                    connection.sendall(str(soc).encode())                    
                else:
                    #connection.sendall(b'No request!')
                    pass
            else:
                print('[Server] No more data from: ', client_address)
                break
            time.sleep(0.01)  
            print("total_cell_voltage value: " + str(moto_parameters.total_cell_voltage))      
    finally:
        connection.close()

