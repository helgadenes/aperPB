# scan2fits_spec: Create XX & YY beam models from drift scans
# K.M.Hess 19/02/2019 (hess@astro.rug.nl)
# edited by H. Denes 17/08/2020 (denes@astron.nl)
__author__ = "Kelley M. Hess"
__date__ = "$04-jun-2019 16:00:00$"
__version__ = "0.2"

"""
This script creates fits cubes from drift scan data, using the previously created .csv files. 

input: 
- A file with the list of task_ids
- Select plots or no plots

Example: python scan2fits_ant.py -f ./task_id_lists/task_ids_190303.txt -d '190303' -b '1,7'

"""

from glob import glob
import os

from argparse import ArgumentParser, RawTextHelpFormatter
from astropy.coordinates import SkyCoord, FK5
from astropy.io import fits
from astropy.time import Time
from astropy.table import Table
import astropy.units as u
from astropy.wcs import WCS
import numpy as np
from scipy import interpolate
import time

from modules.telescope_params import westerbork


def task_id2equinox(task_id):

    # Automatically take the date of the observaitons from the task_id to calculate apparent coordinates of calibrator
    year = 2000 + int(str(task_id)[0:2])
    month = str(task_id)[2:4]
    day = str(task_id)[4:6]
    equinox = Time('{}-{}-{}'.format(year, month, day))

    return equinox.decimalyear


def make_gifs(root):

    os.system('convert -delay 50 {}*db0_reconstructed.png {}all_beams0.gif'.format(root, root))
    os.system('convert -delay 50 {}*_difference.png {}diff_xx-yy.gif'.format(root, root))

    return


def parse_args():

    parser = ArgumentParser(
        description="Make cubes of all 40 beams from drift scans.",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c', '--calibname', default='Cyg A',
                        help="Specify the calibrator. (default: '%(default)s').")
    parser.add_argument('-f', "--task_ids", default="",
                        help="A file with a list of task_ids. (default: '%(default)s').")
    parser.add_argument('-o', '--basedir', default='/tank/apertif/driftscans/',
                        help="Specify the root directory. \n(default: '%(default)s').")
    parser.add_argument('-b', '--beams', default='0,39',
                        help="Specify the first and the last beam as a string. \n(default: '%(default)s').")  
    parser.add_argument('-n', '--bin_num', default=18,
                        help="Number of frequency bins. \n(default: '%(default)s').") 
    parser.add_argument('-d', '--date', default="test",
                        help="Date for the output name. \n(default: '%(default)s').")                     
                        


    args = parser.parse_args()
    return args


def main():

	start = time.time()
	args = parse_args()

	print(args.beams)
	beam_range = args.beams.split(',')
	beams = range(int(beam_range[0]), int(beam_range[1])+1)
	freqchunks = args.bin_num
	date = args.date

	#print(beams)

	basedir = args.basedir

	with open(args.task_ids) as f:
		task_id = f.read().splitlines()	

	np.warnings.filterwarnings('ignore')

	# Find calibrator position
	calib = SkyCoord.from_name(args.calibname)

	cell_size = 100. / 3600.

	# Put all the output from drift_scan_auto_corr.ipynb in a unique folder per source, per set of drift scans.
	datafiles, posfiles = [], []

	for i in range(len(task_id)):
		datafiles.append('{}{}/{}_exported_data_frequency_split.csv'.format(basedir, task_id[i], task_id[i]))
		posfiles.append('{}{}/{}_hadec.csv'.format(basedir, task_id[i], task_id[i]))

	datafiles.sort()
	posfiles.sort()

	# Put calibrator into apparent coordinates (because that is what the telescope observes it in.)
	test = calib.transform_to('fk5')
	calibnow = test.transform_to(FK5(equinox='J{}'.format(task_id2equinox(task_id[0]))))

	# Read data from tables
	data_tab, hadec_tab = [], []
	print("\nReading in all the data...")
	for file, pos in zip(datafiles, posfiles):
		data_tab.append(Table.read(file, format='csv'))  # list of tables
		hadec_tab.append(Table.read(pos, format='csv'))  # list of tables

	print("Making beam maps: ")
	for ant in range(12):
		print('Creating modells for antenna:', ant)
		try:
			for beam in beams:
				print(beam)

				for f in range(freqchunks):
					x, y, z_xx, z_yy = [], [], [], []
					decs = []

					for data, hadec in zip(data_tab, hadec_tab):
						hadec_start = SkyCoord(ra=hadec['ha'], dec=hadec['dec'], unit=(u.rad, u.rad))
						time_mjd = Time(data['time'] / (3600 * 24), format='mjd')
						time_mjd.delta_ut1_utc = 0  # extra line to compensate for missing icrs tables
						lst = time_mjd.sidereal_time('apparent', westerbork().lon)

						HAcal = lst - calibnow.ra  # in sky coords
						dHAsky = HAcal - hadec_start[beam].ra + (24 * u.hourangle)  # in sky coords in hours
						dHAsky.wrap_at('180d', inplace=True)
						dHAphys = dHAsky * np.cos(hadec_start[beam].dec.deg * u.deg)  # physical offset in hours

						x = np.append(x, dHAphys.deg)
						y = np.append(y, np.full(len(dHAphys.deg), hadec_start[beam].dec.deg))
						z_xx = np.append(z_xx, data['auto_corr_beam_{}_freq_{}_xx_antenna_{}'.format(beam, f, ant)] - np.median(
							data['auto_corr_beam_{}_freq_{}_xx_antenna_{}'.format(beam, f, ant)]))
						z_yy = np.append(z_yy, data['auto_corr_beam_{}_freq_{}_yy_antenna_{}'.format(beam, f, ant)] - np.median(
							data['auto_corr_beam_{}_freq_{}_yy_antenna_{}'.format(beam, f, ant)]))

			
					# Create the 2D plane, do a cubic interpolation, and append it to the cube.
					tx = np.arange(min(x), max(x), cell_size)
					ty = np.arange(min(y), max(y), cell_size)
					XI, YI = np.meshgrid(tx, ty)
					gridcubx = interpolate.griddata((x, y), z_xx, (XI, YI), method='cubic')  # median already subtracted
					gridcuby = interpolate.griddata((x, y), z_yy, (XI, YI), method='cubic')

					# Find the reference pixel at the apparent coordinates of the calibrator
					ref_pixy = (calibnow.dec.deg - min(y)) / cell_size + 1       # FITS indexed from 1
					ref_pixx = (-min(x)) / cell_size + 1                        # FITS indexed from 1
					ref_pixz = 1                                                # FITS indexed from 1

					# Find the peak of the primary beam to normalize
					norm_xx = np.max(gridcubx[int(ref_pixy) - 3:int(ref_pixy) + 4, int(ref_pixx) - 3:int(ref_pixx) + 4])
					norm_yy = np.max(gridcuby[int(ref_pixy) - 3:int(ref_pixy) + 4, int(ref_pixx) - 3:int(ref_pixx) + 4])

					# Create 3D array with proper size for given scan set to save data as a cube
					if f == 0:
						cube_xx = np.zeros((freqchunks, gridcubx.shape[0], gridcubx.shape[1]))
						cube_yy = np.zeros((freqchunks, gridcuby.shape[0], gridcuby.shape[1]))
						db_xx = np.zeros((freqchunks, gridcubx.shape[0], gridcubx.shape[1]))
						db_yy = np.zeros((freqchunks, gridcuby.shape[0], gridcuby.shape[1]))

					cube_xx[f, :, :] = gridcubx/norm_xx
					cube_yy[f, :, :] = gridcuby/norm_yy

					# Convert to decibels
					db_xx[f, :, :] = np.log10(gridcubx/norm_xx) * 10.
					db_yy[f, :, :] = np.log10(gridcuby/norm_yy) * 10.

				stokesI = np.sqrt(0.5 * cube_yy**2 + 0.5 * cube_xx**2)
				squint = cube_xx - cube_yy

				wcs = WCS(naxis=3)
				wcs.wcs.cdelt = np.array([-cell_size, cell_size, 12.207e3*1000]) # channel width: 12.207e3, 1000 channels in 1 bin
				wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN', 'FREQ']
				wcs.wcs.crval = [calib.ra.to_value(u.deg), calib.dec.to_value(u.deg), 1370e6+(12.207e3*(-(24576/2-6500)))]
				wcs.wcs.crpix = [ref_pixx, ref_pixy, ref_pixz]
				wcs.wcs.specsys = 'TOPOCENT'
				wcs.wcs.restfrq = 1.420405752e+9
				header = wcs.to_header()

				hdux = fits.PrimaryHDU(cube_xx, header=header)
				hduy = fits.PrimaryHDU(cube_yy, header=header)
				hduI = fits.PrimaryHDU(stokesI, header=header)
				hdusq = fits.PrimaryHDU(squint, header=header)
	
				if not os.path.exists(basedir + 'fits_files/{}/ant_{}/'.format(date, ant)):
					os.mkdir(basedir + 'fits_files/{}/ant_{}/'.format(date, ant))

				# Save the FITS files
				hdux.writeto(basedir + 'fits_files/{}/ant_{}/{}_{}_{:02}_ant{}_xx.fits'.format(date, ant, args.calibname.replace(" ", ""), date,
																	 beam, ant), overwrite=True)
				hduy.writeto(basedir + 'fits_files/{}/ant_{}/{}_{}_{:02}_ant{}_yy.fits'.format(date, ant, args.calibname.replace(" ", ""), date,
																	 beam, ant), overwrite=True)
				hduI.writeto(basedir + 'fits_files/{}/ant_{}/{}_{}_{:02}_ant{}_I.fits'.format(date, ant, args.calibname.replace(" ", ""), date,
																	 beam, ant), overwrite=True)
				hdusq.writeto(basedir + 'fits_files/{}/ant_{}/{}_{}_{:02}_ant{}_diff.fits'.format(date, ant, args.calibname.replace(" ", ""), date,
																		 beam, ant), overwrite=True)
	
		except Exception as e:
			print('There is no data for antenna: {}'.format(ant))
			continue	
	
	end = time.time()
	print('Time [minutes]: ', (end - start)/60)

if __name__ == '__main__':
    main()
