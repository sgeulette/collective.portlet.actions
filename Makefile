#!/usr/bin/make
#
all: run

BUILDOUT_FILES = bin/buildout buildout.cfg

.PHONY: bootstrap buildout run test cleanall
bin/buildout: requirements.txt buildout.cfg
	virtualenv-2.7 .
	./bin/pip install --upgrade pip
	./bin/pip install -r requirements.txt
	touch $@

buildout: bin/buildout
	bin/buildout -Nt 5

bootstrap: bin/buildout

run: bin/instance
	bin/instance fg

bin/instance: $(BUILDOUT_FILES)
	bin/buildout -Nvt 5
	touch $@

test: bin/test
	rm -fr htmlcov
	bin/test

bin/test: $(BUILDOUT_FILES)
	bin/buildout -Nvt 5
	touch $@

cleanall:
	rm -fr bin develop-eggs htmlcov include .installed.cfg lib .mr.developer.cfg parts downloads eggs
