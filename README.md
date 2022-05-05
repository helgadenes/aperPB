# aperPB
Apertif primary beam characterization. The beam maps created with these scripts are used for mosaicing and primary beam correction.


1. prepare_drift_data.py -- Copies the .MS files from alta to happili and extracts the auto correlation data into .csv files.

`python prepare_drift_data.py -f task_ids_190821.txt`

2. scan2fits_spec.py -- Converts the drift scan data into fits image files for the individual beams. This script needs a file with a list of 31 or 33 drift scan task_ids - corresponding to 31 drifts across the field of view - to construct a fits file with the compaund beam shape. (The script also works if one or two task_ids are missing.)

`python scan2fits_spec.py -f task_ids_190821.txt -d '190821' -c 'Cyg A'`

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

The jupyter notebooks to analyse the properties of the CB maps are located in the directory called CB_analysis. 
