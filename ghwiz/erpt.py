#!/usr/bin/python
# Ralph Doncaster 2022
# post-retrofit report generator

import math, os, sys
import xml.etree.ElementTree as ET


if len(sys.argv) != 2:
    print(sys.argv[0], "E-file")
    sys.exit()

e_file = sys.argv[1]

t = ET.parse(e_file + ".h2k")
pi = t.find("./ProgramInformation")
c = pi.find("Client")
print("Hi " + c.find("Name/First").text.capitalize() + ",\r\n")
#print("I finished working on your file " + pi.find("File/Identification").text +".\r\n")
print("I finished working on your file " + e_file +".\r\n")

tsv = t.find("Program/Results/Tsv")
i5 = tsv.find("Info5")
#if ( i5 != None and "MSHP" in i5.attrib["value"] ):
if ( i5 != None and "HP" in i5.attrib["value"] ):
    ashp = t.find("House/HeatingCooling/Type2/AirHeatPump")
    ei = ashp.find("EquipmentInformation")
    (mfr, model) = (ei.find("Manufacturer").text.capitalize(), ei.find("Model").text)
    print("I found your " + mfr + " " + model, end='')
    print(" heat pump on the cold climate heat pump list and entered it according to guidance I have from NRCan and EfficiencyNS for those that are eligible for grants/rebates.\r\n")

d_file = pi.find("File/PreviousFileId").text + ".h2k"
t2 = ET.parse(d_file)
oldach = float(t2.find("Program/Results/Tsv/AIR50P").attrib["value"])
newach = float(tsv.find("AIR50P").attrib["value"])
percent = round((1.0 - newach/oldach) * 100, 1)

print("The blower door test result was " + str(round(newach, 2)) + " ACH, an improvement of ", end='')
print(str(percent) + "% over the last result of " + str(round(oldach, 2)) + ".\r\n")

print("You'll be sent an email in the coming days including a new homeowner info sheet with the updated details for your house.\r\n")
print("-Ralph")

