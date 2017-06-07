.PHONY: clean run test

clean:
	rm -rf venv/

test: venv
	venv/bin/nosetests test

run-for-test: venv
	PENDING_DIR="test/fixtures/pending" PROCESSED_DIR="test/fixtures/processed" venv/bin/python src/server.py

run: venv
	PENDING_DIR="../runtime/pending" PROCESSED_DIR="../runtime/processed" venv/bin/python src/server.py

# With thanks - http://blog.bottlepy.org/2012/07/16/virtualenv-and-makefiles.html
venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
