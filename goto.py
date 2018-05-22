#!/usr/bin/python
#
# Goto script for INDI Telescope Scripting Gateway
#
# Arguments: RA Dec
# Exit code: 0 for success, 1 for failure
#

import sys
from socket import *



script, ra, dec = sys.argv

s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.connect(('localhost', 5555)) # nawiazanie polaczenia
s.send('2 ' + ra + ' ' + dec) #odbior danych (max 1024 bajow)
s.close()

#coordinates = open('/tmp/indi-status', 'w')
#coordinates.truncate()
#coordinates.write('0 ' + ra + ' ' + dec)
#coordinates.close()

sys.exit(0)