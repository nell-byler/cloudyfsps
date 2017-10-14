# About cloudyFSPS

cloudyFSPS uses Flexible Stellar Population Synthesis (FSPS) models as the ionizing source input to Cloudy. The package can be used to:

* Generate and format FSPS models and compile them for use as ionizing sources (Stellar SED grids) within Cloudy.

* Generate Cloudy input files, either single-parameter or grids of parameters.

* Run Cloudy models using basic shell script or format runs for clustered computing.

* Format Cloudy output files into nice units for explorative manipulation and plotting within python.

* Format Cloudy output for use within FSPS.

* Pre-packaged plots for BPT diagram (NII, SII, OI, OII) with observed
  data from HII regions (van Zee+1998) and SDSS galaxies (DR7,
  generated using astroML). Comparisons with MAPPINGSIII models from
  Dopita+2013.

## [Installation and Usage](https://nell-byler.github.io/cloudyfsps/installation.html)
For instructions on how to install and use cloudyFSPS.

# Using the pre-computed FSPS stellar SEDs in Cloudy

As described in [Byler+2017](http://adsabs.harvard.edu/abs/2017ApJ...840...44B), I have generated tables of FSPS stellar SEDs for anyone to use within Cloudy. Instructions for usage and downloads can be found [here](https://nell-byler.github.io/cloudyfsps/tables.html).
