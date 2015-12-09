#!/bin/csh
# $1: $2:savedir $3:start $4:end
if ($# != 4) then
    echo "Usage: mk_linefile 1[full/path/wavfile] 2[save/dir/path/prefix] 3[start] 4[end]"
    exit
endif
set wavfile = $1
@ i = $3
while ($i <= $4)
    set name=$2$i'.lineflux'
    set oldname=$2$i'.lin'
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

