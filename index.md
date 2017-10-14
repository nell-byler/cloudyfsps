# Using the pre-computed FSPS tables in Cloudy

As described in [Byler+2017](http://adsabs.harvard.edu/abs/2017ApJ...840...44B), I have generated tables of FSPS stellar SEDs for anyone to use within Cloudy. Instructions for usage and downloads can be found [here](https://nell-byler.github.io/cloudyfsps/tables.html).

# About cloudyFSPS
The pre-computed tables are run for specific stellar libraries, evolutionary tracks, IMF, etc. 
In spirit of maintaining the "flexible" part of FSPS, you can generate grids of stellar SEDs in the proper Cloudy-readable ascii file format for *any* combination of FSPS parameters using cloudyFSPS.

## [Installation and Usage](https://nell-byler.github.io/cloudyfsps/installation.html)

The cloudyFSPS package can be used to:

* Generate and format FSPS models and compile them for use as ionizing sources (Stellar SED grids) within Cloudy.

* Generate Cloudy input files, either single-parameter or grids of parameters.

* Run Cloudy models using basic shell script or format runs for clustered computing.

* Format Cloudy output files into nice units for explorative manipulation and plotting within python.

* Format Cloudy output for use within FSPS.

* Pre-packaged plots for BPT diagram (NII, SII, OI, OII) with observed
  data from HII regions (van Zee+1998) and SDSS galaxies (DR7,
  generated using astroML). Comparisons with MAPPINGSIII models from
  Dopita+2013.


