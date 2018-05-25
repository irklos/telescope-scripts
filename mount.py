#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Example of how to run a daemon."""

import time

from daemon import runner
from socket import *
import logging
from threading import Thread
import RPi.GPIO as GPIO

from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz

from config import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(RAP, GPIO.OUT) # W
GPIO.setup(RAN, GPIO.OUT) # E ->
GPIO.setup(DECP, GPIO.OUT) # N
GPIO.setup(DECN, GPIO.OUT) # S ->


class DaemonApp(object):
    """Daemon App."""

    def __init__(self):
        """Initialize Daemon."""
	self.stdin_path = '/dev/null'
#        self.stdout_path = '/dev/tty'
#        self.stderr_path = '/dev/tty'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/tmp/daemon.pid'
	self.log_file = '/tmp/mount.log'
        self.pidfile_timeout = 1
	self.go=0
	self.gra=0
	self.gdec=90
	self.ra=0
	self.dec=90
	self.sra=0
	self.sdec=0
	self.speed=8
	self.mstep=60
	self.alt=52.1344805092
	self.az=0.0331069535695
	self.observing_location=0
	self.flip=1
	
	self.s = socket(AF_INET, SOCK_STREAM) 

    def step(self):
	if self.go==2:
	    if self.sra > 0: 
		GPIO.output(RAP, GPIO.HIGH) 
	    elif self.sra < 0:
		GPIO.output(RAN, GPIO.HIGH) 
	    if self.flip == 1:
		if self.sdec > 0:
		    GPIO.output(DECP, GPIO.HIGH) 
		elif self.sdec <0:
		    GPIO.output(DECN, GPIO.HIGH)
	    if self.flip == 0:
		if self.sdec > 0:
		    GPIO.output(DECN, GPIO.HIGH) 
		elif self.sdec <0:
		    GPIO.output(DECP, GPIO.HIGH)
 
	    time.sleep(self.mstep) # 8x - 30  4x - 60 
	    if self.sra > 0: 
		GPIO.output(RAP, GPIO.LOW) 
		self.ra=self.ra+0.06666
		if self.ra>24 :
		    self.ra=self.ra-24
	    elif self.sra < 0:
		GPIO.output(RAN, GPIO.LOW) 
		self.ra=self.ra-0.06666
		if self.ra<0 :
		    self.ra=self.ra+24
	    if self.flip == 1:     
		if self.sdec > 0: 
		    GPIO.output(DECP, GPIO.LOW)
		    self.dec=self.dec+1
		elif self.sdec <0:
		    GPIO.output(DECN, GPIO.LOW) 
		    self.dec=self.dec-1
	    elif self.flip == 0 :
		if self.sdec > 0: 
		    GPIO.output(DECN, GPIO.LOW)
		    self.dec=self.dec+1
		elif self.sdec <0:
		    GPIO.output(DECP, GPIO.LOW) 
		    self.dec=self.dec-1
	    



    def goto(self):
	

	difra=float(self.gra)-float(self.ra)
	if difra>180 :
	    difra=float(self.gra)-float(self.ra+360)
	elif difra < -180 :
	    difra=float(self.gra)+360-float(self.ra)
 	difdec=float(self.gdec)-float(self.dec)
	rasteps=int(abs(difra)*15) # to degrees
	decsteps=int(abs(difdec))
	difsteps=abs(rasteps-decsteps)
	if rasteps > decsteps:
	    comsteps=decsteps
	else:
	    comsteps=rasteps
	if self.speed==4:
	    logging.debug('Liczba minut (GOTO)  '+str (comsteps+difsteps) )
	if self.speed==8:
	    logging.debug('Liczba minut (GOTO)  '+str ((comsteps+difsteps)/2) )

	if difra > 0:
	    self.sra=1
	elif difra < 0:
	    self.sra=-1

	if difdec > 0:
	    self.sdec=1
	elif difdec < 0:
	    self.sdec=-1
	
	for x in range (0,comsteps):
	    self.step()
	if rasteps > decsteps:
	    self.sdec=0
	else:
	    self.sra=0

	for x in range (0,difsteps):
	    self.step()
	self.sra=0
	self.sdec=0
	self.go=0
	
	logging.debug('GOTO DO END')

    def run(self):
        """Main Daemon Code."""
	fslra=0.000011
	fsldec=0.000166
	self.observing_location = EarthLocation(lat='52.229676', lon='21.012229', height=100*u.m)
	
	if self.speed == 8:
	    self.mstep=30
	    fslra=0.000022
	    fsldec=0.000333
	s = socket(AF_INET, SOCK_STREAM) 
	s.bind(('127.0.0.1', 5555)) #dowiazanie do portu 5555
	s.listen(5)
        logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename=self.log_file,filemode='a')
	park=1
	coord=SkyCoord(ra=self.ra*u.degree, dec=self.dec*u.degree)
        while True:
	    client,addr = s.accept() 
	    data = client.recv(30)
	    if not data: break
	    words = data.split()
	    cmd=int(words[0])
	    if self.go==1:
		self.go=2
		t = Thread(target=self.goto)
	        t.start()
		logging.debug('GOTO DO')
	    if cmd == 0: # unpark
		park=0
	    elif cmd == 1: # park
		observing_time = Time.now()
		coord = SkyCoord(ra=self.ra*u.degree, dec=self.dec*u.degree,frame='icrs', equinox='J2000')
		cord_altaz=coord.transform_to(AltAz(obstime=observing_time, location=self.observing_location))
		self.alt=cord_altaz.alt.deg
		self.az=cord_altaz.az.deg
		park=1

	    elif cmd == 2: # goto 
		self.gra=words[1]
		self.gdec=words[2]
		self.go=1
		logging.debug('GOTO '+str(self.gra)+' '+str(self.gdec))
	    elif cmd == 3: # status
		if park==1:
			observing_time = Time.now()
			newAltAzcoordiantes = SkyCoord(alt = self.alt*u.deg, az = self.az*u.deg, obstime = observing_time, frame = 'altaz',location=self.observing_location)
			logging.debug(str(newAltAzcoordiantes.icrs.ra)+ ' '+ str(newAltAzcoordiantes.icrs.dec) )

			self.ra=newAltAzcoordiantes.icrs.ra.deg
			self.dec=newAltAzcoordiantes.icrs.dec.deg
		client.send(str(park)+' '+str(self.ra) + ' ' + str(self.dec))
#		    logging.debug(str(park)+' '+str(self.ra) + ' ' + str(self.dec))
		    
	    elif cmd == 4: # sync
		self.ra=float(words[1])
		self.dec=float(words[2])
	    elif cmd == 5: # slew
		self.ra=self.ra+fslra*int(words[1])
		self.dec=self.dec+fsldec*int(words[2])
	    elif cmd == 6: # abort
		self.go=0
		GPIO.setmode(GPIO.BCM)
		GPIO.output(RAP, GPIO.LOW) 
		GPIO.output(RAN, GPIO.LOW) 
		GPIO.output(DECP, GPIO.LOW) 
		GPIO.output(DECN, GPIO.LOW) 

#	    logging.debug(data)

	    client.close()
    def __del__(self):
	 logging.debug("End")
#	 self.s.close()
if __name__ == '__main__':
    app = DaemonApp()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()

