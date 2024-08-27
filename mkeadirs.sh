#!/bin/bash
# Ralph Doncaster public domain software

. ./dircfg.sh

echo source = $EASOURCE, dest = $EADEST

for file in `find $EASOURCE -name "*.pdf"`; do
    #ID="$(basename $file .pdf)"
    # strip path and .pdf
    # see bash manual ${parameter%word} in trailing portion match section
    match=${file%.pdf}
    id=${match##*/}
    if [ -e $EADEST/$id* ]
    then
        echo $id exists
    else
        echo create $id
        mkdir $EADEST/$id
        cp $EASOURCE/$id* $EADEST/$id
    fi
done
