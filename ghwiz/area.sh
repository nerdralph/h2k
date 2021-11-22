#!/bin/sh

operim=$1
oarea=$2

let marea=($oarea-$operim/2+1)/10.7584
let farea=$oarea-$operim+4
echo "marea: $marea"
echo "farea: $farea"
