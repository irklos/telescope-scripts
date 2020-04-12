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
import sys
from socket import *
from config import *


GPIO.setmode(GPIO.BCM)
GPIO.setup(DECP, GPIO.OUT)

GPIO.output(DECP, GPIO.HIGH)
time.sleep(0.01)

GPIO.output(DECP, GPIO.LOW)

s = socket(AF_INET, SOCK_STREAM) 
s.connect(('localhost', 5555)) 
s.send('5 0 1') 
s.close()



sys.exit(0)
