import threading
import gene as geneObj
from processData import *
import csv
import scipy.io;
from scipy import mat;
from numpy.linalg import svd
import numpy as np
import math as m
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

#update SMTP settings
fromEmail='kirangilvaz@gmail.com'
smtpServer='mail.rpi.edu'
smtpUsername='gilvak'
smtpPassword='*****'
smtpPort='587'

#update these values
outputDirectory='C:/Users/Kiran/Documents/NetBeansProjects/plot/web/'
downloadDirectory='C:/wamp/www/geneticanalysis/gene/downloads/'
plotUrl='http://24.92.59.145:8084/plot/index.html'

#thread to process data
class ProcessData(threading.Thread):
        def __init__(self,fileName,outputFileName,email):
                self.fileName=fileName
		self.outputFileName=outputFileName
		self.email=email
		threading.Thread.__init__(self)
        def run(self):
                if self.fileName !='':
			print "Started processing"
			matrix=geneObj.processThis(self.fileName,self.outputFileName)
			geneObj.generateOutput(matrix,self.fileName)
			sendMail(fromEmail,self.email,'Genetic Data',str(geneObj.euclideanDistance(matrix)),self.fileName)
			print "Processing completed"


#sends email to user
def sendMail(send_from,send_to, subject, text, fileName):

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach( MIMEText('Hello, \nYour plot is ready at '+plotUrl+'?data='+fileName+'.json'+'\nWe have also sent you a static 2d and 3d plot attached with this email.\n\nEuclidean distances are as follows,\n') )
	msg.attach(MIMEText(text))
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(outputDirectory+fileName+'_2d.png',"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(outputDirectory+fileName+'_2d.png'))
        msg.attach(part)
	
	part = MIMEBase('application', "octet-stream")
        part.set_payload( open(outputDirectory+fileName+'_3d.png',"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(outputDirectory+fileName+'_3d.png'))
        msg.attach(part)


        smtp = smtplib.SMTP(smtpServer,smtpPort)
        smtp.starttls()
        smtp.login(smtpUsername,smtpPassword)

        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
#handles uploaded file
def handle_uploaded_file(fileObj,email):
	fileName=email.replace(' ','').replace('@','').replace('.','')
	outputFileName=fileName+"_"+str(fileObj.name)
	filePath=downloadDirectory+outputFileName
	with open(filePath, 'w+') as destination:
        	for chunk in fileObj.chunks():
                	destination.write(chunk)
	ProcessData(fileName,outputFileName,email).start()





if __name__=="__main__":
	sendMail('kirangilvaz@gmail.com','kirangilvaz@gmail.com','hey','helloii#####','kirangmailcom')
	#ProcessData('hello').start()
