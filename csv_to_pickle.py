# csv_to_pickle: convert auto correlation data from the csv files into pickle files
__author__ = "Helga Denes"
__date__ = "$07-aug-2020 16:00:00$"
__version__ = "0.1"

"""
This script creates fits cubes from drift scan data, using the previously created .csv files. 

input: 
- A file with the list of task_ids
- can also specify a range of beams with -b for example all beams between 0 and 10 : -b '0,10'

Example: python scan2fits_spec.py -f task_ids_190303.txt -d '190303' -b '1,7'
"""

from glob import glob
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from astropy.table import Table
import numpy as np
import pickle
import time


def make_gifs(root):

    os.system('convert -delay 50 {}*db0_reconstructed.png {}all_beams0.gif'.format(root, root))
    os.system('convert -delay 50 {}*_difference.png {}diff_xx-yy.gif'.format(root, root))

    return


def parse_args():

    parser = ArgumentParser(
        description="Convert csv into pickle.",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-f', "--task_ids", default="",
                        help="A file with a list of task_ids. (default: '%(default)s').")
    parser.add_argument('-o', '--basedir', default='/tank/apertif/driftscans/',
                        help="Specify the root directory. \n(default: '%(default)s').")
                     
                        


    args = parser.parse_args()
    return args


def main():

	start = time.time()
	
	args = parse_args()    
	basedir = args.basedir
	print(args.task_ids)

	with open(args.task_ids) as f:
		task_id = f.read().splitlines()	

	np.warnings.filterwarnings('ignore')


	# Make a list of data tables (the csv tables with the auto correlations).
	datafiles, posfiles = [], []

	for i in range(len(task_id)):
		print(task_id[i])
		data = Table.read('{}{}/{}_exported_data_frequency_split.csv'.format(basedir, task_id[i], task_id[i]), format='csv')
		data_2 = Table.read('{}{}/{}_hadec.csv'.format(basedir, task_id[i], task_id[i]), format='csv')
	
		file = open('{}{}/{}_exported_data_frequency_split.pickle'.format(basedir, task_id[i], task_id[i]),'wb')
		pickle.dump(data, file)
	
		file_2 = open('{}{}/{}_hadec.csv'.format(basedir, task_id[i], task_id[i]), 'wb')
		pickle.dump(data_2, file_2)
	
	end = time.time()
	print('Time [minutes]: ', (end - start)/60)

    	
if __name__ == '__main__':
    main()    	
    	
    	