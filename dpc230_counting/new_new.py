from multiprocessing import Process, Pipe 
import time, sys
from qy.hardware import dpc230
from qy.analysis import coincidence

        

if __name__=='__main__':
    def receive_counts(data):
        print '\nTop level received data:' 
        print data

    c=coincidence_counter(callback=receive_counts)

    for position in range(5):
        c.count(1, {'position': position}) 
        c.collect()

    c.shutdown()


