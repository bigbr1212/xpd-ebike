.SUFFIXES: .po .pot .mo

VERSION=$(shell cat VERSION)

# Default target - do nothing
all:
	@echo "Make one of the following targets:"
	@echo "	install		install the library and tools"
	@echo "	dist		build a source code distribution"
	@echo "	win-install	build a Windows binary distribution"
	@echo "	clean		remove all generated files"
	@echo "	update-po	update all po files with new strings from sources"
	@echo "	dist		make a distribution archive"

install:
	python setup.py install

win-dist:
	rm -rf xpd-$(VERSION)
	mkdir xpd-$(VERSION)
	python setup.py install -O1 --root xpd-$(VERSION)
	mv xpd-$(VERSION)/usr/bin/xpd xpd-$(VERSION)/xpd.pyw
	mv xpd-$(VERSION)/usr/lib/python*/site-packages/xpdm xpd-$(VERSION)
	mv xpd-$(VERSION)/usr/share/locale xpd-$(VERSION)
	mv xpd-$(VERSION)/usr/share/xpd xpd-$(VERSION)/share
	rm -rf xpd-$(VERSION)/usr
	convert -background none xpd-$(VERSION)/share/xpd.svg -resize 64 xpd-$(VERSION)/xpd.ico
	zip -mr xpd-$(VERSION)-windows.zip xpd-$(VERSION)

dist:
	rm -rf xpd-$(VERSION)
	mkdir xpd-$(VERSION) xpd-$(VERSION)/po \
	      xpd-$(VERSION)/share xpd-$(VERSION)/xpdm \
	      xpd-$(VERSION)/build xpd-$(VERSION)/debian \
	      xpd-$(VERSION)/docs
	cp -a po/*.po* xpd-$(VERSION)/po
	cp -a share/*.xml share/*.asv share/*.svg xpd-$(VERSION)/share
	cp -a xpdm/*.py xpd-$(VERSION)/xpdm
	cp -a build/xpd.desktop build/xpd.spec xpd-$(VERSION)/build
	cp -a debian/* xpd-$(VERSION)/debian
	cp -a docs/* xpd-$(VERSION)/docs
	cp -a Makefile COPYING README TRANSLATORS VERSION \
	      setup.py debug-read-* debug-scan-ports xpd xpd-$(VERSION)
	tar cvjf xpd-$(VERSION).tar.bz2 xpd-$(VERSION)
	rm -rf xpd-$(VERSION)

clean:
	python setup.py clean -a
	rm -f xpdm/*.pyc *.log
	rm -rf xpd-$(VERSION)

# Update translation files
update-po: $(wildcard po/*.po)

po/%.po: $(wildcard share/*.xml) $(wildcard xpdm/*.py) xpd
	xgettext --omit-header -L glade $(filter %.xml,$^) -o tmp.po
	xgettext --omit-header -L python $(filter-out %.xml,$^) -j -o tmp.po
	msgmerge $@ tmp.po -o $@
	rm -f tmp.po
