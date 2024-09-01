#!/bin/sh

echo $0 $1

FID="0000D69$1"
DEST=($EA/$FID*)
echo dest = "$DEST"

./roomgen.py $EA/$FID*/$FID.h2k
cp rg-out.h2k $DEST/$FID-rooms.h2k
