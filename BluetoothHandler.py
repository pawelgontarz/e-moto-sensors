from threading import Thread
import time
import serial
import serial.tools.list_ports
import re
import threading

class BluetoothHandler(Thread):
    def __init__(self, parameters, debug):
        super().__init__()
        self.lat = 0
        self.lon = 0
        self.USB_port = ""
        self.usb_detected = False
        self.running = True
        self.debug = debug
        self.parameters = parameters

    def run(self):
        #detecting USB device
        self.findDevice()
        # connect with device
        while True:
            print("[BLUETOOTH THREAD] Start connecting to USB port...")
            try:
                self.usb = serial.Serial(self.USB_port, baudrate= 9600)
                break
            except ValueError:
                print("[BLUETOOTH THREAD] Something goes wrong...")
                time.sleep(1)
            except:
                print("[BLUETOOTH THREAD] No port detected...")
                time.sleep(1)
        print("[BLUETOOTH THREAD] Connected to Bluetooth USB port successfully.")
        #main loop
        while self.running:
            try:
                if self.debug == True:
                    print("[BLUETOOTH THREAD] Reading data...")
                data = self.usb.read()
                bluetoothMsg = int.from_bytes(data,byteorder='big')
                if(bluetoothMsg != 4 and bluetoothMsg != 5 and bluetoothMsg != 6):
                    self.parameters.bluetoothData = bluetoothMsg
                if self.debug == True:
                    if(bluetoothMsg != 4 and bluetoothMsg != 5 and bluetoothMsg != 6):
                        print("[BLUETOOTH THREAD] Bluetooth: " + str(self.parameters.bluetoothData)) 
            except:
                print("[BLUETOOTH THREAD] Reading data ERROR!")
            time.sleep(0.2)

    def writeData(self):
        while True:
            try:
                print("[BLUETOOTH THREAD] Writing stream!")
                self.usb.write("50;".encode())
            except:
                print("[BLUETOOTH THREAD] Writing stream ERROR!")
            time.sleep(0.5)

    def readData(self):
        while True:
            try:
                print("[BLUETOOTH THREAD] Reading data...")
                data = self.usb.read()
                bluetoothMsg = int.from_bytes(data,byteorder='big')
                print(bluetoothMsg)
            except:
                print("[BLUETOOTH THREAD] Reading data ERROR!")
            time.sleep(0.5)

    def findDevice(self):
        while self.usb_detected == False:
            ports = list(serial.tools.list_ports.grep('/dev/'))
            regexp = re.compile(r'BLUETOOTH')
            for port in ports:
                if regexp.search(str(port)):
                    print('[BLUETOOTH THREAD] Bluetooth USB module: ' + str(port.product) + " detected on port: " + str(port.device))
                    self.USB_port = port.device
                    self.usb_detected = True
                    break
                else:
                    print("[BLUETOOTH THREAD] Can't find Bluetooth USB device")
            time.sleep(2)
            print("[BLUETOOTH THREAD] Searching USB...")