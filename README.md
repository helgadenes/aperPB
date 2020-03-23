# aperPB
Apertif primary beam characterization


1. prepare_drift_data.py -- Copies the .MS files from alta to happili and extracts the auto correlation data into .csv files.
2. scan2fits_spec.py -- Converts the drift scan data into fits image files for the individual beams
3. beam_spline_fitting.py -- Does a spline interpollation on all beams based on the fits files. And outputs the spline models into a .csv file. For this module to work it is imporatnt to have the full vield of few fits files for all the beams, or to only have beams that are fully covered by drift scans (i.e. no beams that were only half scanned).
4. make_beam_model.py -- creates fits files from the spline fits. These are 40x40 pixel.
