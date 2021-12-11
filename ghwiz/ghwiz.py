#!/usr/bin/python

import math, os, sys
import xml.etree.ElementTree as ET

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

if len(sys.argv) < 4:
    print(sys.argv[0], "wall-height operim oarea fileid template")
    sys.exit()

# wall height in metres
wall_height_m=float(sys.argv[1])/FT_PER_M
operim=float(sys.argv[2])
oarea=float(sys.argv[3])
fileid=sys.argv[4]
#template="tmpl-oil.h2k"
template=sys.argv[5] + ".h2k"

storeys = 2 if wall_height_m > 4 else 1

# for semis subtract 1/2 of the common-wall length from the area

t = ET.parse(template)

#t.find("./ProgramInformation/File").attrib["evaluationDate"] = "2021-11-18"
t.find("./ProgramInformation/File/Identification").text = fileid
#t.find("./House/Specifications/FacingDirection").attrib["code"] = FacingDirection
#t.find("./House/Specifications/YearBuilt").attrib["value"] = YearBuilt

# calculate foundation and main floor area converted to metric
main_area=(oarea-operim/2+1)/SF_PER_SM
bsmt_area=(oarea-operim+4)/SF_PER_SM
hfa = t.find("./House/Specifications/HeatedFloorArea")
hfa.attrib["aboveGrade"] = str(main_area * storeys)
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
# H2K errror if perim <= 4*sqrt(area)
m.attrib["perimeter"] = str(math.sqrt(bsmt_area)*4 + 0.2)

# write prepared h2k file
outfile = "../../" + fileid + ".h2k"
t.write(outfile, "UTF-8", True)
os.system("unix2dos " + outfile)

# copy stick-framed 2x6 house specs
os.system("cp 2x6-house.txt " + "../../" + fileid + "/" + fileid + "-house-data.txt")

