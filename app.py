#! /bin/py
# this is the main app class
# the entry point to the iot beginner app 

import sys
from lib import *
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BOARD)
import time 
class Main: 
	def __init__(self):
		self.led1 = Led(32)
		self.led2 = Led(18)
		self.led3 = Led(12)
		self.c = Config()

	def run(self):
		print 'starting app' 
		cflag = self.c.isOk()
		if cflag == True: 
			try: 
				trig = Trigger(self.c)
				while True: 
					t = trig.getState()
					print t
					if t == 0:
						self.led1.off()
						self.led2.off()
						self.led3.off()
					elif t == 1:
						self.led1.off()
						self.led2.off()
						self.led3.on()
					elif t == 2:
						self.led1.off()
						self.led2.on()
						self.led3.off()
					elif t == 3:
						self.led1.off()
						self.led2.on()
						self.led3.on()
					elif t == 4:
						self.led1.on()
						self.led2.off()
						self.led3.off()
					elif t == 5: 
						self.led1.on()
						self.led2.off()
						self.led3.on()
					elif t == 6:
						self.led1.on()
						self.led2.on()
						self.led3.off()
					elif t == 7:
						self.led1.on()
						self.led2.on()
						self.led3.on()
					
					time.sleep(3)	
			except KeyboardInterrupt:
				print 'Exiting Now'
				GPIO.cleanup()

	def config(self):
		print 'configuring'
		self.c.update()

	def help(self): 
		print 'You can use following options'
		print 'python [app.py] to run the app' 
		print 'python [app.py config] to configure the app'  



if __name__ == '__main__': 
	cmdlen = len(sys.argv)
	m = Main()
	if cmdlen == 1:
		m.run()
	elif cmdlen > 1:
		cmd = sys.argv[1]
		if cmd == 'config': 
			m.config()
		elif cmd == 'run': 
			m.run()
		elif cmd == 'start': 
			m.run()
		elif cmd == 'help': 
			m.help()
	
