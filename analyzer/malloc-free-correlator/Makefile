all: record visualize

record:
	./malloc-free-catcher.sh
	./malloc-free-correlator.py > malloc-free-correlator.txt

visualize:
	./malloc-free-visualizer.py


clean:
	rm -rf *.pdf *.data *.old *.txt
