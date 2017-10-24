import json
import urllib2
import time

NAGIOS_ADDRESS = ''

def monitor(net):
	first_pass = True
	alarms = set()
	while True:
		current_alarms = set()
		req = urllib2.Request(NAGIOS_ADDRESS)
		req.add_header("Authorization",  "Basic ***API_KEY***")
		response = urllib2.urlopen(req)
		html = response.read()
		output = json.loads(html)
		for status in output['status']['service_status']:
			alarm = ":".join([status['host_name'], status['status'], status['service_description']])
			if alarm not in alarms:
				if not first_pass:
					print 'Icinga Alert: %20s %10s %35s' % (status['host_name'], status['status'], status['service_description'])
					net.alarm(status['service_description'], host = status['host_name'])
			current_alarms.add(alarm)
		alarms = current_alarms
		if first_pass:
			first_pass = False
		time.sleep(1)
