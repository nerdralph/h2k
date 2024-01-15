#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, os, requests, sys

def xmlval(xmle, tag: str) -> str:
    return xmle.find(tag).attrib["value"]

# dump xml values using xmlval
def valdump(xmle, tags):
    for tag in tags:
        print(tag +": " + xmlval(xmle, tag))

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

print("Content-type: text/plain; charset=utf-8\n")
print("Solar Si H2k QA scan alpha")

form = cgi.FieldStorage()
h2k = form["h2kfile"]
print("file: " + h2k.filename)

tree = ET.parse(h2k.file)
pi = tree.find("ProgramInformation")

log = open("/tmp/qa.log", 'a')

pif = pi.find("File")
fid = pif.findtext("Identification")
print("File ID: " + fid)
tid = pif.find("TaxNumber").text or "no AAN"
if len(tid) == 7:
    tid = '0' + tid
print("8-digit AAN: " + tid)
log.write(datetime.date.today().isoformat() + " FileID: " + fid + ", AAN: " + tid + '\n')

dz = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + tid).json()
if not len(dz):
    print("AAN not found in PVSC database")
    sys.exit(0)
pvsc = dz[0]

hse = tree.find("House")
specs = hse.find("Specifications")
tsv = tree.find("Program/Results/Tsv")

print("\nNet AEC-AEP: " +xmlval(tsv, "EGHFconTotal"))

print("\nHouse h2k vs online data")
print("Building type: " + xmlval(tsv, "BuildingType"))
print("House type: " + specs.find("HouseType/English").text + " vs " + pvsc.get("style"))

print("Weather " + xmlval(tsv, "WeatherLoc") + " vs ", end='')
# lookup weather station
wkid4326 = pvsc["x_coord"] + "," + pvsc["y_coord"]
ws = requests.get("https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + wkid4326 + "&geometryType=esriGeometryPoint&inSR=4326&f=json")
print(ws.json()["features"][0]["attributes"]["Name"])

hfaa = float(specs.find("HeatedFloorArea").attrib["aboveGrade"]) * SF_PER_SM
hfab = float(specs.find("HeatedFloorArea").attrib["belowGrade"]) * SF_PER_SM
print("HFA above, below grade: " + str(int(hfaa)) + ", " + str(int(hfab)), end='')
print(" vs " + pvsc.get("square_foot_living_area") + " living area")

print("Storeys: " + xmlval(tsv, "Storeys"))
print("Front faces " + specs.find("FacingDirection/English").text)
print("Built " + xmlval(tsv, "YearBuilt") + " vs " + pvsc.get("year_built", "unknown"))

print("\nGeneral Info")
tsvals = ["AtypicalEnergyLoads", "GreenerHomes", "Vermiculite"]
valdump(tsv, tsvals)

print("Reduced operating conditions: todo")

sa = pi.find("Client/StreetAddress")
print(sa.find("Street").text + " vs " + pvsc.get("address_num") + ' ' +\
  pvsc.get("address_street") + ' ' + pvsc.get("address_suffix", ''))
print(sa.find("City").text + " vs " + pvsc.get("address_city"))
print(sa.find("PostalCode").text + " vs " + "todo: Canada Post lookup")

print("\nTemperatures")
temps = hse.find("Temperatures")
print("Basement cooled: " + temps.find("Basement").attrib["cooled"])
print("Crawlspace heated: " + temps.find("Crawlspace").attrib["heated"])
print("MURB basement unit: " + temps.find("Basement").attrib["basementUnit"])

hc = hse.find("Components")
print("\nCeiling and roof")
ceilings = hc.findall("Ceiling")
for c in ceilings:
    m = c.find("Measurements")
    print(c.findtext("Label") + ":" +\
          " area=" + m.attrib["area"] +\
          " len=" + m.attrib["length"] +\
          " " + c.findtext("Construction/Type/English") +\
          " RSI=" + c.find("Construction/CeilingType").attrib["rValue"] +\
          " heel=" + m.attrib["heelHeight"])

print("\nWalls")
walls = hc.findall("Wall")
for w in walls:
    m = w.find("Measurements")
    print(w.findtext("Label") + ":" +\
          " height=" + m.attrib["height"] +\
          " perim=" + m.attrib["perimeter"] +\
          " " + w.findtext("Construction/Type") +\
          " RSI=" + w.find("Construction/Type").attrib["rValue"] +\
          " buffer=" + w.attrib["adjacentEnclosedSpace"])

print("\nMain wall headers - todo")

print("\nExposed floors")
ef = hc.findall("Floor")
for f in ef:
    m = f.find("Measurements")
    print(f.findtext("Label") + ":" +\
          " area=" + m.attrib["area"] +\
          " len=" + m.attrib["length"] +\
          " " + f.findtext("Construction/Type") +\
          " RSI=" + f.find("Construction/Type").attrib["rValue"] +\
          " buffer=" + f.attrib["adjacentEnclosedSpace"])

def windowspecs(w) -> str:
    m = w.find("Measurements")
    return (w.findtext("Label") + ":" +\
          w.findtext("Construction/Type") +\
          " width=" + m.attrib["width"] +\
          " height=" + m.attrib["height"])

#windows = hc.findall("Wall/Components/Window")
windows = hc.findall("*/Components/Window")
print("\nWindows:", len(windows))
for w in windows:
    print(windowspecs(w))

# todo: include basement doors
doors = hc.findall("Wall/Components/Door")
print("\nDoors:", len(doors))
for d in doors:
    m = d.find("Measurements")
    print(d.findtext("Label") + ":" +\
          " width=" + m.attrib["width"] +\
          " height=" + m.attrib["height"])
    windows = d.findall("Components/Window")
    for w in windows:
        print(" lite", windowspecs(w))

bsmt = hc.find("Basement")
print("\nBasement:", bsmt.findtext("Configuration") if bsmt else "N/A")

slab = hc.find("Slab")
print("\nSlab:", slab.findtext("Configuration") if slab else "N/A")

air_specs = hse.find("NaturalAirInfiltration/Specifications")
print("\nACH@50Pa " + air_specs.find("BlowerTest").attrib["airChangeRate"])
