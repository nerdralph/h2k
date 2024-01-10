# process xml template files using filepp

CGIDIR := /usr/lib/cgi-bin/
CGIFILES := $(wildcard *.xt) $(wildcard *.xml) *.py
#TARGETS := $(TEMPLATES:%.xt=%.xml)

#all: d-b-e.xml d-b-b.xml d-s-b.xml
#all: $(TARGETS)

hp.db: hp.db.zst
	zstd -d $<

%.xml: %.xt
	filepp -m for.pm $< > $@

install: $(CGIFILES)
	sudo cp $(CGIFILES) $(CGIDIR)
	cp ghw.js dcf.html /var/www/solarsi.ca/html/
