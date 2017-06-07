.PHONY: clean run test

clean:
	rm -rf venv/

test:
	# Switch this to use setup.py later
	PENDING_DIR=test/fixtures/pending PROCESSED_DIR=test/fixtures/processed nosetests test

fixture:
	cp test/fixtures/pending-static/5c22b510-98ec-4570-a8e5-1c422ffb41f9 runtime/pending/

run: venv
	PENDING_DIR=../runtime/pending PROCESSED_DIR=../runtime/processed venv/bin/python src/aggregator_service/app.py

# With thanks - http://blog.bottlepy.org/2012/07/16/virtualenv-and-makefiles.html
venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
