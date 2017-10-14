## Using cloudyFSPS

* Generate and format FSPS models and compile them for use as ionizing sources (Stellar SED grids) within Cloudy.

* Generate Cloudy input files, either single-parameter or grids of parameters.

* Run Cloudy models using basic shell script or format runs for clustered computing.

* Format Cloudy output files into nice units for explorative manipulation and plotting within python.

* Format Cloudy output for use within FSPS.
  
* Pre-packaged plots for BPT diagram (NII, SII, OI, OII) with observed
  data from HII regions (van Zee+1998) and SDSS galaxies (DR7,
  generated using astroML). Comparisons with MAPPINGSIII models from
  Dopita+2013.

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
## Using the precomputed tables of FSPS stellar SEDs within Cloudy

I have generated Flexible Stellar Population Synthesis stellar SEDs for anyone to use within Cloudy:

https://drive.google.com/open?id=0B2_CMSJX44olb2lqVFJ3bzhRWTA

These can be compiled just like any other stellar SED grid:

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/nell-byler/cloudyfsps/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
