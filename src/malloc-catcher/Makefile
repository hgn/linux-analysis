all: record visualize

record:
	./malloc-catcher.sh

visualize:
	./allocation-spread.py
	./allocation-sum.py
	./allocation-time.py


clean:
	rm -rf *.pdf *.data *.old
