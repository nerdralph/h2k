#!/usr/bin/python

import photos

#from datetime import date
import math, os, sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 3:
    print(sys.argv[0], "D.h2k E-ID")
    sys.exit()

d_file = sys.argv[1]
fileid = sys.argv[2]

t = ET.parse(d_file)

v = t.find("Program/Version").attrib["build"]
print (d_file + " version " + v)

YHZ_CODE = "166"
CURRENT_VER = "21119"
if v != CURRENT_VER:
    pi = t.find("ProgramInformation")
    pi.find("Weather").attrib["library"] = "Wth2020.dir"
    pi.find("Weather/Location").attrib["code"] = YHZ_CODE
    pijo = pi.find("Justifications/Other")
    pijo.attrib["selected"] = "true"
    pijo.text = "v11.11b35 update"
    t.find("FuelCosts").attrib["includeCostCalculations"] = "false"
    t.find("FuelCosts").attrib["library"] = "FuelLib.flc"
    print("Set weather and FCL for upgrade to " + CURRENT_VER)
    print("Open " + d_file + " in H2K and save to complete upgrade.")
    t.write("../../" + d_file, "UTF-8", True)
    os.remove(d_file)
    sys.exit(1)

# extract photos
ymd = photos.extract(fileid)

#t.find("./ProgramInformation/File").attrib["evaluationDate"] = date.today().isoformat()
t.find("./ProgramInformation/File").attrib["evaluationDate"] = ymd
t.find("./ProgramInformation/File/PreviousFileId").text = \
    t.find("./ProgramInformation/File/Identification").text
t.find("./ProgramInformation/File/Identification").text = fileid
t.find("./ProgramInformation/File/EnteredBy").text = "Ralph Doncaster"
t.find("./ProgramInformation/File/UserTelephone").text = "902-401-7056"
t.find("./ProgramInformation/File/CompanyTelephone").text = "902-469-1119"

t.getroot().remove(t.find("./AllResults"))
t.find("./Program").remove(t.find("./Program/Results"))
t.getroot().remove(t.find("./EnergyUpgrades"))

outfile = "../../" + fileid + ".h2k"
t.write(outfile, "UTF-8", True)

