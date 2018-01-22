# cloudyfsps

**Read the documentation:** [nell-byler.github.io/cloudyfsps](http://nell-byler.github.io/cloudyfsps/)

If you use this code, follow the citation requirements [on the FSPS homepage](https://github.com/cconroy20/fsps) and reference these Python bindings:

[![DOI](https://zenodo.org/badge/47210025.svg)](https://zenodo.org/badge/latestdoi/47210025)

#### Python interface between FSPS and Cloudy:
* Compile FSPS models for use as ionizing sources (Stellar SED grids) within Cloudy.

* Generate Cloudy input files, single-parameter or grids of parameters.

* Running Cloudy models (in parallel).

* Format output (nebular continuum and nebular line emission) for FSPS
  input, and for explorative manipulation and plotting within python.
  
* Pre-packaged plots for BPT diagram (NII, SII, OI, OII) with observed
  data from HII regions (Van Zee et al. 1998) and SDSS galaxies (DR7,
  generated using astroML). Comparisons with MAPPINGSIII models from
  Dopita (2013).

#### Prerequisites:
Cloudy (http://www.nublado.org/)  
FSPS (https://github.com/cconroy20/fsps)  
python-fsps (https://github.com/dfm/python-fsps)  

You must have the following system variables set: 
`$SPS_HOME`, `$CLOUDY_EXE`, `$CLOUDY_DATA_PATH`

#### To install:
```
git clone https://github.com/nell-byler/cloudyfsps.git 
cd cloudyfsps 
python setup.py install 
```

#### Basic usage:
Generate stellar SEDs from FSPS SSPs and compile them for use within Cloudy using [generateCloudyBinaryFile.py](demos/generateCloudyBinaryFile.py), then generate a grid of Cloudy input models with [exampleCloudyGrid.py](demos/exampleCloudyGrid.py).

This generates models ZAU1.in, ...ZAUn.in. Run each of these through Cloudy with:  
```
$CLOUDY_EXE -r ZAU1
```
For examples for how to run the full grid, see [runCloudy.sh](scripts/runCloudy.sh), which calls [runCloudy.py](scripts/runCloudy.py), or a clustered computing option at the bottom of [exampleCloudyGrid.py](demos/exampleCloudyGrid.py).

