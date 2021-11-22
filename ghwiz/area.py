#!/usr/bin/python

import sys

operim=float(sys.argv[1])
oarea=float(sys.argv[2])

marea=(oarea-operim/2+1)/10.7584
farea=oarea-operim+4
print("marea:", marea)
print("farea:", farea)
