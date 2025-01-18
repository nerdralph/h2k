#!/usr/bin/env python3
# generates room-by-room heat load list from H2K file and
# H2KRoomLoads.txt with floor room key & heat/cool
# floor = B|G|S
# room key = first character of room name: must be unique

import sys
import xml.etree.ElementTree as ET

# watts to BTU/h
def wb(watts):
    return round(int(watts) * 3.412)

if len(sys.argv) < 2:
    print(sys.argv[0], "file.h2k")
    sys.exit()

#RLF = open("H2KRoomLoads.txt")
RLF = open("C:/HOT2000 v11.13b13/H2KRoomLoads.txt")

roomloads = {}
for line in RLF.readlines():
    # cols = level, ID, heat, cool
    cols = line.split('\t')
    roomloads[cols[1]] = [cols[0],] + cols[2:]

TREE = ET.parse(sys.argv[1])
HC = TREE.find("House/Components")

dhl = 0 
# above & below grade rooms
AGROOMS = HC.findall("Room/Label")
BGROOMS = HC.findall("Basement/Label")
for r in AGROOMS + BGROOMS:
    print(r.text, "BTU/h")
    RHL = wb(roomloads[r.text[0]][1])
    dhl += RHL
    print("Heat:", RHL)
    print("Cool:", wb(roomloads[r.text[0]][2]))
    print()

print("House DHL:", dhl)
