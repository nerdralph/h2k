#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, json, math, os, requests, sys

form = cgi.FieldStorage()

h2kfile = form['filename']

print ("Content-type: text/plain\n")
print ("file: " + h2kfile)
