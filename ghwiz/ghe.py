#!/usr/bin/python

import math, os, sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 3:
    print(sys.argv[0], "D.h2k E-ID")
    sys.exit()

ea = "22RD"
d_file = sys.argv[1]
fileid = ea + sys.argv[2]

t = ET.parse(d_file)

t.find("./ProgramInformation/File/PreviousFileId").text = \
    t.find("./ProgramInformation/File/Identification").text
t.find("./ProgramInformation/File/Identification").text = fileid
t.find("./ProgramInformation/File/EnteredBy").text = "Ralph Doncaster"
t.find("./ProgramInformation/File/UserTelephone").text = "902-401-7056"
t.find("./ProgramInformation/File/CompanyTelephone").text = "902-469-1119"

t.getroot().remove(t.find("./AllResults"))
#t.getroot().remove(t.find("./Program/Results"))
t.find("./Program").remove(t.find("./Program/Results"))
t.getroot().remove(t.find("./EnergyUpgrades"))

outfile = fileid + ".h2k"
t.write(outfile, "UTF-8", True)

