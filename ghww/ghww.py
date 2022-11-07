#!/usr/bin/env python3
# Ralph Doncaster 2021, 2022
# Greener Homes wizard web version: creates H2K house models from templates

#import photos

import cgi, json, math, os, sys
import requests
import subprocess
import xml.etree.ElementTree as ET

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2
CF_PER_CM = FT_PER_M ** 3

# form inputs: fileID AAN template mperim marea [aflht] [ta_delta] [afl_perim]")
# f = foundation, t = top floor, outside measurements

form = cgi.FieldStorage()

fileid = form.getvalue("fileID")

house_data = "/tmp/ghww.log"
hd = open(house_data, 'a')
hd.write("\nStart " + fileid)
hd.write("\nARGS=" + os.getenv("QUERY_STRING"))

outfile = fileid + ".h2k"
print("Content-Type: application/octet-stream")
print('Content-Disposition: attachment; filename="' + outfile + '"\n')

AAN = form.getvalue("AAN")
template = form.getvalue("template") + ".xml"

# main floor interior perimeter
mperim = float(form.getvalue("mperim"))

# main floor interior perimeter
marea = float(form.getvalue("marea"))

# wall height in metres
wall_height_m = float(form.getvalue("aflht", 0))/FT_PER_M

# top floor interior area difference from marea
ta_delta = float(form.getvalue("ta_delta", 0))

# above foundation perimeter if different than mperim
afl_perim = float(form.getvalue("afl_perim", mperim))

jd = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + AAN).json()[0]

t = ET.parse(template)
# xml = subprocess.check_output(["filepp", template])
# t = ET.ElementTree(ET.fromstring(xml))

# set evaluation date
ymd = "2022-09-12"

# load SO+EA info template
so = ET.parse(fileid[:4] + ".xml").getroot()
pi = t.find("ProgramInformation")
f = pi.find("File")
f.extend(so)
f.attrib["evaluationDate"] = ymd
f.find("Identification").text = fileid
f.find("TaxNumber").text = AAN

hs = t.find("House/Specifications")
#hs.find("FacingDirection").attrib["code"] = FacingDirection
hs.find("YearBuilt").attrib["value"] = jd["year_built"]

# 123 Main St
street = jd["address_num"] + ' ' + jd["address_street"] + ' ' + jd["address_suffix"]

# copy stick-framed 2x6 house specs
#house_data = "../../" + fileid  + "/" + fileid + "-house-data.txt"
#os.system("cp 2x6-house.txt " + house_data)
hd.write(json.dumps(jd))

c = pi.find("Client")
c.find("Name/First").text = form.getvalue("First")
c.find("Name/Last").text = form.getvalue("Last")
c.find("Telephone").text = form.getvalue("Telephone")

pii = pi.find("Information")
info = ET.Element("Info", {"code": "Info. 7"})
info.text = "NSPI;;" + form.getvalue("email", "") + ";N"
pii.append(info)
info = ET.Element("Info", {"code": "Info. 8"})
info.text = "H2K template built with Greener Homes Wizard github.com/nerdralph/h2k/"
pii.append(info)

sa = c.find("StreetAddress")
sa.find("Street").text = street
sa.find("City").text = jd["address_city"]
# province set to NS in h2k template
sa.find("PostalCode").text = form.getvalue("postal")

# wc = weather codes
wc = {"GREENWOOD": "165", "HALIFAX INTL": "166", "SHEARWATER": "169"}
pi.find("Weather/Location").attrib["code"] = wc[form.getvalue("weather")]

if wall_height_m == 0:
    wall_height_m = 5.15 if jd["style"] == "2 Storey" else 2.42

storeys = 2 if wall_height_m > 4 else 1
# code 1 = 1 storey, 3 = 2 storey
hs.find("Storeys").attrib["code"] = "1" if storeys == 1 else "3"
#hd.write("\nstoreys: " + str(storeys))

# calculate foundation and main floor area converted to metric
main_area_sm = marea/SF_PER_SM
mperim_m = mperim/FT_PER_M
# assume 12" bsmt walls & 6" walls above basement
bsmt_area_sm = (marea - (mperim -4)/2)/SF_PER_SM
bperim_m = (mperim -4)/FT_PER_M

# calculate sign since ta_delta can be negative
# easier look at first char of argument for '-'?
if ta_delta != 0:
    ta_sign = math.sqrt(pow(ta_delta, 2))/ta_delta
else:
    ta_sign = 1

hc = t.find("House/Components")
if hc.find("Basement"):
    FTYPE = "Basement"
    # 7.8ft bsmt + 1' header
    BSMT_HT = 8.8
elif hc.find("Slab"):
    FTYPE = "Slab"
    BSMT_HT = 0
else:
    print("unrecognized template foundation type")
    sys.exit()

tad_sm = ta_delta/SF_PER_SM
hfa = t.find("House/Specifications/HeatedFloorArea")
above_grade_sm = (main_area_sm * storeys) + tad_sm
hfa.attrib["aboveGrade"] = str(above_grade_sm)
if FTYPE == "Basement":
    hfa.attrib["belowGrade"] = str(bsmt_area_sm)
hd.write("\nheated floor area sf: " + str(round(above_grade_sm * SF_PER_SM)))

volume = (BSMT_HT/FT_PER_M * bsmt_area_sm) + wall_height_m * main_area_sm
# adjust for different top floor area with 8' ceiling and 1' floor
volume += tad_sm *  9/FT_PER_M
t.find("House/NaturalAirInfiltration/Specifications/House").attrib["volume"] = str(volume)
hd.write("\nhouse volume cf: " + str(round(volume * SF_PER_SM * FT_PER_M)))

# calculate highest ceiling height
# template has 4' pony, so add 1' above grade + 1' header to wall height
# highest ceiling is best calculated manually
#highest_ceiling = (4+1+1)/FT_PER_M + wall_height_m
#t.find("House/NaturalAirInfiltration/Specifications/BuildingSite").attrib["highestCeiling"] =
# str(highest_ceiling)

ef = hc.find("Floor")
if ta_delta > 0:
    # configure exposed floor
    efl_m = math.sqrt(tad_sm)
    ef.find("Measurements").attrib["area"] = str(tad_sm)
    ef.find("Measurements").attrib["length"] = str(efl_m)
    hd.write("\nexposed floor area, length: "
             + str(round(tad_sm * SF_PER_SM)) + ", "
             + str(round(efl_m * FT_PER_M)))
else:
    hc.remove(ef)

m = hc.find("Ceiling/Measurements")
# gable roof eave length typically 0.6 * perim
c_len_m = mperim_m * 0.6
m.attrib["length"] = str(c_len_m)
ceiling_area_sm = main_area_sm if ta_delta < 0 else main_area_sm + tad_sm
m.attrib["area"] = str(ceiling_area_sm)
hd.write("\nceiling area, length: " +
         str(round(ceiling_area_sm * SF_PER_SM)) +
         ", " + str(round(c_len_m * FT_PER_M)))

m = hc.find("Wall/Measurements")
m.attrib["height"] = str(wall_height_m)
m.attrib["perimeter"] = str(mperim_m)
hd.write("\nwall height, perim: " +
         str(round(wall_height_m * FT_PER_M)) +
         ", " + str(mperim_m * FT_PER_M))

# calculate foundation perim & area
m = hc.find(FTYPE + "/Floor/Measurements")
m.attrib["area"] = str(bsmt_area_sm)
if FTYPE == "Basement":
    #m = hc.find("Basement/Floor/Measurements")
    hc.find("Basement").attrib["exposedSurfacePerimeter"] = str(bperim_m)
    # H2K errror if perim <= 4*sqrt(area), common ratio is 1.05x
    # relevant for semis and multiple foundations
    bfp_m = math.sqrt(bsmt_area_sm)*4 * 1.05
    m.attrib["perimeter"] = str(bfp_m)

if FTYPE == "Slab":
    #m = hc.find("Slab/Floor/Measurements")
    m.attrib["perimeter"] = str(bperim_m)

hd.write("\nfoundation floor area, perimeter:" +
         str(round(bsmt_area_sm * SF_PER_SM)) +
         ", " + str(round(bperim_m * FT_PER_M)))

# debug
#t.write("out.h2k", "UTF-8", True)
#sys.exit(0)

# write prepared h2k file
#outfile = "../../" + fileid + ".h2k"
#t.write(outfile, "UTF-8", True)
sys.stdout.flush()
t.write(sys.stdout.buffer, encoding="UTF-8", xml_declaration=True)
