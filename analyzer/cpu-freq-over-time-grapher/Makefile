.PHONY: collect prepare analyze all help full-chain clean

COLLECTORS := $(wildcard 00-*.py)
PREPARERS := $(wildcard 10-*.py)
ANALYZERS := $(wildcard 20-*.py)

OUTPUT = "analyze-frequency.pdf"

# defaults to analyze, just that recorded data
# are not simple overwriten
all: help

collect:
	./$(COLLECTORS)

prepare:
	./$(PREPARERS)

analyze:
	./$(ANALYZERS)

show:
	xpdf -fullscreen $(OUTPUT)

clean:
	@rm -rf perf.data perf.data.old
	@rm -rf trace* meta.json
	@rm -rf *.csv
	@rm -rf *.png *.pdf

full-chain: clean collect prepare analyze

help:
	@echo 'Supported targets:'
	@echo 'collect - to generate data file like perf.data'
	@echo 'prepare - pre-converts perf.data for further processing scripts'
	@echo 'analyze - to generate final illustrations'
	@echo ''
	@echo 'full-chain - generate everything in order, it enforce a clean first'





