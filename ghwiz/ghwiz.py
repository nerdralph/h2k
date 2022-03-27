#!/usr/bin/python
# Ralph Doncaster 2021, 2022
# Greener Homes wizard: creates H2K house models from templates

import photos

import math, os, sys
import xml.etree.ElementTree as ET

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

if len(sys.argv) < 6:
    print(sys.argv[0], "fileid template.h2k wall-height operim barea [tadelta]")
    sys.exit()

args = sys.argv
fileid = args.pop(1)
template = args.pop(1)
# wall height in metres
wall_height_m = float(args.pop(1))/FT_PER_M
# outside wall perimeter
operim = float(args.pop(1))
# basement exterior area
barea = float(args.pop(1))
# top floor exterior area difference from barea
ta_delta = float(args.pop(1)) if len(args) > 1 else 0

t = ET.parse(template)

# extract photos
ymd = photos.extract(fileid)

# sample appointment text:
# 123 Main St, Dartmouth, NS B1H 0H0 John MacDonald 902-555-1212
info = input("client info: ")
(street, city, rest) = info.split(',')
# skip over prov if present - set in h2k template
if rest[0:3] == " NS":
    rest = rest[3:]
(postal, name, tel) = rest[1:8], rest[9:-10],rest[-12:]

c = t.find("./ProgramInformation/Client")
c.find("Name/First").text = name.split(' ')[0]
c.find("Name/Last").text = name.split(' ')[1]
c.find("Telephone").text = tel
sa = c.find("StreetAddress")
sa.find("Street").text = street
sa.find("City").text = city
# province set in h2k template
sa.find("PostalCode").text = postal

t.find("ProgramInformation/File").attrib["evaluationDate"] = ymd
t.find("ProgramInformation/File/Identification").text = fileid
#t.find("./House/Specifications/FacingDirection").attrib["code"] = FacingDirection
#t.find("./House/Specifications/YearBuilt").attrib["value"] = YearBuilt

storeys = 2 if wall_height_m > 4 else 1
# code 1 = 1 storey, 3 = 2 storey
t.find("House/Specifications/Storeys").attrib["code"] = "1" if storeys == 1 else "3"

# calculate foundation and main floor area converted to metric
main_area_sm=(barea-operim/2+1)/SF_PER_SM
mperim_m = (operim-4)/FT_PER_M
bsmt_area_sm=(barea-operim+4)/SF_PER_SM
bperim_m = (operim-8)/FT_PER_M
# assume top perim change of 3 * sqrt ta_delta, corrected for inside area
# consider sign since ta_delta can be negative
if ta_delta != 0:
    ta_sign = math.sqrt(pow(ta_delta,2))/ta_delta
else:
    ta_sign = 1

ta_sqrt = math.sqrt(abs(ta_delta))
tad_in_sm = (abs(ta_delta) - ta_sqrt)/SF_PER_SM
tp_delta_m = math.sqrt(abs(tad_in_sm)) * 3 * ta_sign
hfa = t.find("House/Specifications/HeatedFloorArea")
hfa.attrib["aboveGrade"] = str(main_area_sm * storeys + tad_in_sm * ta_sign)
hfa.attrib["belowGrade"] = str(bsmt_area_sm)

# calculate volume 7.75ft bsmt + 1' header + 8ft main flr
volume = ((7.75 + 1)/FT_PER_M * bsmt_area_sm) + wall_height_m * main_area_sm
# adjust for different top floor area with 8' ceiling and 1' floor
volume += tad_in_sm *  9/FT_PER_M
t.find("House/NaturalAirInfiltration/Specifications/House").attrib["volume"] = str(volume)
# calculate highest ceiling height
# template has 4' pony, so add 1' above grade + 1' header to wall height
highest_ceiling = (4+1+1)/FT_PER_M + wall_height_m
t.find("House/NaturalAirInfiltration/Specifications/BuildingSite").attrib["highestCeiling"] = str(highest_ceiling)

hc = t.find("House/Components")
ef = hc.find("Floor")
if ta_delta > 0:
    # configure exposed floor
    ef.find("Measurements").attrib["area"] = str(tad_in_sm)
    ef.find("Measurements").attrib["length"] = str(math.sqrt(tad_in_sm))
else:
    hc.remove(ef)

m = hc.find("Ceiling/Measurements")
# eave length
m.attrib["length"] = str((operim/FT_PER_M)/2)
ceiling_area_sm = main_area_sm if ta_delta < 0 else main_area_sm + tad_in_sm * ta_sign
m.attrib["area"] = str(ceiling_area_sm)

m = hc.find("Wall/Measurements")
m.attrib["height"] = str(wall_height_m)
m.attrib["perimeter"] = str((operim-4)/FT_PER_M)

# calculate foundation perim & area
bsmt_perim = (operim-8)/FT_PER_M
hc.find("Basement").attrib["exposedSurfacePerimeter"] = str(bsmt_perim)
m = hc.find("Basement/Floor/Measurements")
m.attrib["area"] = str(bsmt_area_sm)
# H2K errror if perim <= 4*sqrt(area), common ratio is 1.05x
m.attrib["perimeter"] = str(math.sqrt(bsmt_area_sm)*4 * 1.05)

# debug
#t.write("out.h2k", "UTF-8", True)
#sys.exit(0)

# write prepared h2k file
outfile = "../../" + fileid + ".h2k"
t.write(outfile, "UTF-8", True)
#os.system("unix2dos " + outfile)

# copy stick-framed 2x6 house specs
house_data = "../../" + fileid  + "/" + fileid + "-house-data.txt"
os.system("cp 2x6-house.txt " + house_data)
os.system("echo " + info + ">>" + house_data)

