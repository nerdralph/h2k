#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, ctitb, datetime, json, math, os, requests, sys

cgitb.enable()

print ("Content-type: text/plain\n")
print ("Solar Si H2k QA scanner alpha")

tree = ET.parse(sys.stdin)
print ("file: " + h2kfile)


