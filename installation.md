
# Installation

### Prerequisites
cloudyFSPS relies on the use of the following packages:

Cloudy (http://www.nublado.org/)  
FSPS (https://github.com/cconroy20/fsps)  
python-fsps (https://github.com/dfm/python-fsps)  

You must have the following system variables set: 
`$SPS_HOME`, `$CLOUDY_EXE`, `$CLOUDY_DATA_PATH`

### Command line installation
```
git clone https://github.com/nell-byler/cloudyfsps.git 
cd cloudyfsps 
python setup.py install 
```
# Basic usage:

Generate stellar SEDs from FSPS SSPs and compile them for use within Cloudy using [generateCloudyBinaryFile.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/generateCloudyBinaryFile.py).  

Generate a grid of Cloudy input files with [exampleCloudyGrid.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/exampleCloudyGrid.py). This generates files ZAU1.in, ..., ZAUn.in. Each of these can be run with Cloudy using the standard command:  
```
$CLOUDY_EXE -r ZAU1
```

Examples for how to run the full grid of files can be found in [runCloudy.sh](https://github.com/nell-byler/cloudyfsps/blob/master/scripts/runCloudy.sh), or formatting for a clustered computing option at the bottom of [exampleCloudyGrid.py](https://github.com/nell-byler/cloudyfsps/blob/master/demos/exampleCloudyGrid.py).

