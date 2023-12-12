#!/usr/bin/env python3
# (c) Ralph Doncaster nerdralph.blogspot.ca

import xml.etree.ElementTree as ET
import cgi, datetime, json, math, os, requests, sys

form = cgi.FieldStorage()

h2kfile = form.getvalue("filename", "none")

print ("Content-type: text/plain\n")
print ("Solar Si H2k QA scanner alpha")
print ("file: " + h2kfile)
