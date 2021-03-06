#!/usr/bin/python
#
# Move north script for INDI Telescope Scripting Gateway
#
# Arguments: slew rate (0-3)
# Exit code: 0 for success, 1 for failure
#

import sys
import RPi.GPIO as GPIO
import time
from socket import *
from config import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(RAP, GPIO.OUT)
GPIO.output(RAP, GPIO.HIGH)
time.sleep(0.1)

GPIO.output(RAP, GPIO.LOW)

s = socket(AF_INET, SOCK_STREAM) 
s.connect(('localhost', 5555)) 
s.send('5 1 0') 
s.close()



sys.exit(0)
