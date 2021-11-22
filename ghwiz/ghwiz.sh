#!/bin/sh

# globals
indent="        "
sfpersm=10.7584

cat header.ghw

evaldate=`date -I --date='7 days ago'`
echo "$indent<File evaluationDate=\"$evaldate\">"

cat fileid.ghw

echo "$indent<FacingDirection code=\"$1\" />"
echo "$indent<YearBuilt code="1" value=\"$2\" />"
echo "$indent<HeatedFloorArea aboveGrade=\"60.6\" belowGrade=\"56.5\" />"

operim=$3
oarea=$4

# calculate foundation and main floor area converted to metric
let marea=($oarea-$operim/2+1)/$sfpersm
let farea=($oarea-$operim+4)/$sfpersm
echo "marea: $marea"
echo "farea: $farea"

