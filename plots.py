#!/usr/bin/env python

"""
This is a collection of functions to make plots from the drift scan data.

"""

__author__ = "Helga Denes"
__date__ = "$29-aug-2019 16:00:00$"
__version__ = "0.1"
#-------------------------------------------
# Plots
#-------------------------------------------

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 18
mpl.rcParams['xtick.direction']='in'
mpl.rcParams['ytick.direction']='in'


#---------------------------------------------

def plot_all_beams(task_id, data, data_location):
	"""
	Plot the auto correlations of all 40 beams. Input:
	task_id: string
	data: pandas data frame

	"""
	row_0 = ['00']
	rows = [['39', '38', '37', '36', '35', '34', '33'],
			['32', '31', '30', '29', '28', '27', 'aa'],
			['26', '25', '24', '23', '22', '21', '00'],
			['20', '19', '18', '17', '16', '15', 'aa'],
			['14', '13', '12', '11', '10', '9', '8'],
			['07', '06', '05', '04', '03', '02', '01']]

	fig, axs = plt.subplots(6, 7, figsize=(12, 10))

	for ax, beam in zip(np.array(axs).flatten(), np.array(rows).flatten()):
		if beam != 'aa':
			beam = int(beam)
			ax.plot(data['time'],  data['auto_corr_beam_{}_freq_5_xx'.format(beam)]/max(data['auto_corr_beam_{}_freq_5_xx'.format(beam)]), '.-')
			ax.set_title("Beam {}".format(beam), size=8)
			ax.get_xaxis().set_visible(False)
			ax.get_yaxis().set_visible(False)
		else:
			ax.axis('off')
	fig.suptitle("Auto correlations {}".format(task_id))

	plt.savefig('{}/{}/{}_time_amp_40.png'.format(data_location,task_id,task_id), dpi=100)
    
    
def plot_all_beams_antenna(task_id, data, data_location):
	"""
	Plot the auto correlations of all 40 beams. Display each antenna separately. Input:
	task_id: string
	data: pandas data frame

	"""    

	row_0 = ['00']
	rows = [['39', '38', '37', '36', '35', '34', '33'],
			['32', '31', '30', '29', '28', '27', 'aa'],
			['26', '25', '24', '23', '22', '21', '00'],
			['20', '19', '18', '17', '16', '15', 'aa'],
			['14', '13', '12', '11', '10', '9', '8'],
			['07', '06', '05', '04', '03', '02', '01']]

	fig, axs = plt.subplots(6, 7, figsize=(12, 10))

	for ax, beam in zip(np.array(axs).flatten(), np.array(rows).flatten()):
		if beam != 'aa':
			beam = int(beam)
			for antenna in range(0,12):
				ax.plot(data['time'],  data['auto_corr_beam_{}_freq_5_xx_antenna_{}'.format(beam, antenna)], '-', label=antenna)            
				ax.set_title("Beam {}".format(beam), size=8)
				ax.get_xaxis().set_visible(False)
				ax.get_yaxis().set_visible(False)
				if beam == 0:
					ax.legend(bbox_to_anchor=(1.03, 1.05))
		else:
			ax.axis('off')
	fig.suptitle("Auto correlations {}".format(task_id))    
	plt.savefig('{}/{}/{}_time_amp_40_ant.png'.format(data_location,task_id,task_id), dpi=100)