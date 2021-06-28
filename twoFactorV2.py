import sys

# for the UI
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget

# for OTP generation
import math
import random

# for the email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime


# function to generate OTP
def generateOTP():
    # Declare a string variable
    # which stores all alpha-numeric characters
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    varlen = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * varlen)]

    return (OTP)



def getSenderEmailDetails():
    # Using readlines()
    file1 = open('config/actualPasswords.txt', 'r')
    email = file1.readline()
    password = file1.readline()

    credential = [email, password]
    return credential


def getDefaultMessage():
    # Using readlines()
    file1 = open('txtFiles/message.txt', 'r')
    Lines = file1.readlines()

    mailMessage = ""

    # Strips the newline character
    for line in Lines:
        mailMessage += line
        #includes newline Character

    return mailMessage

def sendEmail(senderEmail, senderPassword, newMessage, receipientEmail):
    print(senderEmail)
    print(senderPassword)
    print(newMessage)
    print(receipientEmail)

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = senderEmail
    message['To'] = receipientEmail
    message['Subject'] = 'OTP from two-factor-auth'  # The subject line

    # The body and the attachments for the mail
    message.attach(MIMEText(newMessage, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(senderEmail, senderPassword)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(senderEmail, receipientEmail, text)
    session.quit()
    print('Mail Sent')
    return

def showDialog(windowText, windowTitle):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(windowText)
    msgBox.setWindowTitle(windowTitle)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.buttonClicked.connect(msgButtonClick)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('OK clicked')


def msgButtonClick(i):
    print("Button clicked is:", i.text())

def on_click():
    # check if password is correct
    if (pwField.text() == "password"):
        # Generate a OTP
        global newOTP
        newOTP = generateOTP()

        # get sender email details
        credentials = getSenderEmailDetails()

        # generate custom email
        mailMessage = getDefaultMessage()
        newMessage = mailMessage.format(PERSON_NAME=nameLine.text(), OTP=newOTP)
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # newMessage += "\n" + "Message sent at " + current_time + "\n"

        # Send off an email
        sendEmail(credentials[0], credentials[1], newMessage, recipientEmailLine.text())

        print('email sent')

        global window2
        window2 = Window2()

        # open secondary window
        window2.show()

        # close window and open next window

    else:
        showDialog("Please enter correct password!", "Wrong Password!")




# show the window
def Window3():
    window3 = QWidget()
    window3.setGeometry(100, 100, 400, 100)
    window3.move(400, 200)
    window3.setWindowTitle('two-factor login')

    # create the form layout
    layout2 = QFormLayout()

    greeting = QLabel()
    greeting.setText('Hello, ' + nameLine.text() + "!")
    layout2.addRow(greeting)

    window3.setLayout(layout2)

    return window3


def submit():
    if (OTPField.text() == newOTP):
        global window3
        window3 = Window3()

        # open secondary window
        window3.show()
    else:
        showDialog("Please enter correct OTP", "OTP Invalid")

######### First login normally
# create new instance of app
app = QApplication(sys.argv)

# make new QWidget window
window = QWidget()
window.setGeometry(100, 100, 400, 100)
window.move(400, 200)
window.setWindowTitle('two-factor login')

# create the form layout
layout = QFormLayout()

nameLine = QLineEdit()
layout.addRow('Name:', nameLine)

pwField = QLineEdit()
pwField.setEchoMode(QLineEdit.Password)
layout.addRow('Password:', pwField)

recipientEmailLine = QLineEdit()
layout.addRow('Email:', recipientEmailLine)

button = QPushButton('Generate OTP')
button.setToolTip('Click to generate otp')
button.move(100, 70)
button.clicked.connect(on_click)

layout.addRow(button)

# apply the created layout to thw QWidget
window.setLayout(layout)

# show the first window
window.show()

######### Second login via email

# show the window
def Window2():
    window2 = QWidget()
    window2.setGeometry(100, 100, 400, 100)
    window2.move(400, 200)
    window2.setWindowTitle('two-factor login')

    # create the form layout
    layout2 = QFormLayout()

    greeting = QLabel()
    greeting.setText('Hello, ' + nameLine.text() + "!")
    layout2.addRow(greeting)

    global OTPField

    OTPField = QLineEdit()
    layout2.addRow('Enter OTP:', OTPField)

    recipientEmailLine = QLineEdit()

    btn2 = QPushButton('Login')
    btn2.setToolTip('Click to login')
    btn2.move(100, 70)
    btn2.clicked.connect(submit)

    layout2.addRow(btn2)

    window2.setLayout(layout2)

    return window2

# close the program
sys.exit(app.exec_())