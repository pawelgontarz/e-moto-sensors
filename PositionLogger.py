from threading import Thread
import time
import smtplib

class PositionLogger(Thread):
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.fromaddr="emoto.smartSystems@gmail.com"
        self.toaddr="gontarzpawe@gmail.com"
        self.password = "smartsystems2019"
        self.subject = "E-Moto PIMPEK Parameters Logger"
        self.timestamp = 600#per 10min

    def run(self):
        while True:
            self.position_logger()
            time.sleep(self.timestamp)

    def position_logger(self):
        msg = "Motorcycle position: " + "\n\n" + "LATTITUDE: " + str(self.parameters.lat) + "\n" + "LONGITUDE: " + str(self.parameters.lon) + "\n \n" + "**Created by E-MOTO SMART SYSTEMS**"
        self.send_email("E-Moto PIMPEK Position logger",msg,self.fromaddr,self.password,self.toaddr)

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