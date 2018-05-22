#!/usr/bin/python
#
# Park script for INDI Telescope Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#


import sys
import RPi.GPIO as GPIO
import time
from socket import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

GPIO.output(24, GPIO.HIGH)

s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.connect(('localhost', 5555)) # nawiazanie polaczenia
s.send('0') #odbior danych (max 1024 bajow)
s.close()


#coordinates = open('/tmp/indi-status', 'w')
#coordinates.truncate()
#coordinates.write('0 0 90')
#coordinates.close()

sys.exit(0)

