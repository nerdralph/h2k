# process xml template files using filepp

# could use wildcard for targets
all: de.xml db.xml

%.xml: %.xt
	filepp $< > $@
