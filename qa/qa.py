#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, json, math, os, requests, sys

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

print ("Content-type: text/plain\n")
print ("Solar Si H2k QA scan alpha")

form = cgi.FieldStorage()
h2k = form["h2kfile"]
print ("file: " + h2k.filename)

tree = ET.parse(h2k.file)
pi = tree.find("ProgramInformation")

pif = pi.find("File")
print ("File ID: " + pif.findtext("Identification"))
tid = pif.find("TaxNumber").text or "no AAN"
if tid.length() == 7:
    tid = '0' + tid
print ("8-digit AAN: " + tid)

pvsc = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + tid).json()[0]
if not pvsc:
    print ("AAN not found in PVSC database")
#print(json.dumps(jd))

hse = tree.find("House")
print ("\nh2k file vs online data")
specs = hse.find("Specifications")
print (specs.find("YearBuilt").attrib["value"] + " vs " + pvsc.get("year_built") )
print (specs.find("HouseType/English").text + " vs " + pvsc.get("style") )
# check floor area
hfaa = float(specs.find("HeatedFloorArea").attrib["aboveGrade"]) * SF_PER_SM
hfab = float(specs.find("HeatedFloorArea").attrib["belowGrade"]) * SF_PER_SM
print ("HFA above, below grade: " + str(int(hfaa)) + ", " + str(int(hfab)), end = '')
print (" vs " + pvsc.get("square_foot_living_area") + " living area")
sa = pi.find("Client/StreetAddress")
print (sa.find("Street").text + " vs " + pvsc.get("address_num") + ' ' + pvsc.get("address_street"))
print (sa.find("City").text + " vs " + pvsc.get("address_city"))

#todo: Canada Post lookup
print (sa.find("PostalCode").text + " vs ")

air_specs = hse.find("NaturalAirInfiltration/Specifications")
print ("\nACH@50Pa " + air_specs.find("BlowerTest").attrib["airChangeRate"])
