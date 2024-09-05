# process xml template files using filepp

CGIDIR := /usr/lib/cgi-bin/
CGIFILES := $(wildcard *.xt) $(wildcard *.xml) *.py
# ERS mechanicals and air leaks are not needed for F280
HTM = head.htm main.htm $(MECH) windoors.htm $(LEAKS) tail.htm

#TARGETS := $(TEMPLATES:%.xt=%.xml)
#all: d-b-e.xml d-b-b.xml d-s-b.xml
#all: $(TARGETS)

dcf.html: *.htm
	$(eval MECH = ersmech.htm)
	$(eval LEAKS = airleaks.htm)
	cat $(HTM) > $@

f280.html: *.htm
	cat $(HTM) > $@

hp.db: hp.db.zst
	zstd -d $<

%.xml: %.xt
	filepp -m for.pm $< > $@

install: $(CGIFILES)
	sudo cp $(CGIFILES) $(CGIDIR)
	cp *.js *.html /var/www/solarsi.ca/html/
