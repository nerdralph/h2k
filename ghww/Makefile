# process xml template files using filepp

# could use wildcard for targets
all: de.xml db.xml d-s-b.xml

%.xml: %.xt
	filepp -m for.pm $< > $@

