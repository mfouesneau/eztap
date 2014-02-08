# Keeps a few frequent commands
#
PROJECT = 'eztap'
cleantemp = rm -rf build; rm -f *.c
TAR = $(PROJECT).tar.gz
DIRS= core backend

.PHONY : clean all build

all: clean gitbuild
gitdeps:
	git submodule init
	git submodule update --recursive
	git submodule foreach git pull origin master

gitmain:
	git pull

gitbuild: gitdeps gitmain

build:  
	#for d in $(DIRS); do (cd $$d; $(MAKE) build );done
	python setup.py build
	$(cleantemp)


clean: 
	#for d in $(DIRS); do (cd $$d; $(MAKE) clean );done
	$(cleantmp)
	find . -name '*pyc' -exec rm -f {} \;
