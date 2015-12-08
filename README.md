# cloudyfsps
===
Python interface between FSPS and Cloudy.

* Compile FSPS models for use as ionizing sources within Cloudy.

* Generate Cloudy input files, single-parameter or grids of parameters.

* Running Cloudy models (in parallel).

* Format output (nebular continuum and nebular line emission) for FSPS
  input, and for explorative manipulation and plotting within python.
  
* Pre-packaged plots for BPT diagram (NII, SII, OI, OII) with observed
  data from HII regions (Van Zee et al. 1998) and SDSS galaxies (DR7,
  generated using astroML). Comparisons with MAPPINGSIII models from
  Dopita (2013).

Must have:
Cloudy (http://www.nublado.org/), 
FSPS (https://github.com/cconroy20/fsps),
python-fsps (https://github.com/dfm/python-fsps)

and relies on the following system variables:
$SPS_HOME, $CLOUDY_EXE