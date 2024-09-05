#!/bin/sh

echo $0 $1 $2

FID="0000D69$1"
DEST=($EA/$FID*)
echo dest = "$DEST"

./roomgen.py $EA/$FID*/$FID.h2k $2
cp rg-out.h2k $DEST/$FID-rooms.h2k
