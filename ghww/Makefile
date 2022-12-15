# process xml template files using filepp

CGIDIR := /usr/lib/cgi-bin/
CGIFILES := $(wildcard *.xt) $(wildcard 1E??.xml) $(wildcard *.i) RURC.xml ghww.py
#TARGETS := $(TEMPLATES:%.xt=%.xml)

#all: d-b-e.xml d-b-b.xml d-s-b.xml
#all: $(TARGETS)

%.xml: %.xt
	filepp -m for.pm $< > $@

install: $(TARGETS)
	sudo cp $(CGIFILES) $(CGIDIR)
