# aperPB
Apertif primary beam characterization


1. prepare_drift_data.py -- Copies the .MS files from alta to happili and extracts the auto correlation data into .csv files.

`python prepare_drift_data.py -f task_ids.txt`

2. scan2fits_spec.py -- Converts the drift scan data into fits image files for the individual beams. This script needs a file with a list of 31 drift scan task_ids - corresponding to 31 drifts across the field of view - to construct a fits file with the compaund beam shape. (The script also works for most beams if the first or the last task_ids are missing. However in this case beam 01 will most likely be corrupted.)

`python scan2fits_spec.py -f task_ids_190303.txt -d '190303'`

3. beam_spline_fitting.py -- Does a spline interpollation on all beams based on the fits files. And outputs the spline models into a .csv file. For this module to work it is imporatnt to have the full field of few fits files for all the beams, or to only have beams that are fully covered by drift scans (i.e. no beams that were only half scanned).

`python beam_spline_fitting.py -f task_ids_190303.txt -d '190303'`

4. make_beam_model.py -- creates fits files from the spline fits. These are 40x40 pixel.

`python make_beam_model.py -f task_ids_190303.txt -d '190303'`
