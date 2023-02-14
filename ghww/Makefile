# process xml template files using filepp

CGIDIR := /usr/lib/cgi-bin/
CGIFILES := $(wildcard *.xt) $(wildcard 1E??.xml) $(wildcard *.i) RURC.xml *.py hp.db
#TARGETS := $(TEMPLATES:%.xt=%.xml)

#all: d-b-e.xml d-b-b.xml d-s-b.xml
#all: $(TARGETS)

hp.db: hp.db.zst
	zstd -d $<

%.xml: %.xt
	filepp -m for.pm $< > $@

install: $(CGIFILES)
	sudo cp $(CGIFILES) $(CGIDIR)
