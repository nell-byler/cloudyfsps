# Using the precomputed tables of FSPS stellar SEDs within Cloudy

I have generated Flexible Stellar Population Synthesis stellar SEDs for anyone to use within Cloudy.
The SPS parameters used to generate the ascii files and the resultant nebular model are described in [Byler+2017](http://adsabs.harvard.edu/abs/2017ApJ...840...44B). 
The ascii files are available for download [here](https://drive.google.com/open?id=0B2_CMSJX44olb2lqVFJ3bzhRWTA).

### Compiling FSPS models
These ascii files can be compiled just like any other stellar SED grid in Cloudy:
```
compile star "FSPS_MIST_SSP.ascii"
```
or
```
compile star "FSPS_PDVA_SSP.ascii"
```
### Using the FSPS models in Cloudy

You can call the FSPS models directly in a Cloudy input file as a function of age and metallicity:
```
table star "FSPS_MIST_SSP.mod" 1.0e6 -1.5
```
which would request a 1 Myr SSP with logZ/Zsun = -1.5.
