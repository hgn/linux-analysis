PYTHON = python3
OUTPUT_FILE = output
HISTOGRAM_PREFIX = histogram

.PHONY: all generate visualize clean distclean

all: generate visualize

generate: clean
	$(PYTHON) 00-collect-cyclictest.py

visualize:
	$(PYTHON) 30-analyze-cyclictest.py

clean:
	rm -f $(OUTPUT_FILE) $(HISTOGRAM_PREFIX)* *.pdf

distclean: clean
	rm -f *.log *.tmp

