#!/usr/bin/python
# extract energy evaluation photos from zip, then remove zip

import os, sys
import zipfile

# iso8601 is YYYY-MM-DD
#def iso8601(dt) -> str:
#    ymd = [str(d) for d in dt[0:3]]
#    return "-".join(ymd)

# extract photos & return ISO8601 date of first photo
def extract(file_id: str) -> str:
    zipname = "Photos-001.zip"
    zf = zipfile.ZipFile(zipname)

    path = "../../" + file_id + "/"
    os.mkdir(path)
    
    file_count = 0
    suffix = ""
    # filename = IMG_YYYYMMDD_HHMMSSmmm, so sort to put earliest first
    nl = zf.namelist()
    nl.sort()
    for name in nl:
        f = open(path + file_id + suffix + ".jpg", 'wb')
        f.write(zf.read(name))
        f.close()
        file_count += 1
        suffix = "-" + str(file_count)
    
    house = path + file_id + ".jpg"
    os.link(house, "../../" + file_id + ".jpg")
    os.remove(zipname)

    #return iso8601(zf.infolist()[0].date_time)

    h = nl[0]
    iso8601 = h[4:8] + '-' + h[8:10] + '-' + h[10:12]
    return iso8601


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print (extract(sys.argv[1]))
    else:
        print( sys.argv[0] + " FILEID")
