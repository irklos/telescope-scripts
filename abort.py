#!/usr/bin/python
#
# Abort script for INDI Telescope Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys
from socket import *


s = socket(AF_INET, SOCK_STREAM) 
s.connect(('localhost', 5555)) 
s.send('6') 
s.close()


sys.exit(0)
