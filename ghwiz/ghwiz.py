#!/usr/bin/python

import os
import sys
import xml.etree.ElementTree as ET

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

if len(sys.argv) < 3:
    # print(sys.argv[0], "wall-height operim oarea fileid template")
    print(sys.argv[0], "wall-height operim oarea fileid")
    sys.exit()

# wall height in metres
wall_height_m=float(sys.argv[1])/FT_PER_M
operim=float(sys.argv[2])
oarea=float(sys.argv[3])
fileid=sys.argv[4]
#template=sys.argv[5] + ".h2k"
template="tmpl-oil.h2k"

t = ET.parse(template)

#t.find("./ProgramInformation/File").attrib["evaluationDate"] = "2021-11-18"
t.find("./ProgramInformation/File/Identification").text = fileid
#t.find("./House/Specifications/FacingDirection").attrib["code"] = FacingDirection
#t.find("./House/Specifications/YearBuilt").attrib["value"] = YearBuilt

# calculate foundation and main floor area converted to metric
main_area=(oarea-operim/2+1)/SF_PER_SM
bsmt_area=(oarea-operim+4)/SF_PER_SM
hfa = t.find("./House/Specifications/HeatedFloorArea")
hfa.attrib["aboveGrade"] = str(main_area)
hfa.attrib["belowGrade"] = str(bsmt_area)

# calculate volume 7.75ft bsmt + header + 8ft main flr
volume=((7.75 + 1)/FT_PER_M * bsmt_area) + wall_height_m * main_area;
t.find(".House/NaturalAirInfiltration/Specifications/House").attrib["volume"] = str(volume)
# calculate highest ceiling height
# template has 4' pony, so add 4.5 + 1' to wall height
highest_ceiling = (4.5 +1)/FT_PER_M + wall_height_m 
t.find(".House/NaturalAirInfiltration/Specifications/BuildingSite").attrib["highestCeiling"] = str(highest_ceiling)

m = t.find("House/Components/Ceiling/Measurements")
m.attrib["length"] = str(operim/FT_PER_M)
m.attrib["area"] = str(main_area)

m = t.find("House/Components/Wall/Measurements")
m.attrib["height"] = str(wall_height_m) 
m.attrib["perimeter"] = str((operim-4)/FT_PER_M)

# calculate foundation perim & area
bsmt_perim = (operim-8)/FT_PER_M
t.find("House/Components/Basement").attrib["exposedSurfacePerimeter"] = str(bsmt_perim)
m = t.find("House/Components/Basement/Floor/Measurements")
m.attrib["area"] = str(bsmt_area)
m.attrib["perimeter"] = str(bsmt_perim)

t.write(fileid + ".h2k", "UTF-8", True)
os.system("unix2dos " + fileid + ".h2k")

