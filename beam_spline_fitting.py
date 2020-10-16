# 6/13/19 DJP
# edited by K.M. Hess and H. Denes

__author__ = "DJP"
__date__ = "$04-jun-2019 16:00:00$"
__version__ = "0.2"

"""
This program will read Apertif FITS files containing one beam map and fit them with RectBivariateSpline. 
The resulting spline fits are written into a .csv file.

input: 
- A date that has beam fits files in the base directory /tank/apertif/driftscans/

Example: python beam_spline_fitting.py -d '190303'

"""


from glob import glob
import os
from scipy.interpolate import RectBivariateSpline
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
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
    
    if not os.path.exists(basedir + 'spline/{}/'.format(date)):
		os.mkdir(basedir + 'spline/{}/'.format(date))
    	    
    for pol in ['I', 'xx', 'yy']:
		files=glob('{}/fits_files/{}/CygA_{}_*{}.fits'.format(basedir, date, date, pol)) 
		files.sort()

		hdu=fits.open(files[0])
		beam=hdu[0].data
		f0=hdu[0].header['CRVAL3']
		fdelt=hdu[0].header['CDELT3']
		hdu.close()
		px_width = 20

		for chan in range(1,10):
			freq = f0 + fdelt * chan
			bmap, fbeam, model = [], [], []

			for i,t in enumerate(files):
				hdu=fits.open(t)
				beam=hdu[0].data
				beam = np.nan_to_num(beam)
				hdu.close()
				bmap.append(beam[chan,int(hdu[0].header['CRPIX2'])-px_width:int(hdu[0].header['CRPIX2'])+px_width,
							 int(hdu[0].header['CRPIX1'])-px_width:int(hdu[0].header['CRPIX1'])+px_width])
				x=arange(0,bmap[i].shape[1])
				y=arange(0,bmap[i].shape[0])
				fbeam.append(RectBivariateSpline(y,x,bmap[i]))  # spline interpolation
				model.append(fbeam[i](y,x)) # 40x40 pixel model


			df = pd.DataFrame()
			maxlen = len(model[0].flatten())
			for b,m in enumerate(model):
				col = list(m.flatten())
				if maxlen != len(col):
					col.extend(['']*(maxlen-len(col)))
				df['B{:02}_{}'.format(b,int(freq))] = col   #the column name is the beam number and the frequency
			
			
			df.to_csv('{}/spline/{}/beam_models_{}_chann_{}_pol_{}.csv'.format(basedir, date, date, chan, pol))


if __name__ == '__main__':
    main()