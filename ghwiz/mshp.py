#!/usr/bin/python
# configure mini-split heat pumps for E files

import csv, math, os, sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 3:
    print(sys.argv[0], "E-file.h2k AHRI heads")
    sys.exit()

e_file = sys.argv[1]
ahri = sys.argv[2]
heads = sys.argv[3]

t = ET.parse(e_file)

# tsv field list: 
# Product group	AHRI  No.	Brand Name	Series Name/Product Line (if applicable)	Outdoor Unit Model	System type	Indoor Type/ Ducting Configuration	Indoor Unit - Model Number  (Evaporator and/or Air Handler)	Furnace Model Number (if applicable)	Rated heating capacity 8.3°C/47°F  Btu/hour 	HSPF  (Region IV)  Btu/(W⋅h)	COP at Max. Capacity  -15°C/5°F	Capacity Maintenance %  (Max -15°C/5°F ÷ Rated 8.3°C/47°F) Btu/hour 	Rated Cooling Capacity 35°C/95°F   Btu/hour	SEER  Btu/(W⋅h)	Grant amount
cchp_search = "grep -i '" + ahri + "' ccashp.tsv|grep -v Ducted"
d = os.popen(cchp_search).read().split('\t')
(mfr, model, size_kw, hspf, cop, seer) = d[2], d[4], str(float(d[9])/3412), d[10], d[11], d[14]
#cchp_search = "grep -i '" + mfr + ".*" + model + "' ccashp.csv"
#row = os.popen(cchp_search).read()
#cols = next([row])
#(ahri, size_kw, hspf, cop, seer) = cols[9], str(float(cols[5])/3412), cols[4], cols[13], cols[12] 

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

#outfile = "MSHP-out.h2k"
outfile = e_file
t.write(outfile, "UTF-8", True)

