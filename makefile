VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: setup jupyter clean

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

jupyter:
	$(VENV)/bin/jupyter notebook

clean:
	rm -rf $(VENV)
