from threading import Thread
import time
import serial
import serial.tools.list_ports
import re

class UARTHandler(Thread):
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
            print("[USB THREAD] Start connecting to USB port...")
            try:
                self.usb = serial.Serial(self.USB_port, baudrate= 9600)
                break
            except ValueError:
                print("[USB THREAD]  Something goes wrong...")
                time.sleep(1)
            except:
                print("[USB THREAD]  No port detected...")
                time.sleep(1)
        print("[USB THREAD] Connected to USB port successfully.")
        #main loop
        while self.running:
            if(self.debug):
                print("[USB THREAD] Listening...")
            try:
                if(self.debug):
                    print("[USB THREAD] Reading data...")
                res = self.usb.read()
                buttonState = int.from_bytes(res,byteorder='big')
                self.parameters.button = buttonState
                if(self.debug):
                    print("[USB THREAD] Button: " + str(self.parameters.button))    
            except:
                print("[USB THREAD]  Except error!")
            time.sleep(0.2)

    def findDevice(self):
        while self.usb_detected == False:
            ports = list(serial.tools.list_ports.grep('/dev/'))
            regexp = re.compile(r'UART')
            for port in ports:
                print("[USB THREAD] Scanning USB Ports")
                if regexp.search(str(port)):
                    print('[USB THREAD] USB module: ' + str(port.product) + " detected on port: " + str(port.device))
                    self.USB_port = port.device
                    self.usb_detected = True
                    break
                else:
                    print("[USB THREAD] Can't find USB USB device")
            time.sleep(0.5)
            print("[USB THREAD] Searching USB...")