# aperPB
Apertif primary beam characterization


1. prepare_drift_data.py -- Copies the .MS files from alta to happili and extracts the auto correlation data into .csv files.
2. scan2fits_spec.py -- Converts the drift scan data into fits image files for the individual beams
3. beam_spline_fitting.py -- Does a spline interpollation on all beams based on the fits files. And outputs the spline models into a .csv file.
