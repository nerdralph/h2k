#!/usr/bin/env python3

import csv, math

# home location to nearest 0.001 degrees
HOME = [-63.517, 44.966]

f = open("F280_Weather.csv")

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

print("closest:", city, distance)
