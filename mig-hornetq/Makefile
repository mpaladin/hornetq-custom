#
# download and check the files declared in the "sources" file
#

.PHONY: sources download check clean

sources: download check

download:
	@cat sources | while read line; do \
	    set $$line; \
	    curl -O -R -S -f -s $$2 ; \
	done

check:
	@cat sources | while read line; do \
	    set $$line; \
	    echo "$$1  `basename $$2`" | md5sum -c; \
	done

clean:
	@cat sources | while read line; do \
	    set $$line; \
	    rm -fv `basename $$2`; \
	done
