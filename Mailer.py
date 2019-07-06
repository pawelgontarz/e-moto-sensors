from threading import Thread
import time
import smtplib

class ParametersController(Thread):
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.fromaddr="emoto.smartSystems@gmail.com"
        self.toaddr="gontarzpawe@gmail.com"
        self.password = "smartsystems2019"
        self.subject = "E-Moto BOBER Parameters Logger"
        #params limits
        self.battery_temp_limit = 80
        self.battery_voltage_limit = 100

    def run(self):
        while True:
            self.parameters_logger()
            time.sleep(1)

    def parameters_logger(self):
        if(self.parameters.battery_temp >= self.battery_temp_limit or self.parameters.battery_voltage >= self.battery_voltage_limit):
            msg = "Probably one of the parameters exceeeded the critical value. Please check them. \n\n" + "Battery temperature: " + str(self.parameters.battery_temp) + "\n" + "Battery voltage: " + str(self.parameters.battery_voltage) + "\n" + "Engine temperature: " + str(0) + "\n" + "Enginge voltage: " + str(0) + "\n \n" + "Motorcycle position: " + "\n" + "LAT: " + str(self.parameters.lat) + "\n" + "LON: " + str(self.parameters.lon) + "\n \n" + "*E-Moto Smart Systems 2019*"
            self.send_email(self.subject,msg,self.fromaddr,self.password,self.toaddr)
            time.sleep(5)
    
    def position_logger(self):
        while True:
            msg = "Motorcycle position: " + "\n\n" + "LATTITUDE: " + str(self.parameters.lat) + "\n" + "LONGITUDE: " + str(self.parameters.lon) + "\n \n" + "**Created by E-MOTO SMART SYSTEMS**"
            self.send_email("E-Moto BOBER Position logger",msg,self.fromaddr,self.password,self.toaddr)
            time.sleep(5)

    def send_email(self,subject,msg,fromaddr,password,toaddr):
        try:
            server=smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(fromaddr,password)
            message = 'Subject: {}\n\n{}'.format(subject,msg)
            server.sendmail(fromaddr,toaddr,message)
            server.quit()
            print("Succes: Email sent!")
        except:
            print("Email failed to send.")