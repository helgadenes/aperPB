# aperPB
These scripts are used to create beam maps of the 40 Apertif compound beams (CBs) from drift scan observations. The CB maps created with these scripts can be used for primary beam correcting and mosaicing Apertif observations. The CB maps are also used to better understand the characteristics of the Apertif system.

Associated publications: Dénes et al. 2022. accepted to A&A, "Characterising the Apertif primary beam response" ArXiv: https://arxiv.org/abs/2205.09662

DOI for aperPB:
[![DOI](https://zenodo.org/badge/203768438.svg)](https://zenodo.org/badge/latestdoi/203768438)

## Description of the scripts that are used to create the maps

1. prepare_drift_data.py -- Copies the .MS files from alta to happili and extracts the auto correlation data into .csv files.

`python prepare_drift_data.py -f task_ids_190821.txt`

2. scan2fits_spec_old.py  and scan2fits_spec_new.py -- Converts the drift scan data into fits image files for the individual beams for the old and the new frequency settings of Apertif observations. This script needs a file with a list of 31 or 33 drift scan task_ids - corresponding to the drifts across the field of view - to construct a fits file with the compaund beam shape. (The script also works if one or two task_ids are missing and fewer drifts are provided.)

`python scan2fits_spec_old.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

`python scan2fits_spec_new.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

3. scan2fits_spec_ant.py -- Converts the drift scan data into fits image files for the individual beams per antenna for the old and the new frequency setting. This script needs a file with a list of 31 or 33 drift scan task_ids - corresponding to 31 drifts across the field of view - to construct a fits file with the compaund beam shape. 

`python scan2fits_spec_ant_old.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

`python scan2fits_spec_ant_new.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

4. beam_spline_fitting.py -- Does a spline interpollation on all beams based on the fits files. And outputs the spline models into a .csv file. For this module to work it is imporatnt to have the full field of few fits files for all the beams, or to only have beams that are fully covered by drift scans (i.e. no beams that were only halfway scanned).

`python beam_spline_fitting.py -d '190821' -c 'Cyg A'`

5. make_beam_model.py -- creates fits files from the spline fits. These are 40x40 pixel.

`python make_beam_model.py -d '190821' -c 'Cyg A'`

6. make_beam_model_ant.py -- creates fits files from the spline fits for each individual antenna in the observation. These are 40x40 pixel.

`python make_beam_model_ant.py -d '190821' -c 'Cyg A'`

Beam maps for each frequency bin can be plotted with:

`Example: python3 plot_beams.py -d '190821'`

## Additional scripts

The directory called CB_analysis contains additional jupyter notebooks that can be used to analyse the properties of the CB maps. 

## Version history

* aperPB v1.0
  * Release 12 May 2022

## Authors

Helga Dénes, Kelley M. Hess, and D. J. Pisano

## Copyright and license

© 2022 Helga Dénes

This programme is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free 
Software Foundation, either version 3 of the License, or (at your option) any 
later version.

This programme is distributed in the hope that it will be useful, but **without 
any warranty**; without even the implied warranty of **merchantability** or **fitness 
for a particular purpose**. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this programme. If not, see http://www.gnu.org/licenses/.
