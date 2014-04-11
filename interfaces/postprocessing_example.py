from qy.formats import ctx
from qy.analysis.coincidence_counting import pattern_parser
from matplotlib import pyplot as plt
from glob import glob
import os


# Get a list of CTX files on the dekstop
all_files=glob('C:/Users/Qubit/Desktop/data_from_example_scripts/*.ctx')
filename=all_files[-1]

# Load up a file for reading
my_file=ctx(filename)

# What do we know about it already?
print my_file


###############################
# Simple reading of data 
###############################
# Read out some countrates
for data in my_file.stream('count_rates'):
    print 'Raw data:', data
    twofolds = pattern_parser.parse_coincidence_pattern('**', data)
    print 'Total twofolds (**):', twofolds

# Read out some positions
for data in my_file.stream('position'):
    print 'Position:', data


###############################
# A different approach --- good for dips
###############################

# Define a lambda function "get_mn", which computes the "MN" count rate some raw data
get_mn=lambda data: pattern_parser.parse_coincidence_pattern('MN', data)

# Then we simply iterate over the file using map, getting two lists:
positions=map(float, my_file.stream('position'))
coincidences=map(get_mn, my_file.stream('count_rates'))
print 'positions:', positions
print 'coincidences:', coincidences

# Make a graph of positions and coincidences
plt.plot(positions, coincidences, 'k.-')
plt.xlabel('Position, mm')
plt.ylabel('Count rate')
plt.grid(color='gray')
pdf_filename=os.path.splitext(filename)[0]+'.pdf'
print pdf_filename
plt.savefig(pdf_filename)
