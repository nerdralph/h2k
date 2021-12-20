#!/usr/bin/python

from datetime import date
import math, os, sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 3:
    print(sys.argv[0], "D.h2k E-ID")
    sys.exit()

d_file = sys.argv[1]
fileid = sys.argv[2]

t = ET.parse(d_file)

t.find("./ProgramInformation/File").attrib["evaluationDate"] = date.today().isoformat()
t.find("./ProgramInformation/File/PreviousFileId").text = \
    t.find("./ProgramInformation/File/Identification").text
t.find("./ProgramInformation/File/Identification").text = fileid
t.find("./ProgramInformation/File/EnteredBy").text = "Ralph Doncaster"
t.find("./ProgramInformation/File/UserTelephone").text = "902-401-7056"
t.find("./ProgramInformation/File/CompanyTelephone").text = "902-469-1119"

t.getroot().remove(t.find("./AllResults"))
t.find("./Program").remove(t.find("./Program/Results"))
t.getroot().remove(t.find("./EnergyUpgrades"))

outfile = fileid + ".h2k"
t.write(outfile, "UTF-8", True)

# extract photos
os.system("./photos.py " + fileid)
