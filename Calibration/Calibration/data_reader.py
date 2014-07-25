import numpy as np
import os

def load_data(datafilename, dd):
	'''Loads data required to perform fit'''
	
	data = open(datafilename)
	count_dict=[]

	for line in data:
		first_colon=line.find(':')
		key =  line[:first_colon]
		
		if key =='count_rates':
			counts = (eval(line[first_colon+1:]))
			number_of_detectors = len(counts)
			
			count_dict.append(counts)
				
		elif key == 'context':
			
			print (eval(line[first_colon+1:]))['voltages']
		
	
	#print count_dict
	for i in range(len(dd.keys())):
		for j in range(len(count_dict)):
			for key, item in count_dict[j].items():
				if key == dd.keys()[i]:
					dd[dd.keys()[i]].append(item)
	
	data = []
	
	for i in range(len(dd.values()[0])):
		ds = 0
		for j in range(len(dd.values())):
			ds += dd.values()[j][i]
		data.append(ds)
	
	print data
	return data
	

	
	

if __name__ == '__main__':

	dir = os.path.dirname(os.path.realpath(__file__))
	datafilename = os.path.join(dir, '2014_05_13_tuesday_11h57m00s.ctx')
	load_data(datafilename, {'i':[]})
	
	#load_data(datafilename, {'i':[], 'j':[]})
	
	#load_data(datafilename, {'i':[], 'k':[],'l':[]})
	
	#load_data(datafilename, {'i':[], 'k':[],'l':[], 'j':[]})
	
	#load_data(datafilename, {'j':[]})