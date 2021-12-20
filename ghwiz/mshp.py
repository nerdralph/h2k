#!/usr/bin/python
# configure mini-split heat pumps for E files

import math, os, sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 4:
    print(sys.argv[0], "E-file mfr model heads")
    sys.exit()

e_file = sys.argv[1]
mfr = sys.argv[2].upper()
model = sys.argv[3].upper()
heads = sys.argv[4]

t = ET.parse(e_file)

cchp_search = "grep -i '" + mfr + ".*" + model + "' ccashp.tsv|grep -v Ducted"
d = os.popen(cchp_search).read().split('\t')
(ahri, size_kw, hspf, cop, seer) = d[1], str(float(d[9])/3412), d[10], d[11], d[14]

e = t.find("./ProgramInformation/Information")

info = ET.Element("Info", {"code": "Info. 5"})
info.text = "MSHP-" + heads
e.append(info)

info = ET.Element("Info", {"code": "Info. 6"})
info.text = mfr + "; ARHI " + ahri + "; " + model 
e.append(info)

#print(info, info.attrib, info.text)

# Type 2 CCHP heating system
type2 = ET.parse("Type2.xml").getroot()
ahp = type2.find("AirHeatPump")
ei = ahp.find("EquipmentInformation")
ei.attrib["AHRI"] = ahri
ei.find("Manufacturer").text = mfr
ei.find("Model").text = model
ahp.find("Equipment").attrib["numberOfHeads"] = heads
specs = ahp.find("Specifications")
specs.find("OutputCapacity").attrib["value"] = size_kw
# HeatingEfficiency is HSPF V, so divide by 1.15
specs.find("HeatingEfficiency").attrib["value"] = str(float(hspf)/1.15)
specs.find("CoolingEfficiency").attrib["value"] = seer
cchp = ahp.find("ColdClimateHeatPump")
cchp.attrib["heatingEfficiency"] = hspf
cchp.attrib["coolingEfficiency"] = seer
cchp.attrib["capacity"] = size_kw
cchp.attrib["cop"] = cop

hc = t.find("./House/HeatingCooling")
hc.remove(hc.find("Type2"))
hc.append(type2)

outfile = "MSHP-E.h2k"
t.write(outfile, "UTF-8", True)

