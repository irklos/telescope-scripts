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
from config import *
GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER, GPIO.OUT)

GPIO.output(POWER, GPIO.HIGH)

s = socket(AF_INET, SOCK_STREAM) 
s.connect(('localhost', 5555)) 
s.send('0') 
s.close()


#coordinates = open('/tmp/indi-status', 'w')
#coordinates.truncate()
#coordinates.write('0 0 90')
#coordinates.close()

sys.exit(0)

