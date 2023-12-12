#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, json, math, os, requests, sys

print ("Content-type: text/plain\n")
print ("Solar Si H2k QA scanner alpha")

form = cgi.FieldStorage()
h2k = form["file"]
print ("file: " + h2k.filename)

tree = ET.parse(h2k.file)
pif = tree.find("ProgramInformation/File)

print ("File ID: " + tree.findtext("Identification"))
tid = pif.find("TaxNumber").text or "no AAN"
print("AAN: " + tid)

jd = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + tid).json()[0]
print(json.dumps(jd))

hse = tree.find("House")
print("h2k file vs PVSC data")
specs = hse.find("Specifications")
print(specs.find("YearBuilt").attrib["value"] + " vs " + jd.get("year_built") )
print(specs.find("HouseType/English").text + " vs " + jd.get("style") )
