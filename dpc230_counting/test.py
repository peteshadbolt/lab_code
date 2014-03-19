from qy.hardware import dpc230
import sys

def callback(x):
    print x

d=dpc230('hardware', callback=callback)
d.count(1)
d.count(1)
d.count(1)
d.count(1)
print str(d)
d.kill()
