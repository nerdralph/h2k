#!/usr/bin/env python3

import sqlite3
import sys
import xml.etree.ElementTree as ET

ASHP_Debug = 0

def query(ahri : str):
    """Find an air-source heat pump given an AHRI reference #."""

    SPEC_COLS = [ "Brand", "Outside_Model", "Heating_kW", "SEER", "HSPF5" ]
    con = sqlite3.connect("hp.db")
    stmt = "SELECT " + ", ".join(SPEC_COLS) + " FROM ASHP WHERE AHRI_Ref = " + ahri + ';'
    row = con.cursor().execute(stmt).fetchone()
    con.close()

    # Type 2 CCHP heating system
    type2 = ET.parse("Type2.xml").getroot()
    ahp = type2.find("AirHeatPump")
    if row:
        specs = dict(zip(SPEC_COLS, row))
        ahp.find("*/Manufacturer").text = specs["Brand"]
        ahp.find("*/Model").text = specs["Outside_Model"]
        ahp.find("*/OutputCapacity").attrib["value"] = specs["Heating_kW"]
        ahp.find("*/HeatingEfficiency").attrib["value"] = specs["HSPF5"]
        ahp.find("*/CoolingEfficiency").attrib["value"] = specs["SEER"]
    else:
        ahri = "-1"
    ahp.find("EquipmentInformation").attrib["AHRI"] = ahri

    if ASHP_Debug:
        print("Set AHRI# = " + ahri )

    return type2

if __name__ == "__main__":
    if len(sys.argv) == 2:
        ASHP_Debug = 1
        print (query(sys.argv[1]))
    else:
        print( sys.argv[0] + " AHRI_Ref")
