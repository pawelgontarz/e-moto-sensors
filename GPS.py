from threading import Thread
import time
import serial


class GPSHandler(Thread):
    def __init__(self, parameters):
        super().__init__()
        self.lat = 0
        self.lon = 0
        self.running = True
        self.parameters = parameters

    def run(self):
        while True:
            print("[GPS] Start connecting to GPS port...")
            try:
                self.gps = serial.Serial("/dev/ttyACM0", baudrate= 115200)
                break
            except ValueError:
                print("Something goes wrong...")
                time.sleep(1)
            except:
                print("No port detected...")
                time.sleep(1)
        print("[GPS] Connected to GPS port succesfully!")

        while self.running:
            dataLine = self.gps.readline()
            self.getCoordinates(dataLine)
            self.getSpeed(dataLine)
    
    def getCoordinates(self,dataLine):
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
                print(str(latitude) + ' ' + str(longitude))
            except:
                print("[GPS THREAD] Lat/lon error!")

    def getSpeed(self,dataLine):
        data = dataLine.decode().split(",")
        if data[0] == "$GPVTG": 
            try:
                speed = round(float(data[7]))
                print("Speed: " + str(speed))
                #moto_parameters.speed = speed + random.randint(1,40)
                self.parameters.speed = speed
            except:
                print("[GPS THREAD] Speed error!")

