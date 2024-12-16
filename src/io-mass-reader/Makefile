SCRIPT = io-file-reader.py

default: record

record:
	python3 $(SCRIPT)
	sudo perf script -i perf-cold.data > trace-cold.txt
	~/src/code/foreign/FlameGraph/stackcollapse-perf.pl trace-cold.txt > trace-cold.folded
	~/src/code/foreign/FlameGraph/flamegraph.pl --colors aqua --bgcolors "#ffffff" trace-cold.folded > cold.svg
	sudo rm -rf trace-cold.folded
	@echo "Changing ownership of perf data files..."
	sudo chown $(USER) *.data *.txt *.svg
	sudo perf script -i perf-warm.data > trace-warm.txt

analyze:
	python3 20-analyze-events-no.py

clean:
	@echo "Cleaning up generated files..."
	-rm -f perf*.data perf*.old *.png *.pdf *.txt *.svg *.folded

.PHONY: default record analyze clean
