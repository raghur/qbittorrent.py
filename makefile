.PHONY: test upload clean bootstrap

test:
	_virtualenv/Scripts/activate
	nosetests tests --with-coverage --cover-package qbittorrent
	
upload:
	python setup.py sdist upload
	make clean
	
register:
	python setup.py register

clean:
	rm -f MANIFEST
	rm -rf dist
	
bootstrap: _virtualenv
	_virtualenv/Scripts/pip install -e .
	_virtualenv/Scripts/pip install -r test-requirements.txt
	make clean

_virtualenv: 
	virtualenv _virtualenv
	_virtualenv/Scripts/pip install --upgrade pip
	_virtualenv/Scripts/pip install --upgrade setuptools
