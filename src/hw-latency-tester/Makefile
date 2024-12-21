PYTHON = python3

.PHONY: all record visualize clean distclean

all: record visualize

record:
	$(PYTHON) hw-latency-tester.py

visualize:
	$(PYTHON) 20-analyze-cpu-specific-latency-distribution.py
	$(PYTHON) 20-analyze-outlier-timeline.py

clean:
	rm -f *.pdf

distclean: clean
	rm -f *.txt
