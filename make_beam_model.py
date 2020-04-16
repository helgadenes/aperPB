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

Example: python make_beam_model.py -d '190303'

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

	files=glob('{}fits_files/{}/CygA_{}_*_I.fits'.format(basedir, date, date))
	files.sort()

	hdu=fits.open(files[0])
	beam=hdu[0].data
	h_measured = hdu[0].header
	f0=hdu[0].header['CRVAL3']
	fdelt=hdu[0].header['CDELT3']
	hdu.close()
	
	for chan in range(1,10):

		freq = f0 + fdelt * chan
		bmap, fbeam, model = [], [], []

		for i,t in enumerate(files):
			hdu=fits.open(t)
			beam=hdu[0].data
			hdu.close()
			bmap.append(beam[chan,int(hdu[0].header['CRPIX2'])-20:int(hdu[0].header['CRPIX2'])+20,
						 int(hdu[0].header['CRPIX1'])-20:int(hdu[0].header['CRPIX1'])+20])
			x=arange(0,bmap[i].shape[1])
			y=arange(0,bmap[i].shape[0])
			fbeam.append(RectBivariateSpline(y,x,bmap[i]))  # spline interpolation
			model.append(fbeam[i](y,x)) # 40x40 pixel model

			h_measured['NAXIS1'] = 40
			h_measured['NAXIS2'] = 40
			h_measured['NAXIS3'] = 1
			h_measured['CRPIX1'] = 20.0
			h_measured['CRPIX2'] = 20.0
			header = h_measured

			hduI = fits.PrimaryHDU(fbeam[i](y,x), header=h_measured)
		
			if not os.path.exists(basedir + 'fits_files/{}/beam_models'.format(date)):
				os.mkdir(basedir + 'fits_files/{}/beam_models'.format(date))
			
			if not os.path.exists(basedir + 'fits_files/{}/beam_models/chann_{}'.format(date, chan)):
				os.mkdir(basedir + 'fits_files/{}/beam_models/chann_{}'.format(date, chan))

			hduI.writeto(basedir + 'fits_files/{}/beam_models/chann_{}/{}_{:02}_I_model.fits'.format(date, chan, date, i), overwrite=True)



if __name__ == '__main__':
    main()