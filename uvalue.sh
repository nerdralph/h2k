#!/bin/sh
# call with h2k file name
# sets all ENERGYSTAR upgrade windows to <1.22 for Greener Homes requirements

perl -p -i -e 's/uValueMin="1\.22"/uValueMin="1.05" uValueMax="1.22"/' $1

