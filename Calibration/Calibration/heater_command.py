def send_one_voltage(self, voltage, heater):
	
	command = '%s%d=%.9f' % (prefix, heater, value)
    response = self.send_rcv(command)
	assert(response=='OK')
	return 'voltage is %s' % (str(voltage))