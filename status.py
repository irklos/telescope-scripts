#!/usr/bin/python
#
# Status script for INDI Telescope Scripting Gateway
#
# Arguments: file name to save current state and coordinates (parked ra dec)
# Exit code: 0 for success, 1 for failure
#

import sys
from socket import *


script, path = sys.argv


s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.connect(('localhost', 5555)) # nawiazanie polaczenia
s.send('3') #odbior danych (max 1024 bajow)
data = s.recv(30)
s.close()

status = open(path, 'w')
status.truncate()
status.write(data)
#status.write(coordinates.readline())
status.close()

sys.exit(0)

