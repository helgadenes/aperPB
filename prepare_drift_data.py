#!/usr/bin/env python

"""
This script copies drift scan files from ALTA to happili. 
Then extracts the auto correlation data for each antenna in 10 frequency bins into a csv file.
Then cleans up space on happili
Based on scripts by Helga Denes (denes@astron.nl) and K.M.Hess (hess@astro.rug.nl)

input: 
- A file with the list of task_ids
- Select plots or no plots

Example: ./prepare_drift_data.py -f task_ids.txt -p True

"""

__author__ = "Helga Denes"
__date__ = "$29-aug-2019 16:00:00$"
__version__ = "0.1"
#-------------------------------------------
# packages
#-------------------------------------------

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
import pandas as pd
import drift_scan_auto_corr_frequency as ds
import plots as plots

#-------------------------------------------
# read in list of task ids
#-------------------------------------------

def parse_args():

    parser = ArgumentParser(
        description="Extract data from drift scans",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-f', '--task_ids', default='',
                        help="File with task_ids. (default: '%(default)s').")
    parser.add_argument('-p', "--plot", default=False,
                        help="If True make plots")

    args = parser.parse_args()
    return args


args = parse_args()
with open(args.task_ids) as f:
    task_id = f.read().splitlines()

#-------------------------------------------
# copy files from alta
# extract autocorrelation data into csv table
# delet ms files
#-------------------------------------------

#task_id = ['190821129']
#task_id = ['190821130', '190821131', '190821132']
data_location = '/data/apertif/driftscans/'

chan_range = [14000, 24500]  # RFI free channels to be used  
bin_num = 10  # number of bins


for i in range(len(task_id)):
	print("Copying data for {}".format(task_id[i]))
	os.system('iget -r /altaZone/archive/apertif_main/visibilities_default/{} '.format(task_id[i])+data_location)
	
	print("Extracting data")
	ds.data_to_csv(data_location, task_id[i], chan_range, bin_num)
	
	print('rm -rf {}{}/WSRTA*.MS'.format(data_location, task_id[i]))
	os.system('rm -rf {}{}/WSRTA*.MS'.format(data_location, task_id[i]))
	
	# Creating plots
	if args.plot == 'True':
		print("Creating plots")
		data = pd.read_csv('{}{}/{}_exported_data_frequency_split.csv'.format(data_location,task_id[i], task_id[i]))

		plots.plot_all_beams(task_id[i], data, data_location)
		plots.plot_all_beams_antenna(task_id[i], data, data_location)



