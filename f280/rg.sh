#!/bin/sh

echo $0 $1

FID="0000D69$1"
./roomgen.py $EA/$FID*/$FID.h2k
cp rg-out.h2k $EA/$FID*/$FID-rooms.h2k
