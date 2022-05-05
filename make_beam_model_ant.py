# 6/13/19 DJP
# edited by K.M. Hess and H. Denes

__author__ = "DJP"
__date__ = "$04-jun-2019 16:00:00$"
__version__ = "0.2"

"""
This program will read Apertif FITS files containing one beam map and fit them with RectBivariateSpline. 
The resulting spline fits are written into a .csv file and 9 times 40 fits files. One fits file for each beam at each of the 9 frequency bins.

input: 
A date that has beam fits files in the base directory /tank/apertif/driftscans/

Example: python make_beam_model_ant.py -d '190303' -c 'Cas A' 

"""


from glob import glob

from scipy.interpolate import RectBivariateSpline
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
from numpy import arange
import pandas as pd
from argparse import ArgumentParser, RawTextHelpFormatter


def parse_args():

    parser = ArgumentParser(
        description="Make cubes of all 40 beams from drift scans.",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c', '--calibname', default='Cyg A',
                        help="Specify the calibrator. (default: '%(default)s').")
    parser.add_argument('-o', '--basedir', default='/tank/apertif/driftscans/',
                        help="Specify the root directory. \n(default: '%(default)s').")
    parser.add_argument('-b', '--beams', default='0,39',
                        help="Specify the first and the last beam as a string. \n(default: '%(default)s').")  
    parser.add_argument('-n', '--bin_num', default=10,
                        help="Number of frequency bins. \n(default: '%(default)s').")  
    parser.add_argument('-d', '--date', default="test",
                        help="Output name. \n(default: '%(default)s').")                      
                        

    args = parser.parse_args()
    return args

def main():
    
	args = parse_args()
	basedir = args.basedir
	date = args.date
	calib = args.calibname

	for ant in range(0,12):
		try:
			print('Spline interpolating antenna: ', ant)
			files=glob('{}fits_files/{}/ant_{}/{}_{}_*_I.fits'.format(basedir, date, ant, calib.replace(' ',''), date))			
			files.sort()

			# loop trough all 40 beams
			for k in range(40):
				hdu=fits.open(files[k])
				beam=hdu[0].data
				h_measured = hdu[0].header
				f0=hdu[0].header['CRVAL3']
				fdelt=hdu[0].header['CDELT3']
				px_width = 20
								
				#hdu.close()
		
				model = []
		
				# loop trough all frequency chunks
				for chan in range(0,10):

					freq = f0 + fdelt * chan
					bmap, fbeam = [], []
		
					bmap = np.flipud(beam[chan,int(hdu[0].header['CRPIX2'])-px_width:int(hdu[0].header['CRPIX2'])+px_width, int(hdu[0].header['CRPIX1'])-px_width:int(hdu[0].header['CRPIX1'])+px_width])				
					x=arange(0,px_width * 2)
					y=arange(0,px_width * 2)
					fbeam.append(RectBivariateSpline(y,x,bmap))  # spline interpolation
					model.append(np.flipud(fbeam[0](x,y))) # 40x40 pixel model

				h_measured['NAXIS1'] = int(px_width * 2)
				h_measured['NAXIS2'] = int(px_width * 2)
				h_measured['CRPIX1'] = px_width
				h_measured['CRPIX2'] = px_width

				hduI = fits.PrimaryHDU(model, header=h_measured)
		
				if not os.path.exists(basedir + 'fits_files/{}/ant_{}/beam_models'.format(date, ant)):
					os.mkdir(basedir + 'fits_files/{}/ant_{}/beam_models'.format(date, ant))
		

				hduI.writeto(basedir + 'fits_files/{}/ant_{}/beam_models/{}_{:02}_I_model.fits'.format(date, ant, date, k), overwrite=True)
		
		except Exception as e:
			print('There is no data for antenna: {}'.format(ant))
			continue



if __name__ == '__main__':
    main()