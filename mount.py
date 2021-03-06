#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Example of how to run a daemon."""

import time

from daemon import runner
from socket import *
import logging
from threading import Thread
import RPi.GPIO as GPIO

import ephem
import numpy as np
from datetime import datetime
from datetime import timedelta

from config import *
#from display import *

from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE

RST = None     # on the PiOLED this pin isnt used
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(RAP, GPIO.OUT) # W
GPIO.setup(RAN, GPIO.OUT) # E ->
GPIO.setup(DECP, GPIO.OUT) # N
GPIO.setup(DECN, GPIO.OUT) # S ->
GPIO.setup(POWER, GPIO.OUT) # S ->


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
	self.log_file = '/var/log/mount.log'
        self.pidfile_timeout = 1
	self.go=0
	self.ggo=0
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
	self.flip=0
	self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
	self.disp.begin()

	self.disp.clear()
	self.disp.display()

	self.width = self.disp.width
	self.height = self.disp.height
	self.image = Image.new('1', (self.width, self.height))

	self.draw = ImageDraw.Draw(self.image)

	self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
	padding = -2
	top = padding
	bottom = self.height-padding
	x = 0
	self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',20)
	self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
	cmd = "hostname -I | cut -d\' \' -f1"
	IP = subprocess.check_output(cmd, shell = True )
	self.draw.text((x, top),       "Mount.py",  font=self.font, fill=255)
	self.draw.text((x, top+26),    str(IP), font=self.font, fill=255)
	self.disp.image(self.image)
	self.disp.display()



# 0 for ar 102/600
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
    def m_step(self):
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
 
	    time.sleep(self.mstep/100) # 8x - 30  4x - 60 
	    if self.sra > 0: 
		GPIO.output(RAP, GPIO.LOW) 
		self.ra=self.ra+0.0006666
		if self.ra>24 :
		    self.ra=self.ra-24
	    elif self.sra < 0:
		GPIO.output(RAN, GPIO.LOW) 
		self.ra=self.ra-0.0006666
		if self.ra<0 :
		    self.ra=self.ra+24
	    if self.flip == 1:     
		if self.sdec > 0: 
		    GPIO.output(DECP, GPIO.LOW)
		    self.dec=self.dec+0.01
		elif self.sdec <0:
		    GPIO.output(DECN, GPIO.LOW) 
		    self.dec=self.dec-0.01
	    elif self.flip == 0 :
		if self.sdec > 0: 
		    GPIO.output(DECN, GPIO.LOW)
		    self.dec=self.dec+0.01
		elif self.sdec <0:
		    GPIO.output(DECP, GPIO.LOW) 
		    self.dec=self.dec-0.01
	    



    def goto(self):
	

	difra=float(self.gra)-float(self.ra)
	if difra>12 :
	    difra=float(self.gra)-float(self.ra+24)
	elif difra < -12 :
	    difra=float(self.gra)+24-float(self.ra)
 	difdec=float(self.gdec)-float(self.dec)
	rasteps=int(abs(difra)*15) # to degrees
	decsteps=int(abs(difdec))
	difsteps=abs(rasteps-decsteps)
	if rasteps > decsteps:
	    comsteps=decsteps
	else:
	    comsteps=rasteps
	if self.speed==4:
	    nextTime = datetime.now() + timedelta(minutes = comsteps+difsteps+1)
	    logging.debug('Liczba minut (GOTO)  '+str (comsteps+difsteps)+" ("+ nextTime.strftime( "%H:%M)") )
	if self.speed==8:
	    nextTime = datetime.now() + timedelta(minutes = (comsteps+difsteps+1)/2)

	    logging.debug('Liczba minut (GOTO)  '+str ((comsteps+difsteps)/2)+" ("+ nextTime.strftime("%H:%M)") )

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

	difra=float(self.gra)-float(self.ra)
	if difra>12 :
	    difra=float(self.gra)-float(self.ra+24)
	elif difra < -12 :
	    difra=float(self.gra)+24-float(self.ra)
 	difdec=float(self.gdec)-float(self.dec)
	rasteps=int(100*abs(difra)*15) # to tithing_degrees
	decsteps=int(abs(100*difdec))
	difsteps=abs(rasteps-decsteps)
	if rasteps > decsteps:
	    comsteps=decsteps
	else:
	    comsteps=rasteps
	if difra > 0:
	    self.sra=1
	elif difra < 0:
	    self.sra=-1

	if difdec > 0:
	    self.sdec=1
	elif difdec < 0:
	    self.sdec=-1
	
	for x in range (0,comsteps):
	    self.m_step()
	if rasteps > decsteps:
	    self.sdec=0
	else:
	    self.sra=0

	for x in range (0,difsteps):
	    self.m_step()

	self.sra=0
	self.sdec=0
	self.go=0
	
	logging.debug('GOTO DO END')

    def run(self):
        """Main Daemon Code."""
	fslra=0.00011
	fsldec=0.00166
	self.observing_location = ephem.Observer();
	self.observing_location =  ephem.city('Warsaw')
	self.observing_location.pressure = 0
	if self.speed == 8:
	    self.mstep=30
	    fslra=0.00022
	    fsldec=0.00333
	s = socket(AF_INET, SOCK_STREAM) 
	
	s.bind(('127.0.0.1', 5555)) #dowiazanie do portu 5555
	s.listen(5)
        logging.basicConfig(level=logging.DEBUG, format='%(message)s', filename=self.log_file,filemode='a')
	park=1
	logging.debug('BEGIN')
        while True:
	    client,addr = s.accept() 
	    data = client.recv(30)
#	    logging.debug(data)
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
#		self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
#		self.draw.text((0, 6),     "ALAAmA",  font=self.font, fill=255)
#		self.disp.image(self.image)
#		self.disp.display()

		logging.debug('UNPARK DO')
	    elif cmd == 1: # park
		
		logging.debug('PARK DO')
		self.observing_location.date = ephem.now()
		star = ephem.FixedBody()
		star._ra=ephem.degrees(str(self.ra*15))
		star._dec=ephem.degrees(str(self.dec))

		star.compute(self.observing_location)

		self.alt=star.alt
		self.az=star.az
		park=1

	    elif cmd == 2: # goto 
		self.gra=words[1]
		self.gdec=words[2]
		self.go=1
		self.ggo=1
		logging.debug('GOTO '+str(self.gra)+' '+str(self.gdec))
	    elif cmd == 3: # status
		if park==1:
			self.observing_location.date =  ephem.now()
			rra,ddec= self.observing_location.radec_of(self.az, self.alt)
			self.ra=np.degrees(rra)/15
			self.dec=np.degrees(ddec)
#			logging.debug(self.observing_location.date)
#			logging.debug('PARK '+str(self.observing_location.date)+' '+str(np.degrees(rra))+' '+str(np.degrees(ddec))+' '+str(self.ra))
#			logging.debug('STATUS '+str(self.az)+' '+str(self.alt))
		time.sleep(1)
#		logging.debug('STATUS '+str(self.ra)+' '+str(self.dec))

		client.send(str(park)+' '+str(self.ra) + ' ' + str(self.dec))

	    elif cmd == 4: # sync
		self.ra=float(words[1])
		self.dec=float(words[2])
		logging.debug('SYNC '+str(self.ra)+' '+str(self.dec))

		if self.ggo==1:
			logging.debug('FLIP '+str(abs(float(self.gdec)-self.dec)))
			if abs(float(self.gdec)-self.dec) > 2. :
			    self.flip=self.flip^1
			    logging.debug('FLIP '+str(self.flip))
		        self.ggo=0
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
	
	 self.disp.clear()
	 self.disp.display()
#	 self.disp.command(Adafruit_SSD1306.SSD1306_DISPLAYOFF)
#	 self.s.close()
if __name__ == '__main__':
    app = DaemonApp()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()

