#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, json, math, os, requests, sys

print ("Content-type: text/plain\n")
print ("Solar Si H2k QA scanner alpha")

form = cgi.FieldStorage()
h2k = form["h2kfile"]
print ("file: " + h2k.filename)

tree = ET.parse(h2k.file)
pi = tree.find("ProgramInformation/")

print ("File ID: " + pi.findtext("Identification"))
tid = pi.find("TaxNumber").text or "no AAN"
print("AAN: " + tid)

jd = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + tid).json()[0]
#print(json.dumps(jd))

hse = tree.find("House")
print("h2k file vs PVSC data")
specs = hse.find("Specifications")
print(specs.find("YearBuilt").attrib["value"] + " vs " + jd.get("year_built") )
print(specs.find("HouseType/English").text + " vs " + jd.get("style") )
# todo: check floor area
sa = pi.find("Client/StreetAddress/")
print(sa.find("Street").text + " vs " + jd.get("address_num") + jd.get("address_street"))
print(sa.find("City").text + " vs " + jd.get("address_city"))
