#!/bin/sh
echo $PATH
echo $PYTHONPATH
echo $CLOUDY_EXE
suffix='.in'
mod_prefix=$2$3
infile=$mod_prefix$suffix
dir=$1
echo $dir
echo $infile
echo "Running CLOUDY on $infile"
cd $dir && $CLOUDY_EXE -r $mod_prefix
echo "CLOUDY finished $infile"
suffix='.out'
outfile="$dir/$mod_prefix$suffix"
echo $outfile
if [ -f $outfile ];
then
  echo "File $outfile exists."
  echo "Running python..."
  python runCloudy.py $outfile
  echo "Python finished."
else
  echo "ERROR: file $outfile does NOT exist."
fi
echo "Done."
