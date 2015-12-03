#!/bin/csh
# $1: $2:savedir $3:start $4:end
if ($# != 4) then
    echo "Usage: mk_linefile [current/dir/path] [save/dir/path] [start] [end]"
    exit
endif
set wavfile = $1'data/shell_lambda.dat'
@ i = $3
while ($i <= $4)
    echo '****ZAU model '$i'****'
    set name=$2'/ZAU'$i'.lineflux'
    set oldname=$2'/ZAU'$i'.lin'
    echo $name
    echo $oldname
    cp $oldname $name
    echo 'created line file'
    awk 'NR > 2 { print }' $name > $name'short'
    awk '{print substr($0,16)}' $name'short' > $name'clean'
    awk 'NR==FNR{a[NR]=$1; next}{print a[FNR],$1}' $wavfile $name'clean' > $name'together'
    mv $name'together' $name
    rm $name'clean'
    rm $name'short'
    @ i += 1
end

