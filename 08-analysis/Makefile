SUBDIRS := $(wildcard */.)


all:
	@for dir in $(SUBDIRS); do \
		 cd $$dir && $(MAKE) --no-print-directory && cd ..; \
	done

clean: 
	@for dir in $(SUBDIRS); do \
		 cd $$dir && $(MAKE) --no-print-directory clean && cd ..; \
	done

.PHONY: all clean


# vim600: fdm=marker tw=120 sw=4 ts=4 sts=4 ff=unix noet:
