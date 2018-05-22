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

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
time.sleep(0.01)

GPIO.output(18, GPIO.LOW)

s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.connect(('localhost', 5555)) # nawiazanie polaczenia
s.send('5 0 -1') #odbior danych (max 1024 bajow)
s.close()



sys.exit(0)
