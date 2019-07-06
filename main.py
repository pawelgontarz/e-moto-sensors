from Parameters import Parameters
from GPS import GPSHandler
from CANHandler import CAN_Data_Handler
from UartHandler import UARTHandler
from Decoder import DECODERS
from Mailer import ParametersController
from PositionLogger import PositionLogger
from BluetoothHandler import BluetoothHandler
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
from time import sleep
import socket
import threading
import serial
import random

debug = False

# CREATE PARAMETERS OBJECT
moto_parameters = Parameters()

# CAN USBTin CONNECTION
can = CAN_Data_Handler(moto_parameters, debug)
can.start()

# GPS CONNECTION
gps = GPSHandler(moto_parameters, debug)
gps.start()

#UART CONNECTION
uartHandler = UARTHandler(moto_parameters, debug)
uartHandler.start()

#BlUETOOTH CONNECTION
bluetoothHandler = BluetoothHandler(moto_parameters, debug)
bluetoothHandler.start()

# GPS CONNECTION
gps = GPSHandler(moto_parameters, debug)
gps.start()

# ParametersController
parametersController = ParametersController(moto_parameters)
parametersController.start()

# Position Logger
positionLogger = PositionLogger(moto_parameters)
positionLogger.start()

#CREATE SERVER
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10001)
print('[Server] Starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
    # Wait for a connection
    print('[Server] Waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print ('[Server] Connection from: ', client_address)  
        while True:           
            data = connection.recv(1024)
            #print("[Server] Request: " + data.decode("utf-8"))
            if data:
                if(data.decode("utf-8")=="min_cell_voltage"): #battery_voltage_overall_parameters
                    connection.sendall(str(moto_parameters.min_cell_voltage).encode())
                elif(data.decode("utf-8")=="max_cell_voltage"):
                    connection.sendall(str(moto_parameters.max_cell_voltage).encode())
                elif(data.decode("utf-8")=="average_cell_voltage"):
                    connection.sendall(str(moto_parameters.average_cell_voltage).encode())
                elif(data.decode("utf-8")=="battery_voltage"): #<----------battery_voltage_parameters
                    connection.sendall(str(moto_parameters.total_cell_voltage).encode())
                elif(data.decode("utf-8")=="min_cell_module_temp"): #cell_module_temperature_overall_parameters
                    connection.sendall(str(moto_parameters.min_cell_module_temp).encode())
                elif(data.decode("utf-8")=="max_cell_module_temp"): 
                    connection.sendall(str(moto_parameters.max_cell_module_temp).encode()) 
                elif(data.decode("utf-8")=="average_cell_module_temp"): 
                    connection.sendall(str(moto_parameters.average_cell_module_temp).encode())     
                elif(data.decode("utf-8")=="min_cell_temp"): #cell_temperature_overall_parameters
                    connection.sendall(str(moto_parameters.min_cell_temp).encode())
                elif(data.decode("utf-8")=="max_cell_temp"): 
                    connection.sendall(str(moto_parameters.max_cell_temp).encode()) 
                elif(data.decode("utf-8")=="battery_temp"): #<----------battery_temp
                    connection.sendall(str(moto_parameters.average_cell_temp).encode())  
                elif(data.decode("utf-8")=="battery_current"): #<----------battery_current
                    connection.sendall(str(moto_parameters.battery_current).encode())
                elif(data.decode("utf-8")=="estimated_charge"): 
                    connection.sendall(str(moto_parameters.estimated_charge).encode()) 
                elif(data.decode("utf-8")=="estimated_state_of_charge"): #<----------estimated_state_of_charge
                    connection.sendall(str(moto_parameters.estimated_state_of_charge).encode())   
                elif(data.decode("utf-8")=="estimated_consumption"): #energy_parameters
                    connection.sendall(str(moto_parameters.estimated_consumption).encode())
                elif(data.decode("utf-8")=="estimated_energy"): 
                    connection.sendall(str(moto_parameters.estimated_energy).encode()) 
                elif(data.decode("utf-8")=="distance_left"): #distance_left
                    connection.sendall(str(moto_parameters.estimated_distance_left).encode())   
                elif(data.decode("utf-8")=="distance_traveled"): 
                    connection.sendall(str(moto_parameters.distance_traveled).encode())  
                elif(data.decode("utf-8")=="engine_current"): #<----------engine_current
                    connection.sendall(str(moto_parameters.engine_current).encode())
                elif(data.decode("utf-8")=="engine_temp"): #<----------engine_temperature
                    connection.sendall(str(moto_parameters.engine_temp).encode())
                elif(data.decode("utf-8")=="speed"): #gps_parameters
                    connection.sendall(str(moto_parameters.speed).encode())    
                elif(data.decode("utf-8")=="lat"):
                    connection.sendall(str(moto_parameters.lat).encode())  
                    print("Moto LAT: " + str(moto_parameters.lat))  
                elif(data.decode("utf-8")=="lon"): 
                    connection.sendall(str(moto_parameters.lon).encode())     
                    print("Moto LON: " + str(moto_parameters.lon))  
                elif(data.decode("utf-8")=="button"): #button data
                    connection.sendall(str(moto_parameters.button).encode())
                elif(data.decode("utf-8")=="bluetooth"): #bluetooth data
                    connection.sendall(str(moto_parameters.bluetoothData).encode())        
                else:
                    print("[Server] No request from client.")
            else:
                print('[Server] No more data from: ', client_address)
                break
            sleep(0.015)      
    finally:
        connection.close()

