#!/usr/bin/env python

"""
This program will read Apertif FITS files containing one beam map and fit them with RectBivariateSpline. 
The resulting spline fits are written into a .csv file.

input: 
- Date of the Drift scans

Example: python3 plot_beams.py -d '190722'

"""

import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import gridspec
import matplotlib.pyplot as plt
from scipy.stats import norm
from argparse import ArgumentParser, RawTextHelpFormatter

mpl.rcParams['font.family'] = 'serif'
#----------------------------------------------------

def parse_args():

    parser = ArgumentParser(
        description="Extract data from drift scans",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('-d', '--date', default='190722',
                        help="Date of maps to plot. (default: '190722').")

    args = parser.parse_args()
    return args


args = parse_args()
date = args.date


def make_beam_plots(date, chan):
    nrows = 7
    ncols = 7*2+1
    beams = 40
    size=40
    freq = 1234867750.0 + 18310500.0 * chan

    df_1 = pd.read_csv('/tank/apertif/driftscans/spline/{0}/beam_models_{0}_chann_{1}_pol_I.csv'.format(date, chan))

    fig = plt.figure(figsize=(14,12))
    gs = gridspec.GridSpec(nrows=nrows, ncols=ncols, figure=fig) 

    # Arrange the plots approx according to beam spacing (only beam 0 really fails)
    ax = [None] * beams
    for b in range(beams-1,-1,-1):
        if (b <= 39) & (b >= 33):
            ax[b] = fig.add_subplot(gs[0,2*(39-b):2*(39-b)+2])
        if (b <= 32) & (b >= 27):
            ax[b] = fig.add_subplot(gs[1,2*(32-b)+1:2*(32-b)+2+1])
        if (b <= 26) & (b >= 21):
            ax[b] = fig.add_subplot(gs[2,2*(26-b)+2:2*(26-b)+2+2])
        if (b == 0):
            ax[b] = fig.add_subplot(gs[3,2*3:2*3+2])
        if (b <= 20) & (b >= 15):
            ax[b] = fig.add_subplot(gs[4,2*(20-b)+1:2*(20-b)+2+1])
        if (b <= 14) & (b >= 8):
            ax[b] = fig.add_subplot(gs[5,2*(14-b):2*(14-b)+2])
        if (b <= 7) & (b >= 1):
            ax[b] = fig.add_subplot(gs[6,2*(7-b)+1:2*(7-b)+2+1])
        ax[b].set_xticks([])
        ax[b].set_yticks([])

    for b in range(beams):
        cb = np.array(df_1['B{:02d}_{}'.format(b, int(freq))]).reshape(size, size)
        ax[b].imshow(cb)
        ax[b].contour(cb, levels=[0,0.2,.4,.60,.80], colors='w')
        ax[b].set_title("Beam {}".format(b), size=10)

    fig.suptitle("Beam models {} chan {}".format(date, chan), size=18)    
    plt.savefig('/tank/apertif/driftscans/spline/{0}/{0}_beams_chan_{1}.png'.format(date, chan), dpi=100, bbox_inches="tight")

for i in range(1,10):
    make_beam_plots(date, i)