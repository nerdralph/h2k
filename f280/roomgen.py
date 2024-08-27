#!/usr/bin/env python3
# Ralph Doncaster 2024 open source MIT licence
# generate h2k room definitions from csv input

import csv, math, sys
import xml.etree.ElementTree as ET

FTPERM = 3.28084

def fttom(ft: str) -> float:
    return float(ft)/FTPERM

roomxml = """
            <Room id="{rmid}">
                <Label>{label}</Label>
                <Construction>
                    <Type code="{rmtype}">
                    </Type>
                    <Floor code="{floor}">
                    </Floor>
                    <FoundationBelow code="0">None</FoundationBelow>
                </Construction>
                <Measurements isRectangular="true" height="2.43" width="{side}" depth="{side}" />
                <Components>
                    <Wall adjacentEnclosedSpace="false" id="{wallid}">
                        <Label>{label} wall</Label>
                        <Construction corners="1" intersections="1">
                            <Type idref="Code 1" rValue="3.0379" nominalInsulation="3.34">RBR wall</Type>
                        </Construction>
                        <Measurements height="2.4384" perimeter="6.7056" />
                        <FacingDirection code="1">
                        </FacingDirection>
                    </Wall>
                </Components>
            </Room>
"""

# starting room id
rmid = 100
# wall id offset from room id
WALLBASE= 50

if len(sys.argv) < 2:
    print(sys.argv[0], "file.h2k")
    sys.exit()

f = open("rooms.csv", encoding='ISO-8859-1')
rd = csv.DictReader(f)
# rd.fieldnames == ['room', 'area', 'rmtype', 'wall perim', 'floor']

# h2k room codes
# 1 = kitchen
# 2 = living
# 3 = dining
# 4 = bedroom
# 5 = bath
# 6 = utility
# 7 = other

H2K = sys.argv[1]
t = ET.parse(H2K)
hc = t.find("House/Components")

for row in rd:
    side = fttom(math.sqrt(row["area"]))
    rmxml = roomxml.format(rmid=rmid, label=row["room"], rmtype=row["rmtype"], floor=row["floor"], width=side, depth=side, wallid=(rmid + WALLBASE))
    root = ET.fromstring(rmxml)
    hc.append(root)
    #print(ET.tostring(root))
    rmid += 1

outfile = "rg-out.h2k"
t.write(outfile, "UTF-8", True)

