#!/usr/bin/env python
# fill NRCan form from D h2k file

from datetime import date

import PyPDF2 as P2
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print(sys.argv[0], "D.h2k")
    sys.exit()

t = ET.parse(sys.argv[1])

pi = t.find("ProgramInformation")
#c.find("StreetAddress/Street").text

reader = P2.PdfFileReader("ERS-Auth-Form.pdf")
print("Read " + str(reader.getNumPages())  + " page PDF")
d = reader.getFields()

"""
d = writer.getFields()
for field in list(d):
    if "Prov" in field:
        d[field] = "Nova Scotia"
    """

print(d.keys())

# todo: move field map to config file
# dictionary of h2k element to form field
# telephone field mis-named City_
field_map = {\
    "Client/Name/First" : "First_",
    "Client/Name/Last" : "Last_",
    "Client/StreetAddress/Street" : "Street_",
    "Client/StreetAddress/City" : "City_",
    "Client/Telephone" : "City_",
    "Client/StreetAddress/Province" : "ProvTerr",
    "Client/StreetAddress/PostalCode" : "Postal_",
    "File/TaxNumber" : "Municipal_",
    } 

#print(field_map)

fieldvalues = {}
formfields = list(d)
for element in field_map.keys():
    fieldname = field_map[element]
    print(fieldname)
    value = pi.find(element).text
    print(value)
    while True:
        f = formfields.pop(0)
        if fieldname in f:
            print(f)
            fieldvalues[f] = value
            break

# house file number = TextField1[0]
# fieldvalues["TextField1[0]"]  = "22RDE999999"
fieldvalues["Date_3[0]"] = date.today().isoformat()
fieldvalues["Signature_3[0]"] = "Ralph Doncaster"
print("fieldvalues: ")
print(fieldvalues)

writer = P2.PdfFileWriter()
# clone doesn't really clone everything
# https://github.com/mstamy2/PyPDF2/issues/219
# writer.cloneDocumentFromReader(reader)

# addPage doesn't copy AcroForm object, but it could be explicitly added
#writer.addPage(reader.getPage(0))
#writer.addPage(reader.getPage(1))

# appendPage is the same as addPage for each page
#writer.appendPagesFromReader(reader)

# add Acroform object
# see https://github.com/mstamy2/PyPDF2/issues/355
writer._root_object.update({
    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})
need_appearances = NameObject("/NeedAppearances")
writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)

pg1 = reader.getPage(0)
# ProvTerr[0]
#fieldvalues = { "ProvTerr[0]" : "Nova Scotia" }
writer.updatePageFormFieldValues(pg1, fieldvalues)
writer.addPage(pg1)
writer.addPage(reader.getPage(1))

os = open("NRCan-out.pdf", "wb")
writer.write(os)

print("Wrote " + str(writer.getNumPages())  + " page PDF")

