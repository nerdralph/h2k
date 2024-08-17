#!/usr/bin/env python3
# Ralph Doncaster 2024 open source MIT licence
# generate h2k room definitions from csv input

import csv, sys

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
                <Measurements isRectangular="true" height="2.43" width="{width}" depth="{depth}" />
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
            </Room>"""

# starting room id
rmid = 100
# wall id offset from room id
WALLBASE= 50

if len(sys.argv) < 2:
    print(sys.argv[0], "file.h2k")
    sys.exit()

f = open("rooms.csv", encoding='ISO-8859-1')
rd = csv.DictReader(f)
# rd.fieldnames == ['room', 'depth', 'width', 'rmtype', 'wall perim', 'floor']

# h2k room codes
# 1 = kitchen
# 2 = living
# 3 = dining
# 4 = bedroom
# 5 = bath
# 6 = utility
# 7 = other

t = ET.parse(sys.argv[1])
hc = t.find("House/Components")

for row in rd:
    print(roomxml.format(rmid=rmid, label=row["room"], rmtype=row["rmtype"], floor=row["floor"], width=fttom(row["width"]), depth=fttom(row["depth"]), wallid=(rmid + WALLBASE)))
    rmid += 1

