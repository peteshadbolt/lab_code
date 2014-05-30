from qy.hardware import dpc230
import argparse

def callback(message):
    print message

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Get timetags')
    parser.add_argument('photon_buffer',  type=str, nargs='?', default=None, help='Directory on disk where timetags will be written')
    parser.add_argument('-t',  '--integration_time', default=1, type=float, help='Integration time, in seconds')
    args = parser.parse_args()

    card=dpc230.dpc230('hardware', callback=callback)
    tdc1, tdc2 = self.dpc230.count(args.integration_time, args.photon_buffer)
    card.kill()

    post=dpc230.dpc230(postprocessing)
    spc_file = post.convert_raw_data(tdc1, tdc2)
    print 'Wrote %s' % spc_file

