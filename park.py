#!/usr/bin/python
#
# Park script for INDI Telescope Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys
from socket import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

GPIO.output(24, GPIO.LOW)

s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.connect(('localhost', 5555)) # nawiazanie polaczenia
s.send('1') #odbior danych (max 1024 bajow)
s.close()



#coordinates = open('/tmp/indi-status', 'w')
#coordinates.truncate()
#coordinates.write('1 0 90')
#coordinates.close()

sys.exit(0)
