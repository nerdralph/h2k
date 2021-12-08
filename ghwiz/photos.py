#!/usr/bin/python

import os, sys
import zipfile

FileID = sys.argv[1]
path = "../../" + FileID + "/"
os.mkdir(path)

zipname = "Photos.zip"
zf = zipfile.ZipFile(zipname)

file_count = 0
suffix = ""
for name in zf.namelist():
    f = open(path + FileID + suffix + ".jpg", 'wb')
    f.write(zf.read(name))
    f.close()
    file_count += 1
    suffix = "-" + str(file_count)

os.symlink(path + FileID + ".jpg", "../../" + FileID + ".jpg")
os.remove(zipname)

