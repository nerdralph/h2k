#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, os, requests, sys

FT_PER_M = 3.28084
SF_PER_SM = FT_PER_M ** 2

def xmlval(xmle, tag: str) -> str:
    return xmle.find(tag).attrib["value"]

# dump xml values using xmlval
def valdump(xmle, tags):
    for tag in tags:
        print(tag +": " + xmlval(xmle, tag))

# key = array of json keys to print
def printjson(jd, keys):
    for key in keys:
        print(key +": " + jd.get(key, "unknown"))

print("Content-type: text/plain; charset=utf-8\n")
print("Solar Si H2k QA scan beta")

form = cgi.FieldStorage()
h2k = form["h2kfile"]
print("file: " + h2k.filename)

tree = ET.parse(h2k.file)
pi = tree.find("ProgramInformation")

log = open("/tmp/qa.log", 'a')

pif = pi.find("File")
fid = pif.findtext("Identification")
print("File ID, date:", fid, pif.attrib["evaluationDate"])
tid = pif.find("TaxNumber").text or "no AAN"
if len(tid) == 7:
    tid = '0' + tid
print("8-digit AAN: " + tid)
log.write(datetime.date.today().isoformat() + " FileID: " + fid + ", AAN: " + tid + '\n')

dz = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + tid).json()
if not len(dz):
    print("AAN not found in PVSC database")
else:
    print("PVSC data:")
    pvsc = dz[0]
    keys = ["style", "square_foot_living_area", "year_built", "address_num", "address_street", "address_city"]
    printjson(pvsc, keys)
    # lookup weather station
    wkid4326 = pvsc["x_coord"] + "," + pvsc["y_coord"]
    ws = requests.get("https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/Carte_climatique_HOT2000_Climate_Map_EN/MapServer/1/query?geometry=" + wkid4326 + "&geometryType=esriGeometryPoint&inSR=4326&f=json")
    print("H2K weather: " + ws.json()["features"][0]["attributes"]["Name"])

hse = tree.find("House")
specs = hse.find("Specifications")
tsv = tree.find("Program/Results/Tsv")

print("\nHouse data:")
print("Net AEC-AEP: " +xmlval(tsv, "EGHFconTotal"))
print("Building type: " + xmlval(tsv, "BuildingType"))
print("House type: " + specs.find("HouseType/English").text)
print("Weather " + xmlval(tsv, "WeatherLoc"))

hfaa = float(specs.find("HeatedFloorArea").attrib["aboveGrade"]) * SF_PER_SM
hfab = float(specs.find("HeatedFloorArea").attrib["belowGrade"]) * SF_PER_SM
print("HFA above, below grade: " + str(int(hfaa)) + ", " + str(int(hfab)))

print("Storeys: " + xmlval(tsv, "Storeys"))
print("Front faces " + specs.find("FacingDirection/English").text)
print("Built " + xmlval(tsv, "YearBuilt"))

print("\nGeneral Info")
tsvals = ["AtypicalEnergyLoads", "GreenerHomes", "Vermiculite"]
valdump(tsv, tsvals)

print("Reduced operating conditions: todo")

sa = pi.find("Client/StreetAddress")
print(sa.find("Street").text)
print(sa.find("City").text)
print(sa.find("PostalCode").text)

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

doors = hc.findall("*/Components/Door")
print("\nDoors:", len(doors))
for d in doors:
    m = d.find("Measurements")
    print(d.findtext("Label") + ":" +\
          " width=" + m.attrib["width"] +\
          " height=" + m.attrib["height"])
    windows = d.findall("Components/Window")
    for w in windows:
        print(" lite", windowspecs(w))

# todo: add foundation details area, R-value
bsmt = hc.find("Basement")
print("\nBasement:", bsmt.findtext("Configuration") if bsmt else "N/A")

slab = hc.find("Slab")
print("\nSlab:", slab.findtext("Configuration") if slab else "N/A")

# todo: crawlspace

print("\nType 1 Heating")
tsvals = ["FurnaceFuel", "FurnaceType", "FurnaceModel"]
valdump(tsv, tsvals)
print("Mfr & model only required for condensing equipment: TP 3.5.14")
# todo: SuppHtgType1

ashp = hse.find("HeatingCooling/Type2/AirHeatPump")
print("\nType 2 Heating", "ASHP" if ashp else "N/A")
if ashp:
    ei = ashp.find("EquipmentInformation")
    print("AHRI", ei.attrib["AHRI"])
    print(ei.findtext("Manufacturer", default="no mfr"), ei.findtext("Model", default="no model"))

print("\nDHW")
tsvals = ["pDHWFuel", "pDHWType", "priDHWModel", "PrimaryDHWTankVolume"]
valdump(tsv, tsvals)
#dhw = hc.find("HotWater/Primary")
#ei = dhw.find("EquipmentInformation")
#print(dhw.findtext("EnergySource/English"))
#print(ei.findtext("Manufacturer", default="no mfr"), ei.findtext("Model", default="no model"))
print("Mfr & model only required for instant & condensing equipment: TP 3.6.1")

v = hse.find("Ventilation")
print("\nVentilation:")
# report dryer
print(len(v.findall("SupplementalVentilatorList/BaseVentilator")), "total bath fans and range hoods (max 3 allowed)")
hrv = v.find("WholeHouseVentilatorList/Hrv")
if not hrv:
    print("No HRV")
else:
    ei = hrv.find("EquipmentInformation")
    print("HRV make/model: ", ei.findtext("Manufacturer"), ei.findtext("Model"))
    print("flow rate" +\
          " supply=" + hrv.attrib["supplyFlowrate"] +\
          " exhaust=" + hrv.attrib["exhaustFlowrate"])
    print("efficiency" +\
          " 0C=" + hrv.attrib["efficiency1"] +\
          " -25C=" + hrv.attrib["efficiency2"])

air_specs = hse.find("NaturalAirInfiltration/Specifications")
print("\nACH@50Pa " + air_specs.find("BlowerTest").attrib["airChangeRate"])
