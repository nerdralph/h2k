#!/usr/bin/python
# extract energy evaluation photos from zip, then remove zip

import os, sys
import zipfile

def ea_photos(file_id: str):
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

if __name__ == "__main__":
    ea_photos(sys.argv[1])
