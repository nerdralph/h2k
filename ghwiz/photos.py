#!/usr/bin/python
# extract energy evaluation photos from zip, then remove zip

import os, sys
import zipfile

# iso8601 is YYYY-MM-DD
def iso8601(dt) -> str:
    ymd = [str(d) for d in dt[0:3]]
    return "-".join(ymd)

# extract photos & return ISO8601 date of first photo
def extract(file_id: str) -> str:
    path = "../../" + file_id + "/"
    os.mkdir(path)
    
    zipname = "Photos.zip"
    zf = zipfile.ZipFile(zipname)
    
    file_count = 0
    suffix = ""
    for name in zf.namelist():
        f = open(path + file_id + suffix + ".jpg", 'wb')
        f.write(zf.read(name))
        f.close()
        file_count += 1
        suffix = "-" + str(file_count)
    
    house = path + file_id + ".jpg"
    os.link(house, "../../" + file_id + ".jpg")
    os.remove(zipname)
    return iso8601(zf.infolist()[0].date_time)


if __name__ == "__main__":
    extract(sys.argv[1])
