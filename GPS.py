from threading import Thread
import time
import serial
import serial.tools.list_ports
import re

class GPSHandler(Thread):
    def __init__(self, parameters):
        super().__init__()
        self.lat = 0
        self.lon = 0
        self.USB_port = ""
        self.running = True
        self.debug = False
        self.parameters = parameters

    def run(self):
        #detecting USB device
        self.findDevice()
        # connect with device
        while True:
            print("[GPS THREAD] Start connecting to GPS port...")
            try:
                self.gps = serial.Serial(self.USB_port, baudrate= 115200)
                break
            except ValueError:
                print("Something goes wrong...")
                time.sleep(1)
            except:
                print("No port detected...")
                time.sleep(1)
        print("[GPS THREAD] Connected to GPS port successfully.")
        #main loop
        while self.running:
            dataLine = self.gps.readline()
            self.getCoordinates(dataLine,self.debug)
            self.getSpeed(dataLine,self.debug)
    
    def getCoordinates(self,dataLine, debug):
        data = dataLine.decode().split(",")
        if data[0] == '$GPRMC':
            try:
                latitudeDegree = float(data[3][0:2])
                latitudeMin = float(data[3][2:]) / 60
                latitudeMark = data[4]
                if latitudeMark == "N":
                    latitude = 1*(latitudeDegree + latitudeMin)
                elif latitudeMark[3] == 'S':
                    latitude = -1*(latitudeDegree + latitudeMin)
                longitudeDegree = float(data[5][0:3])
                longitudeMin = float(data[5][3:]) / 60
                longitudeMark = data[6]
                if longitudeMark == "E":
                    longitude = 1*(longitudeDegree + longitudeMin)
                elif longitudeMark == "W":
                    longitude = -1*(longitudeDegree + longitudeMin)
                self.parameters.lat = latitude
                self.parameters.lon = longitude
                if debug == True:
                    print(str(latitude) + ' ' + str(longitude))
            except:
                print("[GPS THREAD] Lat/lon error!")

    def getSpeed(self,dataLine, debug):
        data = dataLine.decode().split(",")
        if data[0] == "$GPVTG": 
            try:
                speed = round(float(data[7]))
                #moto_parameters.speed = speed + random.randint(1,40)
                self.parameters.speed = speed
                if debug == True:
                    print("Speed: " + str(speed))
            except:
                print("[GPS THREAD] Speed error!")

    def findDevice(self):
        ports = list(serial.tools.list_ports.grep('/dev/ttyACM*'))
        regexp = re.compile(r'GPS')
        for port in ports:
            while True:
                print("[GPS THREAD] Scanning USB Ports")
                if regexp.search(str(port)):
                    print('[GPS THREAD] GPS module: ' + str(port.product) + " detected on port: " + str(port.device))
                    self.USB_port = port.device
                    break
                else:
                    print("[GPS THREAD] Can't find GPS USB device")
                time.sleep(0.5)