# process xml template files using filepp

# could use wildcard for targets
all: d-b-e.xml d-b-b.xml d-s-b.xml

%.xml: %.xt
	filepp -m for.pm $< > $@

