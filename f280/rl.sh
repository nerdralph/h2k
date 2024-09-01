#!/bin/sh

echo $0 $1

FID="0000D69$1"
DEST=($EA/$FID*)

echo dest = "$DEST"

./rooms.py $EA/$FID*/$FID-rooms.h2k > $DEST/$FID-room-loads.txt
