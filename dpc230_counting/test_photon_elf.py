from qy.hardware.wrappers import photon_elf
import sys

if __name__=='__main__':
    photon_elf=photon_elf.threaded_photon_elf()
    for i in range(1000):
        photon_elf.send('status', 'Test'+'!'*i)
        out=photon_elf.recv()
        if out:
            if out[0]=='gui_quit': sys.exit(0)
        rates={'a':2004+i, 'ab':1337, 'b':i, 'abc':100+i, 'ef':5}
        photon_elf.send('count_rates', {'count_rates':rates})
