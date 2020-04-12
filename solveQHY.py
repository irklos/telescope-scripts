#!/usr/bin/env python


import PyIndi
import time
import sys
import threading
import os
from socket import *

     
class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
    def newDevice(self, d):
        pass
    def newProperty(self, p):
        pass
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        global blobEvent
        print("new BLOB ", bp.name)
        blobEvent.set()
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        pass
    def serverDisconnected(self, code):
        pass
 
# connect the server
indiclient=IndiClient()
indiclient.setServer("localhost",7624)
 
if (not(indiclient.connectServer())):
     print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
     print("  indiserver indi_simulator_telescope indi_simulator_ccd")
     sys.exit(1)
 
 
# Let's take some pictures
ccd="QHY CCD QHY5LII-C-6147d"
device_ccd=indiclient.getDevice(ccd)
while not(device_ccd):
    time.sleep(0.5)
    device_ccd=indiclient.getDevice(ccd)   
 
ccd_connect=device_ccd.getSwitch("CONNECTION")
while not(ccd_connect):
    time.sleep(0.5)
    ccd_connect=device_ccd.getSwitch("CONNECTION")
if not(device_ccd.isConnected()):
    ccd_connect[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
    ccd_connect[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
    indiclient.sendNewSwitch(ccd_connect)
 
ccd_exposure=device_ccd.getNumber("CCD_EXPOSURE")
while not(ccd_exposure):
    time.sleep(0.5)
    ccd_exposure=device_ccd.getNumber("CCD_EXPOSURE")
 
# Ensure the CCD simulator snoops the telescope simulator
# otherwise you may not have a picture of vega
ccd_active_devices=device_ccd.getText("ACTIVE_DEVICES")
while not(ccd_active_devices):
    time.sleep(0.5)
    ccd_active_devices=device_ccd.getText("ACTIVE_DEVICES")
ccd_active_devices[0].text="Telescope Script Gateway"
indiclient.sendNewText(ccd_active_devices)
 
# we should inform the indi server that we want to receive the
# "CCD1" blob from this device
indiclient.setBLOBMode(PyIndi.B_ALSO, ccd, "CCD1")
 
ccd_ccd1=device_ccd.getBLOB("CCD1")
while not(ccd_ccd1):
    time.sleep(0.5)
    ccd_ccd1=device_ccd.getBLOB("CCD1")

os.popen('rm -rf /opt/solve/*')
 
# a list of our exposure times
exposures=[5.0]
 
# we use here the threading.Event facility of Python
# we define an event for newBlob event
blobEvent=threading.Event()
blobEvent.clear()
i=0
ccd_exposure[0].value=exposures[i]
indiclient.sendNewNumber(ccd_exposure)

while (i < len(exposures)):
    # wait for the ith exposure
    blobEvent.wait()
    # we can start immediately the next one
    if (i + 1 < len(exposures)):
        ccd_exposure[0].value=exposures[i+1]
        blobEvent.clear()
        indiclient.sendNewNumber(ccd_exposure)
    # and meanwhile process the received one
    for blob in ccd_ccd1:
        print("name: ", blob.name," size: ", blob.size," format: ", blob.format)
        # pyindi-client adds a getblobdata() method to IBLOB item
        # for accessing the contents of the blob, which is a bytearray in Python
        fits=blob.getblobdata()
	with open("/opt/solve/frame.fits", "wb") as f:
	    f.write(fits)
        print("fits data type: ", type(fits))
        # here you may use astropy.io.fits to access the fits data
    # and perform some computations while the ccd is exposing
    # but this is outside the scope of this tutorial
    i+=1
time.sleep(3)
command = os.popen(' solve-field  --downsample 2 /opt/solve/frame.fits')
lines = command.read().splitlines()
command.close()


for line in lines:
    if '(RA,Dec)' in line:
	s=line
	new = ''
	for letter in s:
	    if not(letter.isalpha()):
		new+=letter
	s = new
	s=s.split(") = (",1)[1]
	ra=s.split(",")[0]
	s=s.split(",")[1]
	dec=s.split(")")[0]
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(('localhost', 5555))
	s.send('4 ' + ra + ' ' + dec)
	s.close()
	break


