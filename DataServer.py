from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
import time
import socket

# MOTO PARAMETERSS CLASS
class Parameters:
    def __init__(self,total_voltage):
        self.total_voltage = total_voltage

# CREATE PARAMETERS OBJECT
moto_parameters = Parameters(10)

def log_data(can_message):
        try:
            idx = hex(can_message.mid)
            data = can_message.get_data()
            decoded_data = general_decoder(idx, data)
        except:
            print('Messages queue is EMPTY!')
   
def general_decoder(idx, data):
    if len(data) < 8:
        return {}
    elif idx == '0x19b50001':
        min_cell_voltage = data[0] // 100 + 2
        max_cell_voltage = data[1] // 100 + 2
        avg_cell_voltage = data[2] // 100 + 2
        total_cell_voltage = hex(data[5])[2:] + hex(data[6])[2:] + hex(data[3])[2:] + hex(data[4])[2:]
        total_cell_voltage = int(total_cell_voltage, 16) // 100
        #print("min cell voltage: ",min_cell_voltage)
        #print("max cell voltage: ",max_cell_voltage)
        #print("avg cell voltage: ",avg_cell_voltage)
        #print("total cell voltage: ",total_cell_voltage)
        #return DECODERS.battery_voltage_overall_parameters(data)
        moto_parameters.total_voltage = total_cell_voltage
    elif idx == '0x19b50002':
        #print("ID: " + idx)
        pass
    elif idx == '0x19b50500':
        #print("ID: "+idx)
        pass

  
time.sleep(8) 
usbtin = USBtin()
usbtin.connect("/dev/ttyACM0")
usbtin.add_message_listener(log_data)
usbtin.open_can_channel(250000, USBtin.ACTIVE)

#CREATE SERVER
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10001)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

#while(True):
    #print("tick")
    #print("Dziala?: " + str(moto_parameters.total_voltage))
    #usbtin.send(CANMessage(0x100, "\x11"))
    #sleep(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('connection from', client_address)
        speed = 0
        current = 0
        voltage = 0
        soc = 10       
        while True:           
            data = connection.recv(1024)
            speed = moto_parameters.total_voltage
            print("Voltage value: " + str(speed))
            soc = soc + 1
            if speed >= 160:
                speed = 0
                               
            if soc > 100:
                soc = 0

            print(data.decode("utf-8"))

            if data:
                #print('sending data back to the client')

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
                print('no more data from', client_address)
                break
            time.sleep(0.1)        
    finally:
        connection.close()

