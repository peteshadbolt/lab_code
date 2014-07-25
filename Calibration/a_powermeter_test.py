import time, sys
import numpy as np
#from qy.hardware.powermeter import powermeter
from test_powermeter_class import powermeter
from qy.formats import ctx
import qy.util



powermeter=powermeter()
metadata = {'scan_label':'Looking at bright light'}
#data_file=ctx('C:/Users/Qubit/Code/lab_code/heater_testing/data/%s.ctx' % qy.util.timestamp(), metadata=metadata )


    
total=np.zeros(6)
for i in range(10):
    total += np.array(powermeter.read())


print 'Collected counts: %r' %total
    
raw_input()
    
total=np.zeros(6)
for i in range(10):
    total += np.array(powermeter.read())

    
print 'Collected counts: %r' %total
#print 'Writing some data to file'
#data_file.write('powers', total.tolist())
    
powermeter.kill()