from Parameters import Parameters
from GPS import GPSHandler
from CANHandler import CAN_Data_Handler
import time
import socket
import threading
import serial
import random

# CREATE PARAMETERS OBJECT
moto_parameters = Parameters()

# WORKS UNTIL CONNECT WITH USBTin
can = CAN_Data_Handler(moto_parameters)
can.start()

# GPS CONNECTION
gps = GPSHandler(moto_parameters)
#gps.start()

file=open("/home/parallels/Desktop/log1.txt","w")
file.write("Connected to USBTin CAN Converter!")
file.close()

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
                elif(data.decode("utf-8")=="total_cell_voltage"):
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
                elif(data.decode("utf-8")=="average_cell_temp"): 
                    connection.sendall(str(moto_parameters.average_cell_temp).encode())  
                elif(data.decode("utf-8")=="battery_current"): #state_of_charge_parameters
                    connection.sendall(str(moto_parameters.battery_current).encode())
                elif(data.decode("utf-8")=="estimated_charge"): 
                    connection.sendall(str(moto_parameters.estimated_charge).encode()) 
                elif(data.decode("utf-8")=="estimated_state_of_charge"): 
                    connection.sendall(str(moto_parameters.estimated_state_of_charge).encode())   
                elif(data.decode("utf-8")=="estimated_consumption"): #energy_parameters
                    connection.sendall(str(moto_parameters.estimated_consumption).encode())
                elif(data.decode("utf-8")=="estimated_energy"): 
                    connection.sendall(str(moto_parameters.estimated_energy).encode()) 
                elif(data.decode("utf-8")=="estimated_distance_left"): 
                    connection.sendall(str(moto_parameters.estimated_distance_left).encode())   
                elif(data.decode("utf-8")=="distance_traveled"): 
                    connection.sendall(str(moto_parameters.distance_traveled).encode())  
                elif(data.decode("utf-8")=="speed"): #gps_parameters
                    connection.sendall(str(moto_parameters.speed).encode())    
                elif(data.decode("utf-8")=="lat"):
                    connection.sendall(str(moto_parameters.lat).encode())  
                    print("Moto LAT: " + str(moto_parameters.lat))  
                elif(data.decode("utf-8")=="lon"): 
                    connection.sendall(str(moto_parameters.lon).encode())     
                    print("Moto LON: " + str(moto_parameters.lon))         
                else:
                    print("[Server] No request from client.")
            else:
                print('[Server] No more data from: ', client_address)
                break
            time.sleep(0.4)      
    finally:
        connection.close()

