#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

#def set_val(tree, path, value):
#    tree.find(path).attrib["value"] = value

if len(sys.argv) < 3:
    print(sys.argv[0], "YearBuilt operim oarea fileid")
    sys.exit()

YearBuilt=sys.argv[1]
operim=float(sys.argv[2])
oarea=float(sys.argv[3])
fileid=sys.argv[3]

#t = ET.parse("template.h2k")
t = ET.parse("tmpl-oil.h2k")

t.find("./ProgramInformation/File").attrib["evaluationDate"] = "2021-11-18"
t.find("./ProgramInformation/File/Identification").text = fileid
#t.find("./House/Specifications/FacingDirection").attrib["code"] = FacingDirection
t.find("./House/Specifications/YearBuilt").attrib["value"] = YearBuilt

# calculate foundation and main floor area converted to metric
main_area=(oarea-operim/2+1)/SF_PER_SM
bsmt_area=(oarea-operim+4)/SF_PER_SM
hfa = t.find("./House/Specifications/HeatedFloorArea")
hfa.attrib["aboveGrade"] = str(main_area)
hfa.attrib["belowGrade"] = str(bsmt_area)

# calculate volume 7.75ft bsmt + header + 8ft main flr
volume=(7.75/FT_PER_M * bsmt_area) + (1 + 8)/FT_PER_M * main_area;
t.find(".House/NaturalAirInfiltration/Specifications/House").attrib["volume"] = str(volume)
m = t.find("House/Components/Ceiling/Measurements")
m.attrib["length"] = str(operim/FT_PER_M)
m.attrib["area"] = str(main_area)

#t.write("ghwiz-out.h2k", "UTF-8", True)
t.write(fileid + ".h2k", "UTF-8", True)

