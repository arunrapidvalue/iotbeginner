import RPi.GPIO as GPIO 
import json
import requests
import time

class Led:
        def __init__(self,gpio):
                self.gpio = gpio
                GPIO.setup(self.gpio, GPIO.OUT)
                self.state = 'off'

        def on(self):
                GPIO.output(self.gpio,1)
                self.state = 'on'

        def off(self):
                GPIO.output(self.gpio,0)
                self.state = 'off'

        def state(self):
                return self.state

        def toggle(self):
                if self.state == 'on':
                        self.off()
                else:
                        self.on()


class Config: 
	def __init__(self):
		self.cfile = 'conf.json'
	
	def read(self):
		cont = open('conf.json','r').read()
		print cont

	def isOk(self):
		cont = open('conf.json','r')
		dcont = cont.read()
		jcont = json.loads(dcont)
		readkey = jcont.get('read_key')
		channel = jcont.get('channel')
		if readkey == 'empty' or channel == 'empty':
			cont.close()
			return False
		elif readkey != 'empty' and channel != 'empty':
			cont.close() 
			return True
		else:
			cont.close()
			return False

	def update(self):
		id = raw_input('enter your channel id\n')
		print ''
		key = raw_input('enter your readapi key\n')
		print ''
		cont = open('conf.json','r')
		dcont = cont.read()
		jcont = json.loads(dcont)
		jcont['read_key'] = key
		jcont['channel'] = id
		wcont = json.dumps(jcont)
		cont.close()
		cont = open('conf.json','w')
		cont.write(wcont)
		cont.close()

	def getCreds(self):
		result = {}
		cont = open(self.cfile, 'r')
		dcont = cont.read()
		jcont = json.loads(dcont)
		check = self.isOk()
		if check == True:
			result['channel'] = jcont.get('channel')
			result['key'] = jcont.get('read_key')
			return result
		else:
			return None
		

class Trigger: 
	def __init__(self,c):
		creds = c.getCreds()
		channel = creds.get('channel')
		key = creds.get('key')
		self.url = 'https://api.thingspeak.com/channels/' + channel + '/fields/1.json?api_key=' + key + '&results=1'

	def getState(self):
		try:
			resp = requests.get(self.url)
			try:
				jsond = json.loads(resp.text)
				resj = jsond.get('feeds')
				if resj:
					statej = resj[0].get('field1')
					trigger = int(statej)
					return trigger
				else:
					return -2
			except KeyError, ValueError:
					return -1
		except requests.exceptions.RequestException:
			return 0

# for testing purposes 
"""
if __name__ == '__main__':
	c = Config()
	cflag = c.isOk()
	if cflag == True:
		print 'config is Ok'
		t = Trigger(c)
		print t.getState()
	else:
		c.update()
		print 'config is not ok'
		
	c.read()
"""

"""
if __name__ == '__main__': 
	led = Led(12)
	led.on()
	time.sleep(3)
	print 'done'
	led = None
"""
