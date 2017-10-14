
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

Generate stellar SEDs from FSPS SSPs and compile them for use within Cloudy using [generateCloudyBinaryFile.py](demos/generateCloudyBinaryFile.py), then generate a grid of Cloudy input models with [exampleCloudyGrid.py](demos/exampleCloudyGrid.py).

This generates models ZAU1.in, ...ZAUn.in. Run each of these through Cloudy with:  
```
$CLOUDY_EXE -r ZAU1
```
For examples for how to run the full grid, see [runCloudy.sh](scripts/runCloudy.sh), which calls [runCloudy.py](scripts/runCloudy.py), or a clustered computing option at the bottom of [exampleCloudyGrid.py](demos/exampleCloudyGrid.py).

