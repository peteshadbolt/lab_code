import time, sys
from qy.hardware.wrappers.coincidence_counter import threaded_coincidence_counter
#from qy.hardware.wrappers.photon_elf import threaded_photon_elf
from qy.formats import ctx
        

if __name__=='__main__':
    def handle_data(data):
        ''' Handles data from the counting system '''
        print 'Got data:', data

        # Extract pertinent information
        key, value=data
        if key!='count_rates': return
        count_rates=value['count_rates']
        context=value['context']

        # Send to the GUI
        #elf.send('count_rates', count_rates)

        # Write to disk
        #output_file.write_list('mc_position', context['position'])
        #output_file.write_counts(data)


    # The GUI
    #elf=threaded_photon_elf()

    # Somwhere to put data
    output_file=ctx('test.ctx', mode='write')
    metadata={'scan_label': 'Here is a scan label'}
    output_file.write_metadata(metadata)

    # The counting gear
    counter=threaded_coincidence_counter(callback=handle_data)
    print 'Connected!'

    t=time.clock()
    for position in range(10):
        print '                                 Moved to %d' % position
        counter.count(1, {'position': position}) 
    print time.clock()-t    

    counter.collect()


    counter.shutdown()
    #elf.shutdown()

