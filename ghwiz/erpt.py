#!/usr/bin/python
# Ralph Doncaster 2022
# post-retrofit report generator

import math, os, sys
import xml.etree.ElementTree as ET


if len(sys.argv) != 2:
    print(sys.argv[0], "E-file")
    sys.exit()

e_file = sys.argv[1] + ".h2k"

t = ET.parse(e_file)
pi = t.find("./ProgramInformation")
c = pi.find("Client")
print("Hi " + c.find("Name/First").text.capitalize() + ",\r\n")
#print("I finished working on your file " + pi.find("File/Identification").text +".\r\n")
print("I finished working on your file " + e_file +".\r\n")

tsv = t.find("Program/Results/Tsv")
i5 = tsv.find("Info5").attrib["value"]
if ("MSHP" in i5):
    ashp = t.find("House/HeatingCooling/Type2/AirHeatPump")
    ei = ashp.find("EquipmentInformation")
    (mfr, model) = (ei.find("Manufacturer").text.capitalize(), ei.find("Model").text)
    print("I found your " + mfr + " " + model, end='')
    print(" heat pump on the cold climate heat pump list and entered it according to guidance I have from NRCan and EfficiencyNS for those that are eligible for grants/rebates.\r\n")

d_file = pi.find("File/PreviousFileId").text + ".h2k"
t2 = ET.parse(d_file)
ach = tsv.find("AIR50P").attrib["value"]
oldach = t2.find("Program/Results/Tsv/AIR50P").attrib["value"]
newach = tsv.find("AIR50P").attrib["value"]
percent = round((1.0 - float(newach)/float(oldach)) * 100, 1)

print("The blower door test result was " + newach + " ACH, an improvement of ", end='')
print(str(percent) + "% over the last result of " + oldach + ".")

print("You'll be sent an email in the coming days with a new homeowner info sheet with the full details of my assessment.\r\n")
print("-Ralph")

