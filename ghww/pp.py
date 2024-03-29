#!/usr/bin/env python3
""" populate fields in house template using filepp """

import cgi
import subprocess
import sys

INCH_PER_M = 12 * 3.28084

# 1=south, counter-clockwise to 8=southwest; see ghww.html FacingDirection
def points(code):
    return str(((code - 1) % 8) + 1)

def filepp(template: str):
    form = cgi.FieldStorage()
    FRONT = int(form.getvalue("FacingDirection"))
    PP_DEFS = ["-D_FRONT_=" + points(FRONT),
               "-D_RIGHT_=" + points(FRONT + 2),
               "-D_BACK_=" + points(FRONT + 4),
               "-D_LEFT_=" + points(FRONT + 6)]

    # todo: count windows and prune unused windows
    for k in form.keys():
        if k[0] == '_':
            PP_DEFS.append("-D"+k+'=' + form[k].value)
        if k[1:5] == "Wndw":
            # convert inches to mm
            PP_DEFS.append("-D"+k+'=' + str(25.4 * int(form[k].value)))

    # use filepp to make h2k xml file
    xml = subprocess.check_output(["filepp", "-m", "for.pm", "-m", "maths.pm"] + PP_DEFS + [template])
    xmlstr = xml.decode("utf-8")
    #pp = open("filepp.out", 'w')
    #pp.write(xmlstr)

    return xmlstr

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(filepp(sys.argv[1]))
    else:
        print(sys.argv[0] + " file.xt")
