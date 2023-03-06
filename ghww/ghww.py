#!/usr/bin/env python3
# Ralph Doncaster 2021, 2022
# Greener Homes wizard web version: creates H2K house models from templates

import xml.etree.ElementTree as ET
import cgi, json, math, os, requests, sys

# local modules
import ashp, config, pp

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2
CF_PER_CM = FT_PER_M ** 3

# form inputs: _fileID AAN _Foundation _Heat mperim marea [aflht] [ta_delta] [tp_delta]")
# t = top floor

form = cgi.FieldStorage()

fileid = form.getvalue("_FileID")

house_data = "/tmp/ghww.log"
hd = open(house_data, 'a')
hd.write("\nStart " + fileid)
hd.write("\nARGS=" + os.getenv("QUERY_STRING"))

outfile = fileid + ".h2k"
print("Content-Type: application/octet-stream")
print('Content-Disposition: attachment; filename="' + outfile + '"\n')

AAN = form.getvalue("_AAN")
# main floor interior perimeter
mperim = float(form.getvalue("mperim"))
# main floor interior area
marea = float(form.getvalue("marea"))
# wall height in metres, default to 2.43m = 7.97'
wall_height_m = float(form.getvalue("aflht", 2.43))/FT_PER_M
# top floor area difference from marea
ta_delta = float(form.getvalue("ta_delta", 0))
# top floor area difference from marea
tp_delta_m = float(form.getvalue("tp_delta", 0))/FT_PER_M

#jd = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + AAN).json()[0]
#hd.write(json.dumps(jd))

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

# set default evaluation date 
#ymd = date.today().isoformat()
#f.attrib["evaluationDate"] = ymd

#pii = pi.find("Information")
#info = ET.Element("Info", {"code": "Info. 42"})
#info.text = "H2K template built with Greener Homes Wizard github.com/nerdralph/h2k/"
#pii.append(info)

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

hs = house.find("Specifications")
# hs.find("YearBuilt").attrib["value"] = jd.get("year_built", "1920")
storeys = 2 if wall_height_m > 4 else 1
# code 1 = 1 storey, 3 = 2 storey
hs.find("Storeys").attrib["code"] = "1" if storeys == 1 else "3"

# calculate foundation and main floor area converted to metric
main_area_sm = marea/SF_PER_SM
mperim_m = mperim/FT_PER_M

# assume 12" bsmt walls & 6" walls above basement
bsmt_area_sm = (marea - (mperim -2)/2)/SF_PER_SM
bperim_m = (mperim -4)/FT_PER_M

tad_sm = ta_delta/SF_PER_SM
above_grade_sm = (main_area_sm * storeys) + tad_sm
hfa = hs.find("HeatedFloorArea")
hfa.attrib["aboveGrade"] = str(above_grade_sm)

hc = tree.find("House/Components")
if hc.find("Basement"):
    FTYPE = "Basement"
    # 7.8ft bsmt + 1' header / FT_PER_M
    BSMT_HT_M = 2.683
    hfa.attrib["belowGrade"] = str(bsmt_area_sm)
elif hc.find("Slab"):
    FTYPE = "Slab"
    BSMT_HT_M = 0
else:
    print("unrecognized template foundation type")
    sys.exit()

volume = (BSMT_HT_M * bsmt_area_sm) + wall_height_m * main_area_sm
# adjust for different top floor area with 8' ceiling and 1' floor
volume += tad_sm *  9/FT_PER_M
air_specs = house.find("NaturalAirInfiltration/Specifications")
air_specs.find("House").attrib["volume"] = str(volume)

# default highest ceiling height: BSMT_HT/2 + main wall
ceiling_h = BSMT_HT_M/2 + wall_height_m
air_specs.find("BuildingSite").attrib["highestCeiling"] = str(ceiling_h)

ceiling_area_sm = main_area_sm
ef = hc.find("Floor")
if ta_delta > 0:
    # configure exposed floor
    m = ef.find("Measurements")
    m.attrib["area"] = str(tad_sm)
    m.attrib["length"] = str(math.sqrt(tad_sm))
    ceiling_area_sm += tad_sm
else:
    hc.remove(ef)

m = hc.find("Ceiling/Measurements")
# gable roof eave length typically 0.6 * perim
c_len_m = mperim_m * 0.6
m.attrib["length"] = str(c_len_m)
m.attrib["area"] = str(ceiling_area_sm)

m = hc.find("Wall/Measurements")
m.attrib["height"] = str(wall_height_m)
m.attrib["perimeter"] = str(mperim_m + tp_delta_m/storeys)

# calculate foundation perim & area
f = hc.find(FTYPE)
f.attrib["exposedSurfacePerimeter"] = str(bperim_m)
m = f.find("Floor/Measurements")
m.attrib["area"] = str(bsmt_area_sm)
# H2K requires perim <= exposedSurfacePerimeter: relevant for semis and multiple foundations
m.attrib["perimeter"] = str(max(bperim_m, math.sqrt(bsmt_area_sm)*4 + 0.1))

# write h2k file
#tree.write(outfile, "UTF-8", True)
sys.stdout.flush()
tree.write(sys.stdout.buffer, encoding="UTF-8", xml_declaration=True)
