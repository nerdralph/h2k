# process xml template files using filepp

TEMPLATES := $(wildcard *.xt)

#all: d-b-e.xml d-b-b.xml d-s-b.xml
all: $(TEMPLATES:%.xt=%.xml)

%.xml: %.xt
	filepp -m for.pm $< > $@

