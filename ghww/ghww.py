#!/usr/bin/env python3
# Ralph Doncaster 2021
# Greener Homes wizard web version: creates H2K house models from templates

import xml.etree.ElementTree as ET
import cgi, datetime, math, os, sys

# local modules
import ashp, config, pp

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2
CF_PER_CM = FT_PER_M ** 3

form = cgi.FieldStorage()

fileid = form.getvalue("_FileID")

house_data = "/tmp/ghww.log"
hd = open(house_data, 'a')
hd.write("Start " + fileid + ' ' + datetime.date.today().isoformat())
hd.write("\nARGS=" + os.getenv("QUERY_STRING") +"\n")

outfile = fileid + ".h2k"
print("Content-Type: application/octet-stream")
print('Content-Disposition: attachment; filename="' + outfile + '"\n')

# main floor interior perimeter
mperim = float(form.getvalue("mperim"))
# main floor interior area
marea = float(form.getvalue("marea"))
# wall height in metres
wall_height_m = float(form.getvalue("aflht"))/FT_PER_M
# top floor area difference from marea
tad_sm = float(form.getvalue("ta_delta", 0))/SF_PER_SM
# top floor area difference from marea
tp_delta_m = float(form.getvalue("tp_delta", 0))/FT_PER_M
BSMT_HT_M = float(form.getvalue("_BHt", 0))

# use filepp to make h2k xml file
xml = pp.filepp("house.xt")
tree = ET.ElementTree(ET.fromstring(xml))

pi = tree.find("ProgramInformation")
# set SO + EA
f = pi.find("File")
soea = config.SOEA.setdefault(fileid[:4], config.DFLT_SOEA)
f.find("EnteredBy").text = soea["eaname"]
f.find("Company").text = soea["soname"]
f.find("CompanyTelephone").text = soea["sotel"]

# wc = weather codes
wc = {"BRIER ISLAND": "163",
      "CALGARY INTL": "5",
      "GREENWOOD": "165",
      "HALIFAX INTL": "166",
      "KEJIMKUJIK": "167",
      "MONCTON INTL": "141",
      "SHEARWATER": "169",
      "SYDNEY": "170",
      "WESTERN HEAD": "171",
      "YARMOUTH": "172"}
loc = form.getvalue("weather")
if loc in wc.keys(): 
    pi.find("Weather/Location").attrib["code"] = wc[loc]

house = tree.find("House")
ahri = form.getvalue("AHRI")
if ahri:
    house.find("HeatingCooling").append(ashp.query(ahri))

main_area_sm = marea/SF_PER_SM
mperim_m = mperim/FT_PER_M

# assume basement walls 6" thicker than main walls
bsmt_area_sm = (marea - (mperim -2)/2)/SF_PER_SM
bperim_m = (mperim -4)/FT_PER_M

storey_codes = {"1":1, "2":2, "3":2, "4":2, "5":3, "6":1, "7":1}
storeys = storey_codes[form.getvalue("_Storeys")]
above_grade_sm = (main_area_sm * storeys) + tad_sm
hfa = house.find("Specifications/HeatedFloorArea")
hfa.attrib["aboveGrade"] = str(above_grade_sm)

hc = house.find("Components")
if f := hc.find("Basement"):
    FTYPE = "Basement"
    # add 1' header
    BSMT_HT_M += 1.0/FT_PER_M
    hfa.attrib["belowGrade"] = str(bsmt_area_sm)
    hm = f.find("Components/FloorHeader/Measurements")
    hm.attrib["perimeter"] = str(mperim_m) 
elif hc.find("Slab"):
    # todo: copy main measurements
    FTYPE = "Slab"
else:
    hd.write("unrecognized template foundation type\n")

volume = (BSMT_HT_M * bsmt_area_sm) + wall_height_m * main_area_sm
# adjust for different top floor area with 8' ceiling and 1' floor
volume += tad_sm *  9/FT_PER_M
air_specs = house.find("NaturalAirInfiltration/Specifications")
air_specs.find("House").attrib["volume"] = str(volume)

ceiling_area_sm = main_area_sm
ef = hc.find("Floor")
if tad_sm > 0:
    # configure exposed floor
    m = ef.find("Measurements")
    m.attrib["area"] = str(tad_sm)
    m.attrib["length"] = str(math.sqrt(tad_sm))
    ceiling_area_sm += tad_sm
else:
    hc.remove(ef)

m = hc.find("Ceiling/Measurements")
m.attrib["area"] = str(ceiling_area_sm)
# heel height as per ERS tech procedures 3.5.3.3, house.xt default = 0.13m
if (int(form.getvalue("_YearBuilt")) < 1990):
    m.attrib["heelHeight"] = "0.10"

m = hc.find("Wall/Measurements")
m.attrib["height"] = str(wall_height_m)
m.attrib["perimeter"] = str(mperim_m + tp_delta_m/storeys)

# calculate foundation perim & area
f = hc.find(FTYPE)
f.attrib["exposedSurfacePerimeter"] = str(bperim_m)
m = f.find("Floor/Measurements")
m.attrib["area"] = str(bsmt_area_sm)
# H2K requires perimeter >= exposedSurfacePerimeter: relevant for semis and multiple foundations
m.attrib["perimeter"] = str(max(bperim_m, math.sqrt(bsmt_area_sm)*4 + 0.1))

# write h2k file
sys.stdout.flush()
tree.write(sys.stdout.buffer, encoding="UTF-8", xml_declaration=True)
