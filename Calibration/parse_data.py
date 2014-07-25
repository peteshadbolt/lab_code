import numpy as np
import os
from qy.formats import ctx
from qy.analysis.coincidence_counting.pattern_parser import parse_coincidence_pattern


def parse(datafilename, patterns):
    # This loads the CTX file
    #dir = os.path.dirname(os.path.realpath(__file__))
    #datafilename = os.path.join(dir, '2014_05_13_tuesday_11h57m00s.ctx')
    ctxfile=ctx(datafilename)
    #print ctxfile

    # This pulls out all the stuff to do with count rates
    all_counts = list(ctxfile.stream('count_rates'))

    # This filters for the count rates we care about
    select_counts = lambda data: [parse_coincidence_pattern(pattern, data) for pattern in patterns] 
    interesting_counts_table = np.array(map(select_counts, all_counts))
    print interesting_counts_table
    # Now it's a numpy array, so we can integrate, average sum etc
    #print interesting_counts_table
    fit_data = np.sum(interesting_counts_table, axis=1)
    #print np.sum(interesting_counts_table, axis=1)
    print fit_data
    raw_input()
    return fit_data