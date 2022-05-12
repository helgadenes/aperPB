# aperPB
These scripts are used to creat beam maps of the 40 Apertif compound beams (CBs) from drift scan observations. The CB maps created with these scripts can be used for primary beam correcting and mosaicing Apertif observations. The CB maps are also used to better understand the characteristics of the Apertif system.

Associated publications: Dénes et al. 2022 in prep, "Characterising the Apertif primary beam response"

## Description of the scripts that are used to create the maps

1. prepare_drift_data.py -- Copies the .MS files from alta to happili and extracts the auto correlation data into .csv files.

`python prepare_drift_data.py -f task_ids_190821.txt`

2. scan2fits_spec_old.py  and scan2fits_spec_new.py -- Converts the drift scan data into fits image files for the individual beams for the old and the new frequency settings of Apertif observations. This script needs a file with a list of 31 or 33 drift scan task_ids - corresponding to the drifts across the field of view - to construct a fits file with the compaund beam shape. (The script also works if one or two task_ids are missing and fewer drifts are provided.)

`python scan2fits_spec_old.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'` //
`python scan2fits_spec_new.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

3. scan2fits_spec_ant.py -- Converts the drift scan data into fits image files for the individual beams per antenna. This script needs a file with a list of 31 or 33 drift scan task_ids - corresponding to 31 drifts across the field of view - to construct a fits file with the compaund beam shape. 

`python scan2fits_spec_ant.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

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

