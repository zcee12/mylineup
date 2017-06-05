.PHONY: clean run test

clean:
	rm -rf venv/

test:
	# Switch this to use setup.py later
	nosetests test/*

run: venv
	venv/bin/python src/aggregator_service/app.py

# With thanks - http://blog.bottlepy.org/2012/07/16/virtualenv-and-makefiles.html
venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
