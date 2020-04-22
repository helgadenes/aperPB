# drift_scan_auto_corr: visualise the auto correlations of the drift scans and
# extract auto correlation data from measurement sets.
# Helga Denes 05/06/2019
# Edited by K.M.Hess (hess@astro.rug.nl)
# Edited by H. Denes (26/08/2019, 19/03/2020, 22/04/2020)
__author__ = "Helga Denes"
__date__ = "$19-march-2020 16:00:00$"
__version__ = "0.3"

import casacore.tables as pt
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def extract_data(antennas, beams, chan_range, chan_bins, exclude, data_location, task_id):
	"""
	Extract drift scan data from MS files and put them into a pandas data frame. 
	Data is extracted for each beam in 10 frequency bins and 4 different polarisations. 
	Data is extracted averaged for all antennas and per antenna.
	Several parameters can be specified:

	antennas: A list with all the antennas to read out. (Apertif has 12) [0, 1, 2, 3, ...]
	bemas: A list with all the beams to read out. (Apertif has 40) [0, 1, 2, 3, ...]
	chan_range: rfi free channel range. A list with 2 numbers [x1,x2] 
	chan_bins: A list of channel ranges to bin the data in frequency. By default this function only uses channels between 14000 and 24500 because of strong RFI. [[x1,x2],[x1,x2],...]
	exclude: a string with instructions for taql to exclude certain data, e.g. baselines or antennas.
	data_location: location to copy the data to as a string e.g. '/tank/apertif/driftscans'
	task_id: or observation id as a string 
	""" 
	chan_range_1 = str(chan_range[0])
	chan_range_2 = str(chan_range[1])

	df = pd.DataFrame()

	for j in beams:
		t = pt.taql(
			'select TIME, gmeans(abs(DATA[{0}:{1},0])) as XXPOL, gmeans(abs(DATA[{0}:{1},1])) as XYPOL, gmeans(abs(DATA[{0}:{1},2])) as YXPOL, gmeans(abs(DATA[{0}:{1},3])) as YYPOL from {2}{3}/WSRTA{3}_B0{4:02}.MS where ANTENNA1==ANTENNA2 {5} GROUP BY TIME'.format(chan_range[0], chan_range[1], data_location, task_id, j, exclude))
		print('BEAM: {}'.format(j))
		times = np.array(pt.tablecolumn(t, 'TIME'))
		if j==beams[0]:
			time_steps = len(times)
			print('time steps in first beam: ', time_steps)
		df['time'] = times[:time_steps-3]
		for k, chan in enumerate(chan_bins):
			data_beam_xx = np.mean(np.array(pt.tablecolumn(t, 'XXPOL'))[:, chan[0]:chan[1], :], axis=1)
			auto_corr_xx = np.reshape(data_beam_xx, len(data_beam_xx))
			data_beam_xy = np.mean(np.array(pt.tablecolumn(t, 'XYPOL'))[:, chan[0]:chan[1], :], axis=1)
			auto_corr_xy = np.reshape(data_beam_xy, len(data_beam_xy))
			data_beam_yx = np.mean(np.array(pt.tablecolumn(t, 'YXPOL'))[:, chan[0]:chan[1], :], axis=1)
			auto_corr_yx = np.reshape(data_beam_yx, len(data_beam_yx))						
			data_beam_yy = np.mean(np.array(pt.tablecolumn(t, 'YYPOL'))[:, chan[0]:chan[1], :], axis=1)
			auto_corr_yy = np.reshape(data_beam_yy, len(data_beam_yy))
			df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_xx'] = auto_corr_xx[:time_steps-3]
			df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_xy'] = auto_corr_xy[:time_steps-3]
			df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_yx'] = auto_corr_yx[:time_steps-3]
			df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_yy'] = auto_corr_yy[:time_steps-3]

		for i in antennas:
			t_ant = pt.taql(
				'select TIME, abs(DATA[{0}:{1},0]) as XXPOL, abs(DATA[{0}:{1},1]) as XYPOL, abs(DATA[{0}:{1},2]) as YXPOL, abs(DATA[{0}:{1},3]) as YYPOL from {2}{3}/WSRTA{3}_B0{4:02}.MS where ANTENNA1==ANTENNA2 AND ANTENNA1={5} GROUP BY TIME'.format(chan_range[0], chan_range[1], data_location, task_id, j, i))
			print('ANT: {}'.format(i))

			for k,chan in enumerate(chan_bins):
				data_ant_xx = np.mean(np.array(pt.tablecolumn(t_ant, 'XXPOL'))[:, chan[0]:chan[1], :], axis=1)
				auto_corr_xx_ant = np.reshape(data_ant_xx, len(data_ant_xx))
				data_ant_xy = np.mean(np.array(pt.tablecolumn(t_ant, 'XYPOL'))[:, chan[0]:chan[1], :], axis=1)
				auto_corr_xy_ant = np.reshape(data_ant_xy, len(data_ant_xy))
				data_ant_yx = np.mean(np.array(pt.tablecolumn(t_ant, 'YXPOL'))[:, chan[0]:chan[1], :], axis=1)
				auto_corr_yx_ant = np.reshape(data_ant_yx, len(data_ant_yx))
				data_ant_yy = np.mean(np.array(pt.tablecolumn(t_ant, 'YYPOL'))[:, chan[0]:chan[1], :], axis=1)
				auto_corr_yy_ant = np.reshape(data_ant_yy, len(data_ant_yy))
				df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_xx_antenna_' + str(i)] = auto_corr_xx_ant[:time_steps-3]
				df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_xy_antenna_' + str(i)] = auto_corr_xy_ant[:time_steps-3]
				df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_yx_antenna_' + str(i)] = auto_corr_yx_ant[:time_steps-3]
				df['auto_corr_beam_' + str(j) + '_freq_' + str(k) + '_yy_antenna_' + str(i)] = auto_corr_yy_ant[:time_steps-3]

	return df


def data_to_csv(data_location, task_id, chan_range, bin_num):
	"""
	- Extract data on the observed field into a csv file. This is later used to calculate coordinates.
	- Extract auto correlation data with the "extract_data" function. 
	- Write the extracted data into csv files.
	
	data_location: string
	task_id: string
	chan_range: rfi free channel range. A list with 2 numbers [x1,x2] 
	bin_num: number of bins (integer)
	""" 
	
	print('test', data_location)

	if data_location[-1] != '/':
		data_location += '/'

	output_path = data_location + task_id +'/'

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	# First read HA & Dec from MS file header and save into a csv file for later use.
	# These are the best calculated RA/Dec positions of the centers of the beams.

	beams = range(0, 40)

	hadec = pd.DataFrame()
	ha = np.zeros(40)
	dec = np.zeros(40)
	for j in beams:
		field_table = pt.table('{}{}/WSRTA{}_B0{:02}.MS::FIELD'.format(data_location, task_id, task_id, j))
		(ha[j], dec[j]) = field_table.getcol("DELAY_DIR")[0, 0]
	hadec['ha'] = ha
	hadec['dec'] = dec

	hadec.to_csv(str(output_path) + str(task_id) + '_hadec.csv')

	# Extract data and export data into a csv file

	# count antennas in the MS file:
	t_name = pt.taql('select NAME from {0}{1}/WSRTA{1}_B001.MS::ANTENNA'.format(data_location, task_id))
	ant_names=t_name.getcol("NAME")
	antennas = range(len(ant_names))
	
	exclude = ''
	# exclude = 'AND ANTENNA1!= 11 AND ANTENNA2!=11 AND ANTENNA1!= 10 AND ANTENNA2!=10'
	total_chan_num = chan_range[1] - chan_range[0]
	bin_size = int(total_chan_num / bin_num)
	chan_bins = []
	for i in range(0, int(chan_range[1]-bin_size), bin_size):
		chan_bins.append([i, i + 1050])

	df_1 = extract_data(antennas, beams, chan_range, chan_bins, exclude, data_location, task_id)
	df_1.to_csv(str(output_path) + str(task_id) + '_exported_data_frequency_split.csv')

