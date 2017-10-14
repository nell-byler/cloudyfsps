
# Installation

### Prerequisites
cloudyFSPS relies on the use of the following packages:

Cloudy ([http://www.nublado.org/](http://www.nublado.org/))  
FSPS ([https://github.com/cconroy20/fsps](https://github.com/cconroy20/fsps))  
python-fsps ([https://github.com/dfm/python-fsps](https://github.com/dfm/python-fsps))  

You must have the following system variables set: 
`$SPS_HOME`, `$CLOUDY_EXE`, `$CLOUDY_DATA_PATH`

### Command line installation
```
git clone https://github.com/nell-byler/cloudyfsps.git 
cd cloudyfsps 
python setup.py install 
```
# Basic usage

### Generate and compile Cloudy formatted ascii files
To start, generate stellar SEDs from FSPS SSPs and compile them for use within Cloudy using [generateCloudyBinaryFile.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/generateCloudyBinaryFile.py).

Simply run the script:
```
python generateCloudyBinaryFile.py
```
Which generates `FSPS_MIST_SSP.ascii` using FSPS models as a function of SSP age and SSP metallicity.  


A more complicated example of generating a compiled Cloudy table can be found in [fbhb.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/fbhb.py), which generates an ascii file that varies in metallicity and `fbhb`, the fraction of horizontal branch stars that are blue.
```
table star FSPS_FBHB.mod -1.0 0.5
```
would request the spectrum for a model with logZ/Zsun = -1.0 and where half of the horizontal branch stars are blue.

### Generate Cloudy input files
You can generate a grid of Cloudy input files with [exampleCloudyGrid.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/exampleCloudyGrid.py). This generates files ZAU1.in, ..., ZAUn.in. Each of these can be run with Cloudy using the standard command:  
```
$CLOUDY_EXE -r ZAU1
```

### Running Cloudy models
Examples for how to run the full grid of files can be found in [runCloudy.sh](https://github.com/nell-byler/cloudyfsps/blob/master/scripts/runCloudy.sh), or formatting for a clustered computing option at the bottom of [exampleCloudyGrid.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/exampleCloudyGrid.py).

