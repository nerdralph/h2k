#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET

# watts to BTU/h
def wb(watts):
    return round(int(watts) * 3.412)

if len(sys.argv) < 2:
    print(sys.argv[0], "file.h2k")
    sys.exit()

#RLF = open("H2KRoomLoads.txt")
RLF = open("C:/HOT2000 v11.12b12/H2KRoomLoads.txt")

rooms = {}
for line in RLF.readlines():
    #print(line.rstrip('\n'))
    # cols = level, ID, heat, cool
    cols = line.split('\t')
    rooms[cols[1]] = [cols[0],] + cols[2:]

TREE = ET.parse(sys.argv[1])
HC = TREE.find("House/Components")

DHL = 0
ROOMS = HC.findall("Room/Label")
for r in ROOMS:
    print(r.text, "BTU/h")
    RHL = wb(rooms[r.text[0]][1])
    DHL += RHL
    print("Heat:", RHL)
    print("Cool:", wb(rooms[r.text[0]][2]))
    print()

print("Basement BTU/h")
BHL = wb(rooms['B'][1])
print("Heat:", BHL)
print("Cool:", wb(rooms['B'][2]))

print("\nDHL:", DHL + BHL)
