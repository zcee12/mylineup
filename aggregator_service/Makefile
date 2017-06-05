.PHONY: clean run

clean:
	rm -rf venv/

run: venv
	venv/bin/python src/aggregator_service/main.py

# With thanks - http://blog.bottlepy.org/2012/07/16/virtualenv-and-makefiles.html
venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
