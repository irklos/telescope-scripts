#!/usr/bin/python
#
# Abort script for INDI Telescope Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys
from socket import *


s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.connect(('localhost', 5555)) # nawiazanie polaczenia
s.send('6') #odbior danych (max 1024 bajow)
s.close()


sys.exit(0)
