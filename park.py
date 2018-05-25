#!/usr/bin/python
#
# Park script for INDI Telescope Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys
from socket import *
from config import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER, GPIO.OUT)

GPIO.output(POWER, GPIO.LOW)

s = socket(AF_INET, SOCK_STREAM) 
s.connect(('localhost', 5555)) 
s.send('1') 
s.close()



#coordinates = open('/tmp/indi-status', 'w')
#coordinates.truncate()
#coordinates.write('1 0 90')
#coordinates.close()

sys.exit(0)
