#!/usr/bin/env python3
# Ralph Doncaster open source MIT license

import cgi, csv, json, math, requests

#print("Content-type: text/plain; charset=utf-8\n")
print("Content-type: application/json; charset=utf-8\n")

form = cgi.FieldStorage()
AAN = form.getvalue("AAN")
dz = requests.get("https://www.thedatazone.ca/resource/a859-xvcs.json?aan=" + AAN).json()
pvsc = dz[0]

HOME = [float(pvsc["x_coord"]), float(pvsc["y_coord"])]

# CSA F280_Weather.xlsm exported to CSV
# http://www.csagroup.org/documents/CSA_F280-12.zip
f = open("F280_Weather.csv", encoding='ISO-8859-1')

wd = csv.DictReader(f)
# wd.fieldnames == ['Seq', 'City', 'Region', 'DegDay', 'DHDBT', 'DCDBT', 'Strange', 'OHR', 'DGTEMP', 'JanWind', 'JulWind', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Latidude', 'Longitude', '']
# note Latitude is misspelled as Latidude in the CSA F280 .xlsm file

distance = 360

for row in wd:
    point = [float(row["Longitude"]), float(row["Latidude"])]
    #print(row["City"], math.dist(HOME, point))
    d = math.dist(HOME, point)
    if d < distance:
        distance = d
        city = row["City"]

#print("closest weather station:", city, distance)
print(json.dumps({"city": city}))
